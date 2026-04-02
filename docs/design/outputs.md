# Outputs

Recoleta publishes user-facing artifacts across a few reading surfaces. The base contract is still simple: **Markdown notes are the canonical filesystem output**, and richer surfaces such as trend PDFs or static sites are derived from those notes.

## Goals

- Allow running `recoleta publish` with **no Obsidian Vault** and **no Telegram Bot** configured.
- Keep one canonical human-readable source on disk instead of maintaining multiple primary formats.
- Support denser, better-looking trend surfaces without making the core pipeline depend on a web app.
- Keep output behavior idempotent and easy to reason about.

## Publish targets

Configured by:

- `PUBLISH_TARGETS` / `publish_targets` (default: `["markdown"]`)

Allowed values:

- `markdown`: write item and trend notes under `MARKDOWN_OUTPUT_DIR`
- `obsidian`: write notes under `OBSIDIAN_VAULT_PATH/OBSIDIAN_BASE_FOLDER`
- `telegram`: send curated messages via Telegram Bot API

## Required settings by target

- `markdown`:
  - `MARKDOWN_OUTPUT_DIR` / `markdown_output_dir` (default: platform-specific user data dir + `/outputs`)
- `obsidian`:
  - `OBSIDIAN_VAULT_PATH` / `obsidian_vault_path`
  - `OBSIDIAN_BASE_FOLDER` / `obsidian_base_folder` (default: `Recoleta`)
- `telegram`:
  - `TELEGRAM_BOT_TOKEN` (env-only)
  - `TELEGRAM_CHAT_ID` (env-only)

Recoleta fails fast at the start of `publish` if a configured target is missing its required settings.

## Canonical markdown surfaces

Under `MARKDOWN_OUTPUT_DIR`:

- `latest.md`: entry point for the most recent item publish run
- `Runs/<run_id>.md`: per-run item index (same content as `latest.md`)
- `Inbox/`: one note per published item
- `Trends/`: canonical trend markdown notes plus adjacent
  `<stem>.presentation.json` sidecars
- `Ideas/`: idea briefs derived from canonical `trend_ideas` pass outputs plus
  adjacent `<stem>.presentation.json` sidecars
- `Localized/<language>/Inbox|Trends|Ideas/`: translated or mirrored reading
  surfaces derived from canonical outputs; localized trend and idea notes also
  emit adjacent `<stem>.presentation.json` sidecars
- `site/`: optional derived static site output from `recoleta run site build`

Historical note:

- older shared-stream deployments wrote `Streams/<stream>/Inbox/`,
  `Streams/<stream>/Trends/`, and `Streams/<stream>/latest.md`
- current versions do not read or write that layout

Item notes contain YAML frontmatter and sections such as `Summary` and `Links`.

Trend notes are the canonical source for all downstream trend surfaces:

- Telegram trend PDFs render from `MARKDOWN_OUTPUT_DIR/Trends/*.md`
- `recoleta run site build` discovers sibling trend and idea sidecars first for
  detail-page rendering and falls back to markdown parsing when sidecars are
  missing or invalid
- `recoleta stage site stage` mirrors trend markdown/PDF artifacts plus sibling
  trend and idea sidecars into a repo-local deployment directory
- `recoleta repair outputs` rerenders trend markdown from stored trend
  documents and can optionally refresh PDFs/site output in the same pass
- when available, trend note frontmatter also carries `pass_output_id` / `pass_kind` so projections can be traced back to canonical `trend_synthesis` output
- canonical trend markdown notes also emit adjacent `*.presentation.json`
  sidecars as a structured presentation contract for downstream adoption
- newly generated trend and idea sidecars write the current presentation schema
  and keep reader compatibility with older sidecars
- current trend sidecars can carry ranked shifts plus an optional
  `counter_signal`

Idea notes follow the same projection contract:

- `markdown` and `obsidian` idea notes are derived from canonical `trend_ideas` pass outputs
- canonical idea markdown notes also emit adjacent `*.presentation.json`
  sidecars in the same directory
- current idea sidecars carry best-bet ordering, alternates, optional
  `anti_thesis`, and evidence metadata
- searchable `doc_type=idea` documents are also derived projections, not canonical pass state
- idea note frontmatter and idea document meta chunks carry `pass_output_id` plus the upstream `trend_synthesis` pointer
- those provenance-bearing document `meta` chunks are system-only metadata: they are preserved for repair/audit, but excluded from agent-visible FTS/hybrid retrieval

Localized notes are projections, not canonical state:

- `recoleta run translate` writes incremental translations for canonical item,
  trend, and idea outputs
- `recoleta stage translate backfill` writes translated source-language
  overrides plus optional mirror variants for historical corpora
- localized notes are materialized under `MARKDOWN_OUTPUT_DIR/Localized/<language>/...`
- localized trend and idea notes emit adjacent `.presentation.json` sidecars at
  materialize time; localized item notes remain markdown-only
