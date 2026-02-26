# Configuration

Recoleta uses typed configuration loaded from environment variables (and optionally a config file). Secrets are read from env only and must never be written to disk.

## Optional config file

Recoleta can load non-secret settings from a local YAML/JSON config file pointed to by:

- `RECOLETA_CONFIG_PATH`: absolute or `~`-expanded path to a `.yaml`, `.yml`, or `.json` file.

Precedence:

- Initialization arguments (rare) > environment variables > config file > defaults

Secrets:

- `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` are **forbidden** in the config file and must come from environment variables.

## Required settings

- `RECOLETA_DB_PATH`: path to the SQLite file (e.g. `~/.local/share/recoleta/recoleta.db`).
- `LLM_MODEL`: default model name (LiteLLM format), e.g. `openai/gpt-4o-mini`.
- `PUBLISH_TARGETS` (default `["markdown"]`): publish targets, allowed values: `markdown|obsidian|telegram`.
- `MARKDOWN_OUTPUT_DIR` (default: platform-specific user data dir + `/outputs`): local Markdown output directory.

## Conditionally required settings

- `OBSIDIAN_VAULT_PATH`: required when `PUBLISH_TARGETS` includes `obsidian`.
- `TELEGRAM_BOT_TOKEN`: required when `PUBLISH_TARGETS` includes `telegram` (env-only).
- `TELEGRAM_CHAT_ID`: required when `PUBLISH_TARGETS` includes `telegram` (env-only).

Optional LLM behavior:

- `LLM_OUTPUT_LANGUAGE`: preferred output language for LLM-generated `summary`, `insight`, and `idea_directions`.
  - JSON keys remain English.
  - `topics` remain concise English tags for downstream allow/deny filtering.
  - Empty value means unset.

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
- `TITLE_DEDUP_MAX_CANDIDATES`: int (default 500)

## Scheduling

Choose one:

- External: use cron/launchd, no scheduler config needed.
- Internal (`recoleta run`): configure job intervals:
  - `INGEST_INTERVAL_MINUTES` (default 60)
  - `ANALYZE_INTERVAL_MINUTES` (default 120)
  - `PUBLISH_INTERVAL_MINUTES` (default 120)

## Outputs

- `ARTIFACTS_DIR` (required when `WRITE_DEBUG_ARTIFACTS=true`): where to write raw/debug artifacts (outside the Vault is fine).
- `OBSIDIAN_BASE_FOLDER` (default `Recoleta`): base folder under the Vault.
- `PUBLISH_TARGETS` (default `["markdown"]`): which publish integrations are enabled.
- `MARKDOWN_OUTPUT_DIR`: where local Markdown output is written (e.g. `latest.md`, `Inbox/`, `Runs/`).

## Logging and diagnostics

- `LOG_LEVEL` (default `INFO`)
- `LOG_JSON` (default false): if true, emit JSON logs (recommended for automation).
- `WRITE_DEBUG_ARTIFACTS` (default false): if true, write scrubbed debug JSON for failures and LLM calls.

## Secret handling rules

- Secrets must only come from env (or OS keychain in a future version).
- Debug artifacts must be scrubbed (remove tokens, headers, cookies).
- Logs must never include raw secrets.

