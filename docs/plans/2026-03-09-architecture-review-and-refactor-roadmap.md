# Architecture Review And Refactor Roadmap

Date: 2026-03-09

## Scope

This note reviews the architecture that exists in code today, not just the intended architecture in ADRs and design docs. The goal is to decide whether Recoleta should take a breaking refactor, and if not, what a safer refactor sequence looks like.

## Executive Summary

Recommendation: do a staged internal refactor, not a big-bang rewrite.

Why:

- The system already has a clear runtime model and stage boundaries in docs.
- The repository has broad behavioral test coverage, which makes stable external behavior an asset.
- The main problem is not that the architecture is directionally wrong; it is that several modules have become concentration points for too many responsibilities.

This means the highest-return move is to split implementation units while preserving existing user-facing contracts:

- CLI command names and semantics
- configuration shape
- SQLite state machine and schema compatibility rules
- Markdown/trend output layout
- Telegram idempotency behavior

Breaking changes should be deferred until after the codebase has been decomposed enough to expose which contracts are truly wrong versus merely hard to maintain.

## Status Update

Status as of 2026-03-09 after the first refactor wave:

- Phase 0 is complete.
- Phase 1 is complete.
- Phase 2 is partially complete.
- Phase 3 is largely complete.
- Phase 4 is partially complete.
- Phase 5 is partially complete.

Validated on the current tree with:

- `uv run pyright recoleta`
- `uv run pytest -q`

Latest verification result at update time:

- `209 passed`
- no new type errors

In practical terms, the roadmap is now mostly achieved for the first-wave goals and for the main package-direction changes:

- `recoleta.publish`, `recoleta.pipeline`, `recoleta.storage`, `recoleta.cli`, and `recoleta.app` now exist as real packages
- the old top-level entry modules are compatibility shims or thin facades
- site rendering depends on shared publish helpers instead of private publish internals
- trend and RAG code now depend on `TrendRepositoryPort` rather than concrete `Repository`

What is still not fully at the target shape:

- `recoleta/pipeline/service.py` still contains a large `PipelineService` implementation and has not yet been split into topic-stream, artifact, and metrics collaborators
- `recoleta/storage/facade.py` is still broader than the eventual `schema/runs/leases/analyses/deliveries/maintenance` split
- `recoleta/cli/__init__.py` still hosts most command wiring instead of command-area modules
- `ScopedTrendsRepository` still exists inside `recoleta/pipeline/trends_stage.py`
- `PublishRepositoryPort` and `AnalysisRepositoryPort` have not been introduced as separate real ports yet

## Current State

### What is working

The intended architecture is coherent:

- `ingest` is the durable prepare boundary
- `analyze` is the compute-only LLM boundary
- `publish` is a delivery boundary
- `trends` is its own synthesis flow over item and trend documents

This aligns with:

- `docs/design/architecture.md`
- `docs/adr/0009-split-prepare-and-analyze.md`
- `docs/adr/0021-pydanticai-for-trend-tool-calling.md`

Several modules are still reasonably cohesive and should not be early refactor targets:

- `recoleta/analyzer.py`
- `recoleta/triage.py`
- `recoleta/delivery.py`
- most of `recoleta/config.py`

### What is drifting

The implementation has started to accumulate cross-cutting logic inside a few large modules:

- `recoleta/pipeline.py` is both orchestrator and feature host
- `recoleta/storage.py` is both repository and operational subsystem
- `recoleta/publish.py` is both note writer and rendering stack
- `recoleta/site.py` depends on private helpers from `recoleta/publish.py`

Large files alone are not the problem. The problem is that these files combine concerns that change for different reasons.

## Concrete Findings

### 1. `PipelineService` is the main architectural hotspot

`recoleta/pipeline.py` is the strongest signal that the code wants more modules.

Observed responsibilities inside one class:

- topic stream runtime derivation
- Telegram sender creation and per-stream rate budgeting
- ingest orchestration
- enrich orchestration and content fetching policy
- triage orchestration
- analysis orchestration
- publish orchestration
- trend generation orchestration
- debug artifact writing
- error sanitization and classification
- stream-scoped metrics naming

