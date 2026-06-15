# Translate Force Scope

Status: Accepted and implemented

## Context

`run translate` is the standalone translation workflow. Before this change it
accepted `--granularity`, `--include`, `--limit`, and `--force`, but it did not
accept a date or period window.

The translation runtime already supports bounded windows through
`period_start`, `period_end`, and `all_history`. Workflow commands such as
`run day --date 2026-03-16` use that path and pass `all_history=False` for the
target window. The standalone command did not, so it fell through to the
runtime default of `all_history=True`.

That default is especially risky with `--force`: force disables source-hash
skipping, so a command that looks like a scoped rerun can rewrite every
historical candidate that matches the selected surfaces and granularity.

## Decision

`run translate`, `stage translate run`, and the hidden legacy `translate run`
now accept the same scope controls:

- `--date <YYYY-MM-DD|YYYYMMDD>`
- `--period-start <ISO date or datetime>`
- `--period-end <ISO date or datetime>`
- `--all-history`

`--force` requires either a bounded window or explicit `--all-history`.

The command rejects ambiguous scope combinations:

- `--all-history` cannot be combined with `--date` or a period window.
- `--date` cannot be combined with `--period-start/--period-end`.
- `--period-start` and `--period-end` must be provided together.
- `--period-start` must be before `--period-end`.

`--date` derives a UTC window from `--granularity`:

- no granularity or `--granularity day`: the UTC day containing the date
- `--granularity week`: the ISO week containing the date
- `--granularity month`: the calendar month containing the date

Date-derived windows are deliberately simple. They match the existing
workflow-period helpers and avoid adding a separate date parser or calendar
policy for translation.

## Compatibility

Non-forced `run translate` without a window keeps the existing full-history
default. This preserves the established "fill missing translations" behavior.

The safety change is limited to forced unbounded reruns. Operators who really
want to retranslate all historical candidates can still do so with:

```bash
uv run recoleta run translate --force --all-history
```

For bounded forced reruns, the intended forms are:

```bash
uv run recoleta run translate --force --granularity day --date 2026-03-16
uv run recoleta run translate --force --period-start 2026-03-16 --period-end 2026-03-17
```

## Granularity Is Not A Date Filter

`--granularity` selects trend and idea documents with a matching granularity
value. It does not select a date or historical period. Item translations are not
granularity-scoped at all.

Window options are the only scope controls that bound historical candidates by
time. Help text now calls this out because the old wording implied that
`--granularity day` selected a single day.

## Observability

The resolved scope is visible in machine-readable output for JSON runs:

- `period_start`
- `period_end`
- `all_history`

The run context also records `period_start` and `period_end` when a bounded
translation run starts, matching the existing workflow run-context model.

No new metric is added. Existing translation counters still report scanned,
translated, skipped, failed, and billing totals for the resolved scope.

## Tests

Regression tests cover the user-visible contracts:

- forced standalone translation without a window is rejected before runtime
  setup;
- forced translation with `--date` passes a bounded window to the runner;
- forced translation with `--all-history` remains possible;
- mutually exclusive scope options fail closed;
- public v2 routes forward the new scope options to the shared helper.
