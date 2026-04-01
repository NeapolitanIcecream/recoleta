# Output Quality Redesign for Trends, Ideas, Localization, and Site Projections

Date: 2026-03-31

Status: Partially implemented

Implementation status as of 2026-04-01:

- Phase 1 has landed in PR #25 (`feat(output-quality): land phase 1 presentation groundwork`).
- Canonical English trend and idea markdown now emit adjacent
  `*.presentation.json` sidecars with internal v1 validation at write time.
- Shared reader-facing prompt style guardrails are wired into trend, idea, and
  translation prompts.
- Canonical idea markdown and the markdown-first site parser now use
  reader-facing labels (`Best bet` / `Alternate`, `Type`, `Horizon`, `Role`).
- Translation sidecar-first, localized sidecars, and site sidecar-first
  rendering remain future phases and are not implemented yet.
- `anti_thesis` remains deferred because `TrendIdeasPayload` stays frozen in
  Phase 1.

## Goal

Define a reusable redesign for user-visible output quality across:

- weekly and daily trend briefs
- idea briefs
- localized markdown projections
- static site detail pages derived from markdown

This document uses the generated `26w12` output artifacts as the evidence base,
but the target is a general output-quality architecture rather than a one-off
`w12` patch.

This document intentionally does not depend on
`docs/plans/2026-03-23-2026w12-run-retro.md`. The source of truth here is the
generated artifact set itself.

## Evidence Scope

### Primary evidence set

Use the final user-visible weekly artifacts under the live playground outputs:

The local checkout prefix is normalized below as `<playground-root>` because the
artifact-relative paths are the important evidence, not the machine-specific
absolute root.

- `<playground-root>/fleet/instances/embodied_ai/outputs/site/en/artifacts/week--2026-W12--trend--586.md`
- `<playground-root>/fleet/instances/embodied_ai/outputs/site/en/artifacts/ideas/week--2026-W12--ideas.md`
- `<playground-root>/fleet/instances/software_intelligence/outputs/site/en/artifacts/week--2026-W12--trend--767.md`
- `<playground-root>/fleet/instances/software_intelligence/outputs/site/en/artifacts/ideas/week--2026-W12--ideas.md`
- the corresponding HTML detail pages under `outputs/site/en/trends/` and
  `outputs/site/en/ideas/`

These files are the primary quality baseline because they are the closest
representation of what an end user actually reads.

### Root-cause and regression evidence set

Use the following only as supporting evidence and regression samples:

- `outputs/Trends/*.md`
- `outputs/Ideas/*.md`
- `outputs/Localized/zh-cn/Trends/*.md`
- `outputs/Localized/zh-cn/Ideas/*.md`

These files are useful for tracing where quality degrades, but they are not the
main success surface for this redesign.

### Scope boundary

`26w12` is an evidence sample, not a hard feature boundary. The resulting design
must apply to future windows and to both configured fleet instances.

## Executive Summary

`26w12` exposed three recurring quality failures in the current output path.

### 1. Internal placeholders and schema labels can leak into user-visible text

Observed examples include:

- `Prev_1` and similar placeholder tokens in final weekly trend artifacts
- `prev1` / `prev2` leakage in localized trend prose
- raw user-visible labels such as `Kind:`, `Time horizon:`, `User/job:`
- raw internal enums such as `tooling_wedge`, `new_build`, and `workflow_shift`

This is the most damaging failure because it breaks reader trust immediately.

### 2. Trend prose is often dense but not decisively ranked

The current weekly trend pages usually contain a large amount of concrete
evidence, but they still read like high-density research memos instead of clear
editorial briefs. The main failure mode is not lack of content. It is weak
prioritization:

- too many entities enter the opening summary at once
- too many signals are presented as equal
- the most important change is often implied rather than stated directly

### 3. Ideas pages are structurally valid but feel template-generated

The current idea briefs are coherent, but they overuse a repeated consulting
pitch frame:

- `Build a ...`
- `Why now`
- `What changed`
- `Validation next step`

That structure is useful internally, but the output currently makes four ideas
feel too equal, too generic, and too detached from an explicit best-bet point
of view.

## Quality Contract

This redesign sets a stricter contract for all user-visible text.

### Hard bans

The following must never appear in any user-visible markdown, localized
markdown, or site page body:

- `Prev_1`, `Prev_2`, `prev1`, `prev2`, or similar placeholder tokens
- raw internal enums such as `tooling_wedge`, `new_build`, `workflow_shift`,
  `research_gap`, `now`, `near`, or `frontier`
