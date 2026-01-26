import json
import pandas as pd
import pathlib
from datetime import datetime

BRONZE_BASE = pathlib.Path("data/bronze/github_events")
SILVER_BASE = pathlib.Path("data/silver/github_events")

def run():
    rows = []

    for partition in BRONZE_BASE.iterdir():
        with open(partition / "events.json") as f:
            events = json.load(f)

        for e in events:
            rows.append({
                "event_id": e["id"],
                "event_type": e["type"],
                "repo_name": e.get("repo", {}).get("name"),
                "actor_login": e.get("actor", {}).get("login"),
                "created_at": e["created_at"],
                "ingested_at": datetime.utcnow()
            })

    df = pd.DataFrame(rows)
    df["created_at"] = pd.to_datetime(df["created_at"])

    df = df.dropna(subset=["event_id"])
    df = df.drop_duplicates(subset=["event_id"], keep="last")

    SILVER_BASE.mkdir(parents=True, exist_ok=True)
    df.to_parquet(SILVER_BASE / "github_events.parquet")

    print("✅ GitHub Events Silver written")

if __name__ == "__main__":
    run()