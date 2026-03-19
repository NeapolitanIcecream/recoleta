---
source: hn
url: https://robertsahlin.substack.com/p/your-pipeline-succeeded-your-data
published_at: '2026-03-12T23:06:59'
authors:
- boxer_shorts
topics:
- bigquery
- anomaly-detection
- timesfm
- data-observability
- dbt
relevance_score: 0.58
run_id: materialize-outputs
language_code: en
---

# Catching silent data loss using BigQuery's native ML and Write API

## Summary
This article presents a data volume anomaly detection solution that relies only on BigQuery-native capabilities and dbt to identify silent data loss cases where "the pipeline succeeded but the data quietly shrank." It works uniformly across hundreds of tables, without requiring an external monitoring system or custom-trained models.

## Problem
- The problem being solved is that a data pipeline may execute successfully while the actual number of rows written to a table is significantly below normal levels, especially in cases of partial loss (for example, missing 20%), which are often hard to detect.
- This matters because such issues do not immediately break dashboards; the business still sees numbers that "look reasonable," causing incorrect data to be consumed for days.
- The constraints include: no per-table rules, no additional monitoring infrastructure, and no desire to train and maintain custom ML models.

## Approach
- Use BigQuery's `INFORMATION_SCHEMA.WRITE_API_TIMELINE_BY_PROJECT` as the sole core signal source, recording when each table was written to, how many rows were written, and whether errors occurred; then materialize it as a dbt incremental table, refreshed hourly to retain longer history and improve query performance.
- Automatically profile each table and, based on at least **21 days** of history, coefficient of variation, activity level, and maximum write interval, determine whether it is suitable for detection and which observation window to use from **1/2/3/4/6/8/12/24 hours**.
- Build a "dense time grid": even if a window has no data at all, a window spine + `LEFT JOIN` + `COALESCE(...,0)` ensures `actual_rows = 0` is generated, preventing zero-write windows from disappearing during aggregation.
- Use BigQuery ML's `AI.DETECT_ANOMALIES` with **TimesFM 2.5** for time-series anomaly detection: model each table independently (`id_cols=['table_fqn']`), use a **28-day** training window, and apply a `LOG10(raw_volume + 100)` transform to compress scale differences.
- To reduce false positives, detect only "drops" and not "increases," and add holiday suppression, an absolute significance threshold (do not alert below **0.1%** of peak volume), a relative deviation threshold (do not alert below **25%**), a table-level probability threshold (default **0.99**), and a consecutive anomalous window confirmation mechanism; the final output is a severity such as `WARNING/ERROR/CRITICAL` rather than a single boolean.

## Results
- The solution has been applied in Nordnet's environment to monitor **hundreds of BigQuery tables** behind **200+ Pub/Sub BigQuery subscriptions** in a unified way.
- Detection eligibility requires at least **21 days** of history; the model uses **28 days** of history as training context; the incremental job runs once per hour and looks back over the most recent **2 days** each run to correct for late-arriving data.
- The default detection configuration is highly conservative: the example global anomaly probability threshold in BigQuery ML is **0.95**, while the default table-level threshold is raised further to **0.99** to prioritize minimizing false positives.
- For high-frequency small windows (**1–4 hours**), the system requires two consecutive anomalous windows before escalating to a formal alert; for **6+ hour** windows, consecutive confirmation is not required by default, balancing sensitivity and noise.
- The article does not provide precise evaluation metrics on a standard benchmark dataset, recall/precision, or numerical comparisons with other methods; the strongest concrete claim is that the solution can cover large-scale table-level volume anomalies with a fastest detection latency of about **1–2 hours** under the constraints of **no external services, no custom training, and zero-config default usability**.

## Link
- [https://robertsahlin.substack.com/p/your-pipeline-succeeded-your-data](https://robertsahlin.substack.com/p/your-pipeline-succeeded-your-data)
