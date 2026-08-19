from datetime import datetime, timezone
from typing import Optional

from src.ingestion.api_client import LinkedInAgentClient
from src.quality.dead_letter_repository import save_dead_letter


PIPELINE_NAME = "linkedin_ingestion"


def validate_event(record: dict) -> list[str]:
    """
    Validate an outreach event.

    Returns a list of validation errors.
    """

    errors = []

    if not record.get("event_id"):
        errors.append("event_id is required")

    if not record.get("lead_id"):
        errors.append("lead_id is required")

    if not record.get("event_type"):
        errors.append("event_type is required")

    if not record.get("event_timestamp"):
        errors.append("event_timestamp is required")

    return errors


def get_latest_watermark(
    records: list[dict],
) -> Optional[datetime]:
    """
    Find the latest updated_at value from successfully
    processed records.
    """

    timestamps = []

    for record in records:
        updated_at = record.get("updated_at")

        if not updated_at:
            continue

        if isinstance(updated_at, str):
            updated_at = datetime.fromisoformat(
                updated_at.replace("Z", "+00:00")
            )

        timestamps.append(updated_at)

    if not timestamps:
        return None

    return max(timestamps)


def run_pipeline():
    """
    Execute one incremental ingestion run.
    """

    rows_in = 0
    rows_out = 0

    # Import database repositories lazily so that lightweight unit tests
    # which only import `validate_event` don't require a configured DB URL.
    from src.database.watermark_repository import (
        get_watermark,
        save_watermark,
    )
    from src.database.pipeline_run_repository import (
        complete_pipeline_run,
        fail_pipeline_run,
        start_pipeline_run,
    )
    from src.database.outreach_repository import upsert_outreach_event

    old_watermark = get_watermark(PIPELINE_NAME)

    run_id = start_pipeline_run(
        pipeline_name=PIPELINE_NAME,
        watermark_start=old_watermark,
    )

    try:
        client = LinkedInAgentClient()

        params = {}

        if old_watermark:
            params["updated_at_gt"] = old_watermark.isoformat()

        # Replace this endpoint with the real API endpoint
        # once the Polluxa API documentation is available.
        endpoint = "REPLACE_WITH_REAL_ENDPOINT"

        records = client.get(
            endpoint=endpoint,
            params=params,
        )

        rows_in = len(records)

        successful_records = []

        for record in records:
            errors = validate_event(record)

            if errors:
                save_dead_letter(
                    run_id=run_id,
                    record=record,
                    error_reason="; ".join(errors),
                )
                continue

            successful_records.append(record)

        for record in successful_records:
            upsert_outreach_event(record)

        rows_out = len(successful_records)

        new_watermark = get_latest_watermark(
            successful_records
        )

        if new_watermark:
            save_watermark(
                pipeline_name=PIPELINE_NAME,
                watermark=new_watermark,
            )

        complete_pipeline_run(
            run_id=run_id,
            rows_in=rows_in,
            rows_out=rows_out,
            watermark_end=new_watermark,
        )

        return {
            "run_id": run_id,
            "rows_in": rows_in,
            "rows_out": rows_out,
            "status": "SUCCESS",
            "watermark_start": old_watermark,
            "watermark_end": new_watermark,
        }

    except Exception as exc:
        fail_pipeline_run(
            run_id=run_id,
            rows_in=rows_in,
            rows_out=rows_out,
            error_message=str(exc),
        )

        raise