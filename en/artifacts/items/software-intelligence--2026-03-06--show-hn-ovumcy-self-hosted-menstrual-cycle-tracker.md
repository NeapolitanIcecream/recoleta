---
source: hn
url: https://github.com/terraincognita07/ovumcy
published_at: '2026-03-06T23:17:07'
authors:
- terrain07
topics:
- self-hosted-app
- privacy-first
- health-tracking
- go-web-app
- sqlite-postgres
relevance_score: 0.13
run_id: materialize-outputs
language_code: en
---

# Show HN: Ovumcy – self-hosted menstrual cycle tracker

## Summary
Ovumcy is a privacy-first, self-hosted menstrual cycle tracking app centered on privacy and self-hosting, aiming to provide fast daily logging and cycle insights without relying on cloud accounts, telemetry, or third-party infrastructure. It reads more like an engineered software product description than a research paper proposing a new algorithm or model.

## Problem
- Existing menstrual tracking apps often depend on cloud accounts, analytics instrumentation, or third-party services, exposing sensitive health data to external infrastructure.
- Users need an alternative that allows convenient recording of periods, symptoms, and cycle information while retaining full control over data storage, export, and deployment.
- This matters because menstrual and fertility-related data is highly sensitive, and privacy, portability, and tracker-free operation directly affect user trust and safety.

## Approach
- The core approach is simple: build menstrual tracking as a **self-hosted web app delivered as a single Go service**, so users deploy it on servers they control instead of handing data to a vendor cloud.
- The frontend uses **server-rendered HTML + HTMX + a small amount of vanilla JavaScript**, supporting browser access and home-screen installation on phones while reducing client complexity and external dependencies.
- The storage layer uses **SQLite** by default and offers **PostgreSQL** as a more advanced self-hosted option; it also supports **CSV/JSON export** to keep data portable.
- Product features include **daily logging** (period days, flow intensity, symptoms, notes), **custom symptom management**, and history-based **prediction of the next period, ovulation, fertile window, and cycle phase**.
- On privacy, it emphasizes **no telemetry, no ad tracking, and no core third-party API dependencies**, using only necessary first-party cookies and supplementing this with security checks such as CodeQL, gosec, Trivy, and CycloneDX SBOM workflows.

## Results
- The text **does not provide standard research-style quantitative results**: there are no published accuracy, F1, AUC, user study sample sizes, or numerical comparisons with other cycle trackers.
- The most concrete outcomes presented are product and engineering status: the latest tagged release is **v0.4.1**, and it supports **3 interface languages** (English, Russian, Spanish).
- In deployment terms, the system runs as **1 Go service**, uses **SQLite** as the default database, and also supports **PostgreSQL**; it can be deployed via **Docker Compose** or as a single binary.
- Functional claims include support for **daily tracking**, **cycle prediction**, **calendar and statistics views**, **CSV/JSON export**, **home-screen installation on phones**, and **creation/renaming/hiding/restoring of custom symptoms** while preserving historical records.
- Its strongest privacy and security claims are: **no analytics, no ad trackers, no third-party API dependencies**, plus **CodeQL, gosec, Trivy scans, and CycloneDX SBOM generation** run in CI.
- Accordingly, its main “breakthrough” is not algorithmic performance, but turning a **privacy-first, self-hosted, low-dependency, portable** product philosophy into a deployable real-world system.

## Link
- [https://github.com/terraincognita07/ovumcy](https://github.com/terraincognita07/ovumcy)
