# ADR 0004: v0 Pipeline Bootstrap Scope

## Status
Accepted

## Context
The repository had design documents and dependencies but no executable pipeline.
We need a runnable baseline that validates configuration, persists state, and enforces idempotent behavior.

## Decision
Implement a CLI-first pipeline skeleton with `ingest`, `analyze`, `publish`, and `run` commands.
Ship full SQLite schema, structured logging, metrics writes, and debug artifact hooks now.
Use RSS-based ingestion as the first concrete connector while keeping analyzer and delivery extensible via interfaces.

## Consequences
The project is immediately runnable end-to-end for core workflow validation.
Additional connectors (arXiv, OpenReview, HF) can be added without changing storage contracts.
Observability and failure semantics are available from day one for operational debugging.
