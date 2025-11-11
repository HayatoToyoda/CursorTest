import csv
import io
import os
import re
import time
from datetime import datetime, timezone
from typing import Dict, Iterable, List, Optional, Tuple

import boto3

LOG_GROUP_NAME = os.environ.get("LOG_GROUP_NAME")
QUERY_STRING = os.environ.get(
    "LOG_QUERY_STRING",
    (
        "fields @timestamp, @message "
        "| filter @message like /REPORT RequestId:/ "
        "      or @message like /requestId[:=]/ "
        "| sort @timestamp asc | limit 10000"
    ),
)
QUERY_POLL_INTERVAL = float(os.environ.get("QUERY_POLL_INTERVAL_SECONDS", "2.0"))
MAX_QUERY_WAIT_SECONDS = int(os.environ.get("MAX_QUERY_WAIT_SECONDS", "60"))
OUTPUT_S3_BUCKET = os.environ.get("OUTPUT_S3_BUCKET")
OUTPUT_S3_PREFIX = os.environ.get("OUTPUT_S3_PREFIX", "")
INCLUDE_HEADERS = os.environ.get("CSV_INCLUDE_HEADERS", "true").lower() == "true"

logs_client = boto3.client("logs")

REPORT_LOG_PATTERN = re.compile(
    r"REPORT\s+RequestId:\s+(?P<request_id>\S+)\s+"
    r"Duration:\s+(?P<duration_ms>[\d.]+)\s+ms\s+"
    r"Billed Duration:\s+(?P<billed_duration_ms>\d+)\s+ms\s+"
    r"Memory Size:\s+(?P<memory_size_mb>\d+)\s+MB"
    r"(?:\s+Max Memory Used:\s+(?P<max_memory_used_mb>\d+)\s+MB)?",
    re.IGNORECASE,
)
REQUEST_ID_PATTERN = re.compile(r"request[_\- ]?id[:=]\s*(?P<request_id>[A-Za-z0-9\-]+)", re.IGNORECASE)
CLIENT_ID_PATTERN = re.compile(
    r"(?:client|customer|user)[_\- ]?id[:=]\s*(?P<client_id>[A-Za-z0-9_\-\.]+)",
    re.IGNORECASE,
)


def _previous_month_range(now: datetime) -> Tuple[datetime, datetime]:
    """Return the time range (start, end) for the previous month relative to `now`."""
    if now.tzinfo is None:
        raise ValueError("`now` must be timezone-aware (UTC).")

    if now.month == 1:
        prev_year = now.year - 1
        prev_month = 12
    else:
        prev_year = now.year
        prev_month = now.month - 1

    previous_month_start = datetime(prev_year, prev_month, 1, tzinfo=timezone.utc)
    return previous_month_start, now


def _validate_configuration() -> None:
    if not LOG_GROUP_NAME:
        raise ValueError("Environment variable `LOG_GROUP_NAME` must be set.")
    if not QUERY_STRING:
        raise ValueError("Log Insights `LOG_QUERY_STRING` must not be empty.")


def _read_messages_from_results(results: List[List[Dict[str, str]]]) -> Iterable[str]:
    for row in results:
        row_dict = {entry["field"]: entry["value"] for entry in row if entry.get("field")}
        message = row_dict.get("@message")
        if message:
            yield message


def _parse_report_log(message: str) -> Optional[Dict[str, str]]:
    match = REPORT_LOG_PATTERN.search(message)
    if not match:
        return None
    data = match.groupdict()
    max_memory = data.get("max_memory_used_mb")
    return {
        "request_id": data["request_id"],
        "billed_duration_ms": data["billed_duration_ms"],
        "memory_mb": max_memory or data["memory_size_mb"],
    }


def _parse_custom_log(message: str) -> Optional[Dict[str, str]]:
    request_match = REQUEST_ID_PATTERN.search(message)
    client_match = CLIENT_ID_PATTERN.search(message)
    if not request_match or not client_match:
        return None
    return {
        "request_id": request_match.group("request_id"),
        "client_identifier": client_match.group("client_id"),
    }


