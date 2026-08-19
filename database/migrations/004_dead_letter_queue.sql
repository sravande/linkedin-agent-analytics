CREATE TABLE IF NOT EXISTS stg_dead_letter_queue (
    dead_letter_id BIGSERIAL PRIMARY KEY,

    run_id BIGINT,

    record_payload JSONB NOT NULL,

    error_reason TEXT NOT NULL,

    retry_count INTEGER NOT NULL DEFAULT 0,

    status VARCHAR(30) NOT NULL DEFAULT 'PENDING',

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    reviewed_at TIMESTAMPTZ,

    reviewed_by VARCHAR(255)
);