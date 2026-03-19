---
source: hn
url: https://robertsahlin.substack.com/p/your-pipeline-succeeded-your-data
published_at: '2026-03-12T23:06:59'
authors:
- boxer_shorts
topics:
- bigquery-ml
- anomaly-detection
- data-quality
- timeseries-monitoring
- dbt
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Catching silent data loss using BigQuery's native ML and Write API

## Summary
This article proposes a data volume anomaly detection solution that relies only on BigQuery-native capabilities and dbt to detect silent data loss where “the pipeline succeeded but the data quietly shrank.” Its core value is that it can monitor write volume anomalies across hundreds of tables in bulk without introducing external monitoring, excessive configuration, or custom model training.

## Problem
- The problem it solves is that even if a data pipeline runs successfully, it may still write only part of the data or even 0 rows, and this kind of **partial loss** is often harder to detect than a complete outage.
- This matters because dashboards still display, the numbers still look “reasonable,” and the business may continue making decisions based on incorrect data for days.
- The author needed a scalable solution that could automatically detect ingestion-volume deviations across the hundreds of tables behind **200+ BigQuery Pub/Sub subscriptions**, without requiring per-table rules, external monitoring systems, or custom ML training.

## Approach
- The core mechanism is straightforward: directly use BigQuery’s automatically provided `INFORMATION_SCHEMA.WRITE_API_TIMELINE_BY_PROJECT` as the “ingestion volume signal” for each table, materializing each write’s timestamp, table name, row count, error code, and so on into a dbt incremental table.
- Then, for each table, build a **dense time grid** over fixed windows (1/2/3/4/6/8/12/24 hours). Even if a window has no data at all, the system still forces a row to be generated and records `actual_rows = 0`, avoiding the blind spot of “no data means nothing is visible.”
- On these windowed time series, it calls BigQuery-native `AI.DETECT_ANOMALIES`, using **TimesFM 2.5** for anomaly detection; the input is table-grouped `log_volume = LOG10(raw_volume + 100)`, and it uses a **28-day training window** to learn each table’s periodic patterns.
- The system uses a three-layer configuration: default parameters, BigQuery table labels, and seed overrides; it also automatically profiles tables (for example `history_days >= 21`, `cv_score`, `liveness_score`, `max_gap_hours`) to choose appropriate windows and thresholds for different tables.
- To reduce false positives, the author detects only “drops,” not “spikes,” and adds holiday suppression, an absolute-difference filter (ignore anything below **0.1%** of peak volume), a relative-difference filter (ignore anything below **25%**), per-table thresholds (default **0.99**), and a consecutive-window confirmation mechanism.

## Results
- The deployment scale described in the article is: in Nordnet’s environment, it monitors **200+ Pub/Sub BigQuery subscriptions** and **hundreds of BigQuery tables**, with detection completed on an hourly basis using a **single dbt model**.
- In terms of training and detection settings, the system requires a table to have at least **21 days of history** before it is eligible for detection; the model uses a **28-day training window**, runs incrementally every hour, and looks back over the most recent **2 days** on each run to correct for late-arriving data.
- For monitoring latency, the author says the fastest detection delay is about **1–2 hours**: one window must finish first, then the next hourly schedule performs the evaluation; larger windows introduce longer delays.
- For false-positive control, it uses BigQuery `AI.DETECT_ANOMALIES`’ global `anomaly_prob_threshold = 0.95` by default, then layers on a per-table default threshold of **0.99**, a relative deviation of **25%**, an absolute deviation of **0.1% peak volume**, and other rules, with the design goal of “it is better to miss some alerts than to significantly reduce false positives.”
- In terms of cost and engineering complexity, the author explicitly states that this solution **does not require external monitoring services, does not require custom model training/hosting, and does not require additional infrastructure**; it can be implemented using only BigQuery + dbt.
- The article **does not provide quantitative accuracy metrics on a standard dataset** (such as precision/recall/F1 or AUC), nor a systematic comparison with other methods; the strongest result claim is that the solution is already used in production to cover hundreds of tables at low cost and with zero external infrastructure, and can detect volume anomalies caused by upstream interruptions, partial deliveries, and schema change.

## Link
- [https://robertsahlin.substack.com/p/your-pipeline-succeeded-your-data](https://robertsahlin.substack.com/p/your-pipeline-succeeded-your-data)
