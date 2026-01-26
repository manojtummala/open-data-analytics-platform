import pandas as pd
from datetime import datetime
from pathlib import Path

from monitoring_config import SILVER_DATASETS, MONITORING_BASE

OUTPUT_FILE = MONITORING_BASE / "data_quality_metrics.parquet"

def to_utc(ts: pd.Timestamp) -> pd.Timestamp:
    if ts.tzinfo is None:
        return ts.tz_localize("UTC")
    return ts.tz_convert("UTC")

def compute_metrics(dataset_name, config):
    path = config["path"]
    if not path.exists():
        print(f"⚠️ Dataset not found: {dataset_name}")
        return None

    # Load dataset
    if path.is_dir():
        all_files = list(path.glob("**/*.parquet"))
        if not all_files:
            print(f"⚠️ No Parquet files for {dataset_name}")
            return None
        df = pd.concat([pd.read_parquet(f) for f in all_files], ignore_index=True)
    else:
        df = pd.read_parquet(path)

    row_count = len(df)

    # Freshness
    freshness = None
    for dt_col in config.get("datetime_cols", []):
        if dt_col in df.columns:
            max_ts = pd.to_datetime(df[dt_col], errors="coerce").max()

            if pd.notna(max_ts):
                print(
                    f"[DEBUG] dataset={dataset_name}, column={dt_col}, "
                    f"max_ts={max_ts}, tzinfo={max_ts.tzinfo}"
                )

                max_ts = to_utc(max_ts)
                now = to_utc(pd.Timestamp.utcnow())

                freshness = (now - max_ts).total_seconds() / 60
                break

    # Quality violations
    violations = {}
    for col, rule in config.get("quality_rules", {}).items():
        if col in df.columns:
            try:
                valid_mask = rule(df[col])
                violations[col] = int((~valid_mask).sum())
            except Exception:
                violations[col] = -1
        else:
            violations[col] = -1

    record = {
        "dataset": dataset_name,
        "row_count": row_count,
        "freshness_minutes": freshness,
        "last_ingested_at": datetime.utcnow().isoformat(),
    }

    for k, v in violations.items():
        record[f"{k}_violations"] = v

    return record

def run_monitoring():
    records = []
    for name, cfg in SILVER_DATASETS.items():
        metrics = compute_metrics(name, cfg)
        if metrics:
            records.append(metrics)

    if not records:
        print("⚠️ No metrics to write")
        return

    metrics_df = pd.DataFrame(records)
    if OUTPUT_FILE.exists():
        existing = pd.read_parquet(OUTPUT_FILE)
        metrics_df = pd.concat([existing, metrics_df], ignore_index=True)

    metrics_df.to_parquet(OUTPUT_FILE, index=False)
    print(f"✅ Monitoring metrics updated at {OUTPUT_FILE}")
    print(metrics_df)

if __name__ == "__main__":
    run_monitoring()