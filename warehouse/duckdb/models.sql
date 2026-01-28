-- DIMENSION: DATE
CREATE OR REPLACE TABLE mart.dim_date AS
SELECT DISTINCT
    date,
    EXTRACT(year FROM date) AS year,
    EXTRACT(month FROM date) AS month,
    EXTRACT(day FROM date) AS day
FROM gold.nyc_taxi_daily;

-- FACT: NYC TAXI DAILY
CREATE OR REPLACE TABLE mart.fact_taxi_daily AS
SELECT
    d.date,
    d.year,
    d.month,
    g.trips,
    g.total_revenue,
    g.avg_distance
FROM gold.nyc_taxi_daily g
JOIN mart.dim_date d
ON g.date = d.date;

-- SEC ANALYTICS
CREATE OR REPLACE VIEW mart.sec_filings_by_company AS
SELECT
    cik,
    filing_count
FROM gold.sec_company_filings;

-- GITHUB ANALYTICS
CREATE OR REPLACE VIEW mart.github_trending_repos AS
SELECT
    repo_name,
    event_count
FROM gold.github_trending
ORDER BY event_count DESC;

