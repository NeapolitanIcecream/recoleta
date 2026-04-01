# Trend Surfaces

This document records the current design for trend-facing reading surfaces beyond raw markdown notes: browser-rendered PDFs for Telegram delivery and the static trends website.

## Goals

- Keep one canonical, inspectable source artifact for each trend note.
- Produce a denser, more polished reading surface for Telegram than plain markdown or Story-based PDF layout alone.
- Reuse the same canonical content for both PDF and web publishing.
- Make visual regressions debuggable without requiring the live pipeline to rerun.
- Keep CI and deployment decoupled from the full Recoleta runtime configuration.

## Canonical source: trend markdown

Trend markdown under `MARKDOWN_OUTPUT_DIR/Trends/` is the source of truth for
downstream publishing surfaces. Canonical trend notes also emit adjacent
`*.presentation.json` sidecars as a structured companion artifact. Browser PDF
rendering still derives from the markdown note itself, while static trend and
idea detail pages now prefer sibling sidecars and fall back to markdown
parsing when sidecars are missing or invalid.

Why:

- It is the existing human-readable artifact already written by the trend pipeline.
- It can be versioned, diffed, copied, and debugged directly.
- It avoids maintaining parallel content serializers for PDF, Telegram captions, and the website.

Downstream surfaces are derived from that markdown note and its sibling
sidecar:

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

The static site exporter consumes trend markdown notes and sibling idea briefs
when present, then emits a standalone relative-link website. When localized
markdown trees exist, it also aggregates peer language roots and exports a
multilingual site.

Outputs include:

- homepage
- archive page
- ideas index
- topics index
- topic detail pages
- trend detail pages
- idea detail pages
- copied markdown/PDF artifacts
- site manifest
- optional per-language roots such as `/en/...` and `/zh-cn/...`

Design constraints:

- The output directory is treated as a managed artifact and is rebuilt cleanly each run.
- The site reuses the same trend section structure and visual language as the browser PDF, but with web navigation added.
- Relative links keep the output portable across GitHub Pages, Cloudflare Pages, local filesystem previews, and generic static hosting.
- Fixed UI chrome stays English even when localized long-form content is present.
- Multilingual builds emit a root redirect page that prefers the browser's remembered language and otherwise uses the configured default language.
- Page-level language switches route to the peer page when available and otherwise fall back to the target language home page.

## Deployment strategy

GitHub Pages deployment now prefers a derived branch workflow, similar to `mkdocs gh-deploy`, rather than storing a staged content snapshot on `main`.

Flow:

1. Generate/update canonical trend notes locally.
2. Run `recoleta run deploy`.
3. Recoleta builds the public site in a temporary directory.
4. Recoleta commits that derived output to a dedicated deployment branch such as `gh-pages`.
5. GitHub Pages publishes directly from that branch.

Why this shape:

- `main` stays free of `site-content/` snapshots and Pages-specific workflow files.
- Deployment does not require CI access to local Recoleta state, local config files, or private output directories.
- The deployment branch remains an explicit, inspectable public artifact, but it is clearly segregated from source code.
- `run site build` and `stage site stage` still exist for custom CI or
  non-GitHub static hosts when an explicit repo-local snapshot is useful.

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
- Branch deployment rewrites a derived branch by default. This is appropriate for generated output, but it means branch history is operational rather than authorial.
- Browser PDF rendering improves layout quality but introduces a browser runtime dependency. The Story fallback absorbs that risk.
