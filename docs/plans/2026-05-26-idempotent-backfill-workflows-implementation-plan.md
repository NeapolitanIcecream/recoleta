# Idempotent Backfill Workflows Implementation Plan

Date: 2026-05-26

Status: proposed for one implementation PR

Source proposal: `docs/plans/2026-05-26-idempotent-backfill-workflows-research-proposal.md`

## Problem Statement

The current granularity workflows are too imperative. Operators can ask for
`fleet run week` after seven successful `fleet run day` runs, but the weekly
workflow still expands and executes day-level invocations by default. That makes
users responsible for knowing which lower-level steps are already complete and
which `--skip` recipe is safe.

The target product model is declarative:

- `run day` ensures one UTC day is complete.
- `run week` ensures all seven day windows and the week window are complete.
- `run month` ensures all day windows, week windows, and the month window are
  complete.
- `fleet run ...` applies the same semantics independently to every child
  instance and then reports an aggregate plan/result.
- Non-forced runs reconcile missing or stale work and skip complete expensive
  work.
- Deliberate regeneration must be explicit through force or repair controls.

This PR must make the safe path the default. "Use `--skip` after day runs" is
not an acceptable final design.

## Current-State Findings

### Invocation graph

`recoleta/cli/workflow_runner.py` currently builds plans in two phases:

- `granularity_stack(..., recursive_lower_levels=True)` returns `["day"]`,
  `["day", "week"]`, or `["day", "week", "month"]`.
- `build_granularity_plan` adds `ingest`, `analyze`, optional `publish`, and
  every trend/idea step for that stack.
- `_build_granularity_invocations` expands a week into seven day invocations
  plus one week invocation, and expands a month into all day, week, and month
  invocations.
- `execute_workflow_loop` executes every invocation in the plan. It dedupes
  `executed_steps` for payload display, but the `steps` payload and billing
  diffs still come from every invocation.

The existing tests lock this in. `test_run_week_executes_recursive_day_and_week_synthesis_workflow`
expects seven prepare/analyze/publish/day-trends/day-ideas calls plus one
weekly trends/ideas pair. `test_run_month_executes_recursive_day_week_and_month_synthesis_workflow`
expects 31 day invocations, six week invocations, and one month invocation for
March 2026.

### Defaults and CLI surface

`WorkflowPolicyConfig.recursive_lower_levels` defaults to `True` in
`recoleta/config.py`, so lower-level recursion is the default for week and
month. `run day`, `run week`, `run month`, and the fleet equivalents currently
accept `--date`, `--include`, `--skip`, and `--json`; they do not expose
`--dry-run`, planner output, or a content-generation `--force`.

`run deploy` and `fleet run deploy` already expose `--force/--no-force`, but
that force is a Git deployment force-push control. The implementation must not
reuse that flag internally for trend/idea regeneration without separating the
meaning in code.

### Fleet behavior

`execute_fleet_granularity_workflow` performs fleet arXiv pool pre-sync and
readiness checks, then calls `execute_granularity_workflow` for every child.
Fleet therefore inherits the unconditional lower-level execution graph. The
readiness layer is useful, but it is not an idempotency planner.

### W21 runtime evidence

The replay logs at
`/Users/chenmohan/Playground/recoleta-playground/fleet/replay-logs/20260525-w21-v1/`
show material repeated LLM work:

| Run group | Children | Total cost | Analyze cost | Day trends cost | Day ideas cost | Week trends+ideas cost | Translation cost |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Seven `fleet run day` runs, 2026-05-18..2026-05-24 | 3 per day | $38.5532 | $17.9644 | $3.9993 | $2.3825 | $0.0000 | $14.2042 |
| One `fleet run week --date 2026-05-18` | 3 | $33.0860 | $13.6047 | $4.6146 | $2.3906 | $1.7971 | $10.6777 |

The weekly run still executed day-level expensive work after the seven daily
runs. Weekly-only trends and ideas were about $1.80; the large weekly cost was
from lower-level replay plus translation. Translation cannot currently be split
by source granularity in billing, which is itself part of the problem.

### Stage idempotency and authority

