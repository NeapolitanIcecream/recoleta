# ADR 0016: Preserve MathML in arXiv HTML and mitigate marker device failures

## Context
arXiv `html_document` enrichment converts LaTeXML HTML to Markdown via Pandoc. Aggressive HTML attribute stripping removed MathML namespace/annotation attributes, increasing Pandoc math conversion warnings and risking lower-quality markdown. PDF enrichment may fall back to `marker-pdf`, which can fail on some devices (e.g., MPS) with meta-tensor initialization errors.

## Decision
- Keep attribute stripping for noise reduction, but **do not strip attributes inside MathML subtrees** (preserve `xmlns`, `encoding`, and other MathML-required attributes).
- Prefer `pymupdf4llm` outputs even when the text-layer heuristic is inconclusive, to reduce unnecessary OCR.
- Add `MARKER_TORCH_DEVICE` (optional) to force marker model device, and **retry marker once on CPU** when a meta-tensor failure is detected.

## Consequences
Pandoc receives valid MathML, reducing math-related warnings and improving markdown fidelity. Marker failures are less likely to abort enrichment, and CPU retry provides a robust fallback on Apple Silicon.
