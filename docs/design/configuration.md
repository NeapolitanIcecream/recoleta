# Configuration

Recoleta uses typed configuration loaded from environment variables, `.env`, and an optional config file. Secrets are read from env only and must never be written to disk.

## Optional config file

Recoleta can load non-secret settings from a local YAML/JSON config file pointed to by:

- `RECOLETA_CONFIG_PATH`: absolute or `~`-expanded path to a `.yaml`, `.yml`, or `.json` file.

Precedence:

- Initialization arguments (rare) > environment variables > `.env` > config file > defaults

Secrets:

- `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, and `RECOLETA_LLM_API_KEY` are **forbidden** in the config file and must come from environment variables.

## Required settings

- `RECOLETA_DB_PATH`: path to the SQLite file (e.g. `~/.local/share/recoleta/recoleta.db`).
- `LLM_MODEL`: default model name (LiteLLM format), e.g. `openai/gpt-5.4`.
- `PUBLISH_TARGETS` (default `["markdown"]`): publish targets, allowed values: `markdown|obsidian|telegram`.
- `MARKDOWN_OUTPUT_DIR` (default: platform-specific user data dir + `/outputs`): local Markdown output directory.

## Conditionally required settings

- `OBSIDIAN_VAULT_PATH`: required when `PUBLISH_TARGETS` includes `obsidian`.
- `TELEGRAM_BOT_TOKEN`: required when `PUBLISH_TARGETS` includes `telegram` (env-only).
- `TELEGRAM_CHAT_ID`: required when `PUBLISH_TARGETS` includes `telegram` (env-only).

Optional LLM behavior:

- `RECOLETA_LLM_API_KEY`: Recoleta-scoped API key override for LiteLLM / PydanticAI calls (env-only).
- `RECOLETA_LLM_BASE_URL`: Recoleta-scoped base URL override for OpenAI-compatible or OpenRouter endpoints.
- `LLM_OUTPUT_LANGUAGE`: canonical language label for newly generated LLM output such as item summaries, trend briefs, and idea briefs.
  - JSON keys remain English.
  - `topics` remain concise English tags for downstream allow/deny filtering.
  - Empty value means unset.

## Localization (optional)

Use `LOCALIZATION` / `localization` when one language remains canonical in
SQLite and one or more additional language variants should be stored in
`localized_outputs`, materialized under `MARKDOWN_OUTPUT_DIR/Localized/<code>/`,
and exported into a multilingual static site.

- `LOCALIZATION.source_language_code`: canonical language code for new output, for example `en`.
- `LOCALIZATION.targets`: derived language variants.
  - `code`: language code, for example `zh-CN`.
  - `llm_label`: prompt label passed to the translation model, for example `Chinese (Simplified)`.
- `LOCALIZATION.site_default_language_code`: default site language when multilingual site export is enabled.
- `LOCALIZATION.legacy_backfill_source_language_code`: language code used by historical canonical rows during `recoleta translate backfill`.

Validation rules:

- target codes must be unique
- a target code must not duplicate `source_language_code`
- `site_default_language_code` must match either `source_language_code` or one configured target code
- when `targets` is non-empty, `LLM_OUTPUT_LANGUAGE` must be set

Operational notes:

- `recoleta translate run` fills derived translations for new canonical rows.
- `recoleta translate backfill` projects historical canonical content into the configured `source_language_code` without rewriting `analyses`, `pass_outputs`, or `documents`.

Example:

```yaml
llm_output_language: "English"

localization:
  source_language_code: "en"
  site_default_language_code: "en"
  legacy_backfill_source_language_code: "zh-CN"
  targets:
    - code: "zh-CN"
      llm_label: "Chinese (Simplified)"
