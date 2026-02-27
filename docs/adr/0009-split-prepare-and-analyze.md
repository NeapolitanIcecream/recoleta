# ADR 0009: Split Prepare and Analyze Boundaries

## Status
Accepted

## Context
Stage 3 (enrich) and Stage 3.5 (triage) were executed inside `recoleta analyze`, which mixed storage-heavy work and LLM-heavy work in one stage. This blurred cost control, candidate-volume control, and cache boundaries.

## Decision
`recoleta ingest` is the prepare command (ingest + enrich + optional triage), and `recoleta analyze` is Stage 4 only (LLM on prepared items). Introduce `ITEM_STATE_TRIAGED` as the durable handoff when triage is enabled, and add `ANALYZE_LIMIT` as the default Stage 4 batch/selection limit.

## Consequences
Control flow becomes simpler: prepare stores durable artifacts, analyze computes lazily. Triage output is persisted and observable. Stage 4 no longer performs network enrichment; missing content now fails fast with retryable state and machine-readable diagnostics.

