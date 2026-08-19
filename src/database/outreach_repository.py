from sqlalchemy import text

from src.database.connection import engine


def upsert_outreach_event(event: dict) -> None:
    query = text(
        """
        INSERT INTO outreach_events (
            event_id,
            lead_id,
            event_type,
            event_timestamp,
            campaign_id,
            agent_id
        )
        VALUES (
            :event_id,
            :lead_id,
            :event_type,
            :event_timestamp,
            :campaign_id,
            :agent_id
        )
        ON CONFLICT (event_id)
        DO UPDATE SET
            lead_id = EXCLUDED.lead_id,
            event_type = EXCLUDED.event_type,
            event_timestamp = EXCLUDED.event_timestamp,
            campaign_id = EXCLUDED.campaign_id,
            agent_id = EXCLUDED.agent_id
        """
    )

    with engine.begin() as connection:
        connection.execute(
            query,
            {
                "event_id": event["event_id"],
                "lead_id": event["lead_id"],
                "event_type": event["event_type"],
                "event_timestamp": event["event_timestamp"],
                "campaign_id": event.get("campaign_id"),
                "agent_id": event.get("agent_id"),
            },
        )