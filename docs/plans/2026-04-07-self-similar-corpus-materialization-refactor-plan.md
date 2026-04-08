# Self-Similar Corpus Materialization Refactor

## Context

[ADR 0024](../adr/0024-self-similar-multi-level-trend-corpus.md) established the target direction: multi-level trend generation should stay self-similar across `day`, `week`, and `month`.

The current implementation had drifted from that contract in two ways:

1. `item` sources only became retrieval-ready after an explicit indexing pass that wrote `documents + chunks + FTS`.
2. `trend` sources were materialized inline during persistence, so `reuse_existing_corpus=True` accidentally meant two different things:
   - skip duplicate `prepare/analyze`
   - assume every required source was already materialized

That mismatch let fresh day/week/month runs produce empty or degraded trend corpora even when upstream analyses already existed.

## Problem Statement

The old `reuse_existing_corpus` path checked only one primary corpus:

- `day` -> `documents(doc_type=item)`
- `week` -> `documents(doc_type=trend, granularity=day)`
- `month` -> `documents(doc_type=trend, granularity=week)`

That was not sufficient because actual generation depends on the full planned source set:

- primary corpus
- `TrendGenerationPlan.rag_sources`
- item-backed representative repair and enforcement

The consequence was asymmetrical behavior:

- `day` could skip item materialization and emit an empty trend from a fresh database
- `week/month` could silently run with incomplete `item` or lower-level trend sources
- overview generation still read `analyses` directly, so the system boundary was not actually self-similar

## Target Contract

The corrected boundary is:

- upstream stages produce canonical source rows
- downstream trend generation consumes retrieval-ready corpus
- retrieval-ready corpus means `documents + chunks + FTS`
- vector sync remains separate and lazy; it is not part of the correctness boundary

This yields one shared contract for all source kinds:

- `item` source -> analyzed items materialized into `item` documents plus `summary/content/meta` chunks
- `trend` source -> trend payloads materialized into `trend` documents plus `summary/meta` chunks

In other words, self-similarity is restored at the corpus boundary, not at the raw storage-table boundary.

## Key Decisions

### 1. `item` meta stays stored but not searchable

`item` materialization now writes a `meta` chunk containing the minimum structured ranking fields:

- `item_id`
- canonical URL
- title
- authors
- published time
- relevance score
- novelty score

This chunk is intentionally:

- readable through repository batch helpers
- excluded from agent-visible text search
- excluded from summary-only vector sync
- excluded from chunk FTS writes

### 2. Day overview becomes docs-only

`item_top_k` overview assembly no longer reads `analyses` directly.

It now reads:

- `item` summary chunks for narrative fields
- `item` meta chunks for ranking and dedupe

This keeps overview generation on the same retrieval-ready contract used by trend synthesis.

### 3. `reuse_existing_corpus` now means skip compute, not skip source readiness

The refactor keeps the public flag but narrows its semantics:

- skip duplicate `prepare/analyze`
- still ensure every required source is materialized before generation

Required sources are derived from:

- the primary corpus for the target granularity
- `TrendGenerationPlan.rag_sources`
- item-backed representative enforcement

### 4. Source ensure is tokenized and plan-driven

The runner now operates on a small fixed token set:

- `item`
- `trend_day`
- `trend_week`

Each token is checked once per stage run and is responsible for the full in-window source set for that token.

### 5. Required trend sources self-heal, but only from canonical data

For required in-window trend sources, ready means:

- trend document exists
- summary chunk exists
- valid meta chunk exists

Repair strategy:

- first try canonical `trend_synthesis` pass output for the same `(granularity, period_start, period_end)`
- if found, re-materialize the trend document from that payload
- if the document is missing and no pass output exists, generate the lower-level trend normally
- if the document already exists but structured repair is impossible, fail instead of silently accepting summary fallback

Read-only compatibility paths still keep the old summary fallback for historical browsing and materialization commands.

## Repository Changes

The storage layer now exposes kind-aware period helpers:

- `list_document_chunks_in_period(...)`
- `list_document_chunk_index_rows_in_period(...)`

The previous summary-only helpers remain as thin wrappers over the generic implementations.

This keeps existing consumers working while making docs-only overview assembly and future structured-source readers straightforward.

## Observability Changes

`pipeline.trends.source_materialization.*` is the canonical readiness metric family:

- `checked_total`
- `already_ready_total`
- `materialized_total`
- `failed_total`

Metrics are emitted per low-cardinality source token.

Existing metric families keep their narrower roles:

- `pipeline.trends.index.*` -> item materializer work
- `pipeline.trends.backfill.*` -> explicit lower-level regeneration only

This avoids double-encoding source readiness in both `backfill.*` and `index.*`.

## Expected Behavioral Changes

- Fresh `day` runs with `reuse_existing_corpus=True` no longer emit empty trends just because `item` docs were absent.
- `week/month` runs ensure lower-level trend sources even without explicit `backfill=True`.
- Structured lower-level trend corruption is now surfaced as a failure when canonical repair is impossible.
- Day overview generation works from materialized corpus only.

## Verification

The refactor is covered by regression tests for:

- fresh `reuse_existing_corpus` day runs
- week source ensure from missing daily trends
- month source ensure from missing weekly and daily trends
- trend meta repair from canonical pass outputs
- failure on unrecoverable structured trend-source corruption
- docs-only day overview
- item meta stored-but-not-searchable semantics

## Follow-up

This refactor intentionally does not add a historical repair job.

If we later decide to normalize old trend documents proactively, that work should be a separate migration or repair command built on top of the same source materialization contract, not another set of stage-level special cases.

There is also one remaining translation/runtime follow-up from the same live-fleet validation cycle:

- `recoleta translate run --json` still reports `"status": "ok"` whenever `aborted=false`, even if `failed_total > 0`.
- Managed workflows now treat non-zero translation failures according to `on_translate_failure`, so fleet/runtime semantics are corrected there.
- The standalone translate CLI should be aligned to the same contract in a follow-up change:
  - either emit a non-`ok` status whenever `failed_total > 0`
  - or add an explicit machine-readable terminal state that distinguishes `clean`, `partial_failure`, and `aborted`
- That follow-up should preserve the new failure typing and observability added during this refactor:
  - `pipeline.translate.failed_total`
  - `pipeline.translate.failed_total.<reason>`
  - structured `failure_reason` / `finish_reason` logging
