-- =========================
-- Schemas
-- =========================
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;
CREATE SCHEMA IF NOT EXISTS mart;

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