- raw schema labels such as `Kind:`, `Time horizon:`, `User/job:`, `Thesis.`
  unless they are intentionally mapped to reader-facing labels
- any unresolved internal label or fallback token from projection logic

### Trend brief contract

Each user-visible trend page must present:

- one direct headline judgment
- one short hero/dek that states the week-level change in plain language
- two to three ranked shifts
- zero or one counter-signal
- clusters that add supporting depth rather than restating the ranked shifts

The output must prefer explicit ranking over exhaustive listing. If evidence is
too weak to support three shifts, it must emit fewer shifts rather than pad.

### Idea brief contract

Each user-visible idea page must present:

- one best bet
- up to two alternate opportunities
- a clear user/job
- a concrete buyer trigger or operational pain
- a short anti-thesis describing what would make the idea weak or premature
- a validation next step that can be executed without further framing

The output must not default to four equal-weight opportunities.

### Bilingual parity contract

English and Chinese outputs are both first-class quality targets.

- English final site artifacts set the canonical readability bar.
- Chinese localized artifacts must meet the same structural rules.
- Fixed site chrome remains English as already defined in the site design, but
  user-visible body labels inside localized notes or cards must come from an
  explicit localized label map rather than ad hoc translation of raw schema
  text.

## Non-Goals

This redesign does not:

- change canonical pass schemas for `TrendPayload` or `TrendIdeasPayload`
- move publishing to a DB-first or web-first runtime
- redesign the entire site visual system
- introduce a new end-user CLI in the first implementation phase
- require historical backfill before new windows can use the improved path

Markdown remains the canonical human-readable artifact. The redesign adds a
machine-readable presentation layer beside it.

## Core Architecture Decision

The sections below describe the target end state of the redesign. Unless a
section explicitly says otherwise, read them as design intent across all
phases, not as a claim that every step is already implemented.

Add a machine-readable presentation contract between canonical pass outputs and
reader-facing markdown/site projections.

Current state:

- canonical pass outputs exist
- markdown notes are human-readable but not stable enough for machine parsing
- translation and site rendering still infer too much structure from prose and
  English labels

Target state:

- canonical pass outputs stay unchanged
- markdown notes remain human-readable
- each published trend or idea note gets an adjacent versioned
  `*.presentation.json` sidecar
- translation and site rendering use the sidecar as the preferred structured
  input
- markdown parsing becomes a compatibility fallback, not the primary contract

This keeps current authoring and repair workflows intact while removing the
need to parse reader-facing prose as if it were an API.

## Presentation Contract

### File placement

For each published trend or idea markdown note, generate an adjacent sidecar
with the same stem:

- `Trends/<stem>.md`
- `Trends/<stem>.presentation.json`
- `Ideas/<stem>.md`
- `Ideas/<stem>.presentation.json`

Localized projections follow the same rule in the target end state:

- `Localized/<language>/Trends/<stem>.md`
- `Localized/<language>/Trends/<stem>.presentation.json`
- `Localized/<language>/Ideas/<stem>.md`
- `Localized/<language>/Ideas/<stem>.presentation.json`

### Versioning

All sidecars use:

- `presentation_schema_version=1`

The site and translation code must branch on this version. Unknown versions must
fail closed for structured rendering and fall back to legacy markdown parsing.
In the current Phase 1 implementation, sidecar versioning is enforced for
canonical trend and idea sidecars; translation and site adoption remain later
phases.

### Common envelope

Both trend and idea sidecars share a small envelope:

```json
{
  "presentation_schema_version": 1,
  "surface_kind": "trend",
  "language_code": "en",
  "source_markdown_path": "Trends/week--2026-W12--trend--586.md",
  "display_labels": {},
  "content": {}
}
```

Required fields:

- `presentation_schema_version`
- `surface_kind`
- `language_code`
- `source_markdown_path`
- `display_labels`
- `content`

`display_labels` exists so projection code never needs to infer reader-facing
labels from raw enums or English markdown text.

### TrendPresentationV1

`surface_kind="trend"` sidecars must include the following content shape:

