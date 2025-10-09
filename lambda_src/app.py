import json
import logging
from typing import Any, Dict

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event: Dict[str, Any], context) -> Dict[str, Any]:
    """API Gateway (REST v1) Lambda proxy handler.

    目的:
      - API Gateway のアクセスログとアプリケーションログを確実にひも付けるため、
        次の相関情報を 1 行の JSON として CloudWatch Logs に出力します。
          * applicationId: URL パスから取得（例: /apps/{applicationId}）
          * apiKeyId: リクエストに使われた API キーの ID（値そのものではない）
          * requestId: API Gateway が発行するリクエスト ID（アクセスログと一致）
          * lambdaRequestId: Lambda 実行ごとの ID（デバッグに有用）

    受け取り想定のイベント:
      - API Gateway REST の "Lambda プロキシ統合" イベント（event 形式は公式ドキュメントを参照）

    セキュリティ配慮:
      - 機密である API キーの「値」はログしません。代わりに安全な識別子である
        apiKeyId を記録します（API Gateway REST の requestContext.identity.apiKeyId）。
    """

    # requestContext には API Gateway が付与するメタ情報が入っています。
    # dict.get(...) はキーが無い場合に None を返すため、or {} で空辞書を補います。
    request_context = event.get("requestContext") or {}

    # API Gateway のアクセスログと同一の requestId。相関の主キーとして使えます。
    request_id = request_context.get("requestId")

    # API キーの「ID」を取得します。値そのものは含まれません。
    identity = request_context.get("identity") or {}
    api_key_id = identity.get("apiKeyId")

    # URL パスの {applicationId} を取得します。
    path_parameters = event.get("pathParameters") or {}
    application_id = path_parameters.get("applicationId")

    # 解析・転送しやすいよう、1 行の JSON として標準出力に出します。
    # CloudWatch Logs に取り込まれ、後続の Athena や ETL で集計可能になります。
    log_entry = {
        "message": "app-correlation",          # ログの種類（検索の手掛かり）
        "applicationId": application_id,       # テナント/アプリ識別子
        "apiKeyId": api_key_id,                # 機密非該当のキーID
        "requestId": request_id,               # API Gateway のリクエストID
        "lambdaRequestId": getattr(context, "aws_request_id", None),
    }
    print(json.dumps(log_entry, ensure_ascii=False))

    # API の通常応答。ここではデモとして applicationId をそのまま返します。
    body = {"ok": True, "applicationId": application_id}
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body, ensure_ascii=False),
    }
