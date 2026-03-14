# Pass-Oriented Trends And Ideas Plan

Date: 2026-03-14
Status: Implemented

## Scope

This plan turns the current `trends` pipeline into a pass-oriented architecture
with a clean canonical boundary for follow-on work such as idea extraction.

The immediate target is not to ship `ideas` end to end in one jump. The first
goal is to create the architecture that makes `ideas` a separable, observable,
and rerunnable pass.

Related ADR:

- `docs/adr/0030-pass-oriented-trends-and-ideas.md`

## Implementation Notes

As of 2026-03-14, the planned phases have been implemented in the repo:

- Phase 0: pass primitives and `pass_outputs` persistence
- Phase 1: canonical `trend_synthesis` dual-write
- Phase 2: canonical trend payload persistence before publish-only rewrites
- Phase 3: shared retrieval via `CorpusSpec` and `SearchService`
- Phase 4: independent `ideas` stage/pass/markdown projection

## Goals

1. Preserve current `recoleta trends` user-facing behavior while splitting its
   internals into canonical synthesis and projection.
2. Introduce a durable canonical pass-output boundary that later passes can
   consume directly.
3. Reuse trend retrieval infrastructure in a pass-scoped way instead of keeping
   it hard-coded to one agent.
4. Add a path for a future `ideas` stage that does not require a monolithic
   trend+ideas agent run.
5. Keep the system observable at every new boundary.

## Non-Goals

- redesigning current trend note layout
- making every pass output immediately searchable
- introducing arbitrary DAG scheduling across all pipeline stages
- changing existing topic-stream or delivery semantics

## Current-State Findings

### 1. Canonical output and publish projection are mixed

Today the trend flow:

1. builds a `TrendPayload`
2. materializes note-oriented rewrites
3. writes the resulting payload into `trend_payload_json`
4. projects it to markdown / PDF / Telegram / `Document`

That means the persisted trend payload is already influenced by publish-layer
concerns such as note-link rewriting and render-oriented text clamping.

### 2. Retrieval infra is reusable in practice but trend-specific in shape

The current trend agent already has reusable building blocks:

- document listing
- document bundle retrieval
- text search
- semantic search
- hybrid search

But those live under trend-specific deps and prompt contracts. A follow-on pass
cannot reuse them cleanly without importing trend agent machinery.

### 3. The right intermediate boundary is a pass output, not markdown

The future `ideas` pass should consume:

- structured trend synthesis output
- deterministic context packs
- selected searchable corpora

It should not consume:

- published markdown trend notes
- Telegram caption text
- render-shaped output rewritten for note links

## Proposed Runtime Model

```text
Stage
  -> PassRunner
      -> resolve_inputs()
      -> build_context_packs()
      -> run_agent_or_deterministic_logic()
      -> normalize()
      -> persist canonical PassOutput
      -> project()
```

### Terminology

- `stage`: top-level CLI/service orchestration entrypoint
- `pass`: one canonical, typed computation step
- `projection`: one sink-specific materialization of a pass output

## Canonical Data Contracts

### `PassOutputEnvelope`

Every pass should persist an envelope rather than only a naked payload.

Recommended fields:

- `pass_kind`
- `schema_version`
- `status`
- `scope`
- `granularity`
- `period_start`
- `period_end`
- `run_id`
- `input_refs`
- `payload`
- `diagnostics`

The envelope is the stable handoff artifact across passes.

### `input_refs`

Keep upstream linkage explicit and machine-readable. The first version only
needs a small schema, for example:

```json
[
  {
    "ref_kind": "pass_output",
    "pass_kind": "trend_synthesis",
    "scope": "default",
    "granularity": "week",
    "period_start": "2026-03-09T00:00:00+00:00",
    "period_end": "2026-03-16T00:00:00+00:00",
    "pass_output_id": 123
  }
]
```

This is enough for downstream provenance and debug artifacts without adding full
workflow orchestration complexity.

### `TrendSynthesisPayload`

The canonical trend payload can stay close to today's `TrendPayload`, but it
should be persisted before publish-only rewriting.

Expected structure:

- `title`
- `granularity`
- `period_start`
- `period_end`
- `overview_md`
- `topics`
- `clusters`
- `highlights`
- `evolution`

The important change is semantic, not structural:

- this payload is canonical analysis output
- projection-specific rewrites happen later

### `TrendIdeasPayload`

The `ideas` pass needs a schema tuned for opportunity extraction rather than
trend summarization.

Suggested shape:

- `summary_md`
- `ideas`

Each `idea` should include:

- `title`
- `kind`
- `thesis`
- `why_now`
- `what_changed`
- `user_or_job`
- `evidence_refs`
- `validation_next_step`
- `time_horizon`

`evidence_refs` should point back to concrete upstream evidence instead of
embedding free-form citation prose only.

## Storage Design

### New `pass_outputs` table

Recommended columns:

- `id`
- `run_id`
- `scope`
- `pass_kind`
- `status`
- `granularity`
- `period_start`
- `period_end`
- `schema_version`
- `content_hash`
- `payload_json`
- `diagnostics_json`
- `input_refs_json`
- `created_at`

Recommended behavior:

- append-oriented writes
- no destructive overwrite of historical outputs
- helper query for "latest successful output for logical target"

### Why not reuse `documents`?

Because `documents` currently serve retrieval and publish/search projection
needs. Using them as the canonical pass store would mix:

- execution lifecycle
- provenance
- publish/search representation

Those concerns need different invariants.

## Shared Retrieval Design

### `CorpusSpec`

Each pass should declare which sources it may access.

Examples:

