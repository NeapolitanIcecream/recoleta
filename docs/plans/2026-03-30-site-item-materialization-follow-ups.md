# Site Item Materialization Follow-ups

Date: 2026-03-30

Status: linked-only item export landed for `site build` and `site stage`; the
retention and archive follow-ups below are intentionally deferred

## What Landed

- `site build` now defaults to `item_export_scope=linked`.
- `site stage` now uses the same default and no longer mirrors every
  `Inbox/*.md` file by default.
- `site serve`, `fleet site build`, and `fleet site serve` forward the same
  option.
- `--item-export-scope all` restores the old behavior for compatibility.
- build/stage manifests and human-readable CLI output now report:
  - `item_export_scope`
  - `items_total`
  - `items_available_total`
  - `items_unreferenced_total`

This change is intentionally narrow. It removes obvious over-materialization but
does not yet change archive structure, retention rules, or pass lineage.

## Why This Was Necessary

The previous site export path materialized every item note into:

- `site/items/*.html`
- `site/artifacts/items/*.md`

That happened even when the published trend and idea pages only linked to a
small subset of those items.

One representative audit sample on 2026-03-30 from
`bench-out-peer-history-treatment-v5/materialized-v3` showed:

- `8` trend pages
- `494` item pages
- `60` item pages actually linked from trend pages
- `434` item pages with no in-site incoming link
- roughly `88%` of item pages were therefore unreachable leaf pages
- total site size around `6.2 MB`
- `site/items` plus `site/artifacts/items` accounted for about `5.9 MB`

That is not yet catastrophic in absolute size, but it is already the dominant
source of file-count and output-size growth. The linked-only default addresses
that waste directly.

## Deferred Issues

### 1. Trend archive pagination or month-level sharding

The current archive page is still one long page.

This is a usability concern, especially once the trend history grows across many
months and multiple localized or fleet outputs. It is not the main driver of
site size today, so it stays deferred behind the linked-only item export fix.

Recommended follow-up:

- split archive output by month or paginate the archive surface
- keep stable canonical links for individual trend detail pages
- keep the home page and trends index focused on recent history only

### 2. Layered retention for `documents`, `document_chunks`, and site output

Current retention tooling can prune rebuildable caches in coarse categories, but
it does not express hot/warm/cold retention tiers.

Recommended follow-up:

- keep authoritative history such as canonical `items`, `analyses`, and
  `pass_outputs`
- retain richer `documents` / `document_chunks` for a hot window
- downgrade older windows to thinner summaries or metadata-only records where
  possible
- treat site output and staged site content as rebuildable derived surfaces with
  shorter retention than canonical markdown

This should be modeled as explicit retention policy, not as ad hoc cleanup.

### 3. Reference-aware TTL / retire behavior

The product question is valid: small-granularity outputs should generally expire
faster unless they are still kept alive by larger-granularity outputs that have
not yet expired.

That requires more than a timestamp-based TTL. It needs reference-aware
retention semantics.

Recommended follow-up:

- define retention policy by surface granularity
  - day-level outputs: shortest TTL
  - week-level outputs: medium TTL
  - month-level outputs: longest TTL
- only retire a lower-granularity derived surface when it is both old enough and
  not referenced by a still-live roll-up surface
- keep the implementation terminology explicit:
  - product-facing term can be `archive` or `retire`
  - implementation-facing term should stay `retention` / `expire`

### 4. Trend pass lineage as the prerequisite for reference-aware retention

This is the hard constraint behind the previous item.

Today, canonical `trend_synthesis` pass outputs do not yet record lower-level
structured dependencies. The builder currently uses `input_refs=[]`, so the
system does not know which day trends were rolled into a week trend or which
week trends were rolled into a month trend.

By contrast, ideas already have a better upstream story:

- `trend_ideas` pass outputs can record structured `PassInputRef` input refs
- idea notes and idea document metadata already carry the upstream
  `trend_synthesis` pointer

Recommended follow-up:

- extend `trend_synthesis` outputs to record lower-level trend dependencies as
  structured `input_refs`
- decide whether item-level lineage is also required or whether window-level
  trend lineage is enough for retention
- only build reference-aware retention after this lineage contract exists

Without that lineage graph, TTL can only be time-window-based, not
reference-aware.

## Why These Remain Deferred

- The linked-only export change removes the clearest current waste with a small,
  low-risk code change.
- Pagination and retention policy both need a product decision, not just a
  mechanical refactor.
- Reference-aware TTL would be unsafe to implement before trend lineage is
  explicit in canonical pass state.
- None of the deferred items should silently mutate or delete canonical history
  until the retention contract is written down first.
