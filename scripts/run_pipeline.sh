#!/bin/bash

set -e

python ingestion/nyc_ingest.py
python ingestion/sec_ingest.py
python ingestion/github_ingest.py

python processing/silver/nyc_taxi_silver.py
python processing/silver/sec_filings_silver.py
python processing/silver/github_events_silver.py

python processing/gold/nyc_taxi_gold.py
python processing/gold/sec_filings_gold.py
python processing/gold/github_gold.py

python monitoring/monitoring.py
python warehouse/duckdb/load_data.py
python warehouse/duckdb/load_metrics.py