# ADR 0010: CLI Billing Report for Runs

## Status
Accepted

## Context
Recoleta spend is dominated by LLM and embedding calls, but users need an immediate, end-of-command view of cost and usage for `recoleta run --once` and `recoleta trends`.

## Decision
Record low-cardinality usage/cost aggregates in the SQLite `metrics` table for triage/analyze/trends, and print a Rich `Billing report` table by default at the end of `run --once` and `trends`. Prefer LiteLLM-provided `response_cost` when available; otherwise estimate USD from tokens via LiteLLM pricing helpers, and emit `*_cost_missing_total` when cost cannot be computed.

## Consequences
Users get a human-readable billing summary by default, while automation can query the same run-scoped metrics. Cost may be partial when pricing/token data is unavailable, but missing cost is observable via explicit counters.

