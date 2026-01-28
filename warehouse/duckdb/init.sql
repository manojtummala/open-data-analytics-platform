-- =========================
-- Schemas
-- =========================
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;
CREATE SCHEMA IF NOT EXISTS mart;
CREATE SCHEMA IF NOT EXISTS monitoring;

-- =========================
-- SILVER TABLES (EMPTY)
-- =========================
CREATE TABLE IF NOT EXISTS silver.nyc_taxi (
    pickup_datetime TIMESTAMP,
    dropoff_datetime TIMESTAMP,
    passenger_count INTEGER,
    trip_distance DOUBLE,
    fare_amount DOUBLE,
    total_amount DOUBLE,
    payment_type INTEGER
);

CREATE TABLE IF NOT EXISTS silver.github_events (
    event_id VARCHAR,
    event_type VARCHAR,
    repo_name VARCHAR,
    actor_login VARCHAR,
    created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS silver.sec_filings (
    accession_number VARCHAR,
    cik VARCHAR,
    company_name VARCHAR,
    form_type VARCHAR,
    filing_date DATE
);

-- =========================
-- GOLD TABLES (EMPTY)
-- =========================
CREATE TABLE IF NOT EXISTS gold.nyc_taxi_daily (
    date DATE,
    total_trips BIGINT,
    total_revenue DOUBLE
);

CREATE TABLE IF NOT EXISTS gold.github_trending (
    repo_name VARCHAR,
    event_count BIGINT
);

CREATE TABLE IF NOT EXISTS gold.sec_company_filings (
    cik VARCHAR,
    filing_count BIGINT
);


-- =========================
-- MONITORING
-- =========================
CREATE SCHEMA IF NOT EXISTS monitoring;

CREATE TABLE IF NOT EXISTS monitoring.dataset_metrics (
    dataset VARCHAR,
    year INT,
    month INT,
    total_rows BIGINT,
    freshness_minutes DOUBLE,
    passenger_count_violations BIGINT,
    trip_distance_violations BIGINT,
    fare_amount_violations BIGINT,
    total_amount_violations BIGINT,
    ingested_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS monitoring.sla_definitions (
    dataset VARCHAR PRIMARY KEY,
    max_freshness_minutes DOUBLE,
    max_violation_ratio DOUBLE
);

CREATE TABLE IF NOT EXISTS monitoring.dataset_lineage (
    dataset VARCHAR PRIMARY KEY,
    source VARCHAR,
    bronze_path VARCHAR,
    silver_path VARCHAR,
    gold_table VARCHAR
);