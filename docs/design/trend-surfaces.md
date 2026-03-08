# Trend Surfaces

This document records the current design for trend-facing reading surfaces beyond raw markdown notes: browser-rendered PDFs for Telegram delivery and the static trends website.

## Goals

- Keep one canonical, inspectable source artifact for each trend note.
- Produce a denser, more polished reading surface for Telegram than plain markdown or Story-based PDF layout alone.
- Reuse the same canonical content for both PDF and web publishing.
- Make visual regressions debuggable without requiring the live pipeline to rerun.
- Keep CI and deployment decoupled from the full Recoleta runtime configuration.

## Canonical source: trend markdown

Trend markdown under `MARKDOWN_OUTPUT_DIR/Trends/` is the source of truth for downstream publishing surfaces.

Why:

- It is the existing human-readable artifact already written by the trend pipeline.
- It can be versioned, diffed, copied, and debugged directly.
- It avoids maintaining parallel content serializers for PDF, Telegram captions, and the website.

Downstream surfaces are derived from that markdown note:

- Telegram PDF
- PDF debug bundle
- static site detail pages, archive pages, and topic pages
- repository-staged site content for deployment

## PDF rendering strategy

### Renderer selection

Trend PDF rendering uses `backend="auto"`:

1. Try the browser renderer first.
2. Fall back to the Story renderer if browser rendering fails.

The browser renderer is preferred because it supports a more modern grid/card layout and better horizontal density than `PyMuPDF Story`.

The Story renderer remains as a resilience fallback so Telegram delivery can still succeed when a browser runtime is unavailable.

### Browser renderer

The browser renderer path is:

1. Normalize markdown and extract semantic sections.
2. Build an HTML document with a trend-specific card layout.
3. Inject print-safe CSS.
4. Render to PDF via Playwright's Chromium backend.

Telegram uses `page_mode="continuous"` so the PDF behaves like a long scrolling sheet instead of an A4 report. This avoids awkward page breaks in dense sections such as clusters.

### Visual compatibility constraint

Some PDF viewers and rasterizers do not reproduce CSS vector gradients reliably. To keep the browser PDF visually aligned with the browser screenshot/PNG output, key card gradients are embedded as small PNG data URIs instead of relying purely on CSS gradient paints.

This is a rendering compatibility decision, not a content-model decision.

## PDF debug bundle

`recoleta trends --debug-pdf` exports a bundle under:

- `MARKDOWN_OUTPUT_DIR/Trends/.pdf-debug/<pdf-stem>/`

Bundle contents:

- source markdown
- normalized markdown
- HTML
- CSS
- manifest with renderer/page mode
- per-page PNG previews

This supports visual debugging without mutating the canonical markdown note and without needing to rerun the whole trend pipeline just to inspect layout state.

## Static site strategy

The static site exporter consumes trend markdown notes and emits a standalone relative-link website.

Outputs include:

- homepage
- archive page
- topics index
- topic detail pages
- trend detail pages
- copied markdown/PDF artifacts
- site manifest

Design constraints:

- The output directory is treated as a managed artifact and is rebuilt cleanly each run.
- The site reuses the same trend section structure and visual language as the browser PDF, but with web navigation added.
- Relative links keep the output portable across GitHub Pages, Cloudflare Pages, local filesystem previews, and generic static hosting.

## Deployment strategy

Deployment uses a staged content snapshot rather than building from the operator's personal runtime directory on CI.

Flow:

1. Generate/update canonical trend notes locally.
2. Run `recoleta site stage` to mirror trend markdown/PDF artifacts into `site-content/`.
3. Commit the staged snapshot.
4. GitHub Actions builds the public site from `site-content/`.

Why this shape:

- CI does not need access to local Recoleta state, local config files, or private output directories.
- The exact content being deployed is reviewable in git.
- `site build` and `site stage` can run in CI with explicit paths and no full runtime settings load.

## Observability

Current diagnostics include:

- `pipeline.trends.pdf.generated_total`
- `pipeline.trends.pdf.failed_total`
- `pipeline.trends.pdf.debug.generated_total`
- `pipeline.trends.pdf.debug.failed_total`
- `pipeline.trends.pdf.browser.generated_total`
- `pipeline.trends.pdf.story.generated_total`

The static site exporter also writes a manifest describing the generated files and counts, and logs a single low-cardinality completion event for build/stage operations.

## Tradeoffs

- Markdown remains canonical even though the browser HTML surface is visually richer. This intentionally favors inspectability and portability over a pure web-first content model.
- Site deployment is snapshot-based, so publishing new content requires committing staged trend notes. This adds one manual step but keeps deployment deterministic.
- Browser PDF rendering improves layout quality but introduces a browser runtime dependency. The Story fallback absorbs that risk.
