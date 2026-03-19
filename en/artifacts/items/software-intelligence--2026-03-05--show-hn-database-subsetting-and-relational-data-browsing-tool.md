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
- developer-tooling
relevance_score: 0.33
run_id: materialize-outputs
language_code: en
---

# Show HN: Database Subsetting and Relational Data Browsing Tool

## Summary
Jailer is a subsetting and data browsing tool for relational databases, used to safely generate small, consistent data slices from production databases, and supports interactive browsing based on table relationships. It primarily addresses data movement and integrity maintenance in development, testing, and archiving scenarios.

## Problem
- Production databases are often large and have complex relationships, making direct copying to development or test environments costly and inconvenient.
- When manually extracting partial data, it is easy to break foreign key dependencies and referential integrity, resulting in unusable or inconsistent test data.
- During data archiving or cleanup of obsolete data, if dependencies between tables are not understood, database integrity and performance can be affected.

## Approach
- Provides a **Data Browser** that lets users browse relational data step by step along relationships between tables (foreign keys or user-defined relationships).
- Provides a **Subsetter** that extracts “small slice” data from production databases and imports it into development/test environments while preserving data consistency and referential integrity.
- Generates SQL sorted topologically by dependencies during export, reducing the risk of constraint conflicts when importing or rebuilding data.
- Supports outputting results as SQL, JSON, YAML, XML, and DbUnit datasets, fitting different testing and engineering workflows.
- Supports improving database performance by deleting/archiving obsolete data while minimizing violations of integrity constraints.

## Results
- The text provides no benchmark experiments, public datasets, or quantitative metrics, so there are **no numerical results to report**.
- It explicitly claims to generate **small, consistent, referentially intact** database subsets for development and test environments.
- It explicitly claims support for **5 output formats**: SQL, JSON, YAML, XML, DbUnit datasets.
- It explicitly claims that SQL exports are **topologically sorted**, making them easier to import in dependency order.
- It explicitly claims support for relationship navigation and browsing based on **foreign keys or user-defined relationships**.
- It provides a built-in **demo database**, allowing users to quickly try the tool with almost no configuration.

## Link
- [https://wisser.github.io/Jailer/](https://wisser.github.io/Jailer/)
