# Architecture

This document describes the proposed architecture for Recoleta v0: modules, data flow, scheduling, and operational concerns.

## Runtime shape

Recoleta is a CLI-first application with a small set of commands:

- `recoleta ingest`: run **prepare** work (ingest + enrich + optional triage) and persist a Stage 4-ready backlog.
- `recoleta analyze`: run **Stage 4 only** (LLM analysis on prepared items); no network enrichment or triage in this command.
- `recoleta publish`: publish to configured targets (local Markdown by default; optional Obsidian and Telegram).
- `recoleta run`: schedule ingest/analyze/publish periodically (optional; can also be done by cron/launchd).

## Module boundaries

Current module layout:

- `recoleta/config.py`: typed config, env loading, validation
- `recoleta/sources.py`: source connectors (arXiv, HN RSS, HF papers, OpenReview, newsletter RSS)
- `recoleta/pipeline.py`: pipeline stages + orchestration
- `recoleta/extract.py`: fulltext extraction (HTML/PDF), Markdown conversion
- `recoleta/analyzer.py`: LLM invocation via LiteLLM
- `recoleta/triage.py`: semantic scoring and pre-ranking before LLM (optional)
- `recoleta/storage.py`: SQLite repository + filesystem writers
- `recoleta/publish.py`: Markdown/Obsidian note writers and Telegram message builder
- `recoleta/delivery.py`: Telegram sender
- `recoleta/observability.py`: logging setup, debug artifacts, metrics helpers

## Pipeline stages

Stage flow:

```mermaid
flowchart TD
  Ingest[Stage1_Ingest] --> Normalize[Stage2_Normalize]
  Normalize --> Enrich[Stage3_Enrich]
  Enrich --> Triage[Stage3_5_Triage_optional]
  Triage --> Analyze[Stage4_Analyze_LLM]
  Analyze --> RankFilter[Stage5_Rank_Filter]
  RankFilter --> Publish[Stage6_Publish]
```

### Stage 1: Ingest

Responsibilities:
- Poll configured sources.
- Convert each source record into a normalized `ItemDraft`.
- Compute stable identity keys:
  - `source` + `source_item_id` (if available)
  - `canonical_url_hash` (fallback)
- Upsert into SQLite `items`.

Failure modes:
- Network errors → retry with exponential backoff.
- Parse errors → mark item as `failed_ingest` and persist error metadata.

### Stage 2: Normalize

Responsibilities:
- Normalize fields (title, authors, published_at, url).
- Create derived metadata (domains, arXiv categories, HN score/comment count if available).
- Detect obvious duplicates:
  - exact URL match
  - near-duplicate title via `rapidfuzz` (threshold configurable)

### Stage 3: Enrich (Fulltext/PDF)

Responsibilities:
- For HTML: download and extract main text (e.g., `trafilatura`).
- For PDF: download and extract text/markdown (e.g., `marker-pdf` for arXiv/OpenReview PDFs).
- Persist extracted content to:
  - SQLite `contents` (small text blobs) and/or
  - filesystem artifact store (for larger payloads), with a pointer stored in SQLite.

Operational guidance:
- Cache downloads by URL hash to avoid repeated fetching.
- Never store access tokens inside artifacts.

### Stage 3.5: Triage (Semantic Pre-Ranking) (optional)

Responsibilities:
- Build a candidate pool larger than the Stage 4 limit.
- Score candidates against user-defined `TOPICS` using semantic similarity:
  - embeddings + cosine similarity (recommended)
  - lexical fallback (e.g., `rapidfuzz`) when embeddings are unavailable
- Select items for Stage 4:
  - prioritize mode: rank by similarity and take top-K
  - filter mode (optional): apply a minimum similarity threshold to reduce LLM calls
- Persist Stage 3.5 output by marking selected items as `triaged`, creating a durable handoff into Stage 4.
- Preserve exploration: reserve a small slice of Stage 4 capacity for randomly sampled candidates.
- Fail open: if triage fails, fall back to recency ordering.

