import json

from sqlalchemy import text

from src.database.connection import engine


def save_dead_letter(
    run_id: int,
    record: dict,
    error_reason: str,
    retry_count: int = 0,
    status: str = "PENDING",
) -> None:
    query = text(
        """
        INSERT INTO dead_letter_records (
            run_id,
            record_payload,
            error_reason,
            retry_count,
            status
        )
        VALUES (
            :run_id,
            CAST(:record_payload AS JSONB),
            :error_reason,
            :retry_count,
            :status
        )
        """
    )

    with engine.begin() as connection:
        connection.execute(
            query,
            {
                "run_id": run_id,
                "record_payload": json.dumps(
                    record,
                    default=str,
                ),
                "error_reason": error_reason,
                "retry_count": retry_count,
                "status": status,
            },
        )