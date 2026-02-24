# Recoleta

Recoleta is a personal research intelligence funnel that ingests source items,
analyzes them with an LLM, and publishes curated outputs to Obsidian and Telegram.

## CLI

- `recoleta ingest`
- `recoleta analyze`
- `recoleta publish`
- `recoleta run`

## Required environment variables

- `OBSIDIAN_VAULT_PATH`
- `RECOLETA_DB_PATH`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`
- `LLM_MODEL`

## Optional configuration file

- `RECOLETA_CONFIG_PATH`: path to a `.yaml`/`.yml`/`.json` file for non-secret settings.
  - Secrets (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`) must still come from environment variables.

## Development

```bash
uv run pytest
uv run ruff check .
```