| Stage | Existing authority | Current behavior | Gap to close |
| --- | --- | --- | --- |
| Ingest/prepare | `source_pull_states`, `items`, `contents.content_hash` | Upserts are mostly safe, but source pulls and Huldra access can still be slow or costly. | Planner should skip ingest when the target window is already complete downstream, and run it when lower-level completion is missing. |
| Analyze | `items.state`, `analyses` keyed by item | `list_items_for_llm_analysis` only selects retryable, triaged, or enriched items, so already analyzed/published items are skipped. | Need a period-level "analyze complete" probe and a freshness fingerprint that can explain why no LLM work is planned. |
| Publish | `items.state`, `deliveries`, `trend_deliveries` | Item publish mutates analyzed items to published, and delivery records prevent duplicate Telegram sends. | Treat Telegram and other external sends as historical side effects. Do not replay them automatically; allow repair for local projections only. |
| Trends | `pass_outputs`, `documents`, `document_chunks` | Workflow trends calls use `reuse_existing_corpus=True`, so corpus materialization may skip or repair, but target trend synthesis still regenerates whenever invoked. Stage backfill uses document presence only. | Need exact-window freshness checks for `trend_synthesis` pass outputs and projections before invoking LLM generation. |
| Ideas | Latest upstream `trend_synthesis` pass output and `trend_ideas` pass outputs | Ideas always generates a new pass output when invoked unless the upstream corpus is empty or ideas are suppressed. | Need to treat succeeded and suppressed ideas outputs as terminal when tied to the current upstream trend pass output. |
| Translation | `localized_outputs` keyed by source kind, source record id, language, with `source_hash` | Existing source-hash skip is good, but regenerated pass output IDs force new translation candidates even when semantic source did not change. Metrics are global. | Planner must report skip/run counts before LLM calls; metrics must be attributable by source kind and granularity. |
| Site build | Site input/output manifests and generated files | Static site export is rebuildable presentation material. | Rebuild only after upstream changes or explicit request; never confuse site rebuild with content regeneration. |
| Deploy | Git branch state and deploy result | Deploy is an external side effect and already has a Git force flag. | Keep deploy separate from generation force. |

Existing tables are sufficient for a first implementation without a broad schema
rewrite. `runs` already records requested/executed/skipped steps and
billing-by-step. `pass_outputs` already has `diagnostics_json` and
`input_refs_json`, which can carry freshness fingerprints. `localized_outputs`
already stores `source_hash`.

## Proposed CLI and Config Shape

Add low-side-effect planning to the existing workflow commands:

```bash
uv run recoleta run day --date 2026-05-24 --dry-run --json
uv run recoleta run week --date 2026-05-18 --dry-run --json
uv run recoleta fleet run week --manifest fleet.yaml --date 2026-05-18 --dry-run --json
```

Dry-run output should not create run rows, metrics, pass outputs, localized
outputs, documents, site files, or deliveries. It should load config and
repository state, then emit the same target window plus a `plan` array:

```json
{
  "status": "ok",
  "mode": "dry_run",
  "command": "run week",
  "target_granularity": "week",
  "target_period_start": "2026-05-18T00:00:00+00:00",
  "target_period_end": "2026-05-25T00:00:00+00:00",
  "planned_expensive_steps": 2,
  "plan": [
    {
      "step_id": "trends:day",
      "granularity": "day",
      "period_start": "2026-05-18T00:00:00+00:00",
      "period_end": "2026-05-19T00:00:00+00:00",
      "action": "skip",
      "reason": "fresh_pass_output",
      "expensive": true
    }
  ]
}
```

Add content-generation force to `run day|week|month` and `fleet run
day|week|month`:

```bash
uv run recoleta run week --date 2026-05-18 --force
uv run recoleta fleet run week --manifest fleet.yaml --date 2026-05-18 --force
```

Implementation detail: do not reuse `WorkflowExecutionContext.force` for both
generation and deploy semantics. Rename or split it, for example into
`generation_force` and `site_deploy_force`.

Keep `--include` and `--skip` for compatibility, but update help/docs so they
are advanced repair controls rather than the normal weekly operating model.
Keep `workflows.granularities.*.recursive_lower_levels` for compatibility. With
the default `True`, week/month should still ensure lower-level windows, but the
planner must decide whether each lower-level invocation runs or skips. Existing
configs that set it to `False` should continue to run target-granularity work
only.

No required database migration is needed. New freshness data should be written
into existing `diagnostics_json` or `input_refs_json`. Existing pass outputs
without fingerprints should be classified as `legacy_complete` when their
document/projection contract is present, so old local databases do not
immediately regenerate history.

## Planner Contract