- translation and site rendering prefer sibling sidecars first and fall back to
  markdown parsing when those sidecars are missing or invalid
- canonical `analyses`, `pass_outputs`, and `documents` remain unchanged

## Trend PDF surface

When `telegram` delivery is enabled and the trend corpus is non-empty:

- Recoleta first writes the canonical trend markdown note.
- The PDF renderer consumes that markdown note rather than rendering directly from the LLM payload.
- The renderer uses `backend="auto"`:
  - browser rendering via Playwright + Chromium-compatible browser first
  - `PyMuPDF Story` fallback second
- Telegram trend PDFs use `page_mode="continuous"` so the reading surface is not constrained to A4 pagination.

The browser renderer uses an HTML/CSS card layout and embeds some gradients as PNG data URIs to avoid PDF viewer inconsistencies with vector gradients.

## Trend PDF debug bundle

`recoleta trends --debug-pdf` exports a debug bundle under:

- `MARKDOWN_OUTPUT_DIR/Trends/.pdf-debug/<pdf-stem>/`

Bundle contents:

- `source.md`
- `normalized.md`
- `document.html`
- `styles.css`
- `manifest.json`
- `page-<n>.png` previews

This keeps the canonical markdown unchanged while giving a reproducible record of the exact render inputs used for the PDF.

## Static trend site surface

The static site exporter turns trend markdown notes into a standalone website:

- `recoleta run site serve`: build the site locally and serve it on a loopback
  HTTP endpoint for preview
- `recoleta run site build`: render a clean static site to
  `MARKDOWN_OUTPUT_DIR/site` by default
- `recoleta run deploy`: build the public site and push a dedicated GitHub
  Pages branch (default: `gh-pages`)
- `recoleta stage site stage`: mirror trend markdown/PDF artifacts to
  `./site-content/Trends` by default

Important behavior:

- `recoleta run site serve` uses Python's standard-library HTTP server; it is a
  preview helper, not a full dev server.
- `recoleta repair outputs` is the offline repair path for existing outputs: it
  backfills item notes, repairs sibling Obsidian notes when settings expose a
  vault path, rerenders trend markdown from stored DB documents without
  mutating upstream ingest/analyze state, and can optionally refresh
  site/PDF artifacts.
- when stored trend/idea state exists, the same repair flow also refreshes
  sibling trend/idea sidecars instead of leaving regenerated markdown on an
  older projection contract.
- when stored trend/idea metadata includes projection provenance,
  `recoleta repair outputs` preserves that provenance in the regenerated
  markdown/obsidian notes instead of dropping it.
- in the instance-first runtime, `recoleta repair outputs` always repairs the
  current child instance output tree; choose the target child instance with
  `--config-path` when needed.
- `recoleta repair outputs` does not rebuild derived `documents` projections
  from pass outputs; searchable corpus repair stays separate from
  filesystem/site repair on purpose.
- All commands that rebuild site output treat their output directories as managed artifacts and clear stale files before writing.
- When `--input-dir` and `--output-dir` are passed explicitly, they do not require a full Recoleta runtime config. This is intentional so CI and GitHub Pages can build from a staged content snapshot.
- When multilingual content exists, the exporter emits one site subtree per language, for example `/en/...` and `/zh-cn/...`, plus a root `index.html` redirect page.
- The root redirect prefers the browser's remembered language and then falls back to the configured default language.
- Every page renders a language switcher that stores the chosen language in the browser and routes to the peer page when available.
- `--default-language-code` is required for multilingual exports only when the exporter is running without runtime settings that already expose `localization.site_default_language_code`.
- `recoleta run deploy` keeps `main` free of committed site snapshots and
  Pages-specific workflow files by publishing a derived branch instead.
- `recoleta stage site stage` remains useful for custom CI pipelines and
  non-GitHub static hosts when you want an explicit repo-local snapshot.
- trend and idea detail pages prefer sibling `*.presentation.json` sidecars and
  fall back to markdown parsing so older Phase 1 artifacts remain buildable.
- Historical note: the older shared-stream runtime aggregated stream-local
  `Trends/` trees and exposed a `Streams` navigation surface. The current
  instance-first runtime keeps one canonical output tree per child instance and
  uses fleet-level aggregation when you want a combined site.

## CLI UX

After `recoleta publish`, the CLI prints:

- counts (`sent`, `skipped`, `failed`)
- the local Markdown output directory and the path to `latest.md` (when `markdown` target is enabled)

After `recoleta trends`, the CLI prints:

- trend completion info (`doc_id`, `granularity`, `period_start`, `period_end`)
- the billing report table

After `recoleta run site serve` / `recoleta run site build` /
`recoleta stage site stage` / `recoleta run deploy`, the CLI prints:

- exported trend/topic counts
- output directory path

After `recoleta repair outputs`, the CLI prints:

- per-instance item/trend/pdf totals
- trend materialization failures and canonical-link rewrite totals
- site manifest path when `--site` is enabled
