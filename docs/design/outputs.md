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
- `site/`: optional derived static site output from `recoleta site build`

Item notes contain YAML frontmatter and sections such as `Summary` and `Links`.

Trend notes are the canonical source for all downstream trend surfaces:

- Telegram trend PDFs render from `MARKDOWN_OUTPUT_DIR/Trends/*.md`
- `recoleta site build` renders from a trend markdown directory
- `recoleta site stage` mirrors trend markdown/PDF artifacts into a repo-local deployment directory

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

- `recoleta site build`: render a clean static site to `MARKDOWN_OUTPUT_DIR/site` by default
- `recoleta site stage`: mirror trend markdown/PDF artifacts to `./site-content/Trends` by default for repository-based deployment

Important behavior:

- Both commands treat their output directories as managed artifacts and clear stale files before writing.
- When `--input-dir` and `--output-dir` are passed explicitly, they do not require a full Recoleta runtime config. This is intentional so CI and GitHub Pages can build from a staged content snapshot.
- The default GitHub Pages workflow builds `site-dist/` from `site-content/Trends/`.

## CLI UX

After `recoleta publish`, the CLI prints:

- counts (`sent`, `skipped`, `failed`)
- the local Markdown output directory and the path to `latest.md` (when `markdown` target is enabled)

After `recoleta trends`, the CLI prints:

- trend completion info (`doc_id`, `granularity`, `period_start`, `period_end`)
- the billing report table

After `recoleta site build` / `recoleta site stage`, the CLI prints:

- exported trend/topic counts
- output directory path
