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

