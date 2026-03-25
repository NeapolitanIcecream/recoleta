# Long-running Operations

Status: Accepted and implemented for the current stage

This document captures a pragmatic design for running Recoleta continuously over long periods. It is intentionally narrower than a full platform redesign. The goal is to make the existing single-user, local-first system safe to operate for months, while preserving the current CLI-first model.

## Current iteration assumptions

This design note is being iterated under four explicit assumptions:

- historical successful user-facing work is immutable by default
- SQLite remains the primary database for the current project stage
- built-in scheduling and external one-shot scheduling are both first-class
- migration strategy should stay lightweight while the project is still early

These assumptions are important because they rule out a large class of designs that would add complexity without matching current product expectations.

## Why this exists

Recoleta's long-running operating model is now implemented around a few concrete primitives:

- source-level deduplication, incremental ingest, and persisted pull state
- workflow and stage-separated commands (`run`, `daemon`, `stage`, `repair`)
- SQLite as the durable local index plus `PRAGMA user_version` compatibility checks
- a SQLite-backed workspace lease and run heartbeat for singleton writes
- maintenance and recovery commands (`admin gc`, `admin vacuum`,
  `admin backup`, `admin restore`)
- diagnostics and repair commands (`inspect health`, `inspect stats`,
  `inspect runs`, `inspect llm`, `inspect why-empty`, `repair streams`) plus a
  documented container contract

The remaining design questions are mostly about defaults and future policy, for example retention windows, cache pruning scope, and how much schema migration machinery the project should eventually adopt.

## Goals

- Keep the current single-machine, single-user shape.
- Make repeated scheduled execution safe and understandable.
- Preserve historical user expectations: old successful work should not replay automatically.
- Bound long-term storage growth with explicit retention rules.
- Add enough schema/version checking to fail safely instead of mutating blindly.
- Standardize deployment enough for cron/systemd/Docker without redesigning the app around containers.

## Non-goals

- Multi-user tenancy.
- Distributed workers or remote job queues.
- Replacing SQLite with a network database.
- Building a web admin console.
- Solving every future analytics need up front.
- Automatically reprocessing old successful history when prompts/models/config change.

## Design principles

- Prefer extending current stage boundaries over introducing a new execution model.
- Treat local CLI commands as the primitive. Scheduling is a wrapper around them.
- Keep "source identity", "historical result", and "rebuildable cache" as separate concerns.
- Classify data by whether it is authoritative or rebuildable.
- Add operational safety before adding deployment surface area.

## Operating model

Recoleta supports two long-running modes with the same execution semantics:

- built-in scheduler for local always-on usage
- external scheduler calling one-shot commands for cron/systemd/Docker-style environments

Neither mode is legacy or test-only. They serve different operator environments.

### Built-in scheduler mode

`recoleta daemon start` remains a valid primary entry point for local
long-running usage.

Current invariant:

- scheduler-driven stage execution obeys the same locking, diagnostics, and failure semantics as one-shot runs

### External scheduler mode

`recoleta run now` remains important, but it should be treated as the external
orchestration primitive rather than as a special testing path.

Typical uses:

- cron
- launchd / systemd timer
- Docker / Compose
- CI or other scheduled jobs

In practice, the primitive remains:

```bash
uv run recoleta run now
```

or explicit stage commands when the operator wants finer control.

### Single active writer

For one Recoleta workspace, there is at most one active write-capable process at a time. This applies whether the trigger is cron, systemd, Docker, or the built-in scheduler.

This is enforced by the SQLite-backed workspace lease described in ADR 0025.

## Design areas

### 1. Idempotency and rebuild policy

Current behavior is already good at deduplicating source items and preventing duplicate Telegram sends. The main missing question is not "how do we automatically recompute everything?" but rather:

- which stored outputs are historical facts?
- which stored outputs are rebuildable maintenance material?
- which operator actions should explicitly rebuild old state?

The guiding product rule for the current stage should be:

- successful user-facing historical work should not be replayed automatically

That means:

- do not automatically re-analyze already analyzed historical items because config changed
- do not automatically re-publish already delivered historical items
- do not surprise the user with a flood of old outputs after changing settings

Instead, Recoleta should expose explicit operator escape hatches for rebuilds or resets.

#### Two categories of stored results

Stored results should be split into two categories.

1. Historical user-facing results
   - item analyses that were already completed
   - publish decisions and deliveries
   - canonical trend notes once generated

2. Rebuildable maintenance material
   - document/chunk indices
   - vector indices
   - static site output
   - derived PDFs and debug bundles

The first category is append-only by default. The second category may be refreshed or rebuilt as needed.

#### Minimal freshness model

Freshness metadata is still useful, but only for the right classes of work.

Each rebuildable or in-progress stage should conceptually depend on two things:

- input fingerprint: the effective upstream data for this stage
- spec fingerprint: the behavior of the stage itself

Examples:

- analyze:
  - relevant mainly for pending/retryable work, not for replaying completed history by default
