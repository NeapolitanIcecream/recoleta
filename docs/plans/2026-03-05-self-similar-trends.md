# Self-similar Trends Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make trend generation self-similar across day/week/month by pre-injecting previous-level overviews and enabling multi-level RAG, while enforcing paper-level citations and a stable Top-N must-read ranking.

**Architecture:** Compute a generic `TrendGenerationPlan` from `(granularity, period)` and apply it uniformly. Always index `item` docs for the target window, build an `overview_pack_md` from the previous level, and enforce `doc_type=item` representatives post-generation.

**Tech Stack:** Python, Pydantic, PydanticAI tool-calling agent, SQLite (`documents/document_chunks`), FTS5, LanceDB semantic search, Loguru metrics/logs, Pytest.

---

### Task 1: Add settings for self-similar trends (config + validation)

**Files:**
- Modify: `recoleta/config.py`
- Test: `tests/test_recoleta_specs_settings.py`

**Step 1: Write the failing test**

Add a new test case that validates parsing/validation for the new settings:

- `TRENDS_SELF_SIMILAR_ENABLED` (bool)
- `TRENDS_RANKING_N` (int, >= 1)
- `TRENDS_OVERVIEW_PACK_MAX_CHARS` (int, >= 1)
- `TRENDS_ITEM_OVERVIEW_TOP_K` (int, >= 0)
- `TRENDS_ITEM_OVERVIEW_ITEM_MAX_CHARS` (int, >= 1)
- `TRENDS_REP_MIN_PER_CLUSTER` (int, >= 1)

**Step 2: Run test to verify it fails**

Run:
- `uv run pytest tests/test_recoleta_specs_settings.py -q`

Expected:
- FAIL due to missing settings fields / unknown env mapping.

**Step 3: Write minimal implementation**

In `recoleta/config.py`:
- Add the env-to-field mapping keys to `_ConfigFileSettingsSource._KEY_MAP`.
- Add corresponding `Settings` fields with defaults (safe rollout: disabled by default).
- Add validators if needed (e.g., non-negative / sane bounds).

**Step 4: Run tests to verify it passes**

Run:
- `uv run pytest tests/test_recoleta_specs_settings.py -q`

Expected:
- PASS.

---

### Task 2: Define `TrendGenerationPlan` and level-chain helpers

**Files:**
- Modify: `recoleta/trends.py`
- Test: `tests/test_trends_plan_self_similarity.py` (new)

**Step 1: Write the failing test**

Create `tests/test_trends_plan_self_similarity.py` to assert:
- `prev_level("week") == "day"`, `prev_level("month") == "week"`, `prev_level("day") == "item"`
- plan for `week` includes:
  - `rag_sources` includes `item` and `trend(day)`
  - `rep_source_doc_type == "item"`
- plan for `day` uses item-top-K overview strategy

**Step 2: Run test to verify it fails**

Run:
- `uv run pytest tests/test_trends_plan_self_similarity.py -q`

Expected:
- FAIL (functions/classes missing).

**Step 3: Write minimal implementation**

In `recoleta/trends.py`, add:
- `TrendLevel` helpers (`prev_level_for_granularity`, `rag_sources_for_granularity`)
- `TrendGenerationPlan` (Pydantic model or dataclass) containing:
  - `target_granularity`, `period_start`, `period_end`
  - `overview_pack_strategy`
  - `rag_sources` (e.g., list of `{doc_type, granularity, purpose}` dicts)
  - `rep_source_doc_type="item"`
  - numeric budgets (ranking_n, top_k, max_chars, rep_min_per_cluster, …)

**Step 4: Run tests to verify it passes**

Run:
- `uv run pytest tests/test_trends_plan_self_similarity.py -q`

Expected:
- PASS.

---

### Task 3: Build `overview_pack_md` (prev-level overviews, bounded)

**Files:**
- Modify: `recoleta/trends.py`
- Modify: `recoleta/storage.py` (only if a small helper is needed)
- Test: `tests/test_trends_overview_pack.py` (new)

**Step 1: Write the failing test**

Create tests for:
- `week` overview pack collects 7 daily overviews (or placeholders) in order.
- `day` overview pack uses top-K items with title/url/summary and enforces per-item max chars.
- truncation behavior sets a boolean/metric-ready flag.

**Step 2: Run test to verify it fails**

Run:
- `uv run pytest tests/test_trends_overview_pack.py -q`

Expected:
- FAIL (builder missing).

**Step 3: Write minimal implementation**

Implement:
- `build_overview_pack_md(repository, plan) -> (md: str, stats: dict)`
  - For trend(prev): query `documents` for `doc_type=trend, granularity=prev` in window; read `chunk_index=0` (trend_overview).
  - For item(prev): use `Repository.list_analyzed_items_in_period(...)`, sort by relevance/novelty, take top-K, and format.
  - Enforce `overview_pack_max_chars` (truncate tail) and return `stats`.

**Step 4: Run tests to verify it passes**

