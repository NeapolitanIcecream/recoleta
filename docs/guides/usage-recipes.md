# Recoleta Usage Recipes

Use this guide when the README quickstart is no longer enough and you need the
exact command for a common workflow.

## Run the pipeline once

Run each stage directly when you want more control:

```bash
uv run recoleta ingest
uv run recoleta analyze --limit 50
uv run recoleta publish --limit 20
```

Or run the whole pipeline in one command:

```bash
uv run recoleta run --once --analyze-limit 50 --publish-limit 20
```

To replay one UTC day:

```bash
uv run recoleta ingest --date 2026-01-02
uv run recoleta analyze --date 2026-01-02 --limit 50
uv run recoleta publish --date 2026-01-02 --limit 20
uv run recoleta run --once --date 2026-01-02 --analyze-limit 50 --publish-limit 20
```

After a successful run, check:

- `MARKDOWN_OUTPUT_DIR/latest.md`
- `MARKDOWN_OUTPUT_DIR/Inbox/`
- `RECOLETA_DB_PATH`
- `MARKDOWN_OUTPUT_DIR/Streams/<stream>/...` when `topic_streams` is enabled

For screenshots and example pages, see
[`first-output-tour.md`](./first-output-tour.md).

## Generate trend briefs

Use these commands when you want a day, week, or month view:

```bash
uv run recoleta trends --granularity day
uv run recoleta trends --granularity week --date 2026-03-02
uv run recoleta trends --granularity week --date 2026-03-02 --backfill
uv run recoleta trends-week --date 2026-03-02
uv run recoleta trends --granularity month --date 2026-03-02 --backfill
uv run recoleta trends --granularity week --date 2026-03-02 --model "openai/gpt-5.4"
```

What to know:

- `--date` is a UTC anchor date.
- `day` trends use analyzed items from that day.
- `week` trends use day trend documents from that ISO week.
- `month` trends use week trend documents from that month.
- `--backfill` creates missing lower-level windows before building the current
  one.
- Empty corpora skip the LLM call and emit a placeholder trend document.

Outputs:

- SQLite `trend` document in `RECOLETA_DB_PATH`
- Markdown brief under `MARKDOWN_OUTPUT_DIR/Trends/`
- Optional Obsidian trend note
- Optional Telegram PDF built from the canonical Markdown brief

More detail:

- [`docs/design/trend-surfaces.md`](../design/trend-surfaces.md)
- [`docs/design/outputs.md`](../design/outputs.md)

## Generate idea briefs

Use `recoleta ideas` after a matching trend window already exists:

```bash
uv run recoleta ideas --granularity day --date 2026-03-09
uv run recoleta ideas --granularity week --date 2026-03-02
uv run recoleta ideas --granularity day --date 2026-03-09 --model "openai/gpt-5.4"
```

What to know:

- `recoleta ideas` needs an upstream trend synthesis output for the same window.
- It does not rerun `recoleta trends`.
- Low-evidence windows can return `status=suppressed` instead of padded output.
- Successful runs can write Markdown and Obsidian notes while keeping canonical
  state in `pass_outputs`.

Outputs:

- Canonical `trend_ideas` pass output in SQLite
- Searchable `doc_type=idea` document
- Optional Markdown brief under `MARKDOWN_OUTPUT_DIR/Ideas/`
- Optional Obsidian note

## Translate localized reading surfaces

Use `recoleta translate run` after the canonical item summaries, trend briefs,
or idea briefs already exist in SQLite:

```bash
uv run recoleta translate run --include items,trends,ideas
uv run recoleta translate run --scope agents_lab --granularity week --include trends,ideas
uv run recoleta translate run --include items --force
```

What to know:

- `translate run` reads canonical rows and writes derived variants to
  `localized_outputs`.
- `--include` accepts `items`, `trends`, and `ideas`.
- `--force` rewrites localized outputs even when the source hash is unchanged.
- `--context-assist` defaults to `direct`.
- `--context-assist hybrid` only reads existing search and vector state. It does
  not sync vectors automatically, and it falls back to direct-context behavior
  if hybrid retrieval fails.

## Backfill historical canonical content into a new source language

Use `recoleta translate backfill` once when the historical canonical corpus is
in one language and future canonical output should be in another:

```bash
uv run recoleta translate backfill --all-history --include items,trends,ideas --emit-mirror-targets
uv run recoleta translate backfill --scope agents_lab --granularity week --include trends,ideas --legacy-source-language zh-CN
```

What to know:

- `localization.source_language_code` is the language you want future canonical
  output to use.
- `localization.legacy_backfill_source_language_code` or
  `--legacy-source-language` tells Recoleta what language the historical
  canonical rows currently use.
- `--emit-mirror-targets` also records localized mirror variants for matching
  target languages so multilingual rendering can stay on one projection layer.
- `--all-history` scans the full historical corpus. `--latest-only` limits the
  pass to the latest available window per granularity.
- Backfill writes `localized_outputs`. It does not rewrite canonical
  `analyses`, `pass_outputs`, or `documents`.

## Build, preview, or publish the site

Use these commands when you want to materialize public-facing output from the
stored Markdown and DB state:

```bash
uv run recoleta site build
uv run recoleta site serve
uv run recoleta site build --default-language-code en
uv run recoleta site gh-deploy --branch gh-pages --pages-config auto
uv run recoleta materialize outputs --site --pdf
uv run recoleta materialize outputs --scope <stream> --granularity week
```

What to know:

- `site build` writes a managed static export to `MARKDOWN_OUTPUT_DIR/site`
  unless you pass explicit paths.
