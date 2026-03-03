# ADR 0016: Preserve MathML in arXiv HTML

## Context
arXiv `html_document` enrichment converts LaTeXML HTML to Markdown via Pandoc. Aggressive HTML attribute stripping can remove MathML namespace/annotation attributes, increasing Pandoc math conversion warnings and risking lower-quality markdown.

## Decision
- Keep attribute stripping for noise reduction, but **do not strip attributes inside MathML subtrees** (preserve `xmlns`, `encoding`, and other MathML-required attributes).
- PDF extraction is non-OCR and uses `pymupdf4llm` only.

## Consequences
Pandoc receives valid MathML, reducing math-related warnings and improving markdown fidelity.
