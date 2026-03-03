# ADR 0020: Remove marker-pdf and make pdf_text strict

## Status
Accepted

## Context
Recoleta v0 prioritizes a small dependency footprint and predictable runtime behavior. OCR-capable PDF stacks introduce heavyweight model dependencies and long initialization paths.

## Decision
- Remove `marker-pdf` and all OCR fallback logic.
- `pdf_text` enrichment uses `pymupdf4llm` only and fails when PDF extraction is empty.

## Consequences
Scanned/image-only PDFs will fail fast during enrichment. HTML/LaTeX enrich methods remain available when configured explicitly.
