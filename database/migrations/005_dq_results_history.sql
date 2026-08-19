-- ============================================================
-- Part 4: Data Quality Results History
-- ============================================================

CREATE TABLE IF NOT EXISTS dq_results_history (
    run_id BIGINT NOT NULL,

    execution_timestamp TIMESTAMPTZ NOT NULL,

    completeness_score DECIMAL(5,2) NOT NULL,
    uniqueness_score DECIMAL(5,2) NOT NULL,
    validity_score DECIMAL(5,2) NOT NULL,
    timeliness_score DECIMAL(5,2) NOT NULL,
    referential_integrity_score DECIMAL(5,2) NOT NULL,

    composite_dq_score DECIMAL(5,2) NOT NULL,

    pass_fail_status VARCHAR(10) NOT NULL,

    failed_test_count INTEGER NOT NULL DEFAULT 0,

    error_message VARCHAR(500),

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_dq_results_history
        PRIMARY KEY (run_id, execution_timestamp),

    CONSTRAINT chk_dq_completeness_score
        CHECK (completeness_score BETWEEN 0 AND 100),

    CONSTRAINT chk_dq_uniqueness_score
        CHECK (uniqueness_score BETWEEN 0 AND 100),

    CONSTRAINT chk_dq_validity_score
        CHECK (validity_score BETWEEN 0 AND 100),

    CONSTRAINT chk_dq_timeliness_score
        CHECK (timeliness_score BETWEEN 0 AND 100),

    CONSTRAINT chk_dq_referential_score
        CHECK (referential_integrity_score BETWEEN 0 AND 100),

    CONSTRAINT chk_dq_composite_score
        CHECK (composite_dq_score BETWEEN 0 AND 100),

    CONSTRAINT chk_dq_pass_fail_status
        CHECK (pass_fail_status IN ('PASS', 'FAIL')),

    CONSTRAINT chk_dq_failed_test_count
        CHECK (failed_test_count >= 0)
);