```json
{
  "presentation_schema_version": 1,
  "surface_kind": "trend",
  "language_code": "en",
  "source_markdown_path": "Trends/week--2026-W12--trend--586.md",
  "display_labels": {
    "overview": "Overview",
    "top_shifts": "Top shifts",
    "counter_signal": "Counter-signal",
    "clusters": "Clusters",
    "representative_sources": "Representative sources",
    "source_type": "Source type",
    "confidence": "Confidence"
  },
  "content": {
    "title": "Robot VLAs Turn Practical with Contact-Rich Control, Simulation-First Training, and Faster Execution",
    "hero": {
      "kicker": "Trend brief",
      "dek": "This week moved embodied AI from broader deployability claims toward measurable execution quality."
    },
    "overview": "Short overview body",
    "ranked_shifts": [
      {
        "rank": 1,
        "title": "Execution quality moved ahead of model breadth",
        "summary": "Reader-facing summary",
        "history_refs": ["prev_1", "prev_2"],
        "evidence": []
      }
    ],
    "counter_signal": {
      "title": "Simulation scale still matters, but less than execution-time control",
      "summary": "Optional reader-facing counterpoint",
      "evidence": []
    },
    "clusters": [],
    "representative_sources": []
  }
}
```

Required content fields:

- `title`
- `hero.kicker`
- `hero.dek`
- `overview`
- `ranked_shifts`
- `clusters`
- `representative_sources`

Optional fields:

- `counter_signal`

Trend constraints:

- `ranked_shifts` length must be `2..3`
- `counter_signal` may be `null`, but must never be filled with placeholder
  prose
- no user-visible field may contain unresolved `prev_n` tokens; sidecar may
  keep structured history refs for linking, but final text must be fully
  rendered

### IdeaPresentationV1

`surface_kind="idea"` sidecars must include the following content shape:

```json
{
  "presentation_schema_version": 1,
  "surface_kind": "idea",
  "language_code": "en",
  "source_markdown_path": "Ideas/week--2026-W12--ideas.md",
  "display_labels": {
    "summary": "Summary",
    "best_bet": "Best bet",
    "alternate": "Alternate",
    "role": "Role",
    "thesis": "Thesis",
    "why_now": "Why now",
    "what_changed": "What changed",
    "anti_thesis": "What could break this thesis",
    "validation_next_step": "Validation next step",
    "evidence": "Evidence"
  },
  "content": {
    "title": "Why-now ideas for coding agents moving into evaluation, orchestration, and guardrails",
    "summary": "Reader-facing summary",
    "opportunities": [
      {
        "rank": 1,
        "tier": "best_bet",
        "title": "Repository-grounded evaluation harness for coding agents",
        "kind": "tooling_wedge",
        "time_horizon": "now",
        "display_kind": "Tooling wedge",
        "display_time_horizon": "Now",
        "role": "Platform engineering and developer productivity teams selecting or governing coding agents",
        "thesis": "Reader-facing thesis",
        "why_now": "Reader-facing why now",
        "what_changed": "Reader-facing what changed",
        "anti_thesis": "Reader-facing failure case",
        "validation_next_step": "Reader-facing validation step",
        "evidence": []
      }
    ]
  }
}
```

Required content fields:

- `title`
- `summary`
- `opportunities`

Required opportunity fields:

- `rank`
- `tier`
- `title`
- `kind`
- `time_horizon`
- `display_kind`
- `display_time_horizon`
- `role`
- `thesis`
- `why_now`
- `what_changed`
- `anti_thesis`
- `validation_next_step`
- `evidence`

Idea constraints:

- `opportunities` length must be `1..3`
- exactly one opportunity must have `tier="best_bet"`
- all remaining opportunities, if present, must have `tier="alternate"`
- `kind` and `time_horizon` remain canonical enums in the sidecar for internal
  logic, but user-visible markdown and site pages must use
  `display_kind` / `display_time_horizon`

### Representative source fields

Both trend and idea sidecars must represent sources with explicit metadata:

- `title`
- `href`
- `authors`
- `source_type`
- `confidence`
- `doc_id`
- `chunk_index`

`source_type` must use this controlled vocabulary:

- `paper`
- `benchmark`
- `field_report`
- `product_post`
- `news`
- `forum_post`
- `survey`
- `unknown`

`confidence` must use:

- `high`
- `medium`
- `low`

Default derivation:

- arXiv / OpenReview style research documents -> `paper`, `high`
- benchmark-focused research artifacts -> `benchmark`, `high`
- longitudinal field studies -> `field_report`, `high`
- vendor launch or product posts -> `product_post`, `medium`
- Hacker News Show HN or forum-origin artifacts -> `forum_post`, `medium`
- mainstream reported news -> `news`, `medium`
- surveys -> `survey`, `medium`
- anything else -> `unknown`, `low`

This is not a scientific truth score. It is a reader-facing signal that helps
prevent papers, posts, and anecdotes from being flattened into the same textual
weight.

