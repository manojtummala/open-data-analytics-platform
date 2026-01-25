import duckdb
from pathlib import Path

DB_PATH = "warehouse/analytics.duckdb"
SILVER_BASE = "data/silver/nyc_taxi"

def init_db():
    Path("warehouse").mkdir(exist_ok=True)
    con = duckdb.connect(DB_PATH)

    con.execute("CREATE SCHEMA IF NOT EXISTS GOLD")

    con.execute(f"""
        CREATE OR REPLACE VIEW silver_nyc_taxi AS
        SELECT *
        FROM read_parquet('{SILVER_BASE}/**/*.parquet', hive_partitioning=1) 
    """)

    con.close()

    print("DuckDB initialized")

if __name__ == "__main__":
    init_db()