The constructor already shows this spread by building topic stream runtime defaults, LLM connection state, triage service, Telegram senders, and log scrubbing inputs in one place.

Strong refactor signals:

- `publish()` and `_publish_topic_streams()` duplicate the same delivery workflow with only scope differences.
- `trends()` owns indexing, backfill control flow, corpus readiness checks, trend generation, persistence, PDF export, and metrics.
- `_ScopedTrendsRepository` exists as an adapter inside `pipeline.py`, which is a sign that trends needs a dedicated boundary but does not have one yet.

Verdict: this file should be split first.

### 2. `Repository` is too broad even if SQLite remains the right backend

`recoleta/storage.py` is not just a repository. It currently owns:

- schema version checks and startup-safe migrations
- workspace lease control
- run lifecycle and heartbeats
- metrics persistence
- item/content/analysis CRUD
- per-stream state management
- deliveries and trend deliveries
- document and chunk indexing
- embedding rows
- artifact pruning
- operational history pruning
- database backup and restore
- vacuum

These are valid capabilities for the application, but they are not one cohesive abstraction.

The main issue is organizational, not conceptual. SQLite can remain the truth source. The code should be decomposed into repository slices behind a stable facade first.

Verdict: split internally before changing any storage contract.

### 3. Publishing and rendering concerns are entangled

`recoleta/publish.py` currently mixes:

- item note pathing and note writing
- trend note writing
- Markdown-to-HTML helper logic
- Telegram text formatting
- trend PDF section extraction
- browser PDF rendering
- Story/PyMuPDF fallback rendering
- PNG/asset generation for rendering
- debug bundle export

This file is large because it contains two different product surfaces:

- persisted canonical notes
- derived delivery/rendering artifacts

Those should not live in the same module.

Verdict: split by output concern, especially around trend PDF rendering.

### 4. `site.py` has the wrong dependency direction

`recoleta/site.py` imports multiple private helpers from `recoleta/publish.py`.

That means site generation currently depends on internals of the publishing implementation instead of on a shared rendering boundary. This is a classic sign that reusable rendering utilities should move into a dedicated module.

Verdict: extract shared trend HTML/render helpers and make both publish and site depend on them.

### 5. Ports exist, but concrete dependencies still leak through

`recoleta/ports.py` defines only a partial `RepositoryPort`. That is useful, but the architecture does not consistently stop at the port boundary.

Examples:

- `recoleta/trends.py` depends on `Repository` directly
- `recoleta/rag/agent.py` depends on `Repository` directly
- `_ScopedTrendsRepository` in `recoleta/pipeline.py` uses `__getattr__` passthrough

This means the code has architectural intent but not yet an enforced dependency rule.

Verdict: add narrower ports after service extraction, not before.

### 6. `cli.py` is large, but it is not the first problem to solve

`recoleta/cli.py` is big because it includes:

- lazy imports and runtime wiring
- command definitions
- managed run and workspace lease handling
- maintenance helpers
- scheduler glue

This is worth splitting, but it is less risky than `pipeline.py` and `storage.py`. The current lazy-import strategy is also deliberate and should be preserved unless it is proven harmful.

Verdict: refactor later than pipeline/storage/publish.

## Modules That Are Already Fairly Cohesive

These should mostly be left alone during the first pass:

- `recoleta/analyzer.py`
  - focused on LLM request/validation/retry behavior
- `recoleta/triage.py`
  - focused on scoring and selection strategy
- `recoleta/delivery.py`
  - focused on Telegram transport and retries
- `recoleta/config.py`
  - large, but still mostly about settings normalization and validation

The right strategy is to move orchestration around these modules, not rewrite them.

## Recommended Refactor Strategy

### Principle

Refactor by change axis, not by file size.

Good splits:

- orchestration versus execution
- canonical content generation versus derived delivery rendering
- runtime coordination versus domain persistence
- stream scoping versus base stage logic

Bad splits:

- arbitrary line-count cuts
- introducing ports everywhere before responsibilities are isolated
- changing configuration or schema semantics during the first decomposition pass

