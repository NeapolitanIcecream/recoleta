---
title: "ADR 0028: Container deployment and healthcheck contract"
status: Accepted
---

## Context

Recoleta is currently easy to run from source, but it does not yet have an official container contract. That makes repeatable deployment harder than it should be for cron-like environments, home servers, and simple Compose setups.

The deployment goal is not to turn Recoleta into a service platform. The goal is to package the existing CLI model in a mainstream, low-friction way.

## Decision

Define an official container contract that preserves the CLI-first operating model.

The contract should support:

- local `uv run`
- host scheduling with `run --once`
- containerized `run --once`
- containerized built-in scheduler via `recoleta run`

Neither internal nor external scheduling is treated as second-class.

## Image shape

Use one Dockerfile with two runtime targets:

- `runtime`: core CLI image
- `runtime-full`: extends `runtime` with the heavier browser/PDF-related system dependencies needed for richer trend surfaces

This keeps the default image lighter while avoiding a fragmented packaging story.

## Container process model

One container should run one Recoleta command.

Examples:

- `recoleta run`
- `recoleta run --once`
- `recoleta trends`
- `recoleta site build --input-dir ... --output-dir ...`

The container should not introduce extra supervisors, sidecars, or background daemons as part of the base contract.

## Filesystem contract

The recommended container layout is:

- `/data/recoleta.db`
- `/data/outputs/`
- `/data/artifacts/`
- `/data/lancedb/`
- `/config/recoleta.yaml`

Mapped through existing settings such as:

- `RECOLETA_DB_PATH=/data/recoleta.db`
- `MARKDOWN_OUTPUT_DIR=/data/outputs`
- `ARTIFACTS_DIR=/data/artifacts`
- `RAG_LANCEDB_DIR=/data/lancedb`
- `RECOLETA_CONFIG_PATH=/config/recoleta.yaml`

Operators may still choose different paths, but the official examples should standardize on this contract.

## Healthcheck contract

Add a lightweight diagnostic entry point:

- `recoleta doctor`

And a non-invasive mode intended for container or supervisor health checks:

- `recoleta doctor --healthcheck`

The healthcheck path should:

- validate config loading
- verify required paths are accessible
- verify the DB can be opened
- verify schema compatibility
- read lock/run metadata without taking the write lease

Optional staleness thresholds such as "last successful run is too old" are supported as healthcheck flags rather than being hard-coded into the default contract.

## Scheduling examples

The official docs should show two mainstream deployment patterns:

1. Long-running scheduler container
   - `recoleta run`

2. One-shot execution under an external scheduler
   - `recoleta run --once`

The product should support both cleanly rather than forcing all operators into one pattern.

## Relationship to runtime safety

Container support depends on the runtime safety model from ADR 0025.

If two containers point at the same workspace:

- one may acquire the lease
- the other should fail fast with a lock-contention error

This is acceptable and easier to reason about than pretending multi-writer operation is supported.

## Alternatives considered

### A single heavyweight image only

Rejected.

That would be simpler to explain, but it would impose browser/PDF system dependencies on users who only need core CLI behavior.

### No official image, source-only installs

Rejected.

That keeps maintenance low for the project, but shifts too much friction onto operators and makes reproducible deployment harder than necessary.

### External scheduler only

Rejected.

The built-in scheduler remains useful for local always-on usage and should continue to be supported.

## Consequences

Positive:

- clearer operator story across laptops, home servers, and Compose
- packaging stays aligned with the existing CLI model
- lighter default image without losing a path for richer rendering features

Tradeoffs:

- two image targets add some packaging maintenance
- healthcheck semantics must stay read-only and aligned with the runtime lock model
- official examples will need to document both scheduler styles without confusing users
