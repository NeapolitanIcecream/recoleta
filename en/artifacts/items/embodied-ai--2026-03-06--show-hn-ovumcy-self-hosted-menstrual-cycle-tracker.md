---
source: hn
url: https://github.com/terraincognita07/ovumcy
published_at: '2026-03-06T23:17:07'
authors:
- terrain07
topics:
- self-hosted-app
- privacy-first
- menstrual-cycle-tracker
- go-web-service
- health-data
relevance_score: 0.0
run_id: materialize-outputs
language_code: en
---

# Show HN: Ovumcy – self-hosted menstrual cycle tracker

## Summary
Ovumcy is a privacy-first, self-hosted menstrual cycle tracking app aimed at users who want to record sensitive health data without relying on cloud accounts, telemetry, or third-party infrastructure. It is more like a product/engineering project description than a research paper, and it does not provide experimental benchmark results.

## Problem
- Existing period-tracking apps often depend on cloud accounts, analytics telemetry, or third-party services, resulting in insufficient user control over sensitive health data.
- Users need fast daily logging, basic cycle insights, and cross-device access, but do not want to entrust their data to external platforms.
- This matters because menstrual and fertility-related data is highly sensitive, and the README explicitly presents “data under the user’s own control” as a core value proposition.

## Approach
- The core mechanism is straightforward: menstrual cycle tracking is implemented as a **single Go service + server-rendered web UI** that users deploy themselves, rather than by signing up for a cloud SaaS.
- The storage layer uses SQLite by default, with PostgreSQL offered as a more advanced self-hosted option; it supports Docker, single-binary deployment, and running behind a reverse proxy.
- At the feature level, it provides daily logging (period days, flow intensity, symptoms, notes), predictions (next period, ovulation, fertile window, cycle phase), calendar and statistics views, and CSV/JSON export.
- In terms of privacy design, it emphasizes **no analytics, no ad tracking, and no core third-party API dependencies**, uses only necessary first-party cookies, and supports English/Russian/Spanish localization.

## Results
- The text **does not provide any quantitative experimental results, user studies, accuracy evaluations, or numerical comparisons with other trackers**.
- Confirmable concrete engineering results include: the latest tagged version is **v0.4.1**; it supports **3** first-party UI languages (English/Russian/Spanish).
- In deployment and architecture terms, the system runs as **1 Go service**, uses **SQLite** as the default database, and supports **PostgreSQL** as an advanced path.
- In security and engineering workflow terms, it states that **CodeQL, gosec, Trivy, CycloneDX SBOM** and other automated checks are integrated, but it does not provide figures for vulnerability reduction, performance improvement, or reliability.
- Therefore, the project’s strongest claim is not an algorithmic breakthrough, but rather a privacy-first alternative that is **self-hosted, exportable, and telemetry-free** while maintaining basic cycle prediction and logging functionality.

## Link
- [https://github.com/terraincognita07/ovumcy](https://github.com/terraincognita07/ovumcy)
