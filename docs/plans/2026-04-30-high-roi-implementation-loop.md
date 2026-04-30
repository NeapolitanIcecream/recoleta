# High-ROI Implementation Loop

Date: 2026-04-30

Status: active on `codex/high-roi-improvements`

## Goal

Land the highest-return improvement queue identified by the 2026-04-30 audit in
small, reviewable slices. Keep the PR draft while the asynchronous implementation
loop is running.

## Baseline

Validated before opening this loop:

- `uv run ruff check .`
- `uv run coverage run -m pytest`
- `uv run coverage json -o coverage.json`
- `uv run cremona scan --coverage-json coverage.json`

Observed baseline:

- `602 passed`
- no structural debt regressions
- routing pressure: `investigate_now`
- signal health: `full`

## Queue

1. Productize HTML maintext enrich parallelism.
   - Surface `ENRICH_HTML_MAINTEXT_MAX_CONCURRENCY` in user-facing docs,
     examples, rollback guidance, and fleet runbook material.
   - Preserve default behavior.
   - Validate docs and config examples against the existing setting in
     `recoleta.config.Settings`.
2. Retire or neutralize stale top-level module/package shadow shims.
   - Remove stale same-named top-level files after proving imports resolve to
     package directories.
   - Avoid breaking supported imports such as `import recoleta.pipeline` or the
     `recoleta = "recoleta.cli:main"` console script.
   - Update docs and structural-debt baseline only after behavior is verified.
3. Align standalone translation CLI terminal state with workflow semantics.
   - Ensure non-zero translation failures are machine-readable as partial
     failure, not indistinguishable from a clean run.
   - Preserve existing failure typing and metrics.
4. Add a localization audit/doctor surface.
   - Report localized coverage by surface.
   - Flag missing peer-language pages, orphan localized outputs, and
     materialized/site mismatches.
5. Continue small pipeline/trends decompositions by change axis.
   - Target orchestration boundaries before broad rewrites.
   - Keep public CLI, DB, and output contracts stable.
   - Completed slice: extracted analyze item-state update persistence/status
     fallback handling from `PipelineService` into `recoleta.pipeline`.
6. Add focused tests around low-coverage user-facing edges.
   - Prioritize RAG CLI, translate CLI, delivery failure paths, and extraction
     fallbacks.

## Operating Rules

- Each slice must update tests or docs appropriate to the behavioral risk.
- The implementer edits files but does not commit or push.
- The reviewer inspects only after the implementer marks a slice delivered.
- The supervisor commits, pushes, updates this PR, and starts the next slice only
  after review has no blocking findings.
- Coordination state lives in `.codex-workflows/high-roi-implementation/` and is
  intentionally local-only.

## Validation Expectations

Run the narrowest meaningful checks for each slice. Before marking the whole PR
ready for review, run:

- `uv run ruff check .`
- `uv run pyright`
- `uv run pytest`
- `uv run coverage run -m pytest`
- `uv run coverage json -o coverage.json`
- `uv run cremona scan --coverage-json coverage.json --fail-on-regression`