```

## Source configuration

These can be provided as a JSON/YAML string or a config file.

Recommended fields:

- `SOURCES`:
  - `arxiv`:
    - `enabled`: bool (default `false`). All sources are disabled by default and must be explicitly enabled.
    - `queries`: list of arXiv query strings
    - `max_results_per_run`
    - `max_total_per_run`
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
    - `max_items_per_feed`
    - `max_total_per_run`
  - `hf_daily`:
    - `enabled`: bool
    - `max_items_per_run`
  - `openreview`:
    - `enabled`: bool (default `false`)
    - `venues`: list (conference ids)
    - `max_results_per_venue`
    - `max_total_per_run`
  - `rss`:
    - `enabled`: bool (default `false`)
    - `feeds`: list of newsletter RSS URLs
    - `max_items_per_feed`
    - `max_total_per_run`

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
- `TOPIC_STREAMS`: optional list of virtual topic streams. Each stream shares ingest/enrich state with the same Recoleta instance, but runs its own analyze/publish path.
  - Use `TOPIC_STREAMS` when one user wants multiple topic domains to be processed and delivered independently.
  - Do not set `TOPICS` together with `TOPIC_STREAMS`.
  - Each stream supports:
    - `name`: stable stream identifier (used in metrics, DB scope, and default output paths)
    - `topics`: list of topics for that stream
    - `allow_tags` / `deny_tags`: optional stream-local publish filters; omit or set `null` to inherit the global filters, use `[]` to clear inherited filters explicitly
    - `publish_targets`: optional override for `markdown|obsidian|telegram`
    - `markdown_output_dir`: optional absolute output dir override
    - `obsidian_base_folder`: optional Obsidian subfolder override
    - `min_relevance_score`, `max_deliveries_per_day`: optional per-stream overrides
    - `telegram_bot_token_env`, `telegram_chat_id_env`: optional env var names for stream-local Telegram credentials
  - Default stream output locations:
    - Markdown: `MARKDOWN_OUTPUT_DIR/Streams/<name>/`
    - Obsidian: `OBSIDIAN_BASE_FOLDER/Streams/<name>/`
  - Existing single-stream behavior is unchanged when `TOPIC_STREAMS` is omitted.
  - Trend generation follows the same split:
    - `recoleta trends` indexes item documents per stream scope
    - generated trend docs are stored per stream scope
    - Markdown/Obsidian trend notes are written under each stream's output root
- `MIN_RELEVANCE_SCORE`: float (default 0.6)
- `MAX_DELIVERIES_PER_DAY`: int (default 10)
- `TITLE_DEDUP_THRESHOLD`: float (default 92.0 for rapidfuzz ratio)
- `TITLE_DEDUP_MAX_CANDIDATES`: int (default 500)

## Analyze and write-path controls

- `ANALYZE_LIMIT`: default max number of items analyzed in one run (default `100`)
- `ANALYZE_WRITE_BATCH_SIZE`: batch size for persisting analysis rows (default `32`)
- `ANALYZE_CONTENT_MAX_CHARS`: truncate loaded source content before Stage 4; set `0` to disable truncation (default `32768`)

Example:

```yaml
TOPIC_STREAMS:
  - name: agents_lab
    topics:
      - agents
      - tool-use
    publish_targets:
      - markdown
      - telegram
    telegram_bot_token_env: AGENTS_LAB_TELEGRAM_BOT_TOKEN
    telegram_chat_id_env: AGENTS_LAB_TELEGRAM_CHAT_ID
  - name: biology_watch
    topics:
      - biology
      - therapeutics
