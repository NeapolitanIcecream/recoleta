# 40-Signal Hotspot Burndown Plan

Date: 2026-04-04

Status: Planned

## Goal

Reduce at least 40 active hotspot signals reported by `scripts/refactor_audit.py`,
measured against `quality/refactor-baseline.json`, without relaxing thresholds
or rewriting the baseline to match the current debt.

This plan keeps the existing proactive-refactor discipline:

- count progress by resolved hotspot signals, not by line movement
- prefer symbols hit by multiple tools because they remove several signals at
  once when fully cleared
- keep behavior, schema, config, and CLI contracts stable while the structure
  changes underneath

For this plan, "active hotspot signals" means the signals attached to
`refactor_now` and `refactor_soon` hotspots only. `monitor` items remain part of
the audit evidence but do not count toward the 40-signal target.

## Audit Snapshot

Commands run on 2026-04-04:

- `uv run ruff check .`
- `uv run python scripts/refactor_audit.py`

Observed baseline:

- `ruff`: clean (`All checks passed!`)
- repo verdict: `strained`
- hotspots: `163` total
- `refactor_now`: `42`
- `refactor_soon`: `34`
- `monitor`: `87`
- triple-hit hotspots (`complexipy + lizard + ruff`): `15`
- baseline diff status: `new = 0`, `worsened = 0`, `resolved = 0`

The remaining concentration points are no longer the same as the first refactor
waves. The biggest practical budgets now sit in four clusters:

- trend synthesis and output materialization:
  - `recoleta/trends.py`: `12` signal budget
  - `recoleta/materialize.py`: `5`
  - `recoleta/publish/item_notes.py`: `4`
  - `recoleta/item_summary.py`: `3`
- source extraction and cleanup:
  - `recoleta/extract.py`: `11`
- item persistence and content retrieval:
  - `recoleta/storage/items.py`: `12`
- small orchestration residue reserve:
  - `recoleta/translation.py`: `5`
  - `recoleta/site_deploy.py`: `3`
  - `recoleta/cli/workflows.py`: `2`

This still matches the architecture roadmap's core advice:

- continue refactoring by change axis instead of by file size
- keep `trends` and materialization as orchestration over narrower helpers
- keep `storage` behind the existing facade while splitting internals
- avoid mixing product changes into the structural branch

## Working Rules

- Count success by `len(baseline_diff.resolved)` from the closing audit report.
- Keep `baseline_diff.new == 0` and `baseline_diff.worsened == 0` on the same
  branch.
- Prefer triple-hit hotspots first because they give the largest audited return.
- Do not update `quality/refactor-baseline.json` until the closing execution PR
  shows a real measured reduction.
- Keep public entrypoints stable while extracting helpers or sibling modules.
- Use the reserve slice only if the primary three waves land below the
  40-signal floor.

## Target Portfolio

The portfolio intentionally carries more than 40 potential removals so the
series can still land above the floor even if some large functions only drop
below one or two tool thresholds before the branch closes.

### Wave 1: Trend synthesis and output materialization

Primary target: remove the remaining concentration around trend corpus loading,
overview assembly, trend-output materialization, and item note rendering.

Target symbols:

- `recoleta/trends.py::semantic_search_summaries_in_period`
- `recoleta/trends.py::normalize_trend_evolution`
- `recoleta/trends.py::_trend_payload_summary_lines`
- `recoleta/trends.py::build_overview_pack_md`
- `recoleta/trends.py::_load_latest_content_texts_for_items`
- `recoleta/trends.py::_index_items_as_documents_batched`
- `recoleta/trends.py::index_items_as_documents`
- `recoleta/trends.py::generate_trend_via_tools`
- `recoleta/materialize.py::_materialize_localized_outputs`
- `recoleta/materialize.py::_materialize_outputs_for_target`
- `recoleta/materialize.py::materialize_outputs`
- `recoleta/publish/item_notes.py::_render_item_note_lines`
- `recoleta/publish/item_notes.py::_write_item_note`
- `recoleta/publish/item_notes.py::write_obsidian_note`
- `recoleta/publish/item_notes.py::write_markdown_note`
- `recoleta/item_summary.py::extract_item_summary_sections`

