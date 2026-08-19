from sqlalchemy import text


QUALITY_CHECKS = {
    "fact_required_keys": """
        SELECT COUNT(*)
        FROM fact_outreach_activity
        WHERE agent_sk IS NULL
           OR lead_sk IS NULL
           OR date_sk IS NULL
    """,

    "duplicate_interaction_ids": """
        SELECT COUNT(*)
        FROM (
            SELECT interaction_id
            FROM fact_outreach_activity
            GROUP BY interaction_id
            HAVING COUNT(*) > 1
        ) duplicates
    """,

    "future_events": """
        SELECT COUNT(*)
        FROM fact_outreach_activity
        WHERE event_timestamp > CURRENT_TIMESTAMP
    """,

    "negative_response_times": """
        SELECT COUNT(*)
        FROM fact_outreach_activity
        WHERE response_time_minutes < 0
    """,

    "invalid_daily_utilisation": """
        SELECT COUNT(*)
        FROM fact_outreach_activity
        WHERE daily_limit_utilised_pct < 0
           OR daily_limit_utilised_pct > 100
    """,

    "orphan_agents": """
        SELECT COUNT(*)
        FROM fact_outreach_activity f
        LEFT JOIN dim_agent a
            ON f.agent_sk = a.agent_sk
        WHERE a.agent_sk IS NULL
    """,

    "orphan_leads": """
        SELECT COUNT(*)
        FROM fact_outreach_activity f
        LEFT JOIN dim_lead l
            ON f.lead_sk = l.lead_sk
        WHERE l.lead_sk IS NULL
    """,

    "orphan_dates": """
        SELECT COUNT(*)
        FROM fact_outreach_activity f
        LEFT JOIN dim_date d
            ON f.date_sk = d.date_sk
        WHERE d.date_sk IS NULL
    """,
}


def run_quality_checks() -> dict:
    """
    Execute all registered data quality checks.

    Returns a dictionary containing PASS/FAIL status
    and the number of invalid records.
    """

    results = {}

    # Import the engine lazily so that importing `QUALITY_CHECKS`
    # doesn't require a configured DATABASE_URL during lightweight unit tests.
    from src.database.connection import engine

    with engine.connect() as connection:
        for check_name, query in QUALITY_CHECKS.items():

            invalid_rows = connection.execute(
                text(query)
            ).scalar_one()

            results[check_name] = {
                "status": "PASS" if invalid_rows == 0 else "FAIL",
                "invalid_rows": invalid_rows,
            }

    return results