Create a read-only workflow planner that operates on concrete windows and emits
decisions before execution.

Decision actions:

- `run`: execute because required state is missing or stale.
- `skip`: state is complete and fresh enough for non-forced ensure semantics.
- `repair`: execute a non-LLM repair/materialization step such as missing
  projection documents.
- `force`: execute because the user requested regeneration.
- `blocked`: do not execute because readiness or dependency checks failed.

Each decision should include:

- `step_id`
- `granularity`
- `period_start`
- `period_end`
- `action`
- `reason`
- `expensive`
- `authority`, such as `pass_outputs`, `localized_outputs`, or `item_state`
- optional `freshness_key` or `source_hash`
- optional `estimated_llm_calls` when cheaply known, otherwise `null`

The planner should not try to estimate exact dollars. It should identify
expensive LLM-bearing work and expose why it will or will not run.

Freshness fingerprints for generated outputs should include at least:

- Stage/pass kind and schema version.
- Granularity and period bounds.
- Relevant source IDs and source hashes.
- Upstream pass output ID for ideas.
- Model/provider identifier where available.
- Prompt or generation config version if available.
- Translation source hash and source kind/granularity for translation.

## Implementation Steps

### Step 1: Add workflow planning inspection layer

Intent:
Introduce read-only planner models and storage probes that can classify each
workflow window as complete, missing, stale, repairable, forced, or blocked.
This step should not change command behavior.

Files likely touched:
- `recoleta/cli/workflow_models.py`
- `recoleta/cli/workflow_runner.py`
- `recoleta/cli/workflow_planner.py`
- `recoleta/storage/pass_outputs.py`
- `recoleta/storage/documents.py`
- `recoleta/storage/analyses.py`
- `tests/test_workflow_planner.py`

Acceptance criteria:
- Tests cover a complete daily week producing `skip` decisions for day-level
  `analyze`, `trends:day`, and `ideas:day`.
- Tests cover an incomplete daily week producing `run` decisions only for the
  missing or stale day windows.
- Planner calls are read-only: they do not create run rows, metrics, pass
  outputs, documents, localized outputs, deliveries, or site files.
- Planner decisions include action, reason, authority, expensive flag, window,
  and step ID for every invocation currently produced by the workflow plan.

Commit gate:
- Run: `uv run pytest tests/test_workflow_planner.py -q && uv run ruff check recoleta tests/test_workflow_planner.py`
- Commit only after all acceptance criteria pass.
- Suggested commit subject: `feat(workflows): add read-only ensure planner`

### Step 2: Persist generation freshness fingerprints

Intent:
Make trends and ideas completion checks defensible by persisting stable
freshness metadata on generated pass outputs and by treating legacy outputs
conservatively as complete when their projection contract is present.

Files likely touched:
- `recoleta/pipeline/trends_stage.py`
- `recoleta/pipeline/ideas_runtime.py`
- `recoleta/pipeline/pass_runner.py`
- `recoleta/passes.py`
- `recoleta/storage/pass_outputs.py`
- `tests/test_trends_workflow_freshness.py`
- `tests/test_ideas_workflow_freshness.py`
- `tests/test_trends_reuse_existing_corpus.py`

Acceptance criteria:
- New `trend_synthesis` pass outputs include a deterministic freshness
  fingerprint in diagnostics or input refs.
- New `trend_ideas` pass outputs include the upstream trend pass output ID and
  deterministic freshness fingerprint.
- Planner tests prove matching fingerprints skip generation and changed
  upstream inputs produce `run` or `stale` decisions.
- Legacy pass outputs without freshness metadata are classified as
  `legacy_complete` only when the pass output exists and required document
  projections are readable.

Commit gate:
- Run: `uv run pytest tests/test_trends_workflow_freshness.py tests/test_ideas_workflow_freshness.py tests/test_trends_reuse_existing_corpus.py -q && uv run ruff check recoleta tests`
- Commit only after all acceptance criteria pass.
- Suggested commit subject: `feat(trends): record workflow freshness fingerprints`

### Step 3: Expose dry-run plans for local and fleet workflows

Intent:
Let operators see planned expensive work and skip reasons before any LLM calls,
including across fleet child instances.

