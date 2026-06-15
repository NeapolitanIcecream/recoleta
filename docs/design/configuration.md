# Configuration

Recoleta uses typed configuration loaded from environment variables, `.env`, and an optional config file. Secrets are read from env only and must never be written to disk.

## Optional config file

Recoleta can load non-secret settings from a local YAML/JSON config file pointed to by:

- `RECOLETA_CONFIG_PATH`: absolute or `~`-expanded path to a `.yaml`, `.yml`, or `.json` file.

Precedence:

- Initialization arguments (rare) > environment variables > `.env` > config file > defaults

Secrets:

- `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `RECOLETA_LLM_API_KEY`, and
  `RECOLETA_RESEND_API_KEY` are **forbidden** in the config file and must come
  from environment variables.

## Required settings

- `RECOLETA_DB_PATH`: path to the SQLite file (e.g. `~/.local/share/recoleta/recoleta.db`).
- `LLM_MODEL`: default model name (LiteLLM format), e.g. `openai/gpt-5.4`.
- `PUBLISH_TARGETS` (default `["markdown"]`): publish targets, allowed values: `markdown|obsidian|telegram`.
- `MARKDOWN_OUTPUT_DIR` (default: platform-specific user data dir + `/outputs`): local Markdown output directory.

## Conditionally required settings

- `OBSIDIAN_VAULT_PATH`: required when `PUBLISH_TARGETS` includes `obsidian`.
- `TELEGRAM_BOT_TOKEN`: required when `PUBLISH_TARGETS` includes `telegram` (env-only).
- `TELEGRAM_CHAT_ID`: required when `PUBLISH_TARGETS` includes `telegram` (env-only).
- `RECOLETA_RESEND_API_KEY`: required for `recoleta run email send` and
  `recoleta fleet run email send` (env-only).
- `ARXIV_POOL.huldra_base_url`: required when `SOURCES.arxiv.mode=pool`,
  `ARXIV_POOL.enabled=true`, and `ARXIV_POOL.backend=huldra`.
- `ARXIV_POOL.db_path`: required when `SOURCES.arxiv.mode=pool`,
  `ARXIV_POOL.enabled=true`, and `ARXIV_POOL.backend=local_sqlite`.

Optional LLM behavior:

- `RECOLETA_LLM_API_KEY`: Recoleta-scoped API key override for LiteLLM / PydanticAI calls (env-only).
- `RECOLETA_LLM_BASE_URL`: Recoleta-scoped base URL override for OpenAI-compatible or OpenRouter endpoints.
- `LLM_OUTPUT_LANGUAGE`: canonical language label for newly generated LLM output such as item summaries, trend notes, and idea notes.
  - JSON keys remain English.
  - `topics` remain concise English tags for downstream allow/deny filtering.
  - Empty value means unset.

## Manual trend email (optional)

Manual trend email is configured separately from `PUBLISH_TARGETS`. It is not a
publish target and it is not part of `run publish`.

- `EMAIL.public_site_url`: required absolute base URL for the already deployed
  public site. `run email send` refuses to send any selected granularity unless
  every send-target trend detail page resolves under this base URL and is
  publicly reachable.
- `EMAIL.from_email`: required sender address.
- `EMAIL.from_name`: optional sender display name (default `Recoleta`).
- `EMAIL.to`: required list of recipients.
- `EMAIL.granularities`: required ordered list of selection windows,
  containing one or more of `day|week|month`.
- `EMAIL.language_code`: optional language filter for multilingual output; when
  unset, `run email` uses the current settings' default site language.
- `EMAIL.max_clusters`: max rendered trend clusters per email (default `3`).
- `EMAIL.max_evidence_per_cluster`: max rendered evidence links per cluster
  (default `2`).
- `EMAIL.subject_prefix`: optional subject prefix (default `[Recoleta]`).

Operational notes:

- `recoleta run email preview` is batch-first. It reads canonical trend
  markdown plus sibling `*.presentation.json` sidecars, renders every selected
  granularity in memory first, and writes one preview root under
  `MARKDOWN_OUTPUT_DIR/.recoleta-email/previews/...` only if the full selected
  set succeeds.
- `recoleta run email send` is batch-first. It re-renders from the same
  inputs, performs full preflight across the effective selected set, writes one
  send root under `MARKDOWN_OUTPUT_DIR/.recoleta-email/sends/...`, sends via
  Resend only after preflight passes, and persists dedupe-oriented state in
  `trend_deliveries`.
- Both commands require the private site email link-map artifact written by the
  last site build. With the default site output path, that artifact is
  `MARKDOWN_OUTPUT_DIR/.site-email-links.json`.
- `run email preview` and `run email send` accept repeatable `--granularity`
  selectors. The effective batch always preserves the configured
  `EMAIL.granularities` order after filtering.
- `run email send` rejects mixed partially sent recipient state unless the
  operator passes `--force-batch`. `--force-batch` applies only to the selected
  granularity set.

Example:

```yaml
email:
  public_site_url: "https://example.github.io/recoleta"
  from_email: "recoleta@example.com"
  from_name: "Recoleta"
  to:
    - "you@example.com"
  granularities:
    - "day"
    - "week"
  language_code: "en"
  max_clusters: 3
  max_evidence_per_cluster: 2
  subject_prefix: "[Recoleta]"
