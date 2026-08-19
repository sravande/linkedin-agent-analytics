from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import text

from src.database.connection import engine


def start_pipeline_run(
    pipeline_name: str,
    watermark_start: Optional[datetime] = None,
) -> int:
    """
    Create a new pipeline run and return its run_id.
    """

    query = text(
        """
        INSERT INTO pipeline_runs (
            pipeline_name,
            start_time,
            rows_in,
            rows_out,
            status,
            watermark_start
        )
        VALUES (
            :pipeline_name,
            :start_time,
            0,
            0,
            'RUNNING',
            :watermark_start
        )
        RETURNING run_id
        """
    )

    with engine.begin() as connection:
        run_id = connection.execute(
            query,
            {
                "pipeline_name": pipeline_name,
                "start_time": datetime.now(timezone.utc),
                "watermark_start": watermark_start,
            },
        ).scalar_one()

    return run_id


def complete_pipeline_run(
    run_id: int,
    rows_in: int,
    rows_out: int,
    watermark_end: Optional[datetime] = None,
) -> None:
    """
    Mark a pipeline run as successfully completed.
    """

    query = text(
        """
        UPDATE pipeline_runs
        SET
            end_time = :end_time,
            rows_in = :rows_in,
            rows_out = :rows_out,
            status = 'SUCCESS',
            watermark_end = :watermark_end
        WHERE run_id = :run_id
        """
    )

    with engine.begin() as connection:
        connection.execute(
            query,
            {
                "run_id": run_id,
                "end_time": datetime.now(timezone.utc),
                "rows_in": rows_in,
                "rows_out": rows_out,
                "watermark_end": watermark_end,
            },
        )


def fail_pipeline_run(
    run_id: int,
    rows_in: int,
    rows_out: int,
    error_message: str,
) -> None:
    """
    Mark a pipeline run as failed.
    """

    query = text(
        """
        UPDATE pipeline_runs
        SET
            end_time = :end_time,
            rows_in = :rows_in,
            rows_out = :rows_out,
            status = 'FAILED',
            error_message = :error_message
        WHERE run_id = :run_id
        """
    )

    with engine.begin() as connection:
        connection.execute(
            query,
            {
                "run_id": run_id,
                "end_time": datetime.now(timezone.utc),
                "rows_in": rows_in,
                "rows_out": rows_out,
                "error_message": error_message,
            },
        )