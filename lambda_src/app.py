import json
import logging
from typing import Any, Dict

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event: Dict[str, Any], context) -> Dict[str, Any]:
    """Lambda proxy handler that logs applicationId, apiKeyId, and requestId.

    Expects API Gateway REST (v1) proxy integration.
    - applicationId: from pathParameters
    - apiKeyId: from requestContext.identity.apiKeyId (safe identifier, not secret)
    - requestId: API Gateway request ID for correlation with access logs
    """
    request_context = event.get("requestContext") or {}

    request_id = request_context.get("requestId")
    identity = request_context.get("identity") or {}
    api_key_id = identity.get("apiKeyId")

    path_parameters = event.get("pathParameters") or {}
    application_id = path_parameters.get("applicationId")

    # One-line JSON for easy ingestion
    log_entry = {
        "message": "app-correlation",
        "applicationId": application_id,
        "apiKeyId": api_key_id,
        "requestId": request_id,
        "lambdaRequestId": getattr(context, "aws_request_id", None),
    }
    print(json.dumps(log_entry, ensure_ascii=False))

    # Normal proxy response
    body = {"ok": True, "applicationId": application_id}
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body, ensure_ascii=False),
    }
