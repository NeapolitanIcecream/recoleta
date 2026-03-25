# Recoleta Usage Recipes

Use this guide when the README quickstart is no longer enough and you need the
exact v2 command for a workflow, repair, or maintenance task.

Start with `recoleta run ...`. Use `recoleta stage ...` only when you want one
primitive without workflow orchestration.

## Run a full workflow

```bash
uv run recoleta run now
uv run recoleta run day --date 2026-01-02
uv run recoleta run week --date 2026-03-02
uv run recoleta run month --date 2026-03-02
```

What to know:

- `run now` means "run the current UTC day end to end".
- `run day`, `run week`, and `run month` run ingest, analyze, publish,
  recursive trends and ideas, then translation and site build when your config
  enables them.
- `run week` includes both day-level and week-level trends and ideas.
- `run month` includes day-level, week-level, and month-level trends and ideas.
- Use `--include` and `--skip` when you want to override optional workflow
  steps such as `publish`, `translate`, and `site-build`.

After a successful run, check:

- `MARKDOWN_OUTPUT_DIR/latest.md`
- `MARKDOWN_OUTPUT_DIR/Inbox/`
- `MARKDOWN_OUTPUT_DIR/Trends/`
- `MARKDOWN_OUTPUT_DIR/site/`
- `MARKDOWN_OUTPUT_DIR/Ideas/` when the current window has enough evidence
- `MARKDOWN_OUTPUT_DIR/Streams/<stream>/...` when `topic_streams` is enabled

## Run one stage only

```bash
uv run recoleta stage ingest --date 2026-01-02
uv run recoleta stage analyze --date 2026-01-02 --limit 50
uv run recoleta stage publish --date 2026-01-02 --limit 20
uv run recoleta stage trends --granularity week --date 2026-03-02
uv run recoleta stage ideas --granularity week --date 2026-03-02
```

What to know:

- `stage` commands do one thing only.
- They do not recurse lower-level windows.
- They do not translate or rebuild the site.
- Use them when you already know which primitive needs to rerun.

## Translate localized reading surfaces

Use `run translate` after the canonical item summaries, trend briefs, or idea
briefs already exist in SQLite:

```bash
uv run recoleta run translate --include items,trends,ideas
uv run recoleta run translate --scope agents_lab --granularity week --include trends,ideas
uv run recoleta run translate --include items --force
```

What to know:

- `run translate` reads canonical rows and writes derived variants to
  `localized_outputs`.
- `--include` accepts `items`, `trends`, and `ideas`.
- `--force` rewrites localized outputs even when the source hash is unchanged.
- `--context-assist` defaults to `direct`.
- `--context-assist hybrid` only reads existing search and vector state. It
  does not sync vectors automatically, and it falls back to direct-context
  behavior if hybrid retrieval fails.

## Backfill historical canonical content into a new source language

Use `stage translate backfill` once when the historical canonical corpus is in
one language and future canonical output should be in another:

```bash
uv run recoleta stage translate backfill --all-history --include items,trends,ideas --emit-mirror-targets
uv run recoleta stage translate backfill --scope agents_lab --granularity week --include trends,ideas --legacy-source-language zh-CN
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

## Build, preview, or deploy the site

Use these commands when you want public-facing output from stored Markdown and
DB state:

```bash
uv run recoleta run site build
uv run recoleta run site serve
uv run recoleta run site build --default-language-code en
uv run recoleta run deploy --branch gh-pages --pages-config auto
uv run recoleta repair outputs --site --pdf
uv run recoleta repair outputs --scope agents_lab --granularity week --site
```

What to know:

- `run site build` writes a managed static export to `MARKDOWN_OUTPUT_DIR/site`
  unless you pass explicit paths.
- `run site serve` rebuilds and serves a local preview on `127.0.0.1:8000`.
- `run deploy` translates if configured, builds the site, and pushes a derived
  deployment branch.
- `repair outputs` repairs Markdown, PDFs, and site files from stored DB state
  without rerunning ingest or analyze.
- When localized markdown trees exist, site export writes one subtree per
  language, for example `/en/...` and `/zh-cn/...`.
- The root `index.html` redirects to the remembered browser language first and
  then to the configured default language.

## Keep Recoleta running

Run the built-in scheduler:

```bash
uv run recoleta daemon start
```

Define workflow policy and schedules in `recoleta.yaml`. Start with the example
blocks in `recoleta.example.yaml`, then adjust them for your cadence:

```yaml
workflows:
  granularities:
    default:
      recursive_lower_levels: true
      delivery_mode: all
      translation: auto
      translate_include: [items, trends, ideas]
      site_build: true
      on_translate_failure: partial_success

