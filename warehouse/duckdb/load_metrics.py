import duckdb
import pandas as pd
from pathlib import Path

DB_PATH = "warehouse/duckdb/analytics.duckdb"
QUALITY_BASE = "monitoring"
METRICS_FILE = Path(QUALITY_BASE) / "data_quality_metrics.parquet"


def load_quality_metrics(con: duckdb.DuckDBPyConnection):
    if not METRICS_FILE.exists():
        print("⚠️  No monitoring parquet file found — skipping metrics load")
        return

    df = pd.read_parquet(METRICS_FILE)

    if df.empty:
        print("⚠️  Metrics parquet exists but is empty — skipping insert")
        return

    # -----------------------------
    # Normalize / clean data types
    # -----------------------------

    # Required columns (guarantee existence)
    required_columns = [
        "dataset",
        "year",
        "month",
        "total_rows",
        "freshness_minutes",
        "passenger_count_violations",
        "trip_distance_violations",
        "fare_amount_violations",
        "total_amount_violations",
        "ingested_at",
    ]

    for col in required_columns:
        if col not in df.columns:
            df[col] = None

    # Integers: NaN -> 0
    int_columns = [
        "year",
        "month",
        "total_rows",
        "passenger_count_violations",
        "trip_distance_violations",
        "fare_amount_violations",
        "total_amount_violations",
    ]

    for col in int_columns:
        df[col] = df[col].fillna(0).astype(int)

    # Freshness stays float (nullable)
    df["freshness_minutes"] = pd.to_numeric(
        df["freshness_minutes"], errors="coerce"
    )

    # Timestamps
    df["ingested_at"] = pd.to_datetime(
        df["ingested_at"], errors="coerce"
    )

    # -----------------------------
    # Insert into DuckDB
    # -----------------------------

    con.execute("""
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
        )
    """)

    # Insert row-by-row (safe + explicit)
    for _, row in df.iterrows():
        con.execute(
            """
            INSERT INTO monitoring.dataset_metrics VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                row["dataset"],
                row["year"],
                row["month"],
                row["total_rows"],
                row["freshness_minutes"],
                row["passenger_count_violations"],
                row["trip_distance_violations"],
                row["fare_amount_violations"],
                row["total_amount_violations"],
                row["ingested_at"],
            ],
        )

    print("✅ Monitoring metrics loaded into DuckDB")


def run():
    con = duckdb.connect(DB_PATH)
    load_quality_metrics(con)
    con.close()


if __name__ == "__main__":
    run()