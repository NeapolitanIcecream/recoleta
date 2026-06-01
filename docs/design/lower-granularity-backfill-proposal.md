# Lower-Granularity Backfill Simplification Proposal

## Context

`run week` and `run month` expand into lower-granularity trend and idea windows.
Before this change, recursive planning mixed several completion signals:

- canonical `pass_outputs`
- trend and idea `documents` projections
- workflow freshness hashes
- upstream propagation from planned analyze or lower-level trend work

That made backfill effectively non-idempotent. A lower-level daily or weekly
trend could be regenerated even though the canonical pass had already completed.
Projection drift and freshness drift should not by themselves trigger recursive
LLM generation.

## Decision

Recursive lower-level trend and idea generation is now task-set based and
first-run only:

- a lower-granularity trend/idea task set runs only when no trend or idea
  evidence exists for that lower granularity in the requested parent window;
- evidence includes any lower-level `trend_synthesis` or `trend_ideas` pass
  output, regardless of status, and any lower-level trend or idea document;
- if one lower-level artifact or run exists, the workflow does not recursively
  generate that lower granularity again;
- `--force` still overrides this gate for requested workflow windows.

Target-granularity work still uses the existing freshness and projection checks.
For example, `run week` may still rerun the week trend when its direct daily
source was generated in the same plan, but it does not rerun daily trend or
idea work once any daily trend/idea evidence exists for that week.

## Behavior

`--dry-run --json` exposes the recursive lower-level decision directly:

- `existing_lower_level_task_set`: skip lower-level trend or idea generation
  because that lower-granularity task set has prior evidence;
- `missing_lower_level_task_set`: run lower-level trend or idea generation
  because that lower-granularity task set is untouched.

Projection repair is separate from generation. If documents, Markdown, PDFs, or
site files drift while pass outputs are correct, use `repair outputs`. Required
trend-source materialization can still rebuild missing trend projections from
stored pass outputs before a parent trend uses them, but it does not generate a
missing lower-level pass output inside the parent trend stage.

Missing lower-level trend or idea pass outputs do not by themselves keep same-day
ingest, analyze, or publish work active. The workflow planner may still run
those base steps when they have their own target-level reason, such as candidate
items or an explicitly requested target window.

The legacy `TrendStageRequest.backfill` and `backfill_mode` fields remain
accepted for compatibility, but direct trend stages no longer run a separate
document-probing backfill loop.

## Acceptance

- Week planning skips all daily trend and idea generation when any daily
  trend/idea artifact or pass output exists in the week.
- Week planning can generate daily trend and idea work when the daily task set
  is completely untouched.
- Month planning does not rerun an existing week trend because a day trend was
  generated in the same plan.
- Month planning reruns the target month trend when an untouched week task set
  generates a direct week source in the same plan.
- Direct trend stages rely on source materialization and pass-output repair, not
  `pipeline.trends.backfill.*` metrics or `Trends backfill progress` logs.
