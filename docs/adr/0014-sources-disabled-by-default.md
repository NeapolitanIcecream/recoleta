# ADR 0014: Sources disabled by default

- Status: Accepted
- Date: 2026-02-28

## Context
Recoleta previously pulled some sources implicitly (e.g. HN RSS had a non-empty default URL), which could surprise users and made it easy to run ingestion unintentionally.

## Decision
All sources are disabled by default. Each source must be explicitly enabled via `sources.<name>.enabled: true`. If a source block is configured without `enabled=true`, Recoleta fails fast with a clear error message.

## Consequences
Users get a simpler mental model: “nothing runs unless I turn it on”. Example configs must include explicit `enabled` flags. Existing configs need a one-time update to add `enabled: true` for desired sources.
