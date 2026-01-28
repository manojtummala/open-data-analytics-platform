-- =========================
-- SLA BREACH DETECTION
-- =========================

CREATE OR REPLACE VIEW monitoring.sla_breaches AS
SELECT
    m.dataset,
    m.ingested_at,
    m.freshness_minutes,
    s.max_freshness_minutes,
    CASE
        WHEN m.freshness_minutes > s.max_freshness_minutes
        THEN 'FRESHNESS_BREACH'
        ELSE NULL
    END AS breach_type
FROM monitoring.dataset_metrics m
JOIN monitoring.sla_definitions s
    ON m.dataset = s.dataset
WHERE m.freshness_minutes > s.max_freshness_minutes;