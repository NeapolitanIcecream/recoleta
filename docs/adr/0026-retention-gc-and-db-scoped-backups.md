---
title: "ADR 0026: Retention, garbage collection, and DB-scoped backups"
status: Accepted
---

## Context

Recoleta can run for months, but storage growth is currently mostly unbounded.

The main growth sources are:

- debug artifacts
- per-run metrics
- finished run history
- trend PDF debug bundles
- rebuildable vector indices

At the same time, the current product rule is that successful historical user-facing work should not be replayed automatically. That means cleanup must not silently delete the canonical history that the user expects to persist.

The project needs small operator tools, not a generalized archive platform.

## Decision

Adopt a conservative lifecycle policy with three narrow maintenance commands:

- `recoleta gc`
- `recoleta vacuum`
- `recoleta backup`

Add `recoleta restore` only as the inverse of the DB-scoped backup bundle. Do not expand it into a full workspace snapshot system in this phase.

All four commands should use the same workspace write lease defined by ADR 0025.

## Storage classes

Long-running data should be treated as four classes:

1. Authoritative history
   - items
   - analyses
   - deliveries
   - canonical trend documents

2. Rebuildable cache
   - document index and chunks
   - LanceDB vector tables
   - derived trend PDFs
   - static site build output

3. Debug material
   - debug artifacts
   - PDF debug bundles

4. Operational history
   - runs
   - metrics

## Cleanup policy

`recoleta gc` should be conservative by default.

Default scope:

- prune expired debug material
- prune expired operational history

Default non-scope:

- do not delete authoritative history
- do not delete canonical markdown outputs
- do not delete rebuildable caches unless explicitly requested

This keeps the default command safe enough to run routinely.

## Initial retention defaults

Use simple built-in defaults for the first phase:

- debug artifacts and PDF debug bundles: 14 days
- finished runs and per-run metrics: 60 days

These defaults should stay internal at first rather than immediately becoming a wide configuration surface.

## Explicit cache pruning

Rebuildable caches should be pruned only through an explicit mode such as:

- `recoleta gc --prune-caches`

This mode may remove:

- document index and chunks that are marked rebuildable maintenance material
- inactive LanceDB tables that do not match the current active embedding configuration
- derived trend PDFs
- managed static-site build output

It must not remove:

- canonical markdown trend notes
- item notes under the main markdown output tree

This split balances bounded storage with predictable behavior. Expensive-but-rebuildable caches remain operator-controlled instead of being deleted implicitly.

## GC UX

`recoleta gc` should support:

- a dry-run mode
- per-class counters in output
- a concise summary of deleted DB rows and deleted filesystem paths

The goal is not a full admin console. The goal is to make cleanup auditable and safe.

## Vacuum

`recoleta vacuum` remains a separate command.

Reasons:

- SQLite `VACUUM` can be slow
- operators may want to run it after large cleanup windows, not after every GC
- keeping it separate makes routine GC cheaper and less surprising

## Backup and restore scope

The first backup contract is intentionally narrow.

`recoleta backup` should create:

- a timestamped SQLite backup file
- a small manifest with metadata such as creation time and schema version

`recoleta restore` should restore only from that DB bundle.

This phase does not promise:

- a full workspace snapshot
- snapshotting markdown outputs
- snapshotting artifacts or LanceDB directories

If operators want full filesystem recovery, they should use normal filesystem backup tooling on top of the workspace directories.

## Alternatives considered

### Automatically pruning caches in default GC

Rejected for now.

Caches are rebuildable, but some of them are expensive enough that silent deletion would be surprising. The first phase should make low-risk cleanup routine and make high-cost cleanup explicit.

### Full workspace backup bundles

Rejected for now.

The project does not yet need a full snapshot/archive product. A DB-scoped backup is enough to support schema changes and basic disaster recovery for the state store.

### Making retention windows user-facing settings immediately

Deferred.

The first phase should establish policy and commands before introducing a broader config matrix.

## Consequences

Positive:

- safe default cleanup path
- storage growth becomes manageable without touching historical user-facing records
- backup/restore remains small enough to implement and explain

Tradeoffs:

- caches may still grow until operators opt into cache pruning
- DB-only restore does not reconstruct markdown outputs or artifacts
- some operators may still prefer external filesystem backup for full recovery
