# ADR 0015: Use PyMuPDF4LLM for PDF Extraction

## Status
Accepted

## Context
Recoleta needs a fast, lightweight PDF-to-Markdown path for born-digital papers. OCR-capable stacks add heavy dependencies and are not required for v0.

## Decision
Use `pymupdf4llm` as the only PDF-to-Markdown extractor.

- If extraction returns meaningful Markdown, store it as `pdf_text`.
- If extraction is empty or fails, `pdf_text` enrichment fails (no OCR fallback).

## Consequences
Born-digital PDFs enrich quickly with a small dependency footprint. Scanned/image-only PDFs are not supported by `pdf_text` enrichment and will fail fast.
