-- NYC Taxi: Top revenue days
SELECT *
FROM mart.fact_taxi_daily
ORDER BY total_revenue DESC
LIMIT 10;

-- NYC Taxi: Monthly revenue trend
SELECT
    year,
    month,
    SUM(total_revenue) AS monthly_revenue
FROM mart.fact_taxi_daily
GROUP BY year, month
ORDER BY year, month;

-- SEC: Companies with most filings
SELECT *
FROM mart.sec_filings_by_company
ORDER BY filing_count DESC
LIMIT 10;

-- GitHub: Trending repositories
SELECT *
FROM mart.github_trending_repos
LIMIT 10;