## Proposed Target Shape

One workable end state is:

```text
recoleta/
  app/
    runtime.py
    managed_run.py
    scheduler.py
  cli/
    ingest.py
    analyze.py
    publish.py
    trends.py
    db.py
    site.py
  pipeline/
    service.py
    topic_streams.py
    artifacts.py
    metrics.py
    ingest_stage.py
    enrich_stage.py
    triage_stage.py
    analyze_stage.py
    publish_stage.py
    trends_stage.py
  publish/
    item_notes.py
    trend_notes.py
    telegram_format.py
    trend_render_shared.py
    trend_pdf_browser.py
    trend_pdf_story.py
    trend_pdf_debug.py
  storage/
    facade.py
    schema.py
    runs.py
    leases.py
    items.py
    analyses.py
    deliveries.py
    documents.py
    maintenance.py
  ports/
    repository.py
    trends.py
    publish.py
```

This does not need to happen in one branch or one release. It is a direction for progressive extraction.

Current implementation status against this shape:

- `app/`: mostly aligned
  - `runtime.py` and `managed_run.py` exist
  - `scheduler.py` has not been split out
- `cli/`: partially aligned
  - package exists
  - command modules by area do not yet exist
- `pipeline/`: partially aligned
  - package exists
  - `publish_stage.py` and `trends_stage.py` exist
  - `service.py` now hosts the real `PipelineService` implementation
  - `__init__.py` is now only package export glue
- `publish/`: largely aligned
  - package exists
  - item notes, trend notes, Telegram formatting, shared rendering, and PDF rendering are split out
  - browser/story/debug PDF internals are not yet split into separate modules
- `storage/`: partially aligned
  - package exists with `facade.py`, `common.py`, `runtime.py`, `items.py`, and `documents.py`
  - `schema.py`, `runs.py`, `leases.py`, `analyses.py`, `deliveries.py`, and `maintenance.py` are not yet separated
- `ports/`: partially aligned in intent, not in package shape
  - `TrendRepositoryPort` exists in `recoleta/ports.py`
  - the ports package split and additional narrow ports are still pending

## Phased Roadmap

### Phase 0: Freeze External Contracts

Status: complete.

Before large refactors, explicitly treat these as stable:

- CLI command names and flags
- config file fields and environment variable names
- schema compatibility and startup-safe migration policy
- item state and stream state transitions
- markdown output folder structure
- trend note frontmatter contract
- delivery idempotency behavior

Deliverables:

- architecture note
- explicit refactor checklist
- targeted regression tests for the most fragile seams if coverage is thin there

### Phase 1: Split `publish.py`

Status: complete.

This is the cleanest first extraction because it is mostly internal structure work.

Extract:

- item note writing
- trend note writing
- Telegram message formatting
- shared trend HTML helpers
- browser PDF renderer
- Story/PyMuPDF renderer
- PDF debug bundle export

Expected outcome:

- `site.py` no longer imports private helpers from `publish.py`
- canonical note generation is visibly separate from delivery rendering

Do not change:

- note paths
- note content contract
- PDF output naming

### Phase 2: Split `PipelineService` by stage

Status: partial.

Keep a thin `PipelineService` facade so the CLI and tests do not need to move all at once.

Extract services:

- `PrepareService`
- `AnalyzeService`
- `PublishService`
- `TrendService`
- `TopicStreamCoordinator`
- `ArtifactRecorder`
- `PipelineMetrics`

Expected outcome:

- stream-specific logic no longer duplicates whole stage flows
- `publish()` and `_publish_topic_streams()` collapse into shared stage code plus scope configuration
- `trends()` becomes orchestration over dedicated trend collaborators

Do not change:

- stage semantics
- run-level metrics names unless necessary
- failure classification behavior

Current status note:

- publish-stage and trends-stage logic have been extracted into dedicated modules
- a thin external `recoleta.pipeline` facade is preserved for compatibility
- the remaining `PipelineService` implementation is still too concentrated and has not yet been split into topic-stream, artifact, and metrics collaborators

