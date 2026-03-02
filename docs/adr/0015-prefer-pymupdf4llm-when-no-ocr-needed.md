# ADR 0015: Prefer PyMuPDF4LLM for Non-OCR PDF Extraction

## Status
Accepted

## Context
arXiv PDF enrichment previously always used marker-pdf, which initializes OCR-capable models even when the PDF already has a machine-readable text layer. This adds avoidable latency and model overhead for born-digital papers.

## Decision
Detect text-layer availability from the first few PDF pages. When text is present, extract Markdown with pymupdf4llm. When text is absent, or when pymupdf4llm extraction returns empty/failed output, fall back to marker-pdf as the OCR-capable extractor.

## Consequences
Text-layer arXiv PDFs now avoid OCR startup and generally enrich faster. Scanned or image-only PDFs keep existing behavior through marker fallback. Detection relies on a lightweight heuristic threshold, so rare borderline files may still use the fallback path.
