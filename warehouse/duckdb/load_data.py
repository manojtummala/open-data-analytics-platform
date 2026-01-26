import duckdb
from pathlib import Path

DB_PATH = "warehouse/duckdb/analytics.duckdb"
INIT_SQL = "warehouse/duckdb/init.sql"

TABLE_CONFIG = [
    # silver
    ("silver", "nyc_taxi", "data/silver/nyc_taxi/**/*.parquet", "pickup_datetime"),
    ("silver", "github_events", "data/silver/github_events/**/*.parquet", "event_id"),
    ("silver", "sec_filings", "data/silver/sec_filings/*.parquet", "accession_number"),

    # gold
    ("gold", "nyc_taxi_daily", "data/gold/nyc_taxi/*.parquet", "date"),
    ("gold", "github_trending", "data/gold/github_events/*.parquet", "repo_name"),
    ("gold", "sec_company_filings", "data/gold/sec_filings/*.parquet", "cik"),
]


def run_init(con):
    if not Path(INIT_SQL).exists():
        raise FileNotFoundError("init.sql not found")

    with open(INIT_SQL, "r") as f:
        con.execute(f.read())

    print("✅ DuckDB schemas initialized")


def parquet_has_columns(con, parquet_path: str) -> bool:
    try:
        cols = con.execute(
            f"DESCRIBE SELECT * FROM read_parquet('{parquet_path}')"
        ).fetchall()
        return len(cols) > 0
    except Exception:
        return False


def incremental_load(con, schema, table, path_glob, pk):
    files = list(Path().glob(path_glob))
    if not files:
        print(f"⚠️  {schema}.{table}: no parquet files found — skipping")
        return

    # Check at least one valid parquet file
    valid_file = None
    for f in files:
        if parquet_has_columns(con, str(f)):
            valid_file = str(f)
            break

    if not valid_file:
        print(f"⚠️  {schema}.{table}: parquet files exist but contain no columns — skipping")
        return

    fq_table = f"{schema}.{table}"

    # Create table if missing
    con.execute(f"""
        CREATE TABLE IF NOT EXISTS {fq_table} AS
        SELECT * FROM read_parquet('{valid_file}')
        LIMIT 0
    """)

    # Incremental insert
    con.execute(f"""
        INSERT INTO {fq_table}
        SELECT *
        FROM read_parquet('{path_glob}') src
        WHERE NOT EXISTS (
            SELECT 1 FROM {fq_table} tgt
            WHERE tgt.{pk} = src.{pk}
        )
    """)

    print(f"✅ Loaded {fq_table}")


def run():
    Path("warehouse/duckdb").mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(DB_PATH)

    # 🔹 auto-init schemas
    run_init(con)

    # 🔹 incremental loads
    for schema, table, path, pk in TABLE_CONFIG:
        incremental_load(con, schema, table, path, pk)

    con.close()
    print("🎉 DuckDB load complete")


if __name__ == "__main__":
    run()