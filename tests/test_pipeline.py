from src.ingestion.pipeline import validate_event


def test_valid_event():
    record = {
        "event_id": 123,
        "lead_id": 10,
        "event_type": "INVITE_SENT",
        "event_timestamp": "2026-08-19T10:00:00Z",
    }

    errors = validate_event(record)

    assert errors == []


def test_invalid_event():
    record = {
        "event_id": None,
        "lead_id": None,
        "event_type": None,
        "event_timestamp": None,
    }

    errors = validate_event(record)

    assert "event_id is required" in errors
    assert "lead_id is required" in errors
    assert "event_type is required" in errors
    assert "event_timestamp is required" in errors