Potential signal budget: `24`

Planned change axis:

- Extract trend evolution normalization, overview-pack rendering, summary-line
  assembly, and semantic-search bootstrap into narrower helpers or sibling
  modules under the trend surface.
- Split corpus indexing and latest-content loading away from the top-level trend
  agent orchestration so `generate_trend_via_tools()` becomes a thinner runtime
  entrypoint.
- Split materialization into target discovery/reset, localized payload loading,
  note rendering, site export, and final accounting helpers.
- Collapse note-path selection, frontmatter rendering, and markdown/obsidian
  variants behind a shared item-note writer helper.

Why this wave is first:

- It is the largest remaining product-code budget in the repo.
- It follows the roadmap's trend-service direction instead of inventing a new
  decomposition axis.
- The trend and materialization paths already have broad regression coverage.

Expected validation focus:

- `uv run pytest tests/test_recoleta_specs_trends.py -q`
- `uv run pytest tests/test_trend_materialize.py -q`
- `uv run pytest tests/test_recoleta_specs_materialize_cli.py -q`
- `uv run pytest tests/test_recoleta_specs_publish.py -q`
- `uv run pytest tests/test_publish_note_sections.py tests/test_trends_overview_pack.py -q`

### Wave 2: Source extraction decomposition

Primary target: split PDF backend selection, arXiv-specific HTML cleanup, and
Pandoc conversion orchestration inside `recoleta/extract.py`.

Target symbols:

- `recoleta/extract.py::extract_pdf_text`
- `recoleta/extract.py::extract_html_document_cleaned_with_references`
- `recoleta/extract.py::extract_html_document_cleaned_with_references._simplify_arxiv_html`
- `recoleta/extract.py::convert_html_document_to_markdown`

Potential signal budget: `11`

Planned change axis:

- Extract PDF backend probing and diagnostics from the extraction decision tree.
- Extract HTML body pruning, bibliography splitting, and arXiv simplification
  into focused helpers instead of nesting them inside one large cleanup path.
- Extract Pandoc stderr parsing and failure normalization so markdown conversion
  is a thin coordinator over reusable utilities.

Why this wave is second:

- It contains the current highest-severity remaining triple-hit hotspot.
- It improves the ingest/enrich maintenance boundary without changing the
  external extract API.
- The file is self-contained enough to refactor without broad cross-module
  coordination.

Expected validation focus:

- `uv run pytest tests/test_extract_arxiv_mathml_cleanup.py -q`
- `uv run pytest tests/test_extract_pdf_text_backend_selection.py -q`
- `uv run pytest tests/test_recoleta_specs_ingest.py tests/test_recoleta_specs_ingest_cli.py -q`

### Wave 3: Item persistence and content retrieval split

Primary target: finish the remaining `ItemStore` decomposition inside
`recoleta/storage/items.py`.

Target symbols:

- `recoleta/storage/items.py::ItemStoreMixin::_find_near_duplicate_by_title`
- `recoleta/storage/items.py::ItemStoreMixin::upsert_item`
- `recoleta/storage/items.py::ItemStoreMixin::get_latest_content_texts`
- `recoleta/storage/items.py::ItemStoreMixin::get_latest_content_texts_for_items`
- `recoleta/storage/items.py::ItemStoreMixin::upsert_contents_texts`

Potential signal budget: `12`

Planned change axis:

- Separate identity matching, title-dedup scoring, and metadata merge rules from
  the `upsert_item()` transaction shell.
- Extract latest-content query normalization and row projection from the batch
  retrieval methods.