- publish:
  - relevant mainly for unpublished work
- trends:
  - useful for deciding whether derived non-canonical outputs need refresh
- RAG vectors:
  - input fingerprint: summary chunk text hash
  - spec fingerprint: embedding model + dimensions

The key point is not to drive automatic replay of old successful history. The key point is to stop treating every stored artifact as if it had the same rebuild policy.

#### Minimal implementation direction

The first documentation-backed design should aim for:

- preserve the current `items.state` flow for coarse progress tracking
- avoid automatic replay for already successful historical user-facing work
- support explicit reset/rebuild commands for operators
- add freshness metadata only where it helps maintain caches or pending work

This keeps the mental model simple and avoids introducing a general workflow engine.

### 2. Data lifecycle and retention

Not all stored data deserves the same retention policy.

Current selected direction for the first implementation slice:

- default GC only prunes debug material and operational history
- cache pruning stays explicit rather than automatic
- backup/restore is DB-scoped, not a full workspace snapshot

See `docs/adr/0026-retention-gc-and-db-scoped-backups.md` for the focused proposal.

#### Storage classes

Recoleta data should be treated as four classes:

1. Authoritative state
   - items
   - latest successful analyses per scope
   - deliveries / trend deliveries

2. Rebuildable cache
   - document index and chunks
   - LanceDB vectors
   - derived trend PDFs
   - static site output

3. Short-lived debug data
   - request/response artifacts
   - error context artifacts
   - PDF debug bundles

4. Operational history
   - runs
   - metrics

#### Proposed default retention

These are starting defaults, not hard product commitments:

- debug artifacts and PDF debug bundles: 14 days
- finished runs and per-run metrics: 60 days
- rebuildable caches: prune only through explicit cache-pruning mode

Authoritative state should be kept until explicitly deleted or superseded by a clear policy.

One important consequence of the current rebuild policy:

- retention and GC must not silently delete canonical user-facing history
- destructive cleanup should primarily target caches, debug material, and old operational history

#### Required operator tools

The design should converge on a small set of lifecycle commands:

- `recoleta gc`
  - prune expired artifacts
  - prune expired metrics/runs
  - support an explicit cache-pruning mode for vector tables and rebuildable trend index material
- `recoleta vacuum`
  - run SQLite maintenance after GC-heavy operations
- `recoleta backup`
  - create a timestamped SQLite backup plus a small manifest
- `recoleta restore`
  - restore from a backup bundle

The commands above are intentionally narrow. They are enough to make long-running storage manageable without introducing full archive infrastructure.

### 3. Migration strategy

ADR 0001 already notes that schema evolution needs a proper strategy. The current `init_schema()` approach is still transitional, but the current stage does not justify a full migration framework yet.

Current selected direction for the first implementation slice:

- use SQLite `PRAGMA user_version`
- allow only startup-safe automatic upgrades
- fail closed on newer or rewrite-heavy schemas

See `docs/adr/0027-lightweight-schema-compatibility-via-user-version.md` for the focused proposal.

The minimal migration design should therefore be:

- a schema version marker inside SQLite
- startup checks that refuse obviously incompatible states
- clear operator-facing errors instead of silent best-effort mutation
- optional pre-change backup before risky schema rewrites

Explicitly deferred for now:

- full migration framework
- down migrations
- cross-version rolling compatibility
- a separate migration service

If Alembic is adopted later, it should be because the schema has genuinely grown beyond a lightweight in-repo approach, not because the project wants premature formality.

### 4. Runtime safety

Long-running safety is part of the current deployment model rather than a future prerequisite.

Current implementation:

- use a SQLite-backed workspace lease for singleton writes
- add `runs.heartbeat_at` and derive stale runs from heartbeat age

See `docs/adr/0025-sqlite-lease-and-run-heartbeat.md` for the focused proposal.

#### Singleton protection

Recoleta uses a workspace-level SQLite lease so that only one write-capable process can run against the same database and output roots at a time.

Requirements:

- lock ownership must be visible in diagnostics
- stale locks must be recoverable
- `run now`, date-scoped workflow commands, stage commands, and the built-in
  scheduler should all use the same mechanism

#### Run heartbeat

`runs` should distinguish:

- running and healthy
- running but stale
- succeeded
- failed

The minimal addition is a heartbeat timestamp updated during long-running stages or between stage boundaries. This gives operators and future health checks a reliable signal.

#### Recovery semantics

If a process dies unexpectedly:

- the run should eventually be marked stale/failed
- a later invocation should be able to acquire the lock after a timeout or explicit override
- retryable item states should continue to work as they do now

### 5. Deployment shape

Deployment follows the operating model rather than defining it.

Current implementation:

- support one Dockerfile with `runtime` and `runtime-full` targets
- standardize example container paths under `/data` and `/config`
- add a read-only `inspect health --healthcheck` contract

See `docs/adr/0028-container-deployment-and-healthcheck-contract.md` for the focused proposal.

