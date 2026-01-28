INSERT OR REPLACE INTO monitoring.dataset_lineage VALUES
(
  'nyc_taxi',
  'NYC TLC Open Data',
  'data/bronze/nyc_taxi',
  'data/silver/nyc_taxi',
  'gold.nyc_taxi_daily'
),
(
  'sec_filings',
  'SEC EDGAR',
  'data/bronze/sec_filings',
  'data/silver/sec_filings',
  'gold.sec_company_filings'
),
(
  'github_events',
  'GitHub Events API',
  'data/bronze/github_events',
  'data/silver/github_events',
  'gold.github_trending'
);