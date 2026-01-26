import pandas as pd
import pathlib

BRONZE_BASE = pathlib.Path("data/bronze/nyc_taxi")
SILVER_BASE = pathlib.Path("data/silver/nyc_taxi")

def process_partition(parquet_path: pathlib.Path) -> pd.DataFrame:
    df = pd.read_parquet(parquet_path)

    # Rename if needed
    rename_map = {}
    if "tpep_pickup_datetime" in df.columns:
        rename_map["tpep_pickup_datetime"] = "pickup_datetime"
    if "tpep_dropoff_datetime" in df.columns:
        rename_map["tpep_dropoff_datetime"] = "dropoff_datetime"

    df = df.rename(columns=rename_map)

    # Create columns if missing
    for col in ["pickup_datetime", "dropoff_datetime"]:
        if col not in df.columns:
            df[col] = pd.NaT

    # Datetime normalization
    df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"], errors="coerce")
    df["dropoff_datetime"] = pd.to_datetime(df["dropoff_datetime"], errors="coerce")

    # Filters only if columns exist
    if "trip_distance" in df.columns:
        df = df[df["trip_distance"] > 0]
    if "fare_amount" in df.columns:
        df = df[df["fare_amount"] >= 0]
    if "pickup_datetime" in df.columns and "dropoff_datetime" in df.columns:
        df = df[df["pickup_datetime"] < df["dropoff_datetime"]]

    silver_df = df[[
        col for col in [
            "pickup_datetime",
            "dropoff_datetime",
            "passenger_count",
            "trip_distance",
            "fare_amount",
            "total_amount",
            "payment_type"
        ] if col in df.columns
    ]]

    return silver_df

def run():
    for year_dir in BRONZE_BASE.glob("year=*"):
        for month_dir in year_dir.glob("month=*"):
            parquet_path = month_dir / "data.parquet"
            if not parquet_path.exists():
                print(f"⚠️ Skipping missing file: {parquet_path}")
                continue

            df = process_partition(parquet_path)

            out_dir = (
                SILVER_BASE /
                year_dir.name /
                month_dir.name
            )
            out_dir.mkdir(parents=True, exist_ok=True)

            out_file = out_dir / "data.parquet"
            df.to_parquet(out_file, index=False)

            print(f"✅ NYC Taxi Silver written: {out_file}")

if __name__ == "__main__":
    run()