def _aggregate_usage(messages: Iterable[str]) -> List[Dict[str, str]]:
    report_by_request: Dict[str, Dict[str, str]] = {}
    client_by_request: Dict[str, Dict[str, str]] = {}

    for message in messages:
        report = _parse_report_log(message)
        if report:
            report_by_request[report["request_id"]] = report
            continue

        custom = _parse_custom_log(message)
        if custom:
            client_by_request.setdefault(custom["request_id"], custom)

    combined_rows: List[Dict[str, str]] = []
    for request_id, report in report_by_request.items():
        client = client_by_request.get(request_id)
        if not client:
            continue
        combined_rows.append(
            {
                "client_identifier": client["client_identifier"],
                "memory_mb": report["memory_mb"],
                "billed_duration_ms": report["billed_duration_ms"],
            }
        )

    return combined_rows


def _create_csv(rows: List[Dict[str, str]]) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    if INCLUDE_HEADERS:
        writer.writerow(["client_identifier", "memory_mb", "billed_duration_ms"])
    for row in rows:
        writer.writerow([row["client_identifier"], row["memory_mb"], row["billed_duration_ms"]])
    return output.getvalue()


def _maybe_upload_csv(csv_content: str, start_time: datetime, end_time: datetime) -> Optional[str]:
    if not OUTPUT_S3_BUCKET:
        return None

    s3_client = boto3.client("s3")
    key_timestamp = end_time.strftime("%Y%m%dT%H%M%SZ")
    start_period = start_time.strftime("%Y%m")
    key = f"{OUTPUT_S3_PREFIX.rstrip('/')}/{start_period}/usage_{start_period}_{key_timestamp}.csv".lstrip("/")

    s3_client.put_object(
        Bucket=OUTPUT_S3_BUCKET,
        Key=key,
        Body=csv_content.encode("utf-8"),
        ContentType="text/csv",
    )
    return key


def lambda_handler(event, context):
    """
    AWS Lambda entry point.

    Triggered monthly via EventBridge (e.g., cron(0 2 1 * ? *) in UTC).
    Queries the configured CloudWatch Logs Insights log group for entries from the
    start of the previous month up to the invocation time, aggregates REPORT logs with
    custom logs via request ID, and produces a CSV containing (client identifier,
    execution memory in MB, billed duration in ms).
    """
    _validate_configuration()

    now = datetime.now(timezone.utc)
    start_time, end_time = _previous_month_range(now)

    query_id = logs_client.start_query(
        logGroupName=LOG_GROUP_NAME,
        queryString=QUERY_STRING,
        startTime=int(start_time.timestamp()),
        endTime=int(end_time.timestamp()),
    )["queryId"]

    deadline = time.monotonic() + MAX_QUERY_WAIT_SECONDS
    while True:
        response = logs_client.get_query_results(queryId=query_id)
        status = response["status"]

        if status == "Complete":
            results = response.get("results", [])
            messages = list(_read_messages_from_results(results))
            rows = _aggregate_usage(messages)
            csv_content = _create_csv(rows)
            s3_key = _maybe_upload_csv(csv_content, start_time, end_time)

            print(
                f"Log Insights query complete | log_group={LOG_GROUP_NAME} "
                f"| start={start_time.isoformat()} | end={end_time.isoformat()} "
                f"| raw_results={len(results)} | joined_rows={len(rows)} "
                f"| csv_bytes={len(csv_content.encode('utf-8'))}"
            )

            if s3_key:
                print(
                    f"CSV uploaded to s3://{OUTPUT_S3_BUCKET}/{s3_key} "
                    "(CSV body omitted from response)."
                )
                csv_body = None
            else:
                csv_body = csv_content

            return {
                "row_count": len(rows),
                "csv": csv_body,
                "s3_bucket": OUTPUT_S3_BUCKET,
                "s3_key": s3_key,
            }

        if status in {"Cancelled", "Failed", "Timeout"}:
            raise RuntimeError(
                f"CloudWatch Logs Insights query {query_id} ended with status {status}"
            )

        if time.monotonic() >= deadline:
            raise TimeoutError(
                f"CloudWatch Logs Insights query {query_id} did not complete within "
                f"{MAX_QUERY_WAIT_SECONDS} seconds."
            )

        time.sleep(QUERY_POLL_INTERVAL)
