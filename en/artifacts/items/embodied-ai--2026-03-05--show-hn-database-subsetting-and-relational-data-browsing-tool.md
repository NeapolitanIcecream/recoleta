---
source: hn
url: https://wisser.github.io/Jailer/
published_at: '2026-03-05T23:42:53'
authors:
- mrporter
topics:
- database-subsetting
- relational-data-browsing
- test-data-management
- data-archiving
- sql-tooling
relevance_score: 0.0
run_id: materialize-outputs
language_code: en
---

# Show HN: Database Subsetting and Relational Data Browsing Tool

## Summary
Jailer is a tool for database subsetting and relational data browsing, aimed at development, testing, and data archiving scenarios. It emphasizes preserving referential integrity while reducing data size, and supports multiple export formats.

## Problem
- Production databases are often large and complexly related, making direct copying to development or test environments costly and inefficient.
- Simple sampling or data deletion can easily break foreign key dependencies and referential integrity, making test data unusable.
- If historical/obsolete data cleanup and archiving in databases are handled improperly, they can affect performance or break consistency.

## Approach
- Provides a **Data Browser** that allows users to navigate data along relationships between tables, which can be based on foreign keys or user-defined.
- Provides a **Subsetter** that extracts "small but complete" data slices from production databases and imports them into development/test environments.
- Maintains data **consistent and referentially intact** during extraction, import, and archiving.
- Supports generating multiple output formats: topologically sorted SQL, as well as hierarchically structured JSON, YAML, XML, and DbUnit datasets.
- Includes a demo database, lowering the barrier to first-time use and configuration.

## Results
- The text **does not provide quantitative experimental results**; it gives no benchmark datasets, performance metrics, accuracy figures, or numerical comparisons with other tools.
- The strongest specific claim is that it can create "small slices" from production databases and import them into development/test environments while preserving **referential integrity**.
- It also claims that database performance can be **improved** by deleting and archiving obsolete data, but provides no percentage improvement or latency/throughput figures.
- Supports **5 output types**: SQL, JSON, YAML, XML, and DbUnit; SQL is **topologically sorted**, while the others are **hierarchically structured**.

## Link
- [https://wisser.github.io/Jailer/](https://wisser.github.io/Jailer/)