- `trend_synthesis(day)`: `item`
- `trend_synthesis(week)`: `item` + `trend(day)`
- `ideas(week)`: upstream `trend_synthesis(week)` as structured input, plus
  optional `item` + `trend(day)`

### `SearchService`

Move the reusable retrieval surface behind a generic service used by pass
agents:

- `list_docs`
- `get_doc`
- `get_doc_bundle`
- `read_chunk`
- `search_text`
- `search_semantic`
- `search_hybrid`

The service should enforce `CorpusSpec` instead of trusting each pass prompt to
avoid disallowed sources.

### `ContextPackBuilder`

Generalize today's deterministic packs into reusable builders:

- `overview_pack`
- `history_pack`
- future `trend_snapshot_pack`
- future `ideas_seed_pack`

Each pack builder should emit:

- markdown or structured payload
- bounded stats for diagnostics and metrics

## Stage Design

### `recoleta trends`

Keep the CLI contract, but internally run:

1. `trend_synthesis` pass
2. `trend_publish` projection

This preserves current user-facing behavior while establishing the new
architecture boundary.

### `recoleta ideas`

Add a new stage later with this behavior:

1. resolve target window
2. load latest successful `trend_synthesis` output for that target
3. run `ideas` pass
4. project ideas outputs to configured sinks

The stage should not silently rerun `trend_synthesis` unless the user opts into
that behavior explicitly.

## Pass Status Model

All passes should support:

- `succeeded`
- `suppressed`
- `failed`

Use `suppressed` when a pass chooses not to emit output for evidence-quality
reasons.

This is especially useful for `ideas`, where "no reliable ideas this window" is
often a correct result rather than a runtime error.

## Observability

Follow the existing `pipeline.trends.*` namespace and avoid high-cardinality
metrics.

Recommended pass-level metrics:

- `pipeline.trends.pass.synthesis.duration_ms`
- `pipeline.trends.pass.synthesis.prompt_chars`
- `pipeline.trends.pass.synthesis.tool_calls_total`
- `pipeline.trends.pass.ideas.duration_ms`
- `pipeline.trends.pass.ideas.prompt_chars`
- `pipeline.trends.pass.ideas.tool_calls_total`
- `pipeline.trends.pass.ideas.upstream_missing_total`
- `pipeline.trends.pass.ideas.suppressed_total`
- `pipeline.trends.pass_outputs.persist_failed_total`

Recommended logs:

- `pipeline.trends.pass_runner`
- `pipeline.trends.pass.synthesis`
- `pipeline.trends.pass.ideas`
- `pipeline.trends.projection.trend_publish`
- `pipeline.trends.projection.ideas_markdown`
- `pipeline.trends.projection.ideas_obsidian`
- `pipeline.trends.projection.ideas_documents`

Recommended debug artifacts per pass:

- resolved inputs
- context packs and pack stats
- prompt size stats
- tool-call totals and breakdown
- raw output
- normalized output
- suppression or failure reason

## Migration Plan

### Phase 0. Introduce shared pass primitives

Add:

- `PassOutputEnvelope`
- `PassStatus`
- `PassDefinition`
- `PassRunner`
- `pass_outputs` persistence APIs

No user-facing behavior changes yet.

### Phase 1. Dual-write trend synthesis canonical output

Keep current `recoleta trends` behavior, but also persist canonical
`trend_synthesis` outputs to `pass_outputs`.

Exit criteria:

- trend docs still publish as before
- a canonical pass output exists for each successful trend run

### Phase 2. Move trend publish logic behind projection

Refactor the current trend flow so:

- canonical trend output is persisted before note-materialization rewrites
- trend note materialization reads canonical output and emits publish
  projections

Exit criteria:

- projected trend documents remain stable
- publish-only rewrites no longer mutate canonical output

### Phase 3. Extract shared retrieval infrastructure

Move reusable trend retrieval helpers into generic pass-scoped services.

Exit criteria:

- trend synthesis uses `SearchService` and `CorpusSpec`
- downstream passes can reuse retrieval without importing trend-specific agent
  modules

### Phase 4. Implement `ideas` pass

Add:

- canonical `TrendIdeasPayload`
- upstream pass-output resolution
- pass-level suppression rules
- optional markdown/document/obsidian projection

Exit criteria:

- `ideas` can run independently from an existing trend synthesis output
- `ideas` failure does not block trend publication

## Testing Strategy

### Unit tests

- pass-output persistence and latest-success lookup
- trend synthesis canonical output persistence before projection rewrites
- upstream resolution failures for `ideas`
- `ideas` suppression path emits status and metrics
- `CorpusSpec` enforcement for retrieval

### Regression tests

- current trend markdown output remains stable after the internal split
- `recoleta trends` still writes trend `Document` projections
- `ideas` can consume prior trend synthesis output without reparsing markdown

### Failure-path tests

- pass-output persistence failure emits the expected metric/log signal
- missing upstream trend synthesis output records `upstream_missing_total`
- projection failure does not erase canonical pass output

## Open Questions

1. Should projections record a reverse pointer to their source `pass_output_id`?
   Recommendation: yes for trend and ideas document projections if the storage
   change stays lightweight.
2. Do we want `ideas` to project into `documents` as a new searchable doc type
   in v1?
   Recommendation: yes, but keep it explicitly derived from canonical pass
   output and do not make `materialize outputs` mutate DB state just to rebuild
   it.
3. Should stage-to-pass mapping remain one-to-one long term?
   Recommendation: no strict rule. For now, keep it simple:
   `trends -> synthesis + publish`, `ideas -> ideas + publish`.