- `site serve` rebuilds and serves a local preview on `127.0.0.1:8000`.
- `site gh-deploy` publishes a derived branch and keeps `main` clean.
- `materialize outputs` repairs filesystem output from stored DB state without
  rerunning ingest or analyze.
- When localized markdown trees exist, site export writes one subtree per
  language, for example `/en/...` and `/zh-cn/...`.
- The root `index.html` redirects to the remembered browser language first and
  then to the configured default language.
- `--default-language-code` is only needed when you build or deploy a
  multilingual site without loading a config that already defines
  `localization.site_default_language_code`.

More detail:

- [`docs/design/outputs.md`](../design/outputs.md)
- [`docs/design/trend-surfaces.md`](../design/trend-surfaces.md)

## Keep Recoleta running

Run the built-in scheduler:

```bash
uv run recoleta run
```

Tune the schedule with:

- `INGEST_INTERVAL_MINUTES`
- `ANALYZE_INTERVAL_MINUTES`
- `PUBLISH_INTERVAL_MINUTES`

Use `run --once` for cron, launchd, systemd timers, or scheduled containers:

```bash
uv run recoleta run --once
```

Read-only operator checks:

```bash
uv run recoleta doctor --healthcheck --max-success-age-minutes 180
uv run recoleta stats --json
```

Most long-running commands also support `--json`, including `analyze`,
`publish`, `trends`, `trends-week`, `ideas`, `translate run`,
`translate backfill`, `materialize outputs`, `site build`, `site stage`, and
`site gh-deploy`.

## Deploy with cron or systemd

Minimal cron example:

```bash
*/15 * * * * cd /path/to/recoleta && /path/to/uv run recoleta run --once >> /var/log/recoleta.log 2>&1
```

Minimal systemd example:

```ini
# /etc/systemd/system/recoleta.service
[Unit]
Description=Recoleta one-shot pipeline
After=network-online.target

[Service]
Type=oneshot
WorkingDirectory=/path/to/recoleta
Environment=RECOLETA_CONFIG_PATH=/path/to/recoleta.yaml
ExecStart=/path/to/uv run recoleta run --once
```

```ini
# /etc/systemd/system/recoleta.timer
[Unit]
Description=Run Recoleta every 15 minutes

[Timer]
OnBootSec=5m
OnUnitActiveSec=15m
Unit=recoleta.service

[Install]
WantedBy=timers.target
```

## Maintain or repair a workspace

Routine maintenance:

```bash
uv run recoleta gc
uv run recoleta gc --prune-caches
uv run recoleta vacuum
```

Backup and restore:

```bash
uv run recoleta backup
uv run recoleta restore --bundle /path/to/backup-bundle --yes
```

Workspace reset commands:

```bash
uv run recoleta db reset --trends-only --yes
uv run recoleta db clear --yes
```

Scope notes:

- `backup` and `restore` cover the SQLite database only.
- `db reset --trends-only` clears trend and item document projections while
  keeping ingest and analyze history.
- `materialize outputs` is the safer repair path when the database is still
  correct and only filesystem output drifted.

## Diagnose LLM config, empty corpora, and failed runs

Use these commands when you need to prove what the current shell is doing
before you rerun a date or repair state:

```bash
uv run recoleta doctor llm --json
uv run recoleta doctor llm --ping --json
uv run recoleta doctor why-empty --date 2026-03-15 --granularity day --stream agents_lab --json
uv run recoleta runs show --run-id <run-id> --json
uv run recoleta runs list --limit 10 --json
```

What to know:

- `doctor llm` is read-only. It reports the effective model, provider,
  output language, whether `RECOLETA_LLM_API_KEY` is present, a key
  fingerprint, and whether `base_url` came from the current shell env.
- `doctor llm --ping` runs a small completion probe against the current LLM
  config and returns a non-zero exit code if the probe fails.
- `doctor why-empty` explains why a day, week, or month corpus selected zero
  items. It reports candidate counts, selected counts, filtered-out totals, and
  exclusion reasons such as `missing_analysis` or
  `stream_state_retryable_failed`.
- `runs show` aggregates run status, billing, metrics, pass outputs, artifacts,
  run context, and structured failure summaries in one JSON payload.
- `runs list` gives a compact recent-run view that is easier to automate than
  scraping logs.

## Repair explicit stream analysis state

Use `repair-streams` when a stream-scoped rerun is blocked by stale
`item_stream_states` and the underlying source items are already present in the
database:

```bash
uv run recoleta repair-streams --date 2026-03-15 --streams agents_lab --json
uv run recoleta analyze --date 2026-03-15 --limit 50
uv run recoleta trends --granularity day --date 2026-03-15
uv run recoleta ideas --granularity day --date 2026-03-15
```

What to know:

- `repair-streams` marks the selected stream rows `retryable_failed` for one
  UTC day. It does not rerun analysis, trends, or ideas by itself.
- `repair-streams` is write-capable and applies startup-safe schema migrations
  before it repairs state, so it can be used directly on an older workspace.
- Follow it with `analyze` to rerun the stream-scoped analysis, then `trends`
  and `ideas` if you need new downstream documents for that window.
- If the database is already correct and only Markdown/PDF/site output drifted,
  use `materialize outputs` instead of mutating stream state.

## Further reference

- [`docs/design/configuration.md`](../design/configuration.md)
- [`docs/design/system-overview.md`](../design/system-overview.md)
- [`docs/design/architecture.md`](../design/architecture.md)
- [`docs/design/outputs.md`](../design/outputs.md)
- [`docs/design/data-model.md`](../design/data-model.md)
- [`docs/design/semantic-pre-ranking.md`](../design/semantic-pre-ranking.md)
