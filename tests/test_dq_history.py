from pathlib import Path


def test_dq_history_migration_exists():
    migration = Path(
        "database/migrations/005_dq_results_history.sql"
    )

    assert migration.exists()


def test_dq_history_contains_required_columns():
    migration = Path(
        "database/migrations/005_dq_results_history.sql"
    )

    sql = migration.read_text().lower()

    required_columns = [
        "run_id",
        "execution_timestamp",
        "completeness_score",
        "uniqueness_score",
        "validity_score",
        "timeliness_score",
        "referential_integrity_score",
        "composite_dq_score",
        "pass_fail_status",
        "failed_test_count",
        "error_message",
    ]

    for column in required_columns:
        assert column in sql