## Subsystem Design

### 1. Prompt layer

#### Shared reader-facing style component

Implementation targets:

- `docs/assets/ai-tropes.md`
- `recoleta/prompt_style.py`

Add a shared `ReaderFacingStylePromptV1` component for reader-facing prose.

Rules:

- runtime prompt text comes from a code helper such as
  `reader_facing_ai_tropes_prompt()`
- `docs/assets/ai-tropes.md` remains an editorial reference, not a runtime file
  dependency
- trend synthesis, ideas generation, and translation reuse the same shared
  component
- the shared component only constrains prose quality and rhetorical habits; it
  does not replace shape constraints, sidecar schemas, label mapping, or other
  structured validation
- prompt payload `notes` keep only surface-specific requirements and must not
  duplicate the full shared component text

#### Trend prompt changes

Implementation target:

- `recoleta/rag/agent.py`

Canonical output schema stays `TrendPayload`, but the prompt contract changes.

Required prompt-level behavior:

- trend title must read as a direct editorial judgment, not a topic inventory
- overview must stay within `160` English words or `180` Chinese characters
- output must identify `2..3` ranked shifts
- output may emit one counter-signal if evidence is real; otherwise omit it
- overview must not carry more than three named systems or papers
- evolution must reference historical windows through structured refs only, and
  user-visible text must never expose raw placeholder tokens

Required trend brief target shape:

- one headline judgment
- one hero/dek
- two to three ranked shifts
- one optional counter-signal
- supporting clusters

The prompt must explicitly forbid:

- placeholder tokens in output text
- history refs rendered as raw `prev_n`
- overstuffed opening paragraphs that enumerate many systems without ranking
- generic framing such as "this week touched many themes"

#### Ideas prompt changes

Implementation target:

- `recoleta/rag/ideas_agent.py`

Canonical output schema stays `TrendIdeasPayload`, but the prompt contract
changes.

Required prompt-level behavior:

- emit `1..3` ideas total
- exactly one best bet
- up to two alternates
- each idea must include buyer trigger, anti-thesis, and validation step
- titles must be descriptive labels, not slogan-like abstractions
- ideas must not default to four equal-weight wedges

Required idea target shape:

- one best bet
- up to two alternates
- each with role, thesis, why now, what changed, anti-thesis, validation next
  step, evidence

The prompt must explicitly forbid:

- filling the list to a fixed count
- generic "Build a platform/layer/service" wording without a named user/job and
  trigger
- invented umbrella labels or consultancy-style catchphrases

#### Prompt-level validation behavior

If the LLM response violates shape constraints:

- prompt-layer normalization may trim to the allowed count
- it must not invent missing best bets, counter-signals, or anti-theses
- if the response is too weak after trimming, the pass should fail validation
  rather than silently publish padded output

### 2. Publish and materialize layer

Implementation targets:

- `recoleta/publish/trend_notes.py`
- `recoleta/publish/idea_notes.py`
- `recoleta/materialize.py`

#### Markdown rendering rules

Trend and idea markdown notes remain human-readable, but user-visible labels
must come from an explicit mapping layer rather than raw schema labels.

Rules:

- idea markdown must not display raw `kind` or `time_horizon` enums
- idea markdown must render localized labels from `display_labels`
- trend markdown must not render unresolved history placeholders
- trend and idea markdown must be written alongside a sidecar from the same
  normalized presentation object

#### Label mapping

Use explicit display labels rather than schema labels.

English defaults:

- `best_bet` -> `Best bet`
- `alternate` -> `Alternate`
- `role` -> `Role`
- `thesis` -> `Thesis`
- `why_now` -> `Why now`
- `what_changed` -> `What changed`
- `anti_thesis` -> `What could break this thesis`
- `validation_next_step` -> `Validation next step`
- `representative_sources` -> `Representative sources`
- `counter_signal` -> `Counter-signal`

Chinese defaults:

- `best_bet` -> `首要机会`
- `alternate` -> `备选机会`
- `role` -> `适用角色`
- `thesis` -> `核心判断`
- `why_now` -> `为什么是现在`
- `what_changed` -> `发生了什么变化`
- `anti_thesis` -> `什么情况会削弱这个判断`
- `validation_next_step` -> `下一步验证`
- `representative_sources` -> `代表性来源`
- `counter_signal` -> `反向信号`

#### Sidecar generation

Projection flow becomes:

1. canonical pass output
2. normalized presentation object
3. markdown note
4. adjacent sidecar

