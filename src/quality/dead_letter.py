import json
from datetime import datetime, timezone
from pathlib import Path


DEAD_LETTER_DIR = Path("database/staging/dead_letter")


def capture_dead_letter(
    record: dict,
    error_message: str,
    pipeline_name: str,
) -> None:
    DEAD_LETTER_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    timestamp = datetime.now(timezone.utc).strftime(
        "%Y%m%dT%H%M%SZ"
    )

    output_file = (
        DEAD_LETTER_DIR
        / f"{pipeline_name}_{timestamp}.jsonl"
    )

    dead_letter_record = {
        "captured_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "pipeline_name": pipeline_name,
        "error_message": error_message,
        "record": record,
    }

    with output_file.open(
        "a",
        encoding="utf-8",
    ) as file:
        file.write(
            json.dumps(
                dead_letter_record,
                default=str,
            )
            + "\n"
        )