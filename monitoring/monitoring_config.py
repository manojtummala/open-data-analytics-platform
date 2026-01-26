from pathlib import Path

MONITORING_BASE = Path("monitoring")
MONITORING_BASE.mkdir(exist_ok=True)

SILVER_DATASETS = {
    "nyc_taxi": {
        "path": Path("data/silver/nyc_taxi"),
        "datetime_cols": ["pickup_datetime", "dropoff_datetime"],
        "quality_rules": {
            "passenger_count": lambda x: x >= 0,
            "trip_distance": lambda x: x >= 0,
            "fare_amount": lambda x: x >= 0,
            "total_amount": lambda x: x >= 0,
        }
    },
    "sec_filings": {
        "path": Path("data/silver/sec_filings/sec_filings.parquet"),
        "datetime_cols": ["filing_date"],
        "quality_rules": {
            "accession_number": lambda x: x.notna()
        }
    },
    "github_events": {
        "path": Path("data/silver/github_events/github_events.parquet"),
        "datetime_cols": ["created_at"],
        "quality_rules": {
            "event_id": lambda x: x.notna()
        }
    }
}