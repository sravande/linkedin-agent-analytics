-- ============================================================
-- Part 3: Data Architecture & Modeling
-- Star Schema
-- ============================================================


-- ============================================================
-- Dimension: Agent
-- SCD Type 2
-- ============================================================

CREATE TABLE IF NOT EXISTS dim_agent (
    agent_sk BIGSERIAL PRIMARY KEY,

    agent_id VARCHAR(100) NOT NULL,

    agent_name VARCHAR(255),

    linkedin_email VARCHAR(255),

    account_age_tier VARCHAR(50),

    risk_classification VARCHAR(100),

    max_daily_invites INTEGER,

    max_daily_messages INTEGER,

    status VARCHAR(50),

    effective_date TIMESTAMPTZ NOT NULL,

    expiration_date TIMESTAMPTZ,

    is_current_flag BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX IF NOT EXISTS idx_dim_agent_natural_key
ON dim_agent(agent_id);


CREATE INDEX IF NOT EXISTS idx_dim_agent_current
ON dim_agent(agent_id, is_current_flag);


-- ============================================================
-- Dimension: Lead
-- SCD Type 1
-- ============================================================

CREATE TABLE IF NOT EXISTS dim_lead (
    lead_sk BIGSERIAL PRIMARY KEY,

    lead_id VARCHAR(100) NOT NULL UNIQUE,

    lead_name VARCHAR(255),

    job_title VARCHAR(255),

    company VARCHAR(255),

    industry VARCHAR(255),

    target_segment VARCHAR(255),

    location VARCHAR(255),

    linkedin_profile_url TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- Dimension: Campaign
-- SCD Type 1
-- ============================================================

CREATE TABLE IF NOT EXISTS dim_campaign (
    campaign_sk BIGSERIAL PRIMARY KEY,

    campaign_id VARCHAR(100) NOT NULL UNIQUE,

    campaign_name VARCHAR(255),

    objective TEXT,

    start_date DATE,

    end_date DATE,

    target_audience VARCHAR(255),

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- Dimension: Date
-- ============================================================

CREATE TABLE IF NOT EXISTS dim_date (
    date_sk INTEGER PRIMARY KEY,

    full_date DATE NOT NULL UNIQUE,

    day_of_week INTEGER,

    day_name VARCHAR(20),

    month INTEGER,

    month_name VARCHAR(20),

    quarter INTEGER,

    year INTEGER,

    is_weekend BOOLEAN,

    fiscal_quarter VARCHAR(20)
);


-- ============================================================
-- Fact: Outreach Activity
--
-- Grain:
-- One row per individual outreach interaction event.
-- ============================================================

CREATE TABLE IF NOT EXISTS fact_outreach_activity (
    outreach_activity_sk BIGSERIAL PRIMARY KEY,

    interaction_id VARCHAR(100) NOT NULL UNIQUE,

    agent_sk BIGINT NOT NULL,

    lead_sk BIGINT NOT NULL,

    campaign_sk BIGINT,

    date_sk INTEGER NOT NULL,

    interaction_type VARCHAR(50) NOT NULL,

    event_timestamp TIMESTAMPTZ NOT NULL,

    invites_sent_count INTEGER NOT NULL DEFAULT 0,

    invites_accepted_count INTEGER NOT NULL DEFAULT 0,

    messages_sent_count INTEGER NOT NULL DEFAULT 0,

    replies_received_count INTEGER NOT NULL DEFAULT 0,

    response_time_minutes INTEGER,

    daily_limit_utilised_pct DECIMAL(5,2),

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_fact_agent
        FOREIGN KEY (agent_sk)
        REFERENCES dim_agent(agent_sk),

    CONSTRAINT fk_fact_lead
        FOREIGN KEY (lead_sk)
        REFERENCES dim_lead(lead_sk),

    CONSTRAINT fk_fact_campaign
        FOREIGN KEY (campaign_sk)
        REFERENCES dim_campaign(campaign_sk),

    CONSTRAINT fk_fact_date
        FOREIGN KEY (date_sk)
        REFERENCES dim_date(date_sk)
);


-- ============================================================
-- Fact table indexes
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_fact_agent
ON fact_outreach_activity(agent_sk);


CREATE INDEX IF NOT EXISTS idx_fact_lead
ON fact_outreach_activity(lead_sk);


CREATE INDEX IF NOT EXISTS idx_fact_campaign
ON fact_outreach_activity(campaign_sk);


CREATE INDEX IF NOT EXISTS idx_fact_date
ON fact_outreach_activity(date_sk);


CREATE INDEX IF NOT EXISTS idx_fact_event_timestamp
ON fact_outreach_activity(event_timestamp);