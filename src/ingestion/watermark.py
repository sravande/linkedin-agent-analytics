from datetime import datetime
from typing import Optional


def get_watermark(records: list[dict]) -> Optional[datetime]:
    """
    Return the latest updated_at value from a collection of records.

    Returns None when there are no records.
    """

    if not records:
        return None

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