```

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
- `LOCALIZATION.legacy_backfill_source_language_code`: language code used by
  historical canonical rows during `recoleta stage translate backfill`.

Validation rules:

- target codes must be unique
- a target code must not duplicate `source_language_code`
- `site_default_language_code` must match either `source_language_code` or one configured target code
- when `targets` is non-empty, `LLM_OUTPUT_LANGUAGE` must be set

Operational notes:

- `recoleta run translate` fills derived translations for new canonical rows.
- `recoleta stage translate backfill` projects historical canonical content
  into the configured `source_language_code` without rewriting `analyses`,
  `pass_outputs`, or `documents`.

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
    - `mode`: `direct|pool` (default `direct`). Use `pool` when Recoleta should read arXiv metadata from the configured arXiv pool backend.
    - `queries`: list of arXiv query strings
    - `max_results_per_run`
    - `max_total_per_run`
    - `enrich_method`: `pdf_text|latex_source|html_document` (default `html_document`)
    - `enrich_failure_mode`: `fallback|strict` (default `fallback`)
    - `html_document_max_concurrency`: max parallel workers for `enrich_method=html_document` (default `1`)
    - `html_document_enable_parallel`: enable bounded parallel enrich for `enrich_method=html_document` (default `true`)
    - `html_document_requests_per_second`: global throttle for arXiv HTML fetches across workers (default `0.0667`, about one request every 15 seconds)
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
- When `SOURCES.arxiv.mode=pool`, instance ingest does not call arXiv directly.
  Configure `ARXIV_POOL` / `arxiv_pool` and prewarm requested windows with
  `recoleta arxiv-pool sync` or a fleet pre-sync.

ArXiv pool fields:

- `ARXIV_POOL.enabled`: bool (default `false`). Required when
  `SOURCES.arxiv.mode=pool`.
- `ARXIV_POOL.backend`: `local_sqlite|huldra` (default `local_sqlite`).
- `ARXIV_POOL.huldra_base_url`:
  [Huldra](https://github.com/NeapolitanIcecream/huldra) service URL, required
  for `backend=huldra`.
- `ARXIV_POOL.huldra_request_timeout_seconds`: per-request timeout for Huldra
  calls (default `30.0`).
- `ARXIV_POOL.huldra_wait_timeout_seconds`: optional wait cap for Huldra
  sync/backfill calls. When unset, Recoleta derives a timeout from the requested
  windows.
- `ARXIV_POOL.db_path`: SQLite pool path, required for `backend=local_sqlite`.
- `ARXIV_POOL.maturity_lag_days`: number of days before a pool window is mature
  (default `1`).
- `ARXIV_POOL.readiness_gate`: `off|warn|strict` (default `strict`).
- `ARXIV_POOL.allow_immature_windows`: bool (default `false`).

Huldra is an optional dependency. Install it for Huldra-backed arXiv ingest:

```bash
uv sync --extra huldra
```

Example:

```yaml
SOURCES:
  arxiv:
    enabled: true
    mode: pool
    queries:
      - cat:cs.AI
    max_results_per_run: 50
    enrich_method: latex_source
    enrich_failure_mode: strict
  rss:
    enabled: true
    feeds:
      - https://example.com/feed.xml

ARXIV_POOL:
  enabled: true
  backend: huldra
  huldra_base_url: http://127.0.0.1:8765
  huldra_request_timeout_seconds: 30
  huldra_wait_timeout_seconds: null
  maturity_lag_days: 1
  readiness_gate: strict
  allow_immature_windows: false
