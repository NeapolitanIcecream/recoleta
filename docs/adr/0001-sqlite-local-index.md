# ADR 0001: SQLite as Local Index

## Status
Accepted

## Context
Recoleta needs durable state for idempotency, deduplication, retries, and trend statistics while remaining single-user and easy to operate.

## Decision
Use a local SQLite database as the primary index/state store and treat filesystem outputs (Obsidian + artifacts) as derived artifacts.

## Consequences
- Enables incremental runs, auditing, and safe re-processing.
- Keeps deployment simple (single file DB).
- Requires schema evolution strategy (start with simple create-all; add migrations when needed).