Sidecar generation is mandatory for new projections in:

- markdown output trees
- localized markdown output trees

Repair behavior:

- if canonical pass output exists, repair should regenerate both markdown and
  sidecar
- if only legacy markdown exists, repair may keep markdown-only output until the
  note is regenerated from canonical pass state

### 3. Translation layer

Implementation target for a later phase:

- `recoleta/translation.py`

Current translation logic still reconstructs too much structure from markdown
labels and prose. The redesign changes translation to operate on structured
presentation data.

#### Translation input contract

For trends and ideas, translation must prefer:

1. `*.presentation.json`
2. canonical pass output plus note metadata
3. legacy markdown parsing only as fallback

#### Translation behavior

Translate:

- reader-facing fields in `content`
- localized `display_labels`
- hero/dek text
- opportunity-level body fields

Do not translate:

- canonical enums
- source titles when policy says to preserve them
- source type enum values stored for internal logic

Translation system prompts must also append `ReaderFacingStylePromptV1` plus a
translation-specific guardrail:

- when multiple target-language phrasings are equally faithful, prefer the most
  direct, least rhetorical, least templated rendering
- this freedom must not change claims, add or remove facts, alter JSON shape,
  or reorder arrays

Localized sidecars must preserve:

- canonical `kind`
- canonical `time_horizon`
- `display_kind`
- `display_time_horizon`

#### Translation sanitation

Before localized markdown or localized sidecar is written, the translation layer
must reject or strip:

- raw placeholder tokens
- raw enum leakage in reader-facing fields
- English schema labels that escaped structured mapping

This is the place to guarantee that `Localized/zh-cn/...` never reintroduces
the exact failures seen in `26w12`.

### 4. Site layer

Implementation target for a later phase:

- `recoleta/site.py`

#### Input priority

Site build becomes:

1. sidecar-first
2. markdown-fallback

For trend and idea detail pages:

- if a matching `*.presentation.json` exists, render from that structured
  contract
- if not, fall back to the current markdown parser

This keeps old artifacts renderable while stopping new pages from depending on
label parsing.

#### Site rendering rules

Trend pages:

- render hero title and dek from sidecar
- render ranked shifts explicitly in order
- render optional counter-signal as a distinct block
- render clusters only after ranked shifts
- render representative sources with source type and confidence metadata

Idea pages:

- render best bet first
- render alternates after best bet
- render role, thesis, why-now, what-changed, anti-thesis, validation step via
  structured fields
- stop parsing prose paragraphs that happen to begin with `Thesis.` or
  `Validation next step.`

#### Fixed chrome and localized body rules

Preserve the current product rule:

- fixed site chrome remains English

But for content cards and body labels:

- use `display_labels` from the sidecar
- do not infer labels from English markdown text

#### Source-type and confidence display

Representative sources on detail pages must display lightweight metadata such as:

- `Paper · High`
- `Forum post · Medium`

This gives readers a clearer sense of evidence shape without overloading the
page with methodology detail.

## Validation Strategy

### Internal validators

Add internal validators for presentation objects. These are not first-phase CLI
features.

Validation checks must include:

- no banned placeholder tokens
- no raw enum leakage in user-visible fields
- trend shifts count in allowed range
- idea opportunities count in allowed range
- exactly one best bet
- localized label map completeness
- sidecar schema version and required field presence

The first implementation phase should expose these as internal library checks
and test helpers only. A future optional extension can surface them through a
`doctor output-quality` CLI.

### Golden fixtures

Add golden fixtures based on the `26w12` weekly artifacts for:

- embodied AI weekly trend
- embodied AI weekly ideas
- software intelligence weekly trend
- software intelligence weekly ideas

Fixture assertions must cover:

- no placeholder leakage
- no raw taxonomy leakage
- trend structure conforms to ranked brief rules
- ideas structure conforms to best-bet plus alternates rules
- localized outputs keep bilingual label discipline

## Test Plan

### Prompt tests

Update:

- `tests/test_prompt_style.py`
- `tests/test_trends_output_language.py`
- `tests/test_ideas_agent_prompt.py`
- `tests/test_translation_prompt.py`

Add trend prompt tests for:

- ranked shifts requirement
- optional counter-signal requirement
- overview budget
- no raw history placeholder leakage
- shared `ReaderFacingStylePromptV1` anchor phrases appear in trend
  instructions

Update ideas prompt tests for:

