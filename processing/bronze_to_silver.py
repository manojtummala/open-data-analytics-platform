import os
import pandas as pd
from pathlib import Path
from datetime import datetime

BRONZE_BASE = "data/bronze/nyc_taxi"
SILVER_BASE = "data/silver/nyc_taxi"
QUALITY_BASE = "monitoring"

os.makedirs(QUALITY_BASE, exist_ok=True)

VALIDATION_RULES = {
    "passenger_count": lambda x: x >= 0,
    "trip_distance": lambda x: x >= 0,
    "fare_amount": lambda x: x >= 0,
    "total_amount": lambda x: x >= 0,
}


def load_bronze(year: int, month: int) -> pd.DataFrame:
    month_str = f"{month:02d}"
    path = (
        Path(BRONZE_BASE)
        / f"year={year}"
        / f"month={month_str}"
        / "data.parquet"
    )
    if not path.exists():
        raise FileNotFoundError(f"Bronze data not found: {path}")
    return pd.read_parquet(path)


def enforce_schema(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Datetime columns
    for col in ["pickup_datetime", "dropoff_datetime"]:
        if col not in df.columns:
            df[col] = pd.NaT
        df[col] = pd.to_datetime(df[col], errors="coerce")

    # Integer columns (nullable)
    for col in ["passenger_count", "payment_type"]:
        if col not in df.columns:
            df[col] = pd.NA
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    # Float columns
    for col in ["trip_distance", "fare_amount", "total_amount"]:
        if col not in df.columns:
            df[col] = pd.NA
        df[col] = pd.to_numeric(df[col], errors="coerce")

    ordered_cols = [
        "pickup_datetime",
        "dropoff_datetime",
        "passenger_count",
        "trip_distance",
        "fare_amount",
        "total_amount",
        "payment_type",
    ]

    return df[ordered_cols]


def validate_data(df: pd.DataFrame):
    violations = {}

    for col, rule in VALIDATION_RULES.items():
        invalid_mask = ~rule(df[col].fillna(0))
        violations[col] = int(invalid_mask.sum())

    return violations


def write_quality_metrics(
    year: int,
    month: int,
    total_rows: int,
    violations: dict,
):
    record = {
        "dataset": "nyc_taxi",
        "year": year,
        "month": month,
        "total_rows": total_rows,
        "ingested_at": datetime.utcnow().isoformat(),
    }

    for col, count in violations.items():
        record[f"{col}_violations"] = count

    metrics_df = pd.DataFrame([record])

    output_file = Path(QUALITY_BASE) / "data_quality_metrics.parquet"

    if output_file.exists():
        existing = pd.read_parquet(output_file)
        metrics_df = pd.concat([existing, metrics_df], ignore_index=True)

    metrics_df.to_parquet(output_file, index=False)


def write_silver(df: pd.DataFrame, year: int, month: int):
    month_str = f"{month:02d}"
    out_dir = (
        Path(SILVER_BASE)
        / f"year={year}"
        / f"month={month_str}"
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    out_file = out_dir / "data.parquet"
    df.to_parquet(out_file, index=False)


def run_bronze_to_silver(year: int, month: int):
    print(f"Processing Bronze → Silver for {year}-{month:02d}")

    bronze_df = load_bronze(year, month)
    total_rows = len(bronze_df)

    silver_df = enforce_schema(bronze_df)
    violations = validate_data(silver_df)

    write_silver(silver_df, year, month)
    write_quality_metrics(year, month, total_rows, violations)

    print("Silver data written")
    print("Quality metrics:", violations)


if __name__ == "__main__":
    run_bronze_to_silver(2024, 1)