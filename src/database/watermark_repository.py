from datetime import datetime
from typing import Optional

from sqlalchemy import text

from src.database.connection import engine


def get_watermark(pipeline_name: str) -> Optional[datetime]:
    query = text(
        """
        SELECT last_watermark
        FROM pipeline_watermarks
        WHERE pipeline_name = :pipeline_name
        """
    )

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"pipeline_name": pipeline_name},
        ).scalar_one_or_none()

    return result


def save_watermark(
    pipeline_name: str,
    watermark: datetime,
) -> None:
    query = text(
        """
        INSERT INTO pipeline_watermarks (
            pipeline_name,
            last_watermark,
            updated_at
        )
        VALUES (
            :pipeline_name,
            :watermark,
            CURRENT_TIMESTAMP
        )
        ON CONFLICT (pipeline_name)
        DO UPDATE SET
            last_watermark = EXCLUDED.last_watermark,
            updated_at = CURRENT_TIMESTAMP
        """
    )

    with engine.begin() as connection:
        connection.execute(
            query,
            {
                "pipeline_name": pipeline_name,
                "watermark": watermark,
            },
        )