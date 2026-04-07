# Self-similar Trend Generation (Multi-level Corpus + Overview Pre-injection)

> Status note (2026-04-07): This design note remains useful for the original
> self-similar direction, but parts of the implementation boundary have been
> superseded. For current corpus materialization, `reuse_existing_corpus`
> semantics, and docs-only overview behavior, use
> [2026-04-07-self-similar-corpus-materialization-refactor-plan.md](./2026-04-07-self-similar-corpus-materialization-refactor-plan.md)
> as the source of truth.

Date: 2026-03-05  
Status: Approved (design)

## Context
The current trend pipeline produces strong **daily** trends because it can retrieve directly from `item` documents (paper-level analyses and optional content chunks). However, **weekly** trends degrade because their corpus is restricted to **daily trend documents** (`doc_type=trend, granularity=day`), which collapses evidence and makes citations/ranking unreliable (e.g., “Representative papers” often become daily trend titles instead of paper links).

We want the generation process to be **self-similar across granularities**: for a target level \(N\), the model should (1) see all \(N-1\) overviews at the start, and (2) have RAG capability over **all \(\le N-1\) corpora**, not a hard-coded week→day dependency.

## Goals
- **Self-similarity**: a single, generic trend generation design that applies to day/week/month (and future levels).
- **Grounded clusters**: every cluster must cite paper-level sources (URLs + authors) instead of higher-level trend titles.
- **Cross-period synthesis**: reduce duplication across lower-level summaries; surface common signals, disagreements, and evolution.
- **Stable ranking**: produce a **Top-N must-read** list grounded in paper-level items.
- **Token/cost safety**: bounded pre-injected overviews; bounded retrieval candidate sets.

## Non-goals
- Designing a UI for trends.
- Perfect forward-compatibility for arbitrary granularities beyond `day|week|month` (v0 scope).
- Rewriting the entire LLM trend agent; we reuse the existing tool-calling agent and storage model.

## Definitions
We model “granularity” as a level chain:

- **L0**: `item` (paper/item analysis; may include extracted content chunks)
- **L1**: `trend(day)`
- **L2**: `trend(week)`
- **L3**: `trend(month)`

For a target level \(L_N\):
- **prev level**: \(L_{N-1}\) (if \(N>0\))
- **overview pack**: a deterministic, bounded markdown block injected into the prompt before tool calls
- **RAG sources**: a set of corpora \(\{L_0..L_{N-1}\}\) available via the agent tools

## Current behavior (baseline)
- Daily trend: corpus = `item`; items are indexed into `documents/document_chunks`.
- Weekly trend: corpus = `trend(day)`; does **not** index items for the week window; representative citations may end up referencing `trend` docs.
- Monthly trend: corpus = `trend(week)`.

## Proposed design

### 1) Introduce a generic `TrendGenerationPlan`
Derive a plan from `(target_granularity, period_start, period_end)`:

- **`target`**: one of `day|week|month`
- **`prev`**: previous level (for prompt pre-injection)
- **`rag_sources`**: a list of corpora with purpose:
  - `item` sources are used for **evidence/citations/ranking**
  - `trend` sources are used for **structure + synthesis** (terminology alignment, dedup, evolution)
- **`overview_pack_strategy`**: how to build the pre-injected overview pack
- **`representative_policy`**: enforce representatives to be `doc_type=item`
- **`ranking_n`**: Top-N must-read list size
- **bounds**: character/token budgets and candidate limits

This plan is computed once and used by all granularities; the only unavoidable specialization is **period bounds** (day/week/month) and the **level mapping**.

### 2) Always ensure `item` documents exist for the target window
For any target granularity (day/week/month), run `index_items_as_documents(...)` for the **same (period_start, period_end)** window.

Rationale:
- Guarantees paper-level evidence is always retrievable.
- Avoids “weekly depends on daily being good”.
- Keeps representative citations paper-grounded.

### 3) Build `overview_pack_md` from the previous level (bounded)
Inject `overview_pack_md` into the LLM prompt at the start, to guide initial reasoning without requiring exploratory tool calls.

Rules:
- If **prev is `trend(X)`**: collect **all** trend overviews for `X` within the window, ordered by event time, and join them with clear day/week labels. Missing entries are included as a short placeholder (“missing/empty”).
- If **prev is `item`** (day target): select **Top-K items** in the day window by `(relevance_score desc, novelty_score desc, event_time desc)` and include per-item: title, canonical URL, 1–2 sentence summary. This is the L0 “overview” approximation.

Budgets:
- `overview_pack_max_chars` (hard cap, truncation recorded as a metric)
- `item_overview_top_k` and `item_overview_item_max_chars`

### 4) Multi-level RAG: allow retrieval over all `<= prev` corpora
The agent tools already accept `doc_type` and optionally `granularity`. The prompt should explicitly instruct:
- Use `trend(day|week)` docs to align themes and avoid re-stating the same point.
- Use `item` docs as the authoritative source for:
  - `clusters[].representative_chunks`
  - any “must-read” ranking list
  - claims that require evidence

### 5) Enforce paper-level representatives (post-processing)
After the agent returns a `TrendPayload`, apply a deterministic enforcement step:

- Drop any representative chunk whose `doc_id` resolves to a document with `doc_type != "item"`.
- Backfill representatives per cluster by semantic search over **`doc_type=item`** within the window, using `(cluster.name + cluster.description)` as the query.
- If a cluster cannot satisfy `rep_min_per_cluster`, either merge it into a nearby cluster or demote it into highlights (fail-fast over hallucination).

This turns “paper-level citations” into an invariant, not a prompt wish.

### 6) Require a Top-N must-read ranking block
Always produce a dedicated “Top-N must-read” section, implemented as either:
- a fixed cluster (recommended), or
- a dedicated subsection in `highlights` with strict formatting.

Each ranked entry must include:
- why it matters (1 sentence)
- a paper citation (URL + title; authors optional but preferred)

## Observability (must-have signals)
Reuse the existing `pipeline.trends.*` namespace and avoid high-cardinality values.

Minimal new metrics:
- `pipeline.trends.overview_pack.truncated_total` (count)
- `pipeline.trends.rep_enforcement.dropped_non_item_total` (count)
- `pipeline.trends.rep_enforcement.backfilled_total` (count)
- `pipeline.trends.rep_enforcement.failed_clusters_total` (count)

Logging:
- `logger.bind(module="pipeline.trends.plan", run_id=...)` for plan computation + summary stats.

## Testing plan
Add a regression test for weekly trend quality:
- Asserts representative papers include URLs (paper-level), not just trend titles.
- Asserts a “Top-N must-read” block exists.
- Asserts no raw `doc_id:` references leak into published Markdown.

Add a failure-path test for observability:
- Force non-item representatives and assert `rep_enforcement.dropped_non_item_total` is recorded.

## Rollout
Ship behind config defaults that preserve current behavior unless enabled:
- `TRENDS_SELF_SIMILAR_ENABLED=true|false` (default false for safe rollout)
- `TRENDS_RANKING_N=10`
- `TRENDS_OVERVIEW_PACK_MAX_CHARS=...`

Once the regression test passes and real outputs are validated, flip the default to enabled.
