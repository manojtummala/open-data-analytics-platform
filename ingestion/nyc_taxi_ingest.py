import os
import requests
import pandas as pd
from datetime import datetime
from pathlib import Path
import hashlib

BRONZE_BASE_PATH = "data/bronze/nyc_taxi"
METADATA_PATH = "data/bronze/_metadata"
os.makedirs(METADATA_PATH, exist_ok=True)


def download_file(url: str, local_path: str):
    response = requests.get(url, stream=True, timeout=30)
    response.raise_for_status()

    with open(local_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            f.write(chunk)


def compute_schema_hash(columns):
    joined = ",".join(sorted(columns))
    return hashlib.md5(joined.encode()).hexdigest()


def ingest_month(year: int, month: int):
    month_str = f"{month:02d}"
    file_name = f"yellow_tripdata_{year}-{month_str}.parquet"
    source_url = (
        f"https://d37ci6vzurychx.cloudfront.net/trip-data/{file_name}"
    )

    print(f"Starting ingestion for {year}-{month_str}")

    # Temp download location
    tmp_dir = Path("tmp")
    tmp_dir.mkdir(exist_ok=True)
    local_csv = tmp_dir / file_name

    # Download
    download_file(source_url, str(local_csv))

    # Read CSV (bronze = no strict schema enforcement)
    df = pd.read_parquet(local_csv)

    if df.empty:
        raise ValueError("Downloaded file is empty")

    row_count = len(df)
    schema_hash = compute_schema_hash(df.columns)

    # Partitioned output path
    output_dir = (
        Path(BRONZE_BASE_PATH)
        / f"year={year}"
        / f"month={month_str}"
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "data.parquet"

    # Idempotent overwrite
    df.to_parquet(output_file, index=False)

    # Write ingestion metadata
    metadata_record = {
        "dataset": "nyc_taxi",
        "year": year,
        "month": month,
        "row_count": row_count,
        "schema_hash": schema_hash,
        "source_url": source_url,
        "ingested_at": datetime.utcnow().isoformat()
    }

    metadata_df = pd.DataFrame([metadata_record])
    metadata_file = Path(METADATA_PATH) / "nyc_taxi_ingestion_log.parquet"

    if metadata_file.exists():
        existing = pd.read_parquet(metadata_file)
        metadata_df = pd.concat([existing, metadata_df], ignore_index=True)

    metadata_df.to_parquet(metadata_file, index=False)

    print(
        f"Ingested {row_count} rows for {year}-{month_str} "
        f"→ {output_file}"
    )

    # Cleanup
    local_csv.unlink(missing_ok=True)


if __name__ == "__main__":
    # Example: ingest January 2024
    ingest_month(2024, 1)