Operational guidance:
- Batch embedding calls (`input=[...]`) to control latency and rate limits.
- Keep the candidate factor bounded to avoid excessive enrichment/embedding work.
- See `docs/design/semantic-pre-ranking.md` for scoring and cost-control details.

### Stage 4: Analyze (LLM)

Responsibilities:
- For each prepared item, load **already stored** content (prefer `pdf_text`, then `html_maintext`).
- Call LiteLLM to produce structured output:
  - summary
  - insight
  - idea_directions (list)
  - topics/tags
  - relevance score against user topics
  - novelty score (optional)
- Persist the analysis record and a prompt+response debug artifact (when configured).

Operational guidance:
- Stage 4 is compute-only. Do not fetch URLs or run extraction in this stage.
- If content is missing, fail fast, mark retryable, and emit machine-readable diagnostics.

LLM interface:
- Use LiteLLM's OpenAI-compatible API.
- Prefer **structured output** (JSON schema / response_format) and validate with Pydantic.

### Stage 5: Rank & Filter

Responsibilities:
- Rank items by a combined score:
  - LLM relevance score
  - source-specific signals (HN points/comments; arXiv recency; OpenReview status)
  - novelty/dedup penalty
- Apply user rules:
  - allow/deny tags
  - minimum score threshold
  - max items per run/day
- Decide final `Deliverable` objects.

### Stage 6: Publish

Responsibilities:
- Write local Markdown notes and a per-run index (`latest.md`) by default.
- Optionally write Obsidian notes in Markdown with YAML frontmatter.
- Optionally send Telegram messages (short mobile-friendly format) with safe rate limiting.
- Record delivery results and message IDs for idempotency.

## Durable pre-ranking boundary

When triage is enabled, Stage 4 consumes `triaged` items (plus `retryable_failed` retries).  
When triage is disabled, Stage 4 consumes `enriched` items (plus `retryable_failed`).  
This keeps Stage 3/3.5 cache-friendly and makes Stage 4 a clean, lazy compute boundary.

## Scheduling and execution model

Two supported modes:

- **External scheduler**: run `recoleta ingest && recoleta analyze && recoleta publish` via cron/launchd.  
  (`ingest` now means prepare: Stage 1 + Stage 3 + Stage 3.5)
- **Internal scheduler**: `recoleta run` uses APScheduler to run jobs on intervals with the same stage mapping.

For v0, concurrency should be conservative:
- parallelize network fetches with bounded concurrency
- serialize SQLite writes per transaction
- keep LLM calls bounded to avoid cost spikes
- prefer pre-ranking (Stage 3.5) to keep LLM calls high-signal when backlog exists

## Storage model

Recoleta persists state in two places:

- **SQLite index**: truth source for state machines, dedupe, retries, metrics.
- **Filesystem outputs**:
  - Local Markdown output directory (default, user-facing artifacts)
  - Obsidian Vault notes (user-facing artifacts)
  - optional raw artifacts directory (HTML/PDF/text snapshots, debug JSON)

SQLite enables:
- incremental runs (process only new/changed items)
- delivery idempotency
- auditing and re-processing

## Observability and debugability

Every pipeline stage must emit at least one machine-readable signal:

- **Structured logs** (Loguru): `logger.bind(module="pipeline.ingest", run_id=..., item_id=...)`
  - do not bind unbounded values (full URLs, long filenames) repeatedly
  - never log secrets (tokens, chat IDs, API keys)
- **Metrics in SQLite**:
  - stage duration per run
  - LLM call counts and errors by provider/model
  - delivered item counts
- **Debug artifacts** (optional):
  - `{run_id}/{item_id}/llm-request.json`
  - `{run_id}/{item_id}/llm-response.json`
  - optional triage artifacts (when enabled): `embedding-request.json`, `embedding-response.json`, `triage-summary.json`
  - scrub secrets before writing

## Error handling and retries

- Use `tenacity` for IO retries (HTTP fetches, Telegram transient errors).
- Classify errors:
  - transient: retry, then mark `retryable_failed`
  - permanent: mark `failed` and stop further stages for that item
- Persist failure context (error type, message, stage) in SQLite for later inspection.

