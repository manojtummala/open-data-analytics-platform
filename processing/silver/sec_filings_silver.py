import json
import pandas as pd
import pathlib
from datetime import datetime

BRONZE_BASE = pathlib.Path("data/bronze/sec_filings")
SILVER_BASE = pathlib.Path("data/silver/sec_filings")

def run():
    rows = []

    for partition in BRONZE_BASE.iterdir():
        json_path = partition / "filings.json"
        if not json_path.exists():
            continue
        with open(json_path) as f:
            data = json.load(f)

        for row in data.get("data", []):
            rows.append({
                "accession_number": row[4] if len(row) > 4 else None,
                "cik": row[0] if len(row) > 0 else None,
                "form_type": row[2] if len(row) > 2 else None,
                "filing_date": row[3] if len(row) > 3 else None,
                "file_name": row[5] if len(row) > 5 else None,
                "ingested_at": datetime.utcnow()
            })

    df = pd.DataFrame(rows)

    if "accession_number" in df.columns:
        df = df.dropna(subset=["accession_number"])
        df = df.drop_duplicates(subset=["accession_number"], keep="last")
    else:
        print("⚠️ No accession_number column found; skipping dedupe/dropna")

    SILVER_BASE.mkdir(parents=True, exist_ok=True)
    df.to_parquet(SILVER_BASE / "sec_filings.parquet")

    print("✅ SEC Silver written")

if __name__ == "__main__":
    run()