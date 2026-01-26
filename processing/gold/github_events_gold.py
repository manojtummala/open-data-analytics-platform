import pandas as pd
from pathlib import Path

SILVER_PATH = Path("data/silver/github_events/github_events.parquet")
GOLD_BASE = Path("data/gold/github_events")
GOLD_BASE.mkdir(parents=True, exist_ok=True)

def run():
    if not SILVER_PATH.exists():
        print("⚠️ GitHub Silver data missing")
        return

    df = pd.read_parquet(SILVER_PATH)

    gold_df = (
        df.groupby("repo_name")
        .agg(event_count=("event_type", "count"))
        .reset_index()
        .sort_values("event_count", ascending=False)
    )

    gold_df.to_parquet(GOLD_BASE / "trending_repos.parquet", index=False)
    print("✅ GitHub Gold written")

if __name__ == "__main__":
    run()