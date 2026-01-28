-- Merge dataset metrics with gold tables for easy BI queries
CREATE OR REPLACE VIEW mart.nyc_taxi_with_metrics AS
SELECT
    g.date,
    -- g.total_trips,
    g.total_revenue,
    m.total_rows AS ingested_rows,
    m.freshness_minutes,
    m.passenger_count_violations,
    m.trip_distance_violations,
    m.fare_amount_violations,
    m.total_amount_violations
FROM gold.nyc_taxi_daily g
LEFT JOIN monitoring.dataset_metrics m
    ON m.dataset = 'nyc_taxi' 
    AND m.year = EXTRACT(year FROM g.date)
    AND m.month = EXTRACT(month FROM g.date);

CREATE OR REPLACE VIEW mart.sec_company_filings_with_metrics AS
SELECT
    g.cik,
    g.filing_count,
    m.total_rows AS ingested_rows,
    m.freshness_minutes
FROM gold.sec_company_filings g
LEFT JOIN monitoring.dataset_metrics m
    ON m.dataset = 'sec_filings';

CREATE OR REPLACE VIEW mart.github_trending_with_metrics AS
SELECT
    g.repo_name,
    g.event_count,
    m.total_rows AS ingested_rows,
    m.freshness_minutes
FROM gold.github_trending g
LEFT JOIN monitoring.dataset_metrics m
    ON m.dataset = 'github_events';