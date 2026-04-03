# Site/Render Hotspot Reduction Report

Date: 2026-04-03

## Scope

This branch targeted the `site/render` change axis only.

It kept the public `recoleta.site` surface stable:

- `export_trend_static_site`
- `stage_trend_site_source`
- `TrendSiteInputSpec`

It also kept the public `recoleta.publish.trend_render_shared` import surface
stable while moving heavy internal render logic behind narrower helpers and
module facades.

## Why This Slice

The 2026-04-03 refactor audit and the architecture roadmap both pointed to the
same pressure area:

- `recoleta/site.py` had accumulated page assembly, staging, input discovery,
  and body-render responsibilities in one file
- `recoleta/publish/trend_render_shared.py` was carrying several unrelated
  render concerns behind a single helper cluster
- `recoleta/publish/idea_notes.py` and `recoleta/presentation.py` still had a
  few narrow but persistent render/projector hotspots

This branch therefore followed the planned split by change axis rather than by
line count.

## Changes Landed

### 1. Turned `recoleta.site` into a thinner facade

Added focused internal modules:

- `recoleta/site_models.py`
- `recoleta/site_inputs.py`
- `recoleta/site_pages.py`
- `recoleta/site_presentation.py`

Moved or wrapped these former `site.py` hotspots behind the new modules:

- `_discover_site_language_inputs`
- `_discover_trend_site_input_dirs`
- `_export_trend_static_site_single_language`
- `_load_trend_site_documents`
- `_presentation_local_markdown_targets`
- `_render_idea_opportunity_card`
- `_render_presentation_source_list`
- `_site_page_shell`
- `stage_trend_site_source`

The result is that `site.py` is back to coordinating stable entrypoints and
high-level render flow rather than owning every low-level render and staging
detail.

### 2. Split shared trend render helpers by concern

Added:

- `recoleta/publish/trend_render_models.py`
- `recoleta/publish/trend_render_evolution.py`
- `recoleta/publish/trend_render_sections.py`

`recoleta/publish/trend_render_shared.py` now acts as a stable facade and
re-export surface while the heavy section extraction, evolution rendering, and
body decoration logic lives in narrower modules.

### 3. Split idea evidence and presentation projectors

Added:

- `recoleta/publish/idea_evidence.py`
- `recoleta/presentation_projectors.py`

This removed the remaining evidence-ref formatting and projector hotspots from
their previous mixed-responsibility modules.

## Audit Outcome

Final full-repo audit run:

- command: `uv run python scripts/refactor_audit.py`
- verdict: `strained`
- `new = 0`
- `worsened = 0`
- `resolved = 100`
- `resolved hotspots = 36`

This exceeds the branch gate of `resolved hotspots >= 20`.

Notable resolved hotspot ids on the targeted axis:

- `recoleta/site.py :: _discover_site_language_inputs`
- `recoleta/site.py :: _discover_trend_site_input_dirs`
- `recoleta/site.py :: _export_trend_static_site_single_language`
- `recoleta/site.py :: _load_trend_site_documents`
- `recoleta/site.py :: _presentation_local_markdown_targets`
- `recoleta/site.py :: _render_idea_opportunity_card`
- `recoleta/site.py :: _render_presentation_source_list`
- `recoleta/site.py :: _site_page_shell`
- `recoleta/site.py :: stage_trend_site_source`
- `recoleta/publish/trend_render_shared.py :: _build_trend_browser_body_html`
- `recoleta/publish/trend_render_shared.py :: _decorate_trend_pdf_body_html`
- `recoleta/publish/trend_render_shared.py :: _extract_evolution_signal`
- `recoleta/publish/trend_render_shared.py :: _extract_trend_pdf_sections`
- `recoleta/publish/trend_render_shared.py :: _render_browser_evolution_section_html`
- `recoleta/publish/trend_render_shared.py :: sanitize_trend_overview_markdown`
- `recoleta/publish/idea_notes.py :: _enrich_evidence_ref`
- `recoleta/publish/idea_notes.py :: _format_evidence_ref`
- `recoleta/presentation.py :: _project_idea_evidence`
- `recoleta/presentation.py :: _project_source_metadata`

## Validation

Commands run on this branch:

- `uv run ruff check .`
- `uv run pytest tests/test_trends_static_site.py -q`
- `uv run pytest tests/test_trend_render_shared.py tests/test_publish_note_sections.py tests/test_output_quality_2026w12_regression.py -q`
- `uv run pytest`
- `uv run python scripts/refactor_audit.py`

Additional check run:

- `uv run pyright`

Observed result:

- full `pytest`: `636 passed`
- full audit diff: no regressions
- `pyright` still reports existing repository issues outside this refactor slice,
  including pre-existing test call-site errors and `TypedDict` access warnings
  in `recoleta/publish/trend_notes.py`

## Remaining Queue

The branch intentionally did not try to clear the full `site/render` backlog.
After this slice, the remaining leading site/render hotspot is:

1. `recoleta/site.py :: _render_home_page`

That should be handled in a follow-up branch, not folded back into this one.