### Phase 3: Split `Repository` internally

Status: largely complete.

Keep `Repository` as a facade initially. Move implementation into focused collaborators.

Suggested slices:

- `RunStore`
- `LeaseStore`
- `ItemStore`
- `AnalysisStore`
- `DeliveryStore`
- `DocumentStore`
- `MaintenanceStore`

Expected outcome:

- migrations and operational maintenance stop living next to item persistence logic
- tests can target narrower subsystems
- later port extraction becomes simpler and more honest

Do not change:

- DB schema
- transaction semantics
- migration behavior

Current status note:

- the repository now has a stable facade with internal `runtime`, `items`, and `documents` modules
- the storage package shape is real, but operational concerns are not yet fully split into narrower files

### Phase 4: Introduce real narrow ports

Status: partial.

After the services and repository internals are split, define ports around actual usage patterns.

Examples:

- `AnalysisRepositoryPort`
- `PublishRepositoryPort`
- `TrendRepositoryPort`

At that point:

- `trends.py` should not need concrete `Repository`
- RAG agent deps should not require concrete storage
- `_ScopedTrendsRepository` can disappear

This phase should follow decomposition. Doing it earlier would mostly move complexity around without reducing it.

Current status note:

- `TrendRepositoryPort` is in place and is used by `trends.py` and the RAG modules
- scoped trend behavior still relies on a dedicated adapter inside the pipeline trends stage
- publish and analysis ports remain to be introduced

### Phase 5: Split CLI wiring

Status: partial.

After the application services settle:

- move commands into modules by command area
- keep a small top-level `cli.py` for app assembly
- move managed run and lease helpers into an app/runtime layer

This is mainly a maintainability pass.

Current status note:

- `recoleta.cli` is now a real package and managed-run helpers live under `recoleta.app.runtime`
- top-level `recoleta/cli.py` is now a compatibility shim
- command-level CLI modules are still combined inside `recoleta/cli/__init__.py`

## Breaking Change Decision Gate

Only consider a breaking refactor after Phases 1 to 3.

A breaking change is justified only if at least one of these remains true after decomposition:

- the configuration model still forces invalid combinations or misleading semantics
- the item or trend state machine still prevents correct behavior
- the storage schema still blocks required correctness or performance guarantees
- the canonical output contract is still fundamentally wrong for downstream consumers

If the pain disappears after internal decomposition, then a breaking change was not needed.

## Immediate Priorities

If work starts now, the best sequence is:

1. Extract shared trend rendering helpers out of `recoleta/publish.py`.
2. Split note writing from PDF rendering in `recoleta/publish.py`.
3. Extract publish-stage logic from `PipelineService`.
4. Extract trend-stage logic from `PipelineService`.
5. Split `Repository` into internal stores behind the existing facade.

This order gives the highest maintenance payoff with the lowest behavior risk.

## Risks To Avoid

- Mixing behavior changes into structural refactors
- Renaming metrics casually and losing observability continuity
- Reworking schema and service boundaries in the same change
- Rewriting tests to fit new module boundaries instead of preserving behavior
- Making ports too early and then widening them again through escape hatches

## Exit Criteria For The First Refactor Wave

The first wave is successful when:

- `pipeline.py`, `storage.py`, and `publish.py` are no longer the only places where new behavior lands
- site generation no longer imports private publish helpers
- trend and publish logic can be tested through smaller collaborators
- `Repository` remains externally compatible while being internally decomposed
- the full test suite still passes without output contract changes

Status against exit criteria:

- complete: `pipeline.py`, `storage.py`, and `publish.py` are no longer the only places where new behavior lands
- complete: site generation no longer imports private publish helpers
- complete: trend and publish logic can be tested through smaller collaborators
- complete: `Repository` remains externally compatible while being internally decomposed
- complete: the full test suite still passes without output contract changes

## Bottom Line

Recoleta should be refactored, but the evidence supports modular decomposition, not a disruptive rewrite.

The architecture already has a good backbone. The current problem is implementation concentration. Fix that first, and use the result to decide whether any true breaking redesign is still necessary.
