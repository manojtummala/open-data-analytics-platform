import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

METADATA_FILE = "data/bronze/_metadata/nyc_taxi_ingestion_log.parquet"
SLA_FILE = "monitoring/freshness_sla.parquet"

SLA_DAYS = 35


def track_nyc_taxi_sla():
    if not Path(METADATA_FILE).exists():
        raise FileNotFoundError("No ingestion metadata found")

    metadata = pd.read_parquet(METADATA_FILE)

    records = []

    for _, row in metadata.iterrows():
        year = int(row["year"])
        month = int(row["month"])
        ingested_at = pd.to_datetime(row["ingested_at"])

        month_end = datetime(year, month, 1) + timedelta(days=32)
        month_end = month_end.replace(day=1) - timedelta(days=1)

        expected_by = month_end + timedelta(days=SLA_DAYS)
        delay_days = (ingested_at - expected_by).days

        status = "OK" if delay_days <= 0 else "BREACHED"

        records.append({
            "dataset": "nyc_taxi",
            "year": year,
            "month": month,
            "expected_by": expected_by.date(),
            "ingested_at": ingested_at,
            "delay_days": max(delay_days, 0),
            "status": status
        })

    sla_df = pd.DataFrame(records)
    sla_df.to_parquet(SLA_FILE, index=False)

    print("Freshness SLA updated")


if __name__ == "__main__":
    track_nyc_taxi_sla()