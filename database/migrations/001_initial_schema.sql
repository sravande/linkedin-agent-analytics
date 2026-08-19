CREATE TABLE IF NOT EXISTS leads (
    lead_id BIGSERIAL PRIMARY KEY,
    linkedin_id VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255),
    company VARCHAR(255),
    job_title VARCHAR(255),
    status VARCHAR(100),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS outreach_events (
    event_id BIGSERIAL PRIMARY KEY,
    lead_id BIGINT NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    event_timestamp TIMESTAMPTZ NOT NULL,
    campaign_id VARCHAR(255),
    agent_id VARCHAR(255),

    CONSTRAINT fk_outreach_events_lead
        FOREIGN KEY (lead_id)
        REFERENCES leads(lead_id)
);


CREATE TABLE IF NOT EXISTS pipeline_runs (
    run_id BIGSERIAL PRIMARY KEY,
    pipeline_name VARCHAR(255) NOT NULL,
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ,
    rows_in BIGINT NOT NULL DEFAULT 0,
    rows_out BIGINT NOT NULL DEFAULT 0,
    status VARCHAR(50) NOT NULL,
    error_message TEXT,
    watermark_start TIMESTAMPTZ,
    watermark_end TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS dead_letter_records (
    dead_letter_id BIGSERIAL PRIMARY KEY,
    run_id BIGINT NOT NULL,
    record_payload JSONB NOT NULL,
    error_reason TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    retry_count INTEGER NOT NULL DEFAULT 0,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING',

    CONSTRAINT fk_dead_letter_run
        FOREIGN KEY (run_id)
        REFERENCES pipeline_runs(run_id)
);

CREATE TABLE IF NOT EXISTS pipeline_watermarks (
    pipeline_name VARCHAR(255) PRIMARY KEY,
    last_watermark TIMESTAMPTZ,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);