```

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

## Trends RAG and context packs

Trend generation can augment prompts with semantic retrieval and bounded history. These settings are shared by on-demand trend runs and the explicit `recoleta rag` maintenance commands.

- `RAG_LANCEDB_DIR`: path to the local LanceDB workspace used for trend semantic search (default: platform-specific user data dir + `/lancedb`)
- `TRENDS_EMBEDDING_MODEL`: embedding model for trend search / vector sync (default `text-embedding-3-small`)
- `TRENDS_EMBEDDING_DIMENSIONS`: optional embedding dimensions override
- `TRENDS_EMBEDDING_BATCH_MAX_INPUTS`: max texts per embedding batch (default `64`)
- `TRENDS_EMBEDDING_BATCH_MAX_CHARS`: char budget per embedding batch (default `40000`)
- `TRENDS_EMBEDDING_FAILURE_MODE`: `continue|fail_fast|threshold` (default `continue`)
- `TRENDS_EMBEDDING_MAX_ERRORS`: required and `> 0` when `TRENDS_EMBEDDING_FAILURE_MODE=threshold`
- `TRENDS_SELF_SIMILAR_ENABLED`: enable the overview-pack retrieval flow that ranks related docs and backfills cluster representatives
- `TRENDS_RANKING_N`: number of ranked retrieval hits passed into representative selection (default `10`)
- `TRENDS_OVERVIEW_PACK_MAX_CHARS`: char budget for the generated overview pack injected into the trend prompt (default `16000`)
- `TRENDS_ITEM_OVERVIEW_TOP_K`: max analyzed items folded into day-trend overview packs (default `28`)
- `TRENDS_ITEM_OVERVIEW_ITEM_MAX_CHARS`: per-item char budget when building day-trend overview packs (default `800`)
- `TRENDS_REP_MIN_PER_CLUSTER`: minimum representatives preserved/backfilled per cluster (default `2`)
- `TRENDS_PEER_HISTORY_ENABLED`: enable bounded prior-window context for trend evolution notes (default `true`)
- `TRENDS_PEER_HISTORY_WINDOW_COUNT`: number of earlier peer windows to include (default `3`)
- `TRENDS_PEER_HISTORY_MAX_CHARS`: char budget for the peer-history pack (default `12000`)
- `TRENDS_EVOLUTION_MAX_SIGNALS`: max evolution signals kept after normalization (default `5`)

Operational notes:

- Normal `recoleta trends` runs can sync missing vectors on demand.
- `recoleta rag sync-vectors` is the explicit prewarm / repair path for large backfills or offline preparation.
- `recoleta rag build-index` builds ANN/scalar indices for the current LanceDB embedding table after vector sync succeeds.

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
- `MARKDOWN_OUTPUT_DIR`: where local Markdown output is written (e.g. `latest.md`, `Inbox/`, `Runs/`, `Trends/`, `Ideas/`, `Localized/<language>/...`, and derived `site/` output).
- When `TOPIC_STREAMS` is enabled, Markdown defaults to `MARKDOWN_OUTPUT_DIR/Streams/<stream>/...` for stream-local notes and trend surfaces.

### Browser trend PDF rendering

Trend PDFs are rendered from canonical trend markdown notes. The browser renderer probes browser executables in this order:

- `RECOLETA_PLAYWRIGHT_EXECUTABLE_PATH`
- `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH`
- `GOOGLE_CHROME_BIN`
- `CHROME_BIN`
- common Chrome / Chromium / Edge install locations
- Playwright's default Chromium launcher

Notes:

- Telegram trend delivery uses browser rendering first and falls back to the Story renderer when browser launch or browser PDF export fails.
- `recoleta trends --debug-pdf` is a CLI flag, not a persistent config setting. It exports a per-render debug bundle under `MARKDOWN_OUTPUT_DIR/Trends/.pdf-debug/`.
- `recoleta materialize outputs --pdf --debug-pdf` uses the same debug-bundle contract when regenerating PDFs offline.
- `recoleta site build --input-dir ... --output-dir ...` and `recoleta site stage --input-dir ... --output-dir ...` intentionally work without loading the full runtime config so CI can build from staged trend notes only.
- In `TOPIC_STREAMS` mode, `recoleta site build` auto-discovers `MARKDOWN_OUTPUT_DIR/Streams/<stream>/Trends/` and `recoleta site stage` mirrors them under `./site-content/Streams/<stream>/Trends/` by default.
- When localized markdown trees are present, `recoleta site build`, `recoleta site stage`, `recoleta site serve`, and `recoleta site gh-deploy` use `LOCALIZATION.site_default_language_code` by default when runtime settings are loaded. Use `--default-language-code <code>` when building from explicit input/output paths without full config loading.

## Logging and diagnostics

- `LOG_LEVEL` (default `INFO`)
- `LOG_JSON` (default false): if true, emit JSON logs (recommended for automation).
- `WRITE_DEBUG_ARTIFACTS` (default false): if true, write scrubbed debug JSON for failures and LLM calls.

## Secret handling rules

- Secrets must only come from env (or OS keychain in a future version).
- Debug artifacts must be scrubbed (remove tokens, headers, cookies).
- Logs must never include raw secrets.
