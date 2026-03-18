# Operations Retro: Agent UX, Failure Recovery, and DFX Gaps

Date: 2026-03-18

## Goal

Capture the operational friction observed while rerunning `2026-03-15` day outputs, `2026-W11` week outputs, and the final deploy, then turn those observations into concrete follow-up work.

## Runtime Context

- The target workflow was: rerun `ingest`, `analyze`, `day trend`, `day ideas`, `week trend`, `week ideas`, then `gh-deploy`.
- `2026-03-15` day trend initially produced an empty corpus even though the database contained items for that date.
- The pipeline only became correct after manual database repair and a true rerun of stream analysis.
- After repair, explicit stream analyses were restored and `2026-03-15` day trend used non-empty corpora again:
  - `embodied_ai`: `items_total=8`
  - `software_intelligence`: `items_total=20`
- This confirms that the failure mode was operational and state-machine related, not a lack of source data.

## Executive Summary

Three themes stood out:

1. Common operator tasks are too fragmented. "Rerun a date and deploy" requires too many separate commands and too much implicit knowledge.
2. The stream-analysis retry model has a real design bug. A transient failure can leave data permanently invisible to later stream reruns.
3. Diagnostics are too weak. Explaining an empty corpus or a partial rerun required direct SQLite inspection and manual reasoning across multiple tables.

## Status Update

The highest-value items from this retro are now implemented on the follow-up
branch that landed after the incident:

- explicit stream reruns were decoupled from the global `items.state`
- `401` / `403` auth failures were reclassified as retryable
- `recoleta repair-streams` was added as a supported repair path
- `recoleta doctor why-empty` was added for empty-corpus diagnosis
- `recoleta doctor llm` was added for effective LLM config diagnosis
- `recoleta runs show` / `recoleta runs list` were added for run inspection
- key long-running commands now support `--json`
- runs now store minimal context, and artifacts now store lightweight failure summaries

The main deferred items are still:

- top-level `rerun` and `deploy` shortcuts
- `runs cleanup`
- retry cooldowns / suppression for known bad URLs
- explicit run cancellation
- richer run success semantics beyond `succeeded|failed`

## Findings

### 1. User-visible operation chains that should be simplified

- There is no single command for "rerun this date, regenerate downstream outputs, and deploy." In practice, the operator has to chain `ingest`, `analyze`, `trends`, `ideas`, and `site gh-deploy`.
- There is no supported way to repair stream-analysis state for a date or stream. In this incident, the only workable recovery path was direct SQLite surgery.
- `gh-deploy` is nested under `site gh-deploy`, which is less discoverable than a top-level deploy command. The current CLI entrypoint for deploy is defined under `site` in `recoleta/cli/app.py:308`.
- LLM configuration refresh is awkward in long-lived shells. A changed key in `.zshrc` was not enough; the shell session had to be reloaded before the CLI saw the new value.
- Command names understate side effects. `trends` and `ideas` sound like synthesis-only stages, but in practice the operator has to reason about hidden prerequisites, backfills, and state repair around them.

### 2. Functional bugs and design flaws that should be fixed

- Explicit stream retries are incorrectly coupled to the global item state.
  - `recoleta/storage/items.py:608-611` requires `Item.state` to be `enriched` or `retryable_failed`.
  - `recoleta/storage/items.py:635-639` also requires the per-stream state to be `NULL` or `retryable_failed`.
  - Explicit stream analysis results are saved without mirroring the global item state by default in `recoleta/storage/analyses.py:118-129`.
  - The combination is broken: once the default analysis path marks an item globally `analyzed`, later explicit stream reruns cannot pick it back up even if the stream state is `retryable_failed`.
  - This was the direct root cause of the `2026-03-15` empty day-trend corpus.

- Authentication and configuration failures are treated as terminal item failures.
  - Failure classification in `recoleta/pipeline/artifacts.py:17-29` only marks `5xx`, `429`, and request errors as retryable.
  - A `401 invalid token` therefore becomes a non-retryable failure.
  - Stream-analysis failure handling in `recoleta/pipeline/service.py:3165-3174` and `recoleta/pipeline/service.py:3217-3226` writes `FAILED` or `RETRYABLE_FAILED` based on that classification.
  - In practice this means a run-scoped credential problem can poison many item-stream rows into a terminal state.

