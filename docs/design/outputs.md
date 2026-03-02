# Outputs

Recoleta publishes user-facing artifacts via **publish targets**. The default target is **local Markdown**, so the system is usable without configuring Obsidian or Telegram.

## Goals

- Allow running `recoleta publish` with **no Obsidian Vault** and **no Telegram Bot** configured.
- Provide a friendly, discoverable way to read outputs (plain Markdown on disk).
- Keep publish behavior idempotent and easy to reason about.

## Publish targets

Configured by:

- `PUBLISH_TARGETS` / `publish_targets` (default: `["markdown"]`)

Allowed values:

- `markdown`: write notes + `latest.md` under `MARKDOWN_OUTPUT_DIR`
- `obsidian`: write notes under `OBSIDIAN_VAULT_PATH/OBSIDIAN_BASE_FOLDER/Inbox/`
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

## Local Markdown layout

Under `MARKDOWN_OUTPUT_DIR`:

- `latest.md`: entry point for the most recent publish run
- `Runs/<run_id>.md`: per-run index (same content as `latest.md`)
- `Inbox/`: one note per published item

Each item note contains YAML frontmatter and the sections: `Summary`, `Links`.

## CLI UX

After `recoleta publish`, the CLI prints:

- counts (`sent`, `skipped`, `failed`)
- the local Markdown output directory and the path to `latest.md` (when `markdown` target is enabled)
