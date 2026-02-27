# ADR 0010: Configurable arXiv Enrich Methods

## Status
Accepted

## Context
Recoleta enriches arXiv items into stored content for analysis and triage. Some workflows need direct LaTeX source input or cleaned official arXiv HTML input for the LLM, and they also need a clear failure policy when enrichment cannot be produced.

## Decision
Add `SOURCES.arxiv.enrich_method` with `pdf_text|latex_source|html_document` and `SOURCES.arxiv.enrich_failure_mode` with `fallback|strict`. Implement `latex_source` via `https://arxiv.org/e-print/<id>` and `html_document` via `https://arxiv.org/html/<id>`, store them as `contents.content_type` values, and load analysis content according to the configured method.

## Consequences
Default behavior remains compatible (`pdf_text` + `fallback`). Strict mode enables fail-fast ingest/enrich without implicit fallback. Triage remains local-state-only and can use arXiv `latex_source`/`html_document` fallbacks when `pdf_text` and `html_maintext` are unavailable.

