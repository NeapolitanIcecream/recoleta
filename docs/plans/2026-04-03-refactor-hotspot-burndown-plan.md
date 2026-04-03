# Refactor Hotspot Burndown Plan

Date: 2026-04-03

Status: Proposed tracking plan

## Goal

Reduce at least 20 hotspot signals reported by `scripts/refactor_audit.py`,
measured against `quality/refactor-baseline.json`, without relaxing thresholds
or rewriting the baseline to match the current debt.

This plan is intentionally about signal reduction, not about shrinking files for
its own sake. The target is a safer codebase with smaller change surfaces in the
same subsystems already identified by the architecture roadmap.

## Audit Snapshot

Commands run on 2026-04-03:

- `uv run ruff check .`
- `uv run python scripts/refactor_audit.py`

Observed baseline:

- `ruff`: clean (`All checks passed!`)
- repo verdict: `strained`
- hotspots: `202` total
- `refactor_now`: `58`
- `refactor_soon`: `47`
- `monitor`: `97`
- triple-hit hotspots (`complexipy + lizard + ruff`): `36`

Most important clustering from `output/refactor-audit/report.json`:

- `recoleta/translation.py`: `8` triple-hit hotspots
- `recoleta/pipeline/service.py`: `3` triple-hit hotspots
- `recoleta/pipeline/publish_stage.py`: `1` triple-hit hotspot
- `recoleta/pipeline/ideas_stage.py`: `1` triple-hit hotspot
- `recoleta/storage/documents.py`: `3` triple-hit hotspots

This lines up with the existing architecture review:

- `docs/plans/2026-03-09-architecture-review-and-refactor-roadmap.md` already
  identifies `pipeline` and `storage` as concentration points.
- The current audit shows that `translation` is now the other large
  concentration point and should join the next refactor wave instead of being
  treated as cleanup.

## Working Rules

- Count progress by resolved hotspot signals, not by lines moved.
- Prefer triple-hit symbols first because a fully cleared symbol removes three
  signals at once.
- Plan against more than 20 potential removals because some functions will drop
  below one threshold before clearing all three.
- Keep public behavior stable and lean on the existing spec-style tests.
- Do not update `quality/refactor-baseline.json` until the refactor series has
  produced a real reduction with `has_regressions=false`.

## Target Portfolio

The execution portfolio intentionally carries more than 20 possible removals so
the final series still lands above the requested floor if a few symbols only
partially clear their thresholds.

### Wave 1: Pipeline stage decomposition

Primary target: reduce the stage-runner concentration already called out by the
architecture roadmap.

Target symbols:

- `recoleta/pipeline/service.py::PipelineService::_build_triage_candidates`
- `recoleta/pipeline/service.py::PipelineService::triage`
- `recoleta/pipeline/service.py::PipelineService::analyze`
- `recoleta/pipeline/publish_stage.py::run_publish_stage`
- `recoleta/pipeline/ideas_stage.py::run_ideas_stage`

Potential signal budget: `15`

Planned change axis:

- Extract shared stage-runner helpers for candidate loading, metric recording,
  and debug-artifact writes instead of repeating the template inside each stage.
- Move triage content selection and excerpt fallback ordering out of
  `PipelineService::_build_triage_candidates`.
- Split `PipelineService::analyze` into smaller helpers for:
  - work item preparation
  - outcome accounting
  - persistence/state transitions
  - metric emission
- Split `run_publish_stage` into target setup, per-item publish execution, and
  final index/metric recording helpers.
- Split `run_ideas_stage` into upstream loading, payload generation, and
  projection persistence helpers.

Why this wave is first:

- It matches the existing architecture roadmap instead of inventing a new axis.
- It removes pressure from the top-level runtime path used by the CLI.
- The tests are already broad enough to make structural extraction safer.

Expected validation focus:

- `uv run pytest tests/test_recoleta_specs_analyze.py -q`
- `uv run pytest tests/test_recoleta_specs_publish.py -q`
- `uv run pytest tests/test_ideas_stage.py -q`

### Wave 2: Translation orchestration split

Primary target: separate candidate loading, hybrid retrieval context, and
translation execution orchestration inside `recoleta/translation.py`.

Target symbols:

- `recoleta/translation.py::_hybrid_context_for_query`
- `recoleta/translation.py::_load_idea_candidates`
- `recoleta/translation.py::_translate_structured_payload_with_debug`
- `recoleta/translation.py::run_translation`
- `recoleta/translation.py::run_translation_backfill`

Potential signal budget: `15`

Planned change axis:

- Extract hybrid query building and bundle assembly into a dedicated helper
  module so context-assist behavior is independent from run orchestration.
- Extract idea/trend candidate loading and missing-document projection repair
  into dedicated loaders instead of keeping SQL access, pass-output traversal,
  and document projection writes in one function.
- Extract the shared translation execution loop so `run_translation` and
  `run_translation_backfill` become thin orchestrators around common scheduling,
  provider-failure handling, and persistence steps.

Why this is the second wave:

- It is the single densest triple-hit cluster in the repo.
- The file currently mixes search service use, pass-output recovery, runtime
  parallelism, and persistence concerns.
- The test surface is already deep enough to support an internal split without
  changing user-visible CLI behavior.

Expected validation focus:

- `uv run pytest tests/test_localization_translation.py -q`
- `uv run pytest tests/test_recoleta_specs_run_once_cli.py -q`

### Wave 3: Storage reserve in `documents.py`

Primary target: provide a low-risk reserve if Waves 1 and 2 do not clear the
requested floor because some large functions only partially drop below
thresholds.

Target symbols:

- `recoleta/storage/documents.py::DocumentStoreMixin::delete_document_chunks`
- `recoleta/storage/documents.py::DocumentStoreMixin::list_summary_chunk_index_rows_in_period`
- `recoleta/storage/documents.py::DocumentStoreMixin::search_chunks_text`

Potential signal budget: `9`

Planned change axis:

- Extract chunk-deletion side effects from row selection so SQL cleanup and ORM
  deletion are no longer interleaved in one method.
- Extract document-window normalization and row-to-dict serialization from
  `list_summary_chunk_index_rows_in_period`.
- Extract query normalization and SQL assembly from `search_chunks_text`.

Why this is reserve work instead of the first wave:

- The architecture roadmap is correct that `pipeline` should move first.
- The storage targets are valuable but less central to the main runtime than the
  pipeline and translation clusters.
- They provide extra budget if the first two waves leave a few stubborn
  thresholds in place.

Expected validation focus:

- `uv run pytest tests/test_recoleta_specs_trends.py -q`
- `uv run pytest tests/test_ideas_stage.py -q`

## Reduction Budget

Planned portfolio:

- Wave 1 potential: `15`
- Wave 2 potential: `15`
- Wave 3 reserve potential: `9`
- Total potential: `39`

Delivery bar:

- minimum success: at least `20` resolved hotspot signals
- preferred success: at least `24` resolved hotspot signals
- no new or worsened hotspots in the same series

This means the practical sequence is:

1. Land Wave 1.
2. Land enough of Wave 2 to push the audit over the `20`-signal floor.
3. Use Wave 3 only if the measured audit delta is still short because some
   target functions remain above one tool threshold.

## Tracking Checklist

- [ ] Land pipeline stage decomposition PR(s) for the five primary pipeline
      targets.
- [ ] Land translation decomposition PR(s) for the five primary translation
      targets.
- [ ] Rerun `uv run python scripts/refactor_audit.py` after each execution PR
      and record the before/after delta in the PR body.
- [ ] Use storage reserve work only if the cumulative resolved set is still
      below `20`.
- [ ] Update `quality/refactor-baseline.json` only in the final closing PR for
      this series, after the audit shows the reduction.

## Exit Criteria

The closing execution PR for this series must show all of the following:

- `uv run ruff check .`
- `uv run pyright`
- targeted pytest suites for the touched subsystem(s)
- final `uv run pytest`
- final `uv run python scripts/refactor_audit.py`

And in `output/refactor-audit/report.json`:

- `baseline_diff.has_regressions == false`
- `len(baseline_diff.new) == 0`
- `len(baseline_diff.worsened) == 0`
- `len(baseline_diff.resolved) >= 20`

Only after that should the baseline be updated.

## Non-Goals

This series should not:

- raise audit thresholds
- bulk-delete `vulture` candidates without review
- rewrite stable public CLI contracts
- mix product changes into the refactor PRs
- treat generated benchmark scripts as equal priority with runtime code when the
  `pipeline`, `translation`, and `storage` clusters still dominate the risk

