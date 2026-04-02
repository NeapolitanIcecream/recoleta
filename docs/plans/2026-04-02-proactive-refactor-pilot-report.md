# Proactive Refactoring Pilot Report

Date: 2026-04-02

## Scope

This note records the first pilot run of the proactive refactoring workflow
introduced in PR #27.

The goal of this pilot was not to chase the largest file blindly. The goal was
to verify that the workflow can:

- identify high-value structural hotspots from the current tree
- choose a refactor slice by change axis rather than by line count
- land a behavior-preserving refactor with regression coverage
- reduce the recorded baseline debt without introducing new regressions

## Why This Slice

The refactor audit and the architecture roadmap point to the same pressure area:
trend output generation is still carrying too much control flow inside a small
set of rendering and materialization functions.

This pilot therefore targeted the output/presentation slice:

- `recoleta/presentation.py`
- `recoleta/trend_materialize.py`
- `recoleta/publish/trend_notes.py`

This matches the roadmap principle in
`docs/plans/2026-03-09-architecture-review-and-refactor-roadmap.md`:

- refactor by change axis, not by file size
- separate canonical content generation from derived delivery rendering

## Changes Landed

### 1. Split presentation validation into narrow validation helpers

`validate_presentation_v1()` had become a multi-branch contract validator for
both trend and idea sidecars.

This pilot extracted:

- common top-level field validation
- trend-specific validation
- idea-specific validation
- user-visible string leak checks
- opportunity-level validation helpers

Result:

- the previous `refactor_now` hotspot at `validate_presentation_v1` was removed
- sidecar contract enforcement remains centralized and unchanged at the public API

### 2. Introduce a focused trend note materializer object

`materialize_trend_note_payload()` previously mixed:

- repository caching
- citation rewriting
- canonical-link rewriting
- history-window lookup
- evolution normalization
- representative-source enrichment

This pilot introduced `_TrendNoteMaterializer` so those responsibilities are now
grouped behind narrower methods while preserving the same public entrypoint and
output payload shape.

Result:

- the prior nested hotspots for history-window lookup and doc-ref rewriting were removed
- materialization logic is now organized around explicit sub-responsibilities

### 3. Split trend markdown rendering by render concern

`recoleta/publish/trend_notes.py` now uses small render contexts and focused
helpers for:

- frontmatter construction
- evolution section rendering
- history-window label rendering
- representative-source list rendering

Result:

- markdown assembly still produces the same note and sidecar contract
- the render path is easier to extend without reopening one large function

## Audit Outcome

Audit baseline before this pilot, from the current baseline snapshot:

- hotspots: `285`
- `refactor_now`: `102`
- `refactor_soon`: `76`
- `monitor`: `107`

Audit result after this pilot:

- hotspots: `282`
- `refactor_now`: `100`
- `refactor_soon`: `76`
- `monitor`: `106`

Baseline diff after the final audit run:

- `0` new
- `0` worsened
- `3` resolved

Resolved baseline hotspots:

- `recoleta/presentation.py :: validate_presentation_v1`
- `recoleta/trend_materialize.py :: materialize_trend_note_payload._history_window_ref`
- `recoleta/trend_materialize.py :: materialize_trend_note_payload._rewrite_doc_refs`

Repo verdict after this pilot remains `strained`. That is expected. The pilot
was designed to prove that the workflow can reduce debt incrementally, not to
clear the backlog in one branch.

## Validation

Commands run during this pilot:

- `uv run ruff check recoleta/presentation.py recoleta/trend_materialize.py recoleta/publish/trend_notes.py`
- `uv run pytest tests/test_presentation.py tests/test_trend_materialize.py tests/test_publish_trend_note_representatives.py -q`
- `uv run python scripts/refactor_audit.py`

Final observed result:

- targeted tests: `35 passed`
- audit baseline diff: no regressions

## What This Pilot Proved

The workflow from PR #27 is useful when applied with discipline:

- the audit is good at finding the right change axes
- the roadmap prevents arbitrary line-count-only decompositions
- the baseline diff is strict enough to detect when a refactor only moves debt around
- a narrow pilot can still remove real baseline hotspots without changing user-facing behavior

## Next Recommended Queue

The next `refactor_now` candidates are still concentrated in the larger
orchestration surfaces:

1. `recoleta/pipeline/trends_stage.py :: run_trends_stage`
2. `recoleta/pipeline/service.py :: PipelineService::enrich`
3. `recoleta/sources.py :: fetch_rss_drafts`

Those should be handled in separate follow-up branches. They are larger and
carry more behavior risk than this pilot slice.
