import json
import pathlib
from datetime import datetime

from ingestion.utils import get_with_retry

BRONZE_BASE = pathlib.Path("data/bronze/github_events")
GITHUB_EVENTS_URL = "https://api.github.com/events"

def fetch_events():
    response = get_with_retry(GITHUB_EVENTS_URL)
    return response.json()

def write_bronze(events):
    ingestion_ts = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S")
    partition_path = BRONZE_BASE / f"ingestion_ts={ingestion_ts}"
    partition_path.mkdir(parents=True, exist_ok=True)

    output_file = partition_path / "events.json"
    with open(output_file, "w") as f:
        json.dump(events, f)

    print(f"✅ Wrote {len(events)} GitHub events to {output_file}")

def ingest():
    print("Starting GitHub Events ingestion")
    events = fetch_events()
    write_bronze(events)

if __name__ == "__main__":
    ingest()