```

## HTML maintext enrich parallelism (optional)

Use `ENRICH_HTML_MAINTEXT_MAX_CONCURRENCY` /
`enrich_html_maintext_max_concurrency` to control parallelism for non-arXiv HTML
maintext enrich work.

- Default: `1` (sequential, unchanged behavior)
- Accepted fleet tuning value: `4`
- Bounds: `1..32`

Set `4` when Stage 3 enrich is spending time fetching and extracting
`html_maintext` for HN, Hugging Face Daily Papers, or RSS items, and the source
mix is comparable to the measured fleet-day workload. This does not control the
arXiv `html_document` path, which uses the separate
`SOURCES.arxiv.html_document_*` settings above.

Examples:

```bash
ENRICH_HTML_MAINTEXT_MAX_CONCURRENCY=4 uv run recoleta fleet run day --manifest ./fleet/fleet.yaml
```

```yaml
enrich_html_maintext_max_concurrency: 4
```

Watch these signals after enabling it:

- `pipeline.enrich.failed_total`
- `pipeline.enrich.parallel.html_maintext.items_total`
- `pipeline.enrich.parallel.html_maintext.max_workers`
- source HTTP 429/5xx errors
- SQLite lock errors

Roll back by unsetting `ENRICH_HTML_MAINTEXT_MAX_CONCURRENCY` or setting
`ENRICH_HTML_MAINTEXT_MAX_CONCURRENCY=1` /
`enrich_html_maintext_max_concurrency: 1`. See
[`performance-rollback-policy.md`](performance-rollback-policy.md) for the
shared rollback thresholds.

## Topic and ranking configuration

- `TOPICS`: list of user topics (strings). These are used for LLM relevance scoring.
- `MIN_RELEVANCE_SCORE`: float (default 0.6)
- `MAX_DELIVERIES_PER_DAY`: int (default 10)
- `TITLE_DEDUP_THRESHOLD`: float (default 92.0 for rapidfuzz ratio)
- `TITLE_DEDUP_MAX_CANDIDATES`: int (default 500)

## Analyze and write-path controls

- `ANALYZE_LIMIT`: default max number of items analyzed in one run (default `100`)
- `ANALYZE_WRITE_BATCH_SIZE`: batch size for persisting analysis rows (default `32`)
- `ANALYZE_CONTENT_MAX_CHARS`: truncate loaded source content before Stage 4; set `0` to disable truncation (default `32768`)

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
- `TRENDS_SELF_SIMILAR_ENABLED`: enable the overview-pack retrieval flow that ranks related docs for trend analysis context
- `TRENDS_RANKING_N`: number of ranked retrieval hits passed into the overview-pack prompt context (default `10`)
- `TRENDS_OVERVIEW_PACK_MAX_CHARS`: char budget for the generated overview pack injected into the trend prompt (default `16000`)
- `TRENDS_ITEM_OVERVIEW_TOP_K`: max analyzed items folded into day-trend overview packs (default `28`)
- `TRENDS_ITEM_OVERVIEW_ITEM_MAX_CHARS`: per-item char budget when building day-trend overview packs (default `800`)
- `TRENDS_REP_MIN_PER_CLUSTER`: legacy evidence-floor setting retained for trend prompt assembly; reader-facing clusters now expose only prose plus `evidence` (default `2`)
- `TRENDS_PEER_HISTORY_ENABLED`: enable bounded prior-window context for internal historical comparison during trend writing (default `true`)
- `TRENDS_PEER_HISTORY_WINDOW_COUNT`: number of earlier peer windows to include (default `3`)
- `TRENDS_PEER_HISTORY_MAX_CHARS`: char budget for the peer-history pack (default `12000`)
- `TRENDS_EVOLUTION_MAX_SIGNALS`: max normalized historical-comparison signals kept before prompt injection (default `5`)

Operational notes:

- Normal `recoleta trends` runs can sync missing vectors on demand.
- `recoleta rag sync-vectors` is the explicit prewarm / repair path for large backfills or offline preparation.
- `recoleta rag build-index` builds ANN/scalar indices for the current LanceDB embedding table after vector sync succeeds.

## Scheduling

Choose one:

- External: use cron/launchd, no scheduler config needed.
- Internal (`recoleta daemon start`): configure workflow policy plus one or more daemon schedules.

Workflow policy:

- `WORKFLOWS.granularities.default`
  - `recursive_lower_levels` (default `true`). Week and month workflows include
    lower-level windows by default, but recursive lower-level generation is a
    first-run task-set gate. If any lower-level trend or idea pass output or
    document exists for that lower granularity in the parent window, the
    workflow skips recursive generation for that whole lower granularity. Use
    `--force` for intentional regeneration.
  - `delivery_mode`: `all|local_only|none` (default `all`)
  - `translation`: `auto|off` (default `auto`)
  - `translate_include`: any of `items|trends|ideas` (default all three)
  - `site_build` (default `true`)
  - `on_translate_failure`: `fail|partial_success|skip` (default `partial_success`)
- `WORKFLOWS.granularities.day|week|month`: optional overrides for the same fields
- `WORKFLOWS.deploy`: translation/site-build policy for `run deploy` and `daemon` deploy jobs

CLI controls:

- `recoleta run day|week|month --dry-run --json` and the fleet equivalents emit
  the ensure plan without creating run rows, metrics, pass outputs, localized
  outputs, documents, site files, or deliveries.
- `--force` on `run day|week|month` and `fleet run day|week|month` is a content
  regeneration control for the selected workflow windows, including recursive
  lower-level trend and idea windows. It does not reprocess analyze backlog
  after a day window has already consumed its configured `ANALYZE_LIMIT`. It is
  separate from `run deploy --force`, which remains a Git deployment force-push
  control.
- Analyze workflow planning is budget-based. Remaining `triaged` or
  `retryable_failed` items are backlog metadata once a matching analyze budget
  receipt exists for the day window and config. Run `stage analyze --date ...`
  or increase `ANALYZE_LIMIT` to intentionally process more backlog.
- `--include` and `--skip` are advanced repair controls. They remain available
  for compatibility, but normal week/month operation should rely on the planner.

Daemon schedules:

- `DAEMON.schedules`: list of workflow triggers
  - `workflow`: `now|day|week|month|deploy`
  - either `interval_minutes`
  - or `weekday` + `hour_utc` + `minute_utc`

Migration note:

- `INGEST_INTERVAL_MINUTES`, `ANALYZE_INTERVAL_MINUTES`, and `PUBLISH_INTERVAL_MINUTES` were removed in CLI v2 and are rejected during settings load.
- If you want the pre-v2 ingest/analyze/publish-only timer behavior, use an external scheduler and invoke `recoleta stage ingest`, `recoleta stage analyze`, and `recoleta stage publish` explicitly. `daemon start` now schedules named workflows rather than the old three-stage loop.

## Outputs

- `ARTIFACTS_DIR` (required when `WRITE_DEBUG_ARTIFACTS=true`): where to write raw/debug artifacts (outside the Vault is fine).
- `OBSIDIAN_BASE_FOLDER` (default `Recoleta`): base folder under the Vault.
- `PUBLISH_TARGETS` (default `["markdown"]`): which publish integrations are enabled.
- `MARKDOWN_OUTPUT_DIR`: where local Markdown output is written (e.g. `latest.md`, `Inbox/`, `Runs/`, canonical `Trends/*.md` and `Ideas/*.md` plus adjacent `.presentation.json` sidecars, `Localized/<language>/...`, derived `site/` output, and manual email preview/send bundles under `.recoleta-email/`).
- `BACKUP_OUTPUT_DIR`: optional default root for DB backup bundles used by
  `recoleta admin backup` and `recoleta inspect freshness`.

Backup root resolution order:

- `recoleta admin backup --output-dir ...`
- `BACKUP_OUTPUT_DIR` / `backup_output_dir`
- `<RECOLETA_DB_PATH parent>/backups`

Freshness vocabulary:

- run freshness: latest successful run timestamp and latest successful
  day/week/month workflow windows
- data freshness: latest `items.published_at`, plus latest published item date
- derived windows: latest persisted trend and idea windows
- backup recovery point: latest DB backup manifest timestamp

`recoleta inspect health --healthcheck --max-success-age-minutes ...` only
checks run freshness. Use `recoleta inspect freshness` when you need the full
freshness snapshot.

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
- `recoleta repair outputs --pdf --debug-pdf` uses the same debug-bundle
  contract when regenerating PDFs offline.
- `recoleta run site build --input-dir ... --output-dir ...` and
  `recoleta stage site stage --input-dir ... --output-dir ...` intentionally
  work without loading the full runtime config so CI can build from staged
  trend notes only.
- site build also writes a private email link-map companion artifact beside the
  site root, named `.<site_output_dir.name>-email-links.json`; with the default
  site output path this is `MARKDOWN_OUTPUT_DIR/.site-email-links.json`.
- When localized markdown trees are present, `recoleta run site build`,
  `recoleta stage site stage`, `recoleta run site serve`, and
  `recoleta run deploy` use `LOCALIZATION.site_default_language_code` by
  default when runtime settings are loaded. Use `--default-language-code <code>`
  when building from explicit input/output paths without full config loading.

## Logging and diagnostics

- `LOG_LEVEL` (default `INFO`)
- `LOG_JSON` (default false): if true, emit JSON logs (recommended for automation).
- `WRITE_DEBUG_ARTIFACTS` (default false): if true, write scrubbed debug JSON for failures and LLM calls.

## Secret handling rules

- Secrets must only come from env (or OS keychain in a future version).
- Debug artifacts must be scrubbed (remove tokens, headers, cookies).
- Logs must never include raw secrets.
- This includes Telegram credentials, `RECOLETA_LLM_API_KEY`, and
  `RECOLETA_RESEND_API_KEY`.