daemon:
  schedules:
    - workflow: day
      interval_minutes: 60
    - workflow: week
      weekday: mon
      hour_utc: 2
      minute_utc: 0
    - workflow: deploy
      weekday: mon
      hour_utc: 2
      minute_utc: 30
```

Use one-shot workflows for cron, launchd, systemd timers, or scheduled
containers:

```bash
uv run recoleta run now
```

Read-only operator checks:

```bash
uv run recoleta inspect health --healthcheck --max-success-age-minutes 180
uv run recoleta inspect stats --json
```

Many workflow, stage, repair, and inspect subcommands expose `--json`. Check
the specific subcommand help before scripting it.

## Deploy with cron or systemd

Minimal cron example:

```bash
*/15 * * * * cd /path/to/recoleta && /path/to/uv run recoleta run now >> /var/log/recoleta.log 2>&1
```

Minimal systemd example:

```ini
# /etc/systemd/system/recoleta.service
[Unit]
Description=Recoleta one-shot workflow
After=network-online.target

[Service]
Type=oneshot
WorkingDirectory=/path/to/recoleta
Environment=RECOLETA_CONFIG_PATH=/path/to/recoleta.yaml
ExecStart=/path/to/uv run recoleta run now
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

## Inspect a workspace

Use these commands when you want to prove what the current shell is doing before
you rerun a date or repair state:

```bash
uv run recoleta inspect llm --json
uv run recoleta inspect llm --ping --json
uv run recoleta inspect why-empty --date 2026-03-15 --granularity day --stream agents_lab --json
uv run recoleta inspect runs show --run-id <run-id> --json
uv run recoleta inspect runs list --limit 10 --json
```

What to know:

- `inspect llm` is read-only. It reports the effective model, provider, output
  language, whether `RECOLETA_LLM_API_KEY` is present, a key fingerprint, and
  whether `base_url` came from the current shell env.
- `inspect llm --ping` runs a small completion probe against the current LLM
  config and returns a non-zero exit code if the probe fails.
- `inspect why-empty` explains why a day, week, or month corpus selected zero
  items. It reports candidate counts, selected counts, filtered-out totals, and
  exclusion reasons such as `missing_analysis` or
  `stream_state_retryable_failed`.
- `inspect runs show` aggregates run status, billing, metrics, pass outputs,
  artifacts, run context, and structured failure summaries in one JSON payload.
- `inspect runs list` gives a compact recent-run view that is easier to
  automate than scraping logs.

## Repair outputs or stream state

Use these commands when you need to repair one stream or rebuild output files
from stored state:

```bash
uv run recoleta repair streams --date 2026-03-15 --streams agents_lab --json
uv run recoleta stage analyze --date 2026-03-15 --limit 50
uv run recoleta stage trends --granularity day --date 2026-03-15
uv run recoleta stage ideas --granularity day --date 2026-03-15

uv run recoleta repair outputs --site --pdf
uv run recoleta repair outputs --scope agents_lab --granularity week --site
```

What to know:

- `repair streams` marks the selected stream rows `retryable_failed` for one
  UTC day. It does not rerun analysis, trends, or ideas by itself.
- Follow `repair streams` with `stage analyze`, then downstream `stage trends`
  and `stage ideas` if you need new documents for that window.
- `repair outputs` is the safer path when the database is already correct and
  only Markdown, PDF, or site output drifted.

## Maintain or reset a workspace

Routine maintenance:

```bash
uv run recoleta admin gc
uv run recoleta admin gc --prune-caches
uv run recoleta admin vacuum
```

Backup and restore:

```bash
uv run recoleta admin backup --output-dir /path/to/backups
uv run recoleta admin restore --bundle /path/to/backup-bundle --yes
```

Workspace reset commands:

```bash
uv run recoleta admin db reset --trends-only --yes
uv run recoleta admin db clear --yes
```

Scope notes:

- `admin backup` and `admin restore` cover the SQLite database only.
- `admin db reset --trends-only` clears trend and item document projections
  while keeping ingest and analyze history.
- `admin db clear` removes the configured SQLite file for a clean slate.

## Further reference

- [`docs/guides/first-output-tour.md`](./first-output-tour.md)
- [`docs/guides/cli-v2-migration.md`](./cli-v2-migration.md)
- [`docs/design/configuration.md`](../design/configuration.md)
- [`docs/design/system-overview.md`](../design/system-overview.md)
- [`docs/design/architecture.md`](../design/architecture.md)
- [`docs/design/outputs.md`](../design/outputs.md)
- [`docs/design/data-model.md`](../design/data-model.md)
- [`docs/design/semantic-pre-ranking.md`](../design/semantic-pre-ranking.md)
