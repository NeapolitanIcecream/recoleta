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

- `LLM_OUTPUT_LANGUAGE`: preferred output language for LLM-generated `summary`.
  - JSON keys remain English.
  - `topics` remain concise English tags for downstream allow/deny filtering.
  - Empty value means unset.

## Source configuration

These can be provided as a JSON/YAML string or a config file.

Recommended fields:

- `SOURCES`:
  - `arxiv`:
    - `enabled`: bool (default `false`). All sources are disabled by default and must be explicitly enabled.
    - `queries`: list of arXiv query strings
    - `max_results_per_run`
    - `enrich_method`: `pdf_text|latex_source|html_document` (default `html_document`)
    - `enrich_failure_mode`: `fallback|strict` (default `fallback`)
    - `html_document_max_concurrency`: max parallel workers for `enrich_method=html_document` (default `4`)
    - `html_document_enable_parallel`: enable bounded parallel enrich for `enrich_method=html_document` (default `true`)
    - `html_document_requests_per_second`: global throttle for arXiv HTML fetches across workers (default `2.0`)
    - `html_document_log_sample_rate`: in parallel mode, keep per-item info logs sampled and demote the rest to debug (default `0.05`)
    - `html_document_skip_cleanup_when_complete`: skip cleanup/conversion when `html_document_md` is already present (default `true`)
    - `html_document_use_batched_db_writes`: batch content upserts into fewer commits to reduce SQLite lock contention (default `true`)
  - `hn`:
    - `enabled`: bool (default `false`)
    - `rss_urls`: list (e.g. `https://news.ycombinator.com/rss`)
  - `hf_daily`:
    - `enabled`: bool
  - `openreview`:
    - `enabled`: bool (default `false`)
    - `venues`: list (conference ids)
  - `rss`:
    - `enabled`: bool (default `false`)
    - `feeds`: list of newsletter RSS URLs

Notes:

- When `SOURCES.arxiv.enrich_method=html_document`, Recoleta stores the cleaned HTML as `html_document` and (when Pandoc is available) also generates `html_document_md`, which is preferred for Stage 4 analysis.

Example:

```yaml
SOURCES:
  arxiv:
    enabled: true
    queries:
      - cat:cs.AI
    max_results_per_run: 50
    enrich_method: latex_source
    enrich_failure_mode: strict
  rss:
    enabled: true
    feeds:
      - https://example.com/feed.xml
```

## Topic and ranking configuration

- `TOPICS`: list of user topics (strings). These are used for LLM relevance scoring.
- `MIN_RELEVANCE_SCORE`: float (default 0.6)
- `MAX_DELIVERIES_PER_DAY`: int (default 10)
- `TITLE_DEDUP_THRESHOLD`: float (default 92.0 for rapidfuzz ratio)
- `TITLE_DEDUP_MAX_CANDIDATES`: int (default 500)

### Semantic triage (pre-ranking before LLM) (optional)

These settings control an optional semantic pre-ranking stage that runs before Stage 4 (Analyze/LLM). See `docs/design/semantic-pre-ranking.md`.

- `TRIAGE_ENABLED`: bool (default false)
- `TRIAGE_MODE`: `prioritize|filter` (default `prioritize`)
- `TRIAGE_EMBEDDING_MODEL`: string (default `text-embedding-3-small`)
- `TRIAGE_EMBEDDING_DIMENSIONS`: int (optional; only for supported embedding models)
- `TRIAGE_EMBEDDING_BATCH_MAX_INPUTS`: int (default 64)
- `TRIAGE_EMBEDDING_BATCH_MAX_CHARS`: int (default 40000)
- `TRIAGE_QUERY_MODE`: `joined|max_per_topic` (default `joined`)
- `TRIAGE_CANDIDATE_FACTOR`: int (default 5)
- `TRIAGE_MAX_CANDIDATES`: int (default 500)
- `TRIAGE_ITEM_TEXT_MAX_CHARS`: int (default 1200)
- `TRIAGE_MIN_SIMILARITY`: float (default 0.0; only used in `filter` mode)
- `TRIAGE_EXPLORATION_RATE`: float (default 0.05)
- `TRIAGE_RECENCY_FLOOR`: int (default 5)

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

