# ADR 0011: Default arXiv Enrichment Uses html_document_md

## Status
Accepted

## Context
The analyzer prompt benefits from lower markup noise and fewer raw HTML fragments than cleaned arXiv HTML. We already generate `html_document_md` from `html_document` via Pandoc and prefer it for analysis when `enrich_method=html_document`.

## Decision
Change the default `SOURCES.arxiv.enrich_method` to `html_document`, so the system produces and analyzes `html_document_md` by default (with `fallback` still enabled).

## Consequences
New installations will fetch arXiv HTML and attempt Markdown conversion; if Pandoc is unavailable, analysis falls back to other available content types per `fallback` policy.

