# Configuration

Recoleta uses typed configuration loaded from environment variables (and optionally a config file). Secrets are read from env only and must never be written to disk.

## Required settings

- `OBSIDIAN_VAULT_PATH`: absolute path to the Obsidian Vault root directory.
- `RECOLETA_DB_PATH`: path to the SQLite file (e.g. `~/.local/share/recoleta/recoleta.db`).
- `TELEGRAM_BOT_TOKEN`: Telegram bot token (secret).
- `TELEGRAM_CHAT_ID`: chat id or channel username (secret-ish; treat as sensitive).
- `LLM_MODEL`: default model name (LiteLLM format), e.g. `openai/gpt-4o-mini`.

## Source configuration

These can be provided as a JSON/YAML string or a config file.

Recommended fields:

- `SOURCES`:
  - `arxiv`:
    - `queries`: list of arXiv query strings
    - `max_results_per_run`
  - `hn`:
    - `rss_urls`: list (e.g. `https://news.ycombinator.com/rss`)
  - `hf_daily`:
    - `enabled`: bool
  - `openreview`:
    - `venues`: list (conference ids)
  - `rss`:
    - `feeds`: list of newsletter RSS URLs

## Topic and ranking configuration

- `TOPICS`: list of user topics (strings). These are used for LLM relevance scoring.
- `MIN_RELEVANCE_SCORE`: float (default 0.6)
- `MAX_DELIVERIES_PER_DAY`: int (default 10)
- `TITLE_DEDUP_THRESHOLD`: float (default 92.0 for rapidfuzz ratio)

## Scheduling

Choose one:

- External: use cron/launchd, no scheduler config needed.
- Internal (`recoleta run`): configure job intervals:
  - `INGEST_INTERVAL_MINUTES` (default 60)
  - `ANALYZE_INTERVAL_MINUTES` (default 120)
  - `PUBLISH_INTERVAL_MINUTES` (default 120)

## Outputs

- `ARTIFACTS_DIR` (optional): where to write raw/debug artifacts (outside the Vault is fine).
- `OBSIDIAN_BASE_FOLDER` (default `Recoleta`): base folder under the Vault.

## Logging and diagnostics

- `LOG_LEVEL` (default `INFO`)
- `LOG_JSON` (default false): if true, emit JSON logs (recommended for automation).
- `WRITE_DEBUG_ARTIFACTS` (default false): if true, write scrubbed debug JSON for failures and LLM calls.

## Secret handling rules

- Secrets must only come from env (or OS keychain in a future version).
- Debug artifacts must be scrubbed (remove tokens, headers, cookies).
- Logs must never include raw secrets.