Run:
- `uv run pytest tests/test_trends_overview_pack.py -q`

Expected:
- PASS.

---

### Task 4: Update trend agent prompt to include `overview_pack_md` and multi-level guidance

**Files:**
- Modify: `recoleta/rag/agent.py`
- Test: `tests/test_trends_prompt_includes_overview_pack.py` (new)

**Step 1: Write the failing test**

Add a unit test that:
- calls the prompt builder (extract into a helper if needed)
- asserts the prompt includes:
  - `overview_pack_md` (non-empty)
  - `ranking_n`
  - explicit instruction: representatives must be `doc_type=item`

**Step 2: Run test to verify it fails**

Run:
- `uv run pytest tests/test_trends_prompt_includes_overview_pack.py -q`

Expected:
- FAIL (no prompt field yet).

**Step 3: Write minimal implementation**

In `recoleta/rag/agent.py`:
- extend the JSON prompt to include:
  - `overview_pack_md`
  - `rag_sources`
  - `ranking_n`
  - `rep_source_doc_type="item"`
- update `_build_trend_instructions(...)` to explicitly recommend:
  - use `trend` docs for synthesis
  - use `item` docs for citations and Top-N
  - always include a “Top-N must-read” block (cluster or section)

**Step 4: Run tests to verify it passes**

Run:
- `uv run pytest tests/test_trends_prompt_includes_overview_pack.py -q`

Expected:
- PASS.

---

### Task 5: Enforce paper-level representatives and backfill from `item` only

**Files:**
- Modify: `recoleta/rag/agent.py` (representative backfill doc_type)
- Modify: `recoleta/pipeline.py` (post-processing enforcement + metrics)
- Test: `tests/test_trends_representatives_are_item_docs.py` (new)

**Step 1: Write the failing test**

Create a test where the fake trend payload returns representatives pointing to trend docs, and assert:
- non-item representatives are dropped
- replacement representatives are item docs with URLs after enrichment
- metrics are written:
  - `pipeline.trends.rep_enforcement.dropped_non_item_total`
  - `pipeline.trends.rep_enforcement.backfilled_total`

**Step 2: Run test to verify it fails**

Run:
- `uv run pytest tests/test_trends_representatives_are_item_docs.py -q`

Expected:
- FAIL (no enforcement/metrics).

**Step 3: Write minimal implementation**

Implementation points:
- In `recoleta/rag/agent.py`, change representative backfill search to use `doc_type="item"` (not `corpus_doc_type`).
- In `recoleta/pipeline.py`, after receiving `payload` and before writing notes:
  - resolve each representative `doc_id` and drop if not `item`
  - semantic-search backfill from `item` docs in the period window
  - record low-cardinality metrics in `pipeline.trends.*`

**Step 4: Run tests to verify it passes**

Run:
- `uv run pytest tests/test_trends_representatives_are_item_docs.py -q`

Expected:
- PASS.

---

### Task 6: Make backfill self-similar (prev-level, generic)

**Files:**
- Modify: `recoleta/pipeline.py`
- Test: `tests/test_trends_backfill_prev_level_generic.py` (new)

**Step 1: Write the failing test**

Add a test that:
- runs `month` trends with `backfill=True`
- asserts week-level trends are generated (or at least attempted) before month generation

**Step 2: Run test to verify it fails**

Run:
- `uv run pytest tests/test_trends_backfill_prev_level_generic.py -q`

Expected:
- FAIL (current logic only handles week→day).

**Step 3: Write minimal implementation**

Refactor the backfill logic in `PipelineService.trends`:
- compute `prev_granularity` via the level-chain helper
- enumerate prev windows within the target window (e.g., 7 days in a week, weeks in a month)
- reuse existing metrics names where possible; add only missing low-cardinality counters

**Step 4: Run tests to verify it passes**

Run:
- `uv run pytest tests/test_trends_backfill_prev_level_generic.py -q`

Expected:
- PASS.

---

### Task 7: Weekly quality regression (citations + Top-N)

**Files:**
- Create: `tests/test_trends_week_quality_regression.py`

**Step 1: Write the failing test**

Create a regression test that generates a weekly trend note and asserts:
- at least M representative paper links exist
- a “Top-N must-read” block exists
- no raw internal references leak into the markdown output

**Step 2: Run test to verify it fails**

Run:
- `uv run pytest tests/test_trends_week_quality_regression.py -q`

Expected:
- FAIL before implementation; PASS after.

---

### Task 8: Repo quality gates (format/lint/typecheck)

**Step 1: Run format**

Run:
- `uv run ruff format .`

**Step 2: Run lint**

Run:
- `uv run ruff check .`

**Step 3: Run typecheck**

Run:
- `uv run pyright`

**Step 4: Run full test suite**

Run:
- `uv run pytest -q`

Expected:
- PASS.

---

## References
- Design: `docs/plans/2026-03-05-self-similar-trends-design.md`
- ADR: `docs/adr/0024-self-similar-multi-level-trend-corpus.md`

