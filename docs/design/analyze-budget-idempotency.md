# Analyze Budget Idempotency

## Context

`run day`, `run week`, and `run month` are ensure/backfill workflows. They should
make the selected period complete enough for the configured workflow policy
without replaying expensive LLM work just because older backlog remains.

Today the analyze planner asks whether any item is still eligible for LLM
analysis in the day window. With triage enabled, a bounded day run can
intentionally leave `triaged` or `retryable_failed` items behind after consuming
`ANALYZE_LIMIT`. Treating that backlog as incomplete work makes the next
workflow run plan analyze again, which can also reactivate publish, trends, and
ideas.

## Decision

Analyze completion for workflow planning is budget-based, not backlog-based.

For a day window, a non-forced workflow should skip analyze when a previous
analyze attempt recorded a budget receipt for the same window and configuration
and selected at least the currently configured `ANALYZE_LIMIT` items. Remaining
eligible items are backlog metadata, not a default rerun trigger.

The receipt is a durable workflow-step record with:

- step id: `analyze`
- granularity: `day`
- period start and end
- config fingerprint
- requested limit
- selected, processed, and failed totals
- run id and creation time

The selected total is the budget-consumption signal. It includes items selected
for the analyze batch even when individual items fail and remain
`retryable_failed`. This keeps transient or content-quality backlog from causing
unbounded default workflow retries.

### Budget Configuration Identity

The receipt fingerprint is a versioned projection of Stage 4 semantics, not a
hash of the full application configuration. It includes:

- the effective analyze model, including a workflow model override;
- the LLM endpoint, output language, ordered user topics, and content character
  limit;
- the effective triage handoff gate (`TRIAGE_ENABLED` with non-empty `TOPICS`);
- the arXiv stored-content selection and fallback modes used by analyze;
- the derived source probe multiplier (the enabled-source count, capped at five)
  used by Stage 4 candidate loading and source rebalancing.

It intentionally excludes:

- `ANALYZE_LIMIT`, which is compared with the receipt `selected_total`;
- Stage 3.5 triage ranking parameters and source-pull limits, queries, URLs, and
  venues, whose output is the durable item-state handoff consumed by Stage 4;
- concurrency, persistence batch sizes, logs, debug artifacts, paths, workflow
  scheduling, email, publishing, localization, translation, trends, and RAG
  configuration.

Adding a new `Settings` field does not change analyze budget identity unless the
field is explicitly added to this projection with a schema-version decision.
The projection reads these runtime fields directly rather than trusting a full
settings serialization. For settings-like compatibility objects, it records
every readable Stage 4 field plus an explicit missing-field set, so a partial
serializer cannot hide a semantic change.
The fingerprint controls whether another backlog batch runs. It is not
item-level analysis freshness: changing topics, output language, content limits,
or prompt code does not by itself requeue already analyzed items.

For trusted production `Settings`, the planner continues to try legacy
fingerprint shapes for unchanged older configurations. It does not offer those
compatibility candidates for arbitrary settings-like objects or overridden safe
serializers, because an incomplete serialization could omit Stage 4 semantics
and incorrectly reuse a receipt. Legacy receipts contain only an opaque hash, so
a receipt written before an unrelated configuration change cannot be safely
reclassified and may cause one conservative extra analyze run before a projected
receipt is written.

## Rerun Policy

Default `run day|week|month` behavior:

- skip analyze when the matching receipt selected at least the current
  `ANALYZE_LIMIT`;
- run analyze when no matching receipt exists and candidate items are present;
- run analyze when the current `ANALYZE_LIMIT` is higher than the recorded
  selected total;
- report remaining eligible items as backlog metadata in the planner decision.

Explicit backlog processing remains available through lower-level commands and
repair/backfill paths. `stage analyze --date ... --limit ...` continues to be
the primitive for intentionally processing more items from a day backlog.

`--force` remains a generation force for trend and idea outputs. It does not
mean "reanalyze already-analyzed items" and does not by itself clear analyze
backlog. A separate repair or reprocess path should own that behavior if needed.

## Week And Month Workflows

Week and month workflows expand into day analyze invocations. Those day
invocations use the same budget receipt rule as `run day`. Therefore a completed
set of lower-level day runs remains trusted even when day backlog is still
present.

This matches the existing lower-granularity trend and idea rule: parent
workflows should not silently replay lower-level expensive work after that
lower-level task set has already run under the configured policy.

## Operational Notes

Planner JSON should expose:

- `reason: analyze_budget_satisfied` for skipped analyze decisions;
- the configured limit and matching receipt selected total;
- a bounded backlog summary, preferably by item state when the repository can
  compute it cheaply.

If budget receipts are unavailable, planner behavior falls back to candidate
inspection. That preserves compatibility for older repositories and lightweight
test doubles.