- no equal-weight four-idea default
- one best bet plus at most two alternates
- explicit anti-thesis requirement
- explicit buyer trigger / user-job anchoring
- shared `ReaderFacingStylePromptV1` anchor phrases appear in ideas
  instructions

Add shared prompt tests for:

- runtime helper text stays aligned with `docs/assets/ai-tropes.md` after
  trailing-newline normalization
- translation system prompts include both the shared style component and the
  translation-specific direct-phrasing guardrail

### Publish and sidecar tests

Update:

- `tests/test_publish_idea_notes.py`
- related trend note tests

Add assertions for:

- sidecar generation beside markdown notes
- no raw enum labels in rendered markdown
- localized display labels are used instead of schema labels
- sidecar content matches rendered markdown sections

### Translation tests

Update:

- `tests/test_localization_translation.py`

Add assertions for:

- translation prefers sidecar-first structured input
- localized sidecars are generated
- localized display labels are mapped correctly
- localized outputs contain no `Prev_1`, `Kind:`, `Time horizon:`, or raw enum
  leakage

### Site tests

Update:

- `tests/test_trends_static_site.py`

Add assertions for:

- site exporter uses sidecar when present
- site exporter falls back to markdown parsing when sidecar is missing
- idea detail cards render from structured fields rather than label-parsed prose
- representative source metadata shows source type and confidence

## Rollout Plan

### Phase 1: Prompt and projection cleanup

Scope:

- add `ReaderFacingStylePromptV1` as a shared runtime prompt component mirrored
  from `docs/assets/ai-tropes.md`
- tighten trend prompt and ideas prompt
- apply the shared style component to translation system prompts
- stop rendering raw enums and schema labels in markdown
- add sidecar schemas and sidecar generation in publish/materialize
- add internal validators
- keep canonical pass schemas frozen in Phase 1; `anti_thesis` is deferred until
  a later schema change instead of being inferred heuristically from existing
  prose fields

Exit criteria:

- trend, ideas, and translation prompts all reuse the same reader-facing style
  component
- newly generated English markdown artifacts do not leak placeholders or raw
  taxonomy
- markdown has a stable adjacent sidecar for trend and ideas

### Phase 2: Translation and site adoption

Scope:

- make translation sidecar-first
- generate localized sidecars
- make site rendering sidecar-first with markdown fallback
- add source-type and confidence display

Exit criteria:

- localized weekly artifacts no longer leak placeholders or raw labels
- site pages render correctly from sidecars with fallback preserved

### Phase 3: Quality lint and CI regression

Scope:

- encode banned-token checks
- add golden fixtures
- add regression coverage for bilingual outputs and site rendering

Exit criteria:

- fixture-based regression catches the `26w12` classes of failure
- CI blocks new placeholder or taxonomy leakage

### Phase 4: Historical backfill and repair follow-up

Scope:

- decide whether to backfill old windows
- extend repair flows to regenerate sidecars where canonical pass outputs exist
- add optional operator tooling if quality audits need a CLI surface

Exit criteria:

- a clear historical repair policy exists
- historical windows can be selectively repaired without changing canonical pass
  data contracts

## Implementation Defaults

The following defaults are fixed by this design once all phases land.

- `TrendPayload` and `TrendIdeasPayload` remain unchanged.
- `presentation_schema_version=1` is the initial sidecar version.
- sidecar filenames are adjacent and use the `.presentation.json` suffix.
- site build is sidecar-first and markdown-fallback.
- no new end-user CLI is introduced in Phase 1.
- markdown remains the canonical human-readable artifact.
- site remains a derived projection.
- English and Chinese are equal quality targets from the start.
- runtime prose-style prompt text mirrors `docs/assets/ai-tropes.md` via a code
  helper rather than reading the docs file at runtime.

Current implementation note:

- only the Phase 1 subset above is live today
- canonical English trend and idea projections write adjacent sidecars
- localized projections remain markdown-only
- site rendering remains markdown-first with compatibility for the new idea
  labels

## Why This Is The Right Cut

The `26w12` failures are not caused by one bad prompt or one bad renderer. They
come from a structural mismatch:

- canonical data is stable
- reader-facing markdown is optimized for humans
- downstream systems still parse that human text as if it were a schema

The sidecar contract fixes that mismatch without discarding the current
architecture. It preserves canonical pass outputs, preserves markdown as a
human-readable output, and gives translation, site rendering, and QA a stable
input that can carry explicit labels, rankings, and source metadata.

That is the minimal architectural change that addresses all three failure
classes together instead of patching them one by one.
