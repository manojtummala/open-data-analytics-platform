import pandas as pd
from pathlib import Path

SILVER_BASE = Path("data/silver/nyc_taxi")
GOLD_BASE = Path("data/gold/nyc_taxi")
GOLD_BASE.mkdir(parents=True, exist_ok=True)

def run():
    frames = []

    for partition in SILVER_BASE.glob("year=*/month=*/data.parquet"):
        df = pd.read_parquet(partition)
        frames.append(df)

    if not frames:
        print("⚠️ No Silver NYC Taxi data found")
        return

    df = pd.concat(frames, ignore_index=True)

    df["date"] = df["pickup_datetime"].dt.date

    gold_df = (
        df.groupby("date")
        .agg(
            trips=("pickup_datetime", "count"),
            total_revenue=("total_amount", "sum"),
            avg_distance=("trip_distance", "mean"),
        )
        .reset_index()
    )

    gold_df.to_parquet(GOLD_BASE / "daily_taxi_metrics.parquet", index=False)
    print("✅ NYC Taxi Gold written")

if __name__ == "__main__":
    run()