# Active Hotspot Burndown Wave 3

Date: 2026-04-05

Status: Completed

## Goal

Reduce at least 20 active hotspot signals reported by `scripts/refactor_audit.py`,
measured against the current `quality/refactor-baseline.json`, while removing all
remaining `refactor_now` hotspots without changing thresholds or measurement
rules.

This branch is the follow-up to the earlier hotspot burndown waves. The current
whole-repo audit shows that the remaining active hotspots are concentrated in a
small set of parameter-heavy interfaces plus a few still-branchy script/runtime
helpers.

## Baseline

Whole-repo audit on `2026-04-05`:

- hotspots: `83`
- active hotspot signals: `21`
- `refactor_now`: `8`
- `refactor_soon`: `9`
- `baseline_diff.new = 0`
- `baseline_diff.worsened = 0`
- `baseline_diff.resolved = 0`

## Success Criteria

- Achieve `baseline_diff.resolved >= 20` before updating
  `quality/refactor-baseline.json`.
- Reduce `refactor_now` to `0`.
- Keep `baseline_diff.new == 0` and `baseline_diff.worsened == 0`.
- Preserve CLI behavior, config shape, storage behavior, and publishing/site
  output contracts.

## Execution Order

### Wave 1: RAG and triage request-object cleanup

- `recoleta/rag/vector_store.py`
- `recoleta/rag/sync.py`
- `recoleta/rag/ideas_agent.py`
- `recoleta/triage.py`

Target change axis:

- replace wide keyword-only interfaces with request/context dataclasses while
  preserving current call sites
- split index-building and selection logic into smaller helpers so the active
  hotspots stop accumulating on orchestration entrypoints

### Wave 2: Runtime and site/storage support helpers

- `recoleta/storage/leases.py`
- `recoleta/storage/common.py`
- `recoleta/storage/deliveries.py`
- `recoleta/site.py`
- `recoleta/site_deploy.py`
- `recoleta/app/runtime.py`
- `recoleta/types.py`

Target change axis:

- keep public behavior stable while collapsing parameter-count hotspots into
  stable request/detail objects
- extract homepage/topic aggregation helpers instead of letting page assembly
  remain a single long function

### Wave 3: Audit and bench scripts

- `scripts/refactor_audit.py`
- `scripts/inspect_bench_out_db.py`

Target change axis:

- separate tool execution, hotspot classification, and baseline diffing
- separate prompt-cost row computation from CLI/report rendering

## Validation

Wave 1:

- `uv run pytest tests/test_recoleta_specs_analyze.py tests/test_recoleta_specs_rag_cli.py -q`

Wave 2:

- `uv run pytest tests/test_recoleta_specs_runtime_safety.py tests/test_site_gh_deploy.py -q`

Wave 3:

- `uv run pytest tests/test_refactor_audit.py -q`

Closing validation:

- `uv run ruff check .`
- `uv run pyright`
- `uv run pytest`
- `uv run python scripts/refactor_audit.py`
- `uv run python scripts/refactor_audit.py --fail-on-regression`

After the closing audit confirms the reduction:

- `uv run python scripts/refactor_audit.py --update-baseline`
- rerun `uv run python scripts/refactor_audit.py` to confirm a neutral
  `baseline_diff`

## PR Tracking

- branch: `codex/active-hotspot-burndown-wave-3`
- draft PR title: `[codex] Track active hotspot burndown wave 3`
- merge title: `refactor(repo): remove the final active hotspot signals`

## Outcome

Closing audit after the implementation and review-fix loop:

- hotspots: `66`
- active hotspot signals: `0`
- `refactor_now`: `0`
- `refactor_soon`: `0`
- `baseline_diff.new = 0`
- `baseline_diff.worsened = 0`
- `baseline_diff.resolved = 0`

The PR also closed the follow-up Codex review regressions around explicit zero
parameter handling in `recoleta/rag/sync.py` and `recoleta/rag/vector_store.py`
before merge.
