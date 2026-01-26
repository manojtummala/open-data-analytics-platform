import pandas as pd
from pathlib import Path
from datetime import datetime

MONITORING_PATH = Path("monitoring/data_quality_metrics.parquet")
GOLD_BASE = Path("data/gold")
OUTPUT_PATH = Path("monitoring/gold_health.parquet")

GOLD_CONFIG = {
    "nyc_taxi": {
        "table": "daily_taxi_metrics.parquet",
        "sla_minutes": 60,
    },
    "sec_filings": {
        "table": "company_filing_counts.parquet",
        "sla_minutes": 1440,
    },
    "github_events": {
        "table": "trending_repos.parquet",
        "sla_minutes": 5,
    },
}

def run():
    monitoring_df = pd.read_parquet(MONITORING_PATH)

    records = []

    for dataset, cfg in GOLD_CONFIG.items():
        gold_path = GOLD_BASE / dataset / cfg["table"]

        if not gold_path.exists():
            continue

        gold_df = pd.read_parquet(gold_path)

        row_count = len(gold_df)

        last_monitor = (
            monitoring_df
            [monitoring_df["dataset"] == dataset]
            .sort_values("last_ingested_at", ascending=False)
            .head(1)
        )

        if last_monitor.empty:
            continue

        freshness = last_monitor.iloc[0]["freshness_minutes"]
        sla = cfg["sla_minutes"]

        records.append({
            "dataset": dataset,
            "gold_table": cfg["table"],
            "row_count": row_count,
            "freshness_minutes": freshness,
            "sla_minutes": sla,
            "sla_breached": freshness > sla,
            "checked_at": datetime.utcnow().isoformat()
        })

    pd.DataFrame(records).to_parquet(OUTPUT_PATH, index=False)
    print("✅ Gold health metrics written")

if __name__ == "__main__":
    run()