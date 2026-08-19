-- ============================================================
-- Part 4: Data Quality Checks
-- ============================================================


-- ============================================================
-- 1. COMPLETENESS
-- ============================================================

-- Fact records must have required dimension keys.

SELECT
    COUNT(*) AS invalid_rows
FROM fact_outreach_activity
WHERE agent_sk IS NULL
   OR lead_sk IS NULL
   OR date_sk IS NULL;


-- Interaction ID must not be NULL.

SELECT
    COUNT(*) AS invalid_rows
FROM fact_outreach_activity
WHERE interaction_id IS NULL;


-- Interaction type must not be NULL.

SELECT
    COUNT(*) AS invalid_rows
FROM fact_outreach_activity
WHERE interaction_type IS NULL;


-- Event timestamp must not be NULL.

SELECT
    COUNT(*) AS invalid_rows
FROM fact_outreach_activity
WHERE event_timestamp IS NULL;


-- ============================================================
-- 2. UNIQUENESS
-- ============================================================

-- Interaction IDs must be unique.

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT interaction_id) AS distinct_interaction_ids
FROM fact_outreach_activity;


-- Duplicate interaction IDs.

SELECT
    interaction_id,
    COUNT(*) AS duplicate_count
FROM fact_outreach_activity
GROUP BY interaction_id
HAVING COUNT(*) > 1;


-- Duplicate current Agent dimension records should not exist.

SELECT
    agent_id,
    COUNT(*) AS current_versions
FROM dim_agent
WHERE is_current_flag = TRUE
GROUP BY agent_id
HAVING COUNT(*) > 1;


-- ============================================================
-- 3. VALIDITY
-- ============================================================

-- Valid Agent Account Age Tier values.

SELECT
    COUNT(*) AS invalid_rows
FROM dim_agent
WHERE account_age_tier IS NOT NULL
  AND account_age_tier NOT IN (
      '<1 Month',
      '1 Month',
      '2-6 Months',
      '6-12 Months',
      '1+ Year'
  );


-- Valid risk classification values.

SELECT
    COUNT(*) AS invalid_rows
FROM dim_agent
WHERE risk_classification IS NOT NULL
  AND risk_classification NOT IN (
      'Very High Risk',
      'High Risk',
      'Moderate Risk',
      'Low Risk',
      'Minimal Risk'
  );


-- Valid interaction types.

SELECT
    COUNT(*) AS invalid_rows
FROM fact_outreach_activity
WHERE interaction_type NOT IN (
    'INVITE_SENT',
    'INVITE_ACCEPTED',
    'MESSAGE_SENT',
    'REPLY_RECEIVED'
);


-- Count measures must never be negative.

SELECT
    COUNT(*) AS invalid_rows
FROM fact_outreach_activity
WHERE invites_sent_count < 0
   OR invites_accepted_count < 0
   OR messages_sent_count < 0
   OR replies_received_count < 0;


-- Daily utilisation percentage must be between 0 and 100.

SELECT
    COUNT(*) AS invalid_rows
FROM fact_outreach_activity
WHERE daily_limit_utilised_pct < 0
   OR daily_limit_utilised_pct > 100;


-- Response time cannot be negative.

SELECT
    COUNT(*) AS invalid_rows
FROM fact_outreach_activity
WHERE response_time_minutes < 0;


-- ============================================================
-- 4. TIMELINESS
-- ============================================================

-- Events must not occur in the future.

SELECT
    COUNT(*) AS invalid_rows
FROM fact_outreach_activity
WHERE event_timestamp > CURRENT_TIMESTAMP;


-- Latest event timestamp.

SELECT
    MAX(event_timestamp) AS latest_event_timestamp
FROM fact_outreach_activity;


-- ============================================================
-- 5. REFERENTIAL INTEGRITY
-- ============================================================

-- Fact -> Agent

SELECT
    COUNT(*) AS orphan_agent_rows
FROM fact_outreach_activity f
LEFT JOIN dim_agent a
    ON f.agent_sk = a.agent_sk
WHERE a.agent_sk IS NULL;


-- Fact -> Lead

SELECT
    COUNT(*) AS orphan_lead_rows
FROM fact_outreach_activity f
LEFT JOIN dim_lead l
    ON f.lead_sk = l.lead_sk
WHERE l.lead_sk IS NULL;


-- Fact -> Campaign

SELECT
    COUNT(*) AS orphan_campaign_rows
FROM fact_outreach_activity f
LEFT JOIN dim_campaign c
    ON f.campaign_sk = c.campaign_sk
WHERE f.campaign_sk IS NOT NULL
  AND c.campaign_sk IS NULL;


-- Fact -> Date

SELECT
    COUNT(*) AS orphan_date_rows
FROM fact_outreach_activity f
LEFT JOIN dim_date d
    ON f.date_sk = d.date_sk
WHERE d.date_sk IS NULL;