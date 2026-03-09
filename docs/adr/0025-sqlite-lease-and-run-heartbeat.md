---
title: "ADR 0025: SQLite lease and run heartbeat for singleton writes"
status: Accepted
---

## Context

Recoleta already records `runs`, but it does not yet prevent overlapping write-capable commands across processes.

Today:

- built-in scheduler settings such as `max_workers=1` and `max_instances=1` only protect one APScheduler process
- separate `recoleta run`, `run --once`, cron jobs, or multiple containers can still overlap against the same workspace
- `runs` only stores `started_at`, `finished_at`, and `status`, so a crash can leave `status=running` forever

The project is still single-user, local-first, and SQLite-backed. This phase should improve runtime safety without introducing a heavyweight coordination system.

## Decision

Use a SQLite-backed workspace lease plus run heartbeats as the minimal runtime safety model.

The design for this phase is:

- keep one write lease per workspace
- require all write-capable commands to acquire that lease before doing work
- keep the lease only for the duration of the active command, not for the idle lifetime of `recoleta run`
- generate `run_id` before lease acquisition so lock diagnostics can include the incoming run without creating orphan `runs` rows
- extend `runs` with `heartbeat_at`
- treat stale runs as a derived condition, not as a new persisted status

This keeps the design aligned with the existing SQLite-first architecture and avoids adding a new runtime dependency by default.

## Command scope

The lease should guard write-capable commands:

- `recoleta ingest`
- `recoleta analyze`
- `recoleta publish`
- `recoleta trends`
- `recoleta site`
- `recoleta run --once`
- scheduler-fired stage jobs inside `recoleta run`

Read-only diagnostic commands should not need the lease.

The built-in scheduler should not hold the lease while it is idle between intervals. Each scheduled job should acquire and release the same workspace lease independently.

## Lease shape

One workspace-level lease row is enough for the current stage.

The row should store enough data for both correctness and diagnostics:

- `name`
- `owner_token`
- `run_id`
- `pid`
- `hostname`
- `command`
- `acquired_at`
- `heartbeat_at`
- `expires_at`

`owner_token` should be an opaque random value used for compare-and-swap renewal. This prevents an old process from silently renewing a lease after another process has already taken it over.

## Run heartbeat

`runs` should gain a `heartbeat_at` timestamp.

The persisted run states remain:

- `running`
- `succeeded`
- `failed`

Staleness should be derived from:

- `status == running`
- `heartbeat_at` older than the lease timeout

This is enough for operator diagnostics without expanding the state model prematurely.

## Timing defaults

The initial timing defaults should stay simple:

- heartbeat interval: 15 seconds
- lease timeout: 90 seconds

Rationale:

- short enough to recover within a couple of minutes after a crash
- long enough to tolerate brief pauses and transient SQLite contention

These values can remain internal defaults for now instead of becoming user-facing config immediately.

## Renewal model

Lease renewal and run heartbeat should happen from the same periodic mechanism.

The intended behavior is:

- while a command is active, periodically update both the lease row and `runs.heartbeat_at`
- renewal succeeds only if `owner_token` still matches
- if renewal fails because ownership changed, the process should stop at the next safe check and treat the run as interrupted

Using one mechanism for both signals keeps the implementation smaller and avoids divergent health semantics.

## Recovery semantics

When a new process starts:

- if the lease is absent, it acquires it
- if the lease is present and unexpired, it exits with a lock-contention error that includes visible owner metadata
- if the lease is expired, it may take over

On successful takeover of an expired lease, the new process should mark stale `running` runs older than the timeout as failed before continuing.

This gives operators a clear story:

- a live owner blocks a second writer
- a dead owner is eventually recoverable
- stale runs do not remain `running` forever

## Alternatives considered

### File lock via `filelock`

This remains an acceptable fallback, but it is not the default direction for this phase.

Reasons to prefer the SQLite lease first:

- no new runtime dependency
- ownership metadata lives in the same durable store already used for runs
- stale-run recovery logic naturally lives next to run metadata

Revisit `filelock` only if the SQLite lease proves harder to operate correctly than expected.

### Holding the lease for the full lifetime of `recoleta run`

Rejected.

The scheduler should be free to sit idle without blocking ad hoc commands for long periods. The lock should cover active work, not process presence.

### Adding a persisted `stale` run status

Rejected for now.

A derived stale condition is sufficient at the current stage and keeps the data model simpler.

## Consequences

Positive:

- one coordination model across built-in scheduling and external orchestration
- no new runtime dependency by default
- operator-visible ownership and stale-run recovery

Tradeoffs:

- requires a small schema change and lease-management code
- laptop sleep or long pauses can legitimately expire a lease and interrupt an in-flight run
- correct renewal requires careful compare-and-swap semantics

## Follow-up implications

This ADR does not by itself decide:

- whether lease acquisition uses raw SQL or a repository helper API
- whether SQLite pragmas such as `busy_timeout` should be tuned at the same time
- whether lock diagnostics should surface through `doctor`, CLI stderr, or both

Those are implementation details or nearby follow-up decisions, not part of the core direction here.
