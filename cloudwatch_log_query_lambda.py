import os
import time
from datetime import datetime, timezone

import boto3

LOG_GROUP_NAME = os.environ.get("LOG_GROUP_NAME")
QUERY_STRING = os.environ.get(
    "LOG_QUERY_STRING",
    "fields @timestamp, @message | sort @timestamp desc | limit 100",
)
QUERY_POLL_INTERVAL = float(os.environ.get("QUERY_POLL_INTERVAL_SECONDS", "2.0"))
MAX_QUERY_WAIT_SECONDS = int(os.environ.get("MAX_QUERY_WAIT_SECONDS", "60"))

logs_client = boto3.client("logs")


def _previous_month_range(now: datetime) -> tuple[datetime, datetime]:
    """Return the time range (start, end) for the previous month relative to `now`."""
    if now.tzinfo is None:
        raise ValueError("`now` must be timezone-aware (UTC).")

    current_month_start = datetime(now.year, now.month, 1, tzinfo=timezone.utc)

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


def lambda_handler(event, context):
    """
    AWS Lambda entry point.

    Triggered monthly via EventBridge (e.g., cron(0 2 1 * ? *) in UTC).
    Queries the configured CloudWatch Logs Insights log group for entries from the
    start of the previous month up to the invocation time.
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
            results_count = len(response.get("results", []))
            print(
                f"CloudWatch Logs Insights query complete. "
                f"Log group: {LOG_GROUP_NAME}, "
                f"start: {start_time.isoformat()}, "
                f"end: {end_time.isoformat()}, "
                f"results: {results_count}"
            )
            return response

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