#### Supported deployment targets

The design should explicitly support:

- local `uv run`
- cron / launchd / systemd timer
- Docker / Compose

SQLite remains compatible with this deployment set as long as the system maintains a single active writer per workspace.

#### Docker stance

Docker should package the current CLI model rather than introduce a new runtime model.

Recommended container contract:

- command runs one CLI invocation and exits, or runs the built-in scheduler explicitly
- persistent volumes for:
  - SQLite DB
  - markdown outputs
  - debug artifacts
  - LanceDB
  - config

This allows the same runtime semantics across local shells, timers, and containers.

#### Health and diagnostics

Operators should be able to answer these questions quickly:

- can the process read config and write to the DB?
- is another instance holding the lock?
- when was the last successful run?
- is backlog growing unexpectedly?
- are storage directories growing unexpectedly?

Recoleta exposes two small operator-facing interfaces for this:

- `recoleta inspect health`
- `recoleta inspect stats --json`
- `recoleta inspect runs show` / `recoleta inspect runs list`
- a container/system healthcheck command built on the same checks

Targeted recovery remains separate from the read-only checks:

- `recoleta repair streams --date ... --streams ...` repairs explicit
  stream-analysis state for one UTC day without introducing a general rerun
  workflow engine.

## Dependency stance

Long-running operations should stay conservative about new dependencies.

Preference order:

- use the standard library when it is sufficient
- reuse existing dependencies when they already solve the problem cleanly
- add one focused dependency only when it clearly replaces fragile custom code

This keeps the design aligned with the project's current size and with the requirement to avoid both needless wheel-reinvention and overly heavy stacks.

## Phased rollout

To avoid overdesign, implementation should be staged.

### Phase 0: Design and terminology

- agree on the long-running operating model
- define storage classes and retention defaults
- define the current rebuild policy explicitly

### Phase 1: Runtime safety

- singleton lock
- run heartbeat
- stale-run detection and recovery rules

This is the highest-value first implementation slice.

### Phase 2: Data lifecycle

- retention config
- `gc` and `vacuum`
- backup/restore
- vector table pruning

### Phase 3: Lightweight schema safety

- schema version marker
- incompatibility checks
- minimal backup-before-change behavior

### Phase 4: Packaging and operator UX

- official Dockerfile(s)
- Compose example
- `inspect health` command
- `inspect runs` inspection commands
- targeted repair helpers such as `repair streams`
- documented healthcheck contract

## Implementation workstreams

With ADRs 0025 through 0028 in place, implementation can now be split into a few bounded workstreams.

### Workstream A: runtime core

Status: completed

Scope:

- workspace lease
- run heartbeat
- stale-run recovery
- schema version plumbing

Why this should land first:

- it defines the DB/runtime primitives used by other write-capable commands

### Workstream B: lifecycle tools

Status: completed

Scope:

- `gc`
- `vacuum`
- `backup`
- `restore`

Parallelization note:

- design is independent now
- code can start in parallel with Workstream A
- final merge should expect small rebases onto the lease/schema primitives from Workstream A

### Workstream C: packaging and operator diagnostics

Status: completed

Scope:

- Dockerfile targets
- Compose example
- `doctor`
- healthcheck command contract

Parallelization note:

- packaging work can proceed mostly in parallel
- final healthcheck behavior should align with lock and schema checks from Workstream A

### Workstream D: follow-up polish

Status: completed

Scope:

- retention config exposure, if still needed after defaults ship
- richer operator stats
- more opinionated deployment recipes

Outcome:

- `inspect health`, `inspect stats`, and `inspect runs` now provide the
  intended lightweight operator surface
- `inspect why-empty` and `inspect llm` cover the two most common
  incident-response questions
- `repair streams` provides a bounded write-capable repair path without adding
  a top-level rerun orchestrator
- deployment recipes are documented for cron/systemd/containers
- retention defaults remain internal on purpose for now

Deferred from this workstream:

- user-facing retention knobs until operators actually need them

## Deferred decisions

These should stay out of scope until the earlier phases exist:

- replacing the current state machine with a generalized job graph
- changing away from SQLite
- remote queue workers
- object storage for artifacts
- multi-node coordination
- keeping unlimited historical analysis versions by default

## Open questions for iteration

- Which retention windows should be defaults versus opt-in settings?
- Should lease timings remain internal defaults, or become user-facing settings later?
- Should Docker support ship before or after runtime locking and heartbeat exist?
- How much schema checking is enough before a full migration framework becomes justified?

## Immediate next documents

This document is meant to be the parent design note. The first focused ADR set for implementation planning is now:

- `docs/adr/0025-sqlite-lease-and-run-heartbeat.md`
- `docs/adr/0026-retention-gc-and-db-scoped-backups.md`
- `docs/adr/0027-lightweight-schema-compatibility-via-user-version.md`
- `docs/adr/0028-container-deployment-and-healthcheck-contract.md`
