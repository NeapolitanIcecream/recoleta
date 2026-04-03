# 2026-04-03 Pipeline / Sources / Trends Hotspot Reduction

## Baseline

- Audit date: `2026-04-03`
- Baseline source: `quality/refactor-baseline.json`
- Starting audit summary: `246` hotspots
- Classification split: `85 refactor_now / 60 refactor_soon / 101 monitor`
- Success gate: baseline diff must show `resolved >= 20`, `new = 0`, `worsened = 0`

## Target Hotspots

### Sources

- `recoleta/sources.py::fetch_hf_daily_papers_drafts`
- `recoleta/sources.py::fetch_arxiv_drafts`
- `recoleta/sources.py::fetch_openreview_drafts`
- `recoleta/sources.py::fetch_rss_drafts`
- `recoleta/sources.py::fetch_hn_drafts`
- `recoleta/sources.py::_discover_feed_url_from_html`
- `recoleta/sources.py::_paper_info_to_draft`

### Pipeline Ingest / Enrich

- `recoleta/pipeline/service.py::PipelineService::ingest`
- `recoleta/pipeline/service.py::PipelineService::_pull_source_drafts`
- `recoleta/pipeline/service.py::PipelineService::_pull_source_drafts.pull`
- `recoleta/pipeline/service.py::PipelineService::enrich`
- `recoleta/pipeline/service.py::PipelineService::_rebalance_items_by_source`
- `recoleta/pipeline/service.py::enrich._consume_result`
- `recoleta/pipeline/service.py::PipelineService::_ensure_item_content`
- `recoleta/pipeline/service.py::PipelineService::_ensure_arxiv_content`
- `recoleta/pipeline/service.py::PipelineService::_ensure_arxiv_html_document_content`
- `recoleta/pipeline/service.py::PipelineService::_ensure_pdf_content`

### Trends

- `recoleta/pipeline/trends_stage.py::run_trends_stage`
- `recoleta/pipeline/trends_stage.py::run_trends_stage._prepare_trend_projection_state`
- `recoleta/pipeline/trends_stage.py::run_trends_stage._build_trend_projection_specs`

### Buffer Items Used

- `recoleta/pipeline/service.py::PipelineService::trends`

## Implemented Slice

- Added `recoleta/source_pullers.py` and moved source-specific acquisition logic behind typed request objects.
- Added `recoleta/pipeline/ingest_stage.py` and `recoleta/pipeline/enrich_stage.py` so `PipelineService.ingest()` / `enrich()` are thin façades.
- Rewrote `recoleta/pipeline/trends_stage.py` around `TrendStageRequest` and a stage runner, removing nested projection helpers from `run_trends_stage`.
- Preserved CLI/config/schema/metric names/debug artifact payloads and existing enrich / backfill / telegram semantics.

## Final Audit Outcome

- Post-refactor audit command: `uv run python scripts/refactor_audit.py`
- Post-refactor hotspot summary: `224` hotspots
- Classification split: `73 refactor_now / 54 refactor_soon / 97 monitor`
- Baseline diff: `resolved=22`, `new=0`, `worsened=0`
- Verdict: `strained`
  Existing hotspots remain, but the current scope did not regress.
- Baseline update command: `uv run python scripts/refactor_audit.py --update-baseline`

## Validation Commands

- Focused regression suite:
  - `uv run pytest tests/test_recoleta_specs_sources_cli.py tests/test_recoleta_specs_ingest.py tests/test_recoleta_specs_enrich_source_diagnostics.py tests/test_recoleta_specs_arxiv_html_document_md.py tests/test_pdf_enrich_strict_no_html_fallback.py tests/test_recoleta_specs_trends.py tests/test_trends_week_backfill.py tests/test_parallel_enrich_interrupt.py -q`
- Full validation:
  - `uv run ruff check .`
  - `uv run pytest`
  - `uv run python scripts/refactor_audit.py`
- Baseline update gate satisfied:
  - `uv run python scripts/refactor_audit.py --update-baseline`
