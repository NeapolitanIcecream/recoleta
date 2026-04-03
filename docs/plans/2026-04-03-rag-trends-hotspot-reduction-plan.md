# 2026-04-03 RAG/Trends Hotspot Reduction Plan

Date: 2026-04-03

Status: In Progress

## Goal

Reduce at least 20 hotspot signals reported by `scripts/refactor_audit.py`
without relaxing thresholds and without introducing new or worsened hotspots.

This branch targets the `RAG retrieval/runtime + trend synthesis adapters`
change axis only. It intentionally does not spend budget on `scripts/*` or
`recoleta/cli/app.py` cleanup.

## Baseline

Audit command on the current `main` baseline:

- `uv run python scripts/refactor_audit.py`

Observed baseline before this branch:

- hotspots: `183`
- `refactor_now`: `48`
- `refactor_soon`: `42`
- `monitor`: `93`
- baseline diff: `new=0`, `worsened=0`, `resolved=0`

## Execution Shape

Branch:

- `codex/rag-trends-hotspot-reduction-plan`

Tracking PR shape:

- open as a draft with title `[codex] Track RAG/trends hotspot reduction`
- use this branch as the execution PR as well
- rename the PR to `refactor(rag): remove 20+ RAG/trends hotspots` before merge

## Target Portfolio

### Wave 1: Retrieval Core

Primary files:

- `recoleta/rag/corpus_tools.py`
- `recoleta/rag/semantic_search.py`

New internal modules:

- `recoleta/rag/search_models.py`
- `recoleta/rag/search_helpers.py`
- `recoleta/rag/search_runtime.py`

Target hotspots:

- `recoleta/rag/corpus_tools.py::_candidate_text_queries`
- `recoleta/rag/corpus_tools.py::_collect_text_hits_with_backoff`
- `recoleta/rag/corpus_tools.py::_normalize_summary_sections`
- `recoleta/rag/corpus_tools.py::SearchService::search_text`
- `recoleta/rag/corpus_tools.py::SearchService::search_semantic`
- `recoleta/rag/semantic_search.py::ensure_summary_vectors_for_period`
- `recoleta/rag/semantic_search.py::semantic_search_summaries_in_period`
- `recoleta/rag/semantic_search.py::_summary_corpus_cache_key`

Implementation rules:

- Introduce request objects for corpus window, vector warm-up, and semantic
  search so internal callers stop re-expanding 14 to 19 scalar parameters.
- Move duplicated summary-normalization and chunk-reading helpers out of
  `agent.py` and `corpus_tools.py`.
- Keep `SearchService` as the stable retrieval facade.

### Wave 2: Agent Runtime

Primary file:

- `recoleta/rag/agent.py`

New internal modules:

- `recoleta/rag/agent_models.py`
- `recoleta/rag/agent_runtime.py`

Target hotspots:

- `recoleta/rag/agent.py::ensure_trend_cluster_representatives`
- `recoleta/rag/agent.py::_extract_raw_tool_trace`
- `recoleta/rag/agent.py::_compact_tool_trace_value`
- `recoleta/rag/agent.py::build_trend_prompt_payload`
- `recoleta/rag/agent.py::generate_trend_payload`

Implementation rules:

- Introduce request objects for prompt payload, generation runtime, and
  representative backfill.
- Keep `build_trend_agent()` in `agent.py`, but move prompt assembly,
  representative cleanup/backfill, tool-trace compaction, and run/debug
  aggregation behind `agent_runtime.py`.

### Wave 3: Trends Reserve

Enable only if Waves 1 and 2 still leave the branch below `resolved >= 20`.

Primary files:

- `recoleta/trends.py`
- `recoleta/trend_packs.py`

Target reserve hotspots:

- `recoleta/trends.py::_trend_payload_summary_lines`
- `recoleta/trends.py::normalize_trend_evolution`
- `recoleta/trends.py::build_overview_pack_md`
- `recoleta/trends.py::semantic_search_summaries_in_period`
- `recoleta/trends.py::generate_trend_via_tools`

Implementation rules:

- Move pack/evolution formatting helpers into `trend_packs.py`.
- Keep public module-level exports, but move the heavy logic and large parameter
  surfaces behind request objects introduced in Waves 1 and 2.

## Validation

Focused suites:

- `uv run pytest tests/test_rag_corpus_tools.py tests/test_trends_prompt_includes_overview_pack.py -q`
- `uv run pytest tests/test_recoleta_specs_trends.py tests/test_trends_observability.py tests/test_trends_tool_metrics.py tests/test_trends_reuse_existing_corpus.py tests/test_trends_pipeline_injects_rag_sources.py -q`

Wave gating:

- rerun `uv run python scripts/refactor_audit.py` after Wave 1
- rerun `uv run python scripts/refactor_audit.py` after Wave 2
- only execute Wave 3 if `resolved < 20`

Closing validation:

- `uv run ruff check .`
- `uv run pyright`
- `uv run pytest`
- `uv run python scripts/refactor_audit.py --fail-on-regression`

Baseline update rule:

- only run `uv run python scripts/refactor_audit.py --update-baseline` after the
  closing audit shows `resolved >= 20`, `new = 0`, and `worsened = 0`

## Notes

- `pyright` is currently green on the branch baseline.
- `tests/test_rag_corpus_tools.py` and
  `tests/test_trends_prompt_includes_overview_pack.py` already pass on the
  branch baseline before the refactor.