Files likely touched:
- `recoleta/cli/app.py`
- `recoleta/cli/workflows.py`
- `recoleta/cli/fleet.py`
- `recoleta/cli/workflow_runner.py`
- `tests/test_recoleta_specs_run_once_cli.py`
- `tests/test_fleet_workflows.py` or existing fleet CLI test files
- `docs/guides/usage-recipes.md`

Acceptance criteria:
- `run day|week|month --dry-run --json` emits a machine-readable planner
  payload and exits without executing service methods.
- `fleet run day|week|month --dry-run --json` emits per-child planner payloads
  and an aggregate expensive-step summary.
- Dry-run output includes skip reasons for completed lower-level windows.
- Dry-run does not create run records or metrics.
- Human output for dry-run is short and highlights planned expensive steps.

Commit gate:
- Run: `uv run pytest tests/test_recoleta_specs_run_once_cli.py tests/test_fleet_workflows.py -q && uv run ruff check recoleta tests`
- Commit only after all acceptance criteria pass.
- Suggested commit subject: `feat(cli): add workflow dry-run plans`

### Step 4: Execute workflows from planner decisions

Intent:
Change period workflows from unconditional invocation replay to ensure-style
execution. Week and month still include lower-level windows by default, but
complete expensive lower-level work is skipped.

Files likely touched:
- `recoleta/cli/workflow_runner.py`
- `recoleta/cli/workflow_steps.py`
- `recoleta/cli/workflows.py`
- `recoleta/cli/fleet.py`
- `tests/test_recoleta_specs_run_once_cli.py`
- `tests/test_workflow_planner.py`
- `tests/test_recoleta_specs_runs_cli.py`
- `tests/test_recoleta_specs_billing.py`

Acceptance criteria:
- A week workflow over seven complete day windows does not invoke day-level
  `analyze`, `trends:day`, or `ideas:day` LLM work.
- A week workflow over incomplete day windows backfills only the missing or
  stale windows.
- A month workflow skips complete day/week windows and still runs missing lower
  levels plus month-level work.
- Existing day workflow behavior remains stable.
- Workflow JSON records planned skips separately from config-disabled skips so
  operators can distinguish `translation=off` from `fresh_pass_output`.
- Billing by step does not include skipped expensive steps except as zero-cost
  planner entries if the payload needs to report them.

Commit gate:
- Run: `uv run pytest tests/test_recoleta_specs_run_once_cli.py tests/test_workflow_planner.py tests/test_recoleta_specs_runs_cli.py tests/test_recoleta_specs_billing.py -q && uv run ruff check .`
- Commit only after all acceptance criteria pass.
- Suggested commit subject: `feat(workflows): reconcile period plans idempotently`

### Step 5: Add explicit force and repair semantics

Intent:
Make regeneration deliberate while keeping compatibility for existing scripts.
Normal runs should be safe; force and repair paths should be clear enough for
operators who intentionally want to recompute or rematerialize outputs.

Files likely touched:
- `recoleta/cli/app.py`
- `recoleta/cli/workflows.py`
- `recoleta/cli/fleet.py`
- `recoleta/cli/workflow_models.py`
- `recoleta/cli/workflow_runner.py`
- `recoleta/cli/workflow_steps.py`
- `tests/test_recoleta_specs_run_once_cli.py`
- `tests/test_cli_v2_surface.py`

Acceptance criteria:
- `run day|week|month --force` and `fleet run day|week|month --force`
  intentionally regenerate selected expensive stages.
- Non-forced runs skip fresh expensive work.
- Deploy force remains a Git deployment control and is not conflated with
  generation force in code or docs.
- Existing `--include`, `--skip`, and `recursive_lower_levels` behavior remains
  available for compatibility, but help text and docs classify them as advanced
  repair controls.
- If a hidden rollback flag is added for one release, tests prove it restores
  legacy unconditional replay without changing the new default.

Commit gate:
- Run: `uv run pytest tests/test_recoleta_specs_run_once_cli.py tests/test_cli_v2_surface.py -q && uv run ruff check recoleta tests`
- Commit only after all acceptance criteria pass.
- Suggested commit subject: `feat(workflows): add explicit generation force`

### Step 6: Improve translation freshness attribution

Intent:
Make translation skip/run decisions and billing attribution inspectable without
manual log reconstruction. This closes the W21 evidence gap where the weekly
translation cost could not be split by source granularity.

