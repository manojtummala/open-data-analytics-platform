import pandas as pd
from pathlib import Path

SILVER_PATH = Path("data/silver/sec_filings/sec_filings.parquet")
GOLD_BASE = Path("data/gold/sec_filings")
GOLD_BASE.mkdir(parents=True, exist_ok=True)

REQUIRED_COLS = {"cik", "accession_number"}

def run():
    if not SILVER_PATH.exists():
        print("⚠️ SEC Silver file not found — skipping Gold")
        return

    df = pd.read_parquet(SILVER_PATH)

    # Empty dataset case
    if df.empty:
        print("⚠️ SEC Silver is empty — no Gold metrics generated")
        return

    # Missing schema case
    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        print(f"⚠️ SEC Silver missing columns {missing} — skipping Gold")
        return

    gold_df = (
        df.groupby("cik")
        .agg(filing_count=("accession_number", "count"))
        .reset_index()
        .sort_values("filing_count", ascending=False)
    )

    gold_df.to_parquet(
        GOLD_BASE / "company_filing_counts.parquet",
        index=False
    )

    print("✅ SEC Filings Gold written")

if __name__ == "__main__":
    run()