- Extract content hash preparation and duplicate-pair detection from
  `upsert_contents_texts()` so the write path stops mixing normalization,
  lookup, and insertion in one routine.

Why this wave is third:

- It aligns directly with the roadmap's `ItemStore` internal-split direction.
- It is a strong signal budget in one file, which keeps the branch measurable.
- It does not require any schema or facade contract changes to land.

Expected validation focus:

- `uv run pytest tests/test_storage_latest_content_texts_batch.py -q`
- `uv run pytest tests/test_storage_title_dedup_exact_match.py -q`
- `uv run pytest tests/test_storage_upsert_content_with_inserted.py -q`
- `uv run pytest tests/test_recoleta_specs_ingest.py -q`

### Reserve: Translation and workflow residue

Reserve target: provide extra audited budget if the first three waves do not
clear 40 resolved signals because a few multi-tool hotspots only partially drop
under their thresholds.

Target symbols:

- `recoleta/translation.py::translate_structured_payload`
- `recoleta/translation.py::_incremental_candidates`
- `recoleta/translation.py::_translate_candidate_into_language`
- `recoleta/translation.py::run_translation`
- `recoleta/translation.py::run_translation_backfill`
- `recoleta/site_deploy.py::_gh_api_configure_pages_source`
- `recoleta/site_deploy.py::deploy_trend_static_site_to_github_pages`
- `recoleta/cli/workflows.py::execute_granularity_workflow`
- `recoleta/cli/workflows.py::execute_deploy_workflow`

Potential signal budget: `10`

Why this is reserve work instead of the main branch axis:

- These are mostly orchestration wrappers with smaller isolated budgets.
- They are useful cleanup, but they are not the largest remaining debt
  concentration.
- They can be peeled in small follow-up commits if the measured delta needs
  another push.

Expected validation focus:

- `uv run pytest tests/test_localization_translation.py -q`
- `uv run pytest tests/test_site_gh_deploy.py -q`
- `uv run pytest tests/test_recoleta_specs_run_once_cli.py tests/test_recoleta_specs_publish_cli.py -q`

## Reduction Budget

Primary portfolio:

- Wave 1 potential: `24`
- Wave 2 potential: `11`
- Wave 3 potential: `12`
- Primary total potential: `47`

Reserve portfolio:

- Translation and workflow residue: `10`

Total potential portfolio: `57`

Delivery bar:

- minimum success: at least `40` resolved hotspot signals
- preferred success: at least `44` resolved hotspot signals
- no new or worsened hotspots in the same branch

This means the practical execution sequence is:

1. Land the trend/materialization wave first.
2. Land the extract wave next because it removes the worst remaining triple-hit
   hotspot.
3. Land the `ItemStore` wave to push the branch comfortably over the 40-signal
   floor.
4. Only use the reserve slice if the measured closing audit is still short.

## Tracking Checklist

- [ ] Land Wave 1 trend/materialization decomposition.
- [ ] Land Wave 2 extract decomposition.
- [ ] Land Wave 3 `ItemStore` decomposition.
- [ ] Use the reserve translation/workflow slice only if the measured branch
      delta is still below `40`.
- [ ] Rerun `uv run python scripts/refactor_audit.py` and record the
      before/after delta in the closing execution PR.
- [ ] Run `uv run python scripts/refactor_audit.py --fail-on-regression` before
      updating the baseline.
- [ ] Update `quality/refactor-baseline.json` only in the closing execution PR
      after the measured reduction is confirmed.

## Exit Criteria

The closing execution PR for this series must show all of the following:

- `uv run ruff check .`
- the targeted pytest suites for the touched wave(s)
- `uv run python scripts/refactor_audit.py`
- `uv run python scripts/refactor_audit.py --fail-on-regression`
- `len(baseline_diff.resolved) >= 40`
- `len(baseline_diff.new) == 0`
- `len(baseline_diff.worsened) == 0`

Optional but recommended when the touched code changes typed interfaces:

- `uv run pyright`