- Run success semantics are too weak.
  - `recoleta/storage/runs.py:40-50` records run completion from a single success boolean.
  - The result is that a run can be stored as `succeeded` even when item-level metrics show `processed_total=0` and `failed_total>0`.
  - This makes run history harder to trust during incident response.

- Trend command boundaries are misleading.
  - Operators naturally think of `trends` as "use the current analyzed corpus to synthesize trend documents."
  - In reality, successful trend generation may depend on hidden upstream state conditions and silent backfill behavior.
  - Even if the implementation is intentional, the command surface should make the side effects explicit.

- Retry economics are weak for known bad source URLs.
  - During repeated reruns, known `403`, `404`, `429`, or `503` sources can be retried again without enough operator-visible cooling or suppression.
  - This slows recovery and obscures the useful work in logs.

### 3. Missing or weak DFX and agent-facing ergonomics

- There is no first-class "why is this corpus empty?" diagnostic.
  - The operator had to inspect `items`, `item_stream_states`, `analyses`, and run metrics manually.
  - A dedicated doctor command should explain candidate counts, selected counts, filtered-out counts, and the top exclusion reasons.

- There is no safe CLI for requeueing or repairing states by date, item, or stream.
  - The lack of a supported recovery path forced direct database updates.

- Run metadata is too sparse for operational debugging.
  - The `runs` table does not carry enough structured context such as command, stage, date, granularity, or stream.
  - Operators have to infer too much from free-form logs and metrics blobs.

- Artifacts are not indexed richly enough in the database.
  - The `artifacts` table stores `run_id`, `item_id`, `kind`, `path`, and timestamps, but not a structured error payload.
  - If the on-disk debug artifact is missing or inconvenient to inspect, the failure context is effectively gone.

- Long-running commands do not expose enough machine-readable output.
  - IDs such as generated `doc_id`, `pass_output_id`, billing counters, and output paths are mostly available only through logs.
  - This makes agent automation and post-run validation more brittle than necessary.

- Default logging is too noisy for operator work.
  - Network and library logs can bury the stage-level information that actually matters during a rerun.
  - Operators need a concise summary mode by default, with verbose transport logs behind an explicit debug switch.

- Interrupted or partial runs are not operator-friendly to clean up.
  - Recovery depends on implicit behavior rather than an explicit cancel, unlock, or stale-run cleanup flow.

- LLM connectivity diagnostics are not first-class.
  - When the key changed, the effective question was "what key is this shell actually using, and is the configured provider healthy?"
  - That required ad hoc probing instead of a supported `doctor llm` or equivalent.

## Candidate Command Surface Improvements

The following commands would have directly shortened this incident:

- Deferred: `recoleta rerun --date 2026-03-15 --day --week --ideas --deploy`
- Implemented (minimal form): `recoleta repair-streams --date 2026-03-15 --streams embodied_ai,software_intelligence`
- Implemented: `recoleta doctor why-empty --date 2026-03-15 --granularity day --stream embodied_ai`
- Implemented: `recoleta doctor llm`
- Deferred: `recoleta deploy`
- Implemented (run-id centric): `recoleta runs show --run-id <run-id>`
- Deferred: `recoleta runs cleanup`

The exact spelling can change, but the product need is clear: operators need fewer multi-step recovery playbooks and more first-class, inspectable workflows.

## Recommended Follow-up

### High priority

- Implemented: decouple explicit stream retry selection from the global `items.state`.
- Implemented: reclassify auth and configuration failures so they do not permanently poison item-stream state.
- Implemented: add a supported repair or requeue command for stream analysis.
- Implemented: add a `doctor why-empty` command with machine-readable output.

### Medium priority

- Deferred: add top-level rerun and deploy shortcuts for common workflows.
- Implemented: enrich `runs` metadata so incident analysis does not depend on log archaeology.
- Implemented: store lightweight structured failure payloads alongside artifact paths.
- Implemented: add JSON output modes for long-running CLI commands.

### Lower priority but still useful

- Deferred: add retry cooldowns or suppression windows for repeatedly failing enrich targets.
- Deferred: tighten default log levels so stage summaries remain visible during long reruns.
- Deferred: add explicit run cancellation and stale-run cleanup commands.

## Why This Matters

This incident did not fail because the corpus was genuinely empty. It failed because the current operational model made it too easy for a transient failure to become a long-lived state problem, and too hard to prove that diagnosis quickly.

That is the core issue to fix: the system needs stronger recovery semantics and better operator-facing diagnostics, so a date rerun behaves like a bounded repair task instead of a manual incident investigation.
