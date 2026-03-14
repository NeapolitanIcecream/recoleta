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
- `Trends/`: canonical trend markdown notes
- `Ideas/`: idea briefs derived from canonical `trend_ideas` pass outputs
- `site/`: optional derived static site output from `recoleta site build`

When `TOPIC_STREAMS` is configured, each stream gets its own subtree instead:

- `Streams/<stream>/Inbox/`
- `Streams/<stream>/Trends/`
- `Streams/<stream>/latest.md`

Item notes contain YAML frontmatter and sections such as `Summary` and `Links`.

Trend notes are the canonical source for all downstream trend surfaces:

- Telegram trend PDFs render from `MARKDOWN_OUTPUT_DIR/Trends/*.md`
- `recoleta site build` renders from a trend markdown directory
- `recoleta site stage` mirrors trend markdown/PDF artifacts into a repo-local deployment directory
- `recoleta materialize outputs` rerenders trend markdown from stored trend documents and can optionally refresh PDFs/site output in the same pass
- when available, trend note frontmatter also carries `pass_output_id` / `pass_kind` so projections can be traced back to canonical `trend_synthesis` output

Idea notes follow the same projection contract:

- `markdown` and `obsidian` idea notes are derived from canonical `trend_ideas` pass outputs
- searchable `doc_type=idea` documents are also derived projections, not canonical pass state
- idea note frontmatter and idea document meta chunks carry `pass_output_id` plus the upstream `trend_synthesis` pointer
- those provenance-bearing document `meta` chunks are system-only metadata: they are preserved for repair/audit, but excluded from agent-visible FTS/hybrid retrieval

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

- `recoleta site serve`: build the site locally and serve it on a loopback HTTP endpoint for preview
- `recoleta site build`: render a clean static site to `MARKDOWN_OUTPUT_DIR/site` by default
- `recoleta site gh-deploy`: build the public site and push a dedicated GitHub Pages branch (default: `gh-pages`)
- `recoleta site stage`: mirror trend markdown/PDF artifacts to `./site-content/Trends` by default, or `./site-content/Streams/<stream>/Trends` in topic-stream mode

Important behavior:

- `recoleta site serve` uses Python's standard-library HTTP server; it is a preview helper, not a full dev server.
- `recoleta materialize outputs` is the offline repair path for existing outputs: it backfills item notes, repairs sibling Obsidian notes when settings expose a vault path, rerenders trend markdown from stored DB documents without mutating upstream ingest/analyze state, and can optionally refresh site/PDF artifacts.
- when stored trend/idea metadata includes projection provenance, `recoleta materialize outputs` preserves that provenance in the regenerated markdown/obsidian notes instead of dropping it.
- `recoleta materialize outputs --scope <stream>` lets you repair a single stream without rewriting every configured stream.
- `recoleta materialize outputs` does not rebuild derived `documents` projections from pass outputs; searchable corpus repair stays separate from filesystem/site repair on purpose.
- All commands that rebuild site output treat their output directories as managed artifacts and clear stale files before writing.
- When `--input-dir` and `--output-dir` are passed explicitly, they do not require a full Recoleta runtime config. This is intentional so CI and GitHub Pages can build from a staged content snapshot.
- `recoleta site gh-deploy` keeps `main` free of committed site snapshots and Pages-specific workflow files by publishing a derived branch instead.
- `recoleta site stage` remains useful for custom CI pipelines and non-GitHub static hosts when you want an explicit repo-local snapshot.
- In topic-stream mode, `recoleta site build` and `recoleta site gh-deploy` aggregate stream-local `Trends/` trees and expose a `Streams` navigation surface instead of flattening mixed domains together.

## CLI UX

After `recoleta publish`, the CLI prints:

- counts (`sent`, `skipped`, `failed`)
- the local Markdown output directory and the path to `latest.md` (when `markdown` target is enabled)

After `recoleta trends`, the CLI prints:

- trend completion info (`doc_id`, `granularity`, `period_start`, `period_end`)
- the billing report table

After `recoleta site serve` / `recoleta site build` / `recoleta site stage` / `recoleta site gh-deploy`, the CLI prints:

- exported trend/topic counts
- output directory path

After `recoleta materialize outputs`, the CLI prints:

- per-scope item/trend/pdf totals
- trend materialization failures and canonical-link rewrite totals
- site manifest path when `--site` is enabled