Files likely touched:
- `recoleta/translation_runtime.py`
- `recoleta/translation.py`
- `recoleta/translation_candidates.py`
- `recoleta/storage/localized_outputs.py`
- `recoleta/cli/workflow_planner.py`
- `tests/test_translation_runtime_parallelism.py`
- `tests/test_translate_cli.py`
- `tests/test_recoleta_specs_billing.py`

Acceptance criteria:
- Translation diagnostics include source kind and, for trend and idea sources,
  source granularity and period bounds.
- Translation metrics include low-cardinality source buckets for scanned,
  translated, skipped, failed, request count, token count, and estimated cost.
- Existing source-hash skip behavior is preserved.
- Planner dry-run can report translation candidates that will run or skip by
  source kind/granularity without calling the LLM.
- Billing reports can distinguish day trend/idea translation work from
  week/month translation work.

Commit gate:
- Run: `uv run pytest tests/test_translation_runtime_parallelism.py tests/test_translate_cli.py tests/test_recoleta_specs_billing.py -q && uv run ruff check recoleta tests`
- Commit only after all acceptance criteria pass.
- Suggested commit subject: `feat(translate): attribute freshness by source`

### Step 7: Add guardrails, docs, and final validation

Intent:
Prevent future silent regressions and make the operator story simple: run the
target period and Recoleta ensures it.

Files likely touched:
- `tests/test_recoleta_specs_run_once_cli.py`
- `tests/test_workflow_planner.py`
- `docs/guides/usage-recipes.md`
- `docs/guides/fleet-development-runbook.md`
- `docs/design/configuration.md`
- `recoleta.example.yaml`
- `.cursor/skills/research-site-design-language/SKILL.md` only if site design
  rules change

Acceptance criteria:
- A guard test proves `run week` over seven complete day windows cannot produce
  day-level LLM metrics unless `--force` is present.
- Docs describe ensure/backfill semantics for day, week, month, and fleet.
- Docs state when to use `--force`, `--include`, `--skip`, and
  `recursive_lower_levels=false`.
- Existing examples no longer teach manual weekly `--skip` recipes for normal
  operation.
- The PR description can include before/after W21 behavior: previous weekly run
  repeated day-level analyze/trends/ideas and un-attributed translation; new
  weekly run plans skips for complete daily outputs and runs only weekly or
  missing work.

Commit gate:
- Run: `uv run pytest tests/test_recoleta_specs_run_once_cli.py tests/test_workflow_planner.py -q && uv run ruff check . && uv run pyright`
- Commit only after all acceptance criteria pass.
- Suggested commit subject: `docs(workflows): document idempotent backfill semantics`

## Final PR Validation Checklist

- `uv run ruff check .`
- `uv run pyright`
- `uv run pytest`
- `uv run recoleta run week --date 2026-05-18 --dry-run --json` on a fixture or
  local copy with complete daily outputs shows day-level expensive skips.
- `uv run recoleta fleet run week --manifest <fixture> --date 2026-05-18 --dry-run --json`
  shows per-child skip/run decisions.
- A non-forced week run after seven successful day runs emits no day-level LLM
  metrics.
- A week run with one missing day backfills that day and still runs weekly
  synthesis.
- A forced week run intentionally regenerates the requested expensive outputs.
- Translation billing output can be grouped by source kind and granularity.
- PR description includes the W21 before/after cost-risk explanation and lists
  the acceptance commands run for each commit.

## Rollback Plan

The PR should avoid destructive migrations. New freshness metadata lives in
existing JSON fields, and older rows remain readable.

If planner execution introduces a production regression, rollback options are:

- Revert the behavior commit that switches execution to planner decisions while
  keeping read-only dry-run code if useful.
- Use the temporary hidden legacy replay flag if Step 5 adds one.
- For individual operators, set `recursive_lower_levels=false` to limit
  week/month runs to target-granularity work, then run explicit day/week repair
  commands as needed.

Rollback must not delete pass outputs, localized outputs, documents, deliveries,
or run history.

## Open Questions

None block the first implementation PR, but the PR should make these choices
explicit in tests and docs:

- How strict should legacy outputs without fingerprints be? This plan chooses
  `legacy_complete` when the pass output and projection contract are present.
- Should local markdown publish output be repaired automatically while Telegram
  delivery remains historical? This plan treats external sends as historical
  and local/site projections as repairable.
- Should exact cost estimates appear in dry-run? This plan says no. Dry-run
  should expose expensive step counts and reasons, not pretend to know token
  costs before prompts are built.
