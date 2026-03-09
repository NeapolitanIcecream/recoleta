---
title: "ADR 0027: Lightweight schema compatibility via SQLite user_version"
status: Accepted
---

## Context

Recoleta still initializes schema in a mostly ad hoc way. The project is early, so a full migration framework would be heavier than necessary, but silent schema drift is already too risky.

The immediate need is modest:

- know which schema the DB is using
- refuse incompatible states clearly
- support a small number of safe in-repo upgrades

The project does not yet need rollback support, migration history reporting, or cross-version compatibility guarantees.

## Decision

Use SQLite `PRAGMA user_version` as the schema compatibility marker for the current stage.

The application should maintain a single monotonically increasing schema version integer in code.

## Startup rules

When opening a database:

1. if the DB is empty, initialize schema and set `user_version` to the current version
2. if `user_version` matches the current version, continue normally
3. if `user_version` is older and every step to current is marked startup-safe, apply those steps in order and then bump the version
4. if `user_version` is newer than the application supports, fail closed with an explicit error
5. if `user_version` is older but requires a non-startup-safe rewrite, fail closed with an explicit error

The application should never silently guess how to handle an unknown schema state.

## Migration categories

Two categories are enough for the current stage.

### Startup-safe migration

Allowed examples:

- adding a table
- adding an index
- adding a nullable column
- idempotent metadata repair that does not rewrite large historical state

These may run automatically at startup under the workspace lease.

### Explicit migration

Examples:

- table rewrites
- heavy backfills
- destructive cleanup
- changes that materially rewrite historical stored data

These should not run automatically at startup in the current phase.

Until an explicit migration command exists, such cases should fail with a clear operator-facing message instead of attempting a risky best-effort upgrade.

## Backup policy

For the current phase:

- startup-safe migrations do not require automatic pre-backup
- explicit migrations, when introduced later, should be paired with a DB backup step

This keeps normal startup small while still preserving a path for safer future schema rewrites.

## Compatibility stance

The project should make these guarantees explicit:

- no downgrade support
- no forward compatibility with newer schema versions
- best-effort upgrade only for known older versions

This is appropriate for an early-stage single-user tool and is safer than pretending broader compatibility exists.

## Alternatives considered

### `schema_migrations` table

Deferred.

A dedicated table may become useful later, but `PRAGMA user_version` is simpler and already provided by SQLite.

### Alembic now

Rejected for now.

Alembic is mainstream and reasonable, but it adds more process and machinery than the current stage requires.

### Blind `create_all()` plus hand-written patches

Rejected.

It is too easy to drift into partially upgraded states without a clear compatibility contract.

## Consequences

Positive:

- adds a real compatibility boundary with almost no new machinery
- keeps migration logic small and in-repo
- avoids committing the project to a heavyweight migration framework too early

Tradeoffs:

- migration history is only an integer, not a full audit trail
- explicit migrations may need a dedicated command later
- older unsupported schemas will fail until the operator upgrades through a supported path or resets intentionally
