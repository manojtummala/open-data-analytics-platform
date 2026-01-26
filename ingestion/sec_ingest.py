import json
import pathlib
from datetime import date, timedelta

from ingestion.utils import get_with_retry

BRONZE_BASE = pathlib.Path("data/bronze/sec_filings")

def get_target_date():
    # SEC publishes complete data with a 1-day lag
    return date.today() - timedelta(days=1)

def fetch_daily_index(target_date: date):
    year = target_date.year
    quarter = f"QTR{((target_date.month - 1) // 3) + 1}"
    date_str = target_date.strftime("%Y%m%d")

    url = (
        f"https://www.sec.gov/Archives/edgar/daily-index/"
        f"{year}/{quarter}/master.{date_str}.json"
    )

    try:
        response = get_with_retry(url)
        return response.json()
    except RuntimeError as exc:
        # SEC data not published yet
        print(f"⚠️ SEC index not available for {target_date} yet")
        print(f"⚠️ URL: {url}")
        return None

def write_bronze(data, ingestion_date: date):
    partition_path = BRONZE_BASE / f"ingestion_date={ingestion_date}"
    partition_path.mkdir(parents=True, exist_ok=True)

    output_file = partition_path / "filings.json"
    with open(output_file, "w") as f:
        json.dump(data, f)

    print(f"✅ Wrote SEC filings to {output_file}")

def ingest():
    target_date = get_target_date()
    print(f"Starting SEC ingestion for {target_date}")

    data = fetch_daily_index(target_date)

    if data is None:
        print("⏭️ Skipping ingestion — data not available yet")
        return

    write_bronze(data, target_date)

if __name__ == "__main__":
    ingest()