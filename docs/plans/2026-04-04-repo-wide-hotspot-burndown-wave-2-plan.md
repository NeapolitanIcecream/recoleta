# Repo-Wide Hotspot Burndown Wave 2

Date: 2026-04-04

Status: In Progress

## Goal

Reduce at least 40 additional active hotspot signals reported by
`scripts/refactor_audit.py`, measured against the current
`quality/refactor-baseline.json`, without changing thresholds or rewriting the
measurement rules.

This branch is explicitly a follow-up to PR #36 (`b29e4805`), which already
landed the first 40-signal burndown on `main`.

## Baseline

Latest whole-repo audit before this branch:

- hotspots: `123`
- active hotspot signals: `62`
- `refactor_now`: `17`
- `refactor_soon`: `21`
- `baseline_diff.new = 0`
- `baseline_diff.worsened = 0`
- `baseline_diff.resolved = 0`

## Success Criteria

- Before updating `quality/refactor-baseline.json`, achieve
  `baseline_diff.resolved >= 40`.
- Keep `baseline_diff.new == 0` and `baseline_diff.worsened == 0`.
- Preserve public CLI/config/schema/result contracts.
- Update the baseline only after the measured reduction is confirmed and the
  branch passes validation.

## Execution Order

### Wave 1: Script and harness hotspots

- `scripts/bench_arxiv_enrich_paths.py`
- `scripts/bench_trends_hotspots.py`
- `scripts/eval_trends_agent_loop.py`
- `scripts/ping_openai_embeddings.py`

Target change axis:

- split CLI parsing and validation from execution
- split runtime orchestration from formatting and report writing
- split document/chunk preparation from FTS/index write paths
- split response transport, decoding, and validation for probe helpers

### Wave 2: Runtime/core hotspots

- `recoleta/triage.py`
- `recoleta/config.py`
- `recoleta/llm_costs.py`
- `recoleta/rag/vector_store.py`
- `recoleta/observability.py`

Target change axis:

- keep public entrypoints thin and move branchy work into private helpers
- preserve existing ordering, error handling, and metrics semantics

### Wave 3: Reserve

Use only if the Wave 1 + Wave 2 audit result still lands below 40 resolved
signals.

Reserve order:

1. `recoleta/site_deploy.py`
2. `recoleta/pipeline/pass_runner.py`
3. `recoleta/pipeline/projections.py`
4. `recoleta/pipeline/service.py`
5. `recoleta/storage/documents.py`
6. `recoleta/publish/telegram_format.py`

## Validation

Wave 1:

- `uv run pytest tests/test_bench_arxiv_enrich_paths.py tests/test_ping_openai_embeddings_script.py tests/test_eval_trends_agent_loop.py -q`

Wave 2:

- `uv run pytest tests/test_recoleta_specs_analyze.py tests/test_recoleta_specs_settings.py tests/test_llm_cost_recovery.py tests/test_rag_corpus_tools.py tests/test_observability_logging.py -q`

Wave 3:

- run the smallest relevant regression slices for each touched reserve file

Closing validation:

- `uv run ruff check .`
- `uv run pyright`
- `uv run pytest`
- `uv run python scripts/refactor_audit.py`
- `uv run python scripts/refactor_audit.py --fail-on-regression`

After the closing audit confirms the measured reduction:

- `uv run python scripts/refactor_audit.py --update-baseline`
- rerun `uv run python scripts/refactor_audit.py` to confirm a neutral
  `baseline_diff`

## PR Tracking

- branch: `codex/repo-wide-hotspot-burndown-wave-2`
- draft PR title: `[codex] Track repo-wide hotspot burndown wave 2`
- merge title: `refactor(repo): burn down 40 more hotspot signals`
