# Recoleta Usage Recipes

This guide holds the command recipes and operator workflows that do not need to
live on the README front page.

## First successful pipeline run

Run the three main stages directly when you want explicit control:

```bash
uv run recoleta ingest
uv run recoleta analyze --limit 50
uv run recoleta publish --limit 20
```

Or run the whole pipeline once:

```bash
uv run recoleta run --once --analyze-limit 50 --publish-limit 20
```

For targeted replay of one UTC day:

```bash
uv run recoleta ingest --date 2026-01-02
uv run recoleta analyze --date 2026-01-02 --limit 50
uv run recoleta publish --date 2026-01-02 --limit 20
uv run recoleta run --once --date 2026-01-02 --analyze-limit 50 --publish-limit 20
```

Where to look after a run:

- `MARKDOWN_OUTPUT_DIR/latest.md`
- `MARKDOWN_OUTPUT_DIR/Inbox/`
- `RECOLETA_DB_PATH`
- `MARKDOWN_OUTPUT_DIR/Streams/<stream>/...` when `topic_streams` is enabled

For screenshots and concrete examples of what those outputs should become next,
see [`first-output-tour.md`](./first-output-tour.md).

## Trend briefs

Generate trend notes from analyzed items or existing lower-level trend windows:

```bash
uv run recoleta trends --granularity day
uv run recoleta trends --granularity week --date 2026-03-02
uv run recoleta trends --granularity week --date 2026-03-02 --backfill
uv run recoleta trends-week --date 2026-03-02
uv run recoleta trends --granularity month --date 2026-03-02 --backfill
uv run recoleta trends --granularity week --date 2026-03-02 --model "openai/gpt-5.4"
```

Key behavior:

- `--date` is a UTC anchor date.
- `day` trends use analyzed items from that day.
- `week` trends use day trend documents in that ISO week.
- `month` trends use week trend documents in that month.
- `--backfill` generates missing lower-level windows before the current one.
- Empty corpora skip the LLM call and emit a placeholder trend document.

Outputs:

- SQLite `trend` document in `RECOLETA_DB_PATH`
- canonical markdown note under `MARKDOWN_OUTPUT_DIR/Trends/`
- optional Obsidian trend note
- optional Telegram PDF derived from the canonical markdown note

See also:

- [`docs/design/trend-surfaces.md`](../design/trend-surfaces.md)
- [`docs/design/outputs.md`](../design/outputs.md)

## Idea briefs

Generate evidence-grounded idea briefs from an existing trend synthesis output:

```bash
uv run recoleta ideas --granularity day --date 2026-03-09
uv run recoleta ideas --granularity week --date 2026-03-02
uv run recoleta ideas --granularity day --date 2026-03-09 --model "openai/gpt-5.4"
```

Key behavior:

- `recoleta ideas` requires an upstream trend synthesis output for the same
  window.
- It does not rerun `recoleta trends` automatically.
- Low-evidence windows can return `status=suppressed` instead of padded output.
- Successful runs can project to Markdown and Obsidian while keeping canonical
  state in `pass_outputs`.

Outputs:

- canonical `trend_ideas` pass output in SQLite
- searchable `doc_type=idea` document
- optional Markdown brief under `MARKDOWN_OUTPUT_DIR/Ideas/`
- optional Obsidian note

## Static site and materialization

Build or publish the public site from canonical markdown notes:

```bash
uv run recoleta site build
uv run recoleta site serve
uv run recoleta site gh-deploy --branch gh-pages --pages-config auto
uv run recoleta materialize outputs --site --pdf
uv run recoleta materialize outputs --scope <stream> --granularity week
```

Key behavior:

- `site build` writes a managed static export to `MARKDOWN_OUTPUT_DIR/site`
  unless explicit paths are provided.
- `site serve` rebuilds then serves a local preview on `127.0.0.1:8000`.
- `site gh-deploy` publishes a derived branch without polluting `main`.
- `materialize outputs` repairs filesystem projections from stored DB state
  without rerunning ingest/analyze.

See also:

- [`docs/design/outputs.md`](../design/outputs.md)
- [`docs/design/trend-surfaces.md`](../design/trend-surfaces.md)

## Continuous operation

Run the built-in scheduler:

```bash
uv run recoleta run
```

Tune the cadence with:

- `INGEST_INTERVAL_MINUTES`
- `ANALYZE_INTERVAL_MINUTES`
- `PUBLISH_INTERVAL_MINUTES`

Use `run --once` for cron, launchd, systemd timers, and scheduled containers:

```bash
uv run recoleta run --once
```

Read-only operator checks:

```bash
uv run recoleta doctor --healthcheck --max-success-age-minutes 180
uv run recoleta stats --json
```

## Deployment recipes

Minimal cron pattern:

```bash
*/15 * * * * cd /path/to/recoleta && /path/to/uv run recoleta run --once >> /var/log/recoleta.log 2>&1
```

Minimal systemd pattern:

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

## Maintenance and recovery

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

Workspace resets:

```bash
uv run recoleta db reset --trends-only --yes
uv run recoleta db clear --yes
```

Scope notes:

- `backup` and `restore` cover the SQLite truth store only.
- `db reset --trends-only` clears trend/item document projections while keeping
  ingest/analyze history.
- `materialize outputs` is the safer repair path when DB trend payloads are
  still authoritative and only filesystem outputs drifted.

## Configuration and deeper reference

- [`docs/design/configuration.md`](../design/configuration.md)
- [`docs/design/system-overview.md`](../design/system-overview.md)
- [`docs/design/architecture.md`](../design/architecture.md)
- [`docs/design/outputs.md`](../design/outputs.md)
- [`docs/design/data-model.md`](../design/data-model.md)
- [`docs/design/semantic-pre-ranking.md`](../design/semantic-pre-ranking.md)
