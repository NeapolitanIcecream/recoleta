---
title: "ADR 0030: Pass-oriented canonical outputs for trend synthesis and follow-on ideas"
status: Proposed
---

## Context

Recoleta's `trends` flow currently combines three different concerns inside one
runtime path:

- agentic synthesis over item and trend corpora
- deterministic normalization and representative enforcement
- publish-time projection, including note-link rewrites and render-oriented text
  shaping

This is workable for a single trend report, but it becomes the wrong shape for
follow-on passes such as idea extraction.

The core problems are:

- `TrendPayload` acts as both analysis output and publish-ready payload
- the persisted `trend_payload_json` currently reflects materialized note
  content, not a clean canonical analysis artifact
- trend RAG tools and deps are specialized for one pass rather than reusable as
  pass-scoped corpus access infrastructure
- adding a second responsibility-heavy prompt to the same trend agent run would
  increase cost, reduce reliability, and blur failure boundaries

We want to add a new optional `ideas` capability that works from trend outputs
without turning one trend invocation into a monolithic "do everything" agent
run.

## Decision

Adopt a pass-oriented architecture for trend synthesis and follow-on idea
generation.

### 1. Separate stage, pass, and projection

- A `stage` remains the user-facing orchestration entrypoint (`recoleta trends`,
  future `recoleta ideas`).
- A `pass` is one canonical inference step with explicit inputs, output schema,
  status, and diagnostics.
- A `projection` turns a canonical pass output into downstream sinks such as
  `documents`, markdown notes, PDF artifacts, or Telegram deliveries.

### 2. Persist canonical pass outputs independently of publish projections

Add a new append-oriented `pass_outputs` store for canonical pass artifacts.

Each row should capture at least:

- `run_id`
- `scope`
- `pass_kind`
- `status` (`succeeded`, `suppressed`, `failed`)
- `granularity`
- `period_start`
- `period_end`
- `schema_version`
- `content_hash`
- `payload_json`
- `diagnostics_json`
- `input_refs_json`
- `created_at`

This store is the durable execution boundary between passes. It is not the same
thing as the searchable/publishable `documents` projection.

### 3. Treat `documents` as projections, not canonical pass state

The existing `documents` and `document_chunks` tables remain valid as:

- item corpus for retrieval
- trend corpus for retrieval
- publish/search projections

They should no longer be treated as the only canonical representation of trend
analysis output.

### 4. Split trend work into canonical synthesis plus projection

The current `trends` stage should evolve into:

1. `trend_synthesis` pass
2. `trend_publish` projection

`trend_synthesis` owns:

- prompt/context assembly
- agent execution
- deterministic normalization
- canonical pass output persistence

`trend_publish` owns:

- note-link rewriting
- markdown / obsidian / PDF / Telegram rendering
- trend `Document` projection updates

### 5. Add `ideas` as a separate pass, not a subtask of `trend_synthesis`

Introduce a new optional `ideas` stage built around an `ideas` pass.

Its required upstream input is the canonical output of `trend_synthesis` for the
same `(scope, granularity, period_start, period_end)` target.

The `ideas` pass may also access bounded corpora such as:

- current-window `item` documents
- current-window lower-level `trend` documents

But it should consume the upstream trend synthesis result as structured input,
not by scraping the published markdown note.

### 6. Generalize corpus access infrastructure, not payload schemas

Extract reusable pass-scoped retrieval infrastructure:

- `CorpusSpec`: allowed corpus sources for a pass
- `SearchService`: text / semantic / hybrid / bundle access over allowed sources
- `ContextPackBuilder`: deterministic prompt-pack construction
- `PassDeps`: repository, vector store, scope, period, corpus access policy

Trend and ideas passes should share retrieval infrastructure while keeping
independent prompt contracts and output schemas.

### 7. Do not index canonical pass outputs into semantic search in v1

The first rollout should keep semantic search focused on the existing document
corpora. Canonical pass outputs should be injected into downstream passes via
structured inputs and context packs, not immediately added as a new searchable
corpus.

If later work shows that cross-pass semantic retrieval is valuable, it should be
added as an explicit projection with its own storage and quality rules.

### 8. Support explicit suppression as a first-class pass outcome

Some follow-on passes should be allowed to conclude that no reliable output is
available. `ideas` especially should support `suppressed` when evidence is too
thin or too generic.

This is distinct from:

- `failed`: the pass could not run correctly
- `succeeded`: the pass emitted a usable artifact

## Consequences

### Positive

- Trend synthesis becomes a clean upstream artifact for later passes.
- `ideas` can be rerun independently without regenerating or republishing trend
  notes.
- Failure domains get smaller: `ideas` failure no longer blocks trend delivery.
- Shared retrieval logic can evolve without coupling all passes to one payload
  schema.
- Observability improves because each pass has its own diagnostics and status.

### Negative

- The schema and repository surface area grows.
- Some current convenience paths in `trends_stage.py` need to be decomposed.
- Dual persistence exists during migration: canonical pass outputs and projected
  trend documents both need to stay coherent.

### Neutral / Deferred

- Canonical pass outputs are not searchable in v1.
- CLI compatibility for `recoleta trends` should be preserved while its internal
  implementation is split into pass plus projection.
- The first ideas rollout can target markdown/document projection only; richer
  delivery surfaces can come later.
