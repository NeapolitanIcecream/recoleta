# CLI v2 migration

Recoleta CLI v2 changes the top-level interface.

If you are starting fresh, use the README quickstart. Use this guide only when
you need to map older commands to the workflow-first CLI surface.

Use this guide if you were using `run --once`, `trends-week`, `materialize outputs`, or `site gh-deploy`.

## New top-level groups

Run these commands from the new surface:

```bash
recoleta run ...
recoleta daemon start
recoleta inspect ...
recoleta repair ...
recoleta stage ...
recoleta admin ...
```

`run` is now the main workflow entrypoint.

- `run now` means "run the current UTC day end to end"
- `run day --date YYYY-MM-DD` means "run one UTC day end to end"
- `run week --date YYYY-MM-DD` means "run one ISO week end to end"
- `run month --date YYYY-MM-DD` means "run one month end to end"
- `run deploy` means "translate if configured, build the site, then deploy it"

`daemon start` replaces the old built-in scheduler mode.

`stage` keeps the low-level primitives for expert use.

## Command mapping

Use these replacements:

| Old command | New command |
| --- | --- |
| `recoleta run --once` | `recoleta run now` |
| `recoleta run --once --date 2026-03-16` | `recoleta run day --date 2026-03-16` |
| `recoleta trends-week --date 2026-03-16` | `recoleta run week --date 2026-03-16` |
| `recoleta materialize outputs --site --pdf` | `recoleta repair outputs --site --pdf` |
| `recoleta site gh-deploy` | `recoleta run deploy` |
| `recoleta gc` | `recoleta admin gc` |
| `recoleta vacuum` | `recoleta admin vacuum` |
| `recoleta backup` | `recoleta admin backup` |
| `recoleta restore` | `recoleta admin restore` |
| `recoleta stats` | `recoleta inspect stats` |
| `recoleta doctor --healthcheck` | `recoleta inspect health --healthcheck` |
| `recoleta doctor llm` | `recoleta inspect llm` |
| `recoleta doctor why-empty` | `recoleta inspect why-empty` |
| `recoleta runs list` | `recoleta inspect runs list` |
| `recoleta runs show` | `recoleta inspect runs show` |

`recoleta run week` is a broader end-to-end replacement for `trends-week`. It
reruns the weekly workflow instead of only generating weekly trends.

## Scheduler config

The old interval keys are gone:

- `INGEST_INTERVAL_MINUTES`
- `ANALYZE_INTERVAL_MINUTES`
- `PUBLISH_INTERVAL_MINUTES`

Use workflow schedules instead:

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

## Workflow defaults

`run day`, `run week`, and `run month` now run the full workflow by default:

1. `ingest`
2. `analyze`
3. `publish`
4. recursive `trends + ideas` for the target granularity stack
5. `translate` when `localization.targets` is configured
6. `site-build`

`run week` includes both day-level and week-level `trends + ideas`.

`run month` includes day-level, week-level, and month-level `trends + ideas`.

## What stayed low-level

Use `stage` when you want one primitive without workflow orchestration:

```bash
recoleta stage ingest --date 2026-03-16
recoleta stage trends --granularity week --date 2026-03-16
recoleta stage ideas --granularity week --date 2026-03-16
```

These commands stay narrow on purpose. Recursive orchestration lives under `run`, not under `stage`.
