# Open Data Analytics Platform

## Overview
End-to-end lakehouse-style data platform built on open public datasets. The system models how modern data engineering pipelines ingest, standardize, monitor, and serve analytics across multiple heterogeneous sources, following production-grade architectural patterns used in large-scale data organizations.

---

## Data Sources

### NYC Taxi Trips
- High-volume fact-style dataset
- Batch file ingestion
- Represents large analytical tables with heavy aggregation workloads

### SEC EDGAR Filings
- Regulatory metadata ingestion
- Daily batch processing
- Represents compliance-driven, semi-structured enterprise data

### GitHub Events
- Event-style dataset
- High cardinality, time-series oriented
- Represents user and activity tracking pipelines

Each source introduces different ingestion, schema, and modeling constraints commonly encountered in production data platforms.

---

## Architecture Pattern

- Lakehouse-style architecture
- Separation of storage, compute, and analytics
- Medallion layering:
  - **Bronze**: raw, immutable data
  - **Silver**: clean, conformed datasets
  - **Gold**: business-facing aggregates

All datasets are stored as Parquet and queried through an analytical warehouse layer.

---

## Ingestion Layer

- Python-based ingestion jobs
- Source-specific logic
- Retry handling and API safety
- Partitioned writes by ingestion date

Ingestion is decoupled from downstream processing to support backfills, replayability, and schema evolution.

---

## Bronze Layer

- Immutable, append-only storage
- Minimal transformation
- Partitioned by source and date
- Serves as system of record

Bronze preserves raw source fidelity and enables deterministic reprocessing.

---

## Silver Layer

- Source-specific transformation logic
- Schema enforcement and type normalization
- Null handling and deduplication
- Data quality validation
- Safe handling of empty or delayed upstream data

Silver represents contract-bound, analytics-safe datasets consumed downstream.

---

## Data Quality & Monitoring

Monitoring is integrated directly into the pipeline.

Tracked metrics include:
- Row counts
- Column-level constraint violations
- Data freshness (SLA delay)
- Missing or empty partitions

Metrics are persisted and loaded into the analytics warehouse alongside business data.

---

## Gold Layer

Analytics-ready, business-facing datasets built incrementally from Silver.

### Example Outputs
- NYC Taxi: daily trip volume and revenue metrics
- GitHub: trending repositories
- SEC: filings per company

Gold tables are stable, denormalized, and optimized for analytical queries.

---

## Analytics Warehouse

- DuckDB used as analytical query engine
- Direct querying over Parquet
- Incremental loads
- Schema separation for silver, gold, and monitoring data

DuckDB mirrors the role of cloud warehouses such as Snowflake, BigQuery, or Redshift in production environments.

---

## Data Modeling

- Fact-style Gold tables
- Star-schema-inspired design
- Incremental model builds
- SQL-based analytics views
- Resilient to missing upstream data

---

## End-to-End Flow

1. Ingest raw source data
2. Persist immutable Bronze datasets
3. Normalize and validate into Silver
4. Aggregate into Gold datasets
5. Load analytics and monitoring data into warehouse
6. Query via SQL for reporting and analysis

---

## Production Parallels

| Local Implementation | Production Equivalent |
|---------------------|-----------------------|
| Python ingestion | Airflow / Dagster |
| Local filesystem | S3 / GCS / ADLS |
| Pandas transforms | Spark / Flink |
| DuckDB | Snowflake / BigQuery |
| Custom metrics | Data observability platforms |

The system mirrors production data platforms in design, differing primarily in scale.

---

## Use Case Alignment

This project reflects real-world data engineering scenarios:
- Multi-source ingestion pipelines
- Regulatory and analytical data coexistence
- Incremental processing
- Schema contracts and SLAs
- Analytics-oriented warehouse modeling

---