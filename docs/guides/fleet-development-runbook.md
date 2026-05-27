# Fleet Development Runbook

Use this guide when you operate an instance-first fleet made of several child
configs. If you arrived here from an older shared `topic_streams` deployment,
finish the split first and keep the old workspace read-only.

This is the development-mode operating model:

- run the fleet by hand from one fleet manifest
- keep each child instance isolated
- keep the old shared DB as a read-only archive
- do not wire the fleet into an automatic scheduler until you are ready

## Current deployment closure note

For the current migrated playground fleet, the migration work is complete for
the purpose of future incremental runs.

This means:

- each child instance now has its own config, DB, output tree, and LanceDB root
- `embodied_ai` keeps only the embodied arXiv query
- `software_intelligence` keeps only the software-intelligence arXiv query
- arXiv-enabled children use `sources.arxiv.mode: pool` with the shared
  `arxiv_pool.backend: huldra` endpoint
- `hn` and `hf_daily` remain enabled in both children by design
- stale per-query `source_pull_states` were removed so future incremental pulls
  follow the live child config

This does not mean the historical corpus was repartitioned perfectly. Historical
`items`, `contents`, and other migrated user-facing rows can remain duplicated
across child DBs. That is acceptable for this deployment and should not be
treated as unfinished migration work as long as future incremental ingestion is
correct.

Treat the current source of truth as:

- the live child `recoleta.yaml` files
- the current child DB state

Do not treat `migration-manifest.json` as the live source configuration after
manual cleanup. It records the original migration snapshot, not later hand edits.

## What is canonical now

For a migrated multi-instance deployment, these assets are the live entry
points:

- `fleet.yaml`: the manifest that points at child instance configs
- each child `recoleta.yaml`: the isolated config for one instance
- each child SQLite DB and output tree

The old shared-instance config and DB are no longer the runtime entry point.
Keep them for archive, migration audit, and disaster recovery only.

## Manual commands

Run from the repo root:

```bash
uv run recoleta fleet run day --manifest /path/to/fleet.yaml
uv run recoleta fleet run week --manifest /path/to/fleet.yaml
uv run recoleta fleet run week --manifest /path/to/fleet.yaml --dry-run --json
uv run recoleta fleet run deploy --manifest /path/to/fleet.yaml
```

Use `--date` when you want to replay a historical UTC window:

```bash
uv run recoleta fleet run day --manifest /path/to/fleet.yaml --date 2026-03-25
uv run recoleta fleet run week --manifest /path/to/fleet.yaml --date 2026-03-22
```

`fleet run day` defaults to the latest complete UTC day. Use an explicit date
for replays and backlog repair.

`fleet run day|week|month` uses ensure/backfill semantics. A weekly run still
checks every child and every lower-level window, but fresh day-level expensive
work is skipped automatically. Use `--dry-run --json` to inspect the per-child
plan before a replay. Use `--force` only for deliberate regeneration.

## Development rules

- Treat the fleet manifest as the only manual entry point for the migrated deployment.
- Do not keep running the old shared config after cutover.
- Do not point new writes at the archived shared DB.
- Keep all arXiv-enabled child configs on the same pool backend identity. Mixed
  `local_sqlite`/`huldra` backends or multiple
  [Huldra](https://github.com/NeapolitanIcecream/huldra) endpoints block fleet
  pre-sync before child workflows run.
- When you need to inspect one child directly, use that child config for
  `inspect` or one-off debugging, not for normal recurring workflow runs.

## Health checks

Check a child before or after a replay:

```bash
uv run recoleta inspect health --config /path/to/child/recoleta.yaml
```

Good output should show:

- `settings=ok`
- `paths=ok`
- `lease=free` when nothing is running
- the expected `schema_version`

## Workflow timing metrics

Use these signals when you need to understand where a workflow run spent time:

- `steps[].duration_ms` from `recoleta run ... --json` or `recoleta fleet run ... --json`
- `pipeline.workflow.step.<step>.duration_ms` from run metrics

These two signals describe top-level workflow step wall-time. They are the
right inputs for hotspot ranking and e2e timing reports.

Some stage-local metrics use different semantics. In particular:

- `pipeline.translate.task_duration_ms_total` is cumulative task work across
  translation requests
- it is not the same thing as the workflow `translate` step wall-time

If you need the runtime cost of the `translate` step, use the workflow step
duration, not the cumulative task metric.

Inspect a finished run with:

```bash
uv run recoleta inspect runs show --run-id <run-id> --json
```

That payload includes run metrics, billing, and the executed step list.

## HTML maintext enrich parallelism

Use this tuning only for child fleets where the enrich step spends material time
fetching and extracting non-arXiv HTML maintext from HN, Hugging Face Daily
Papers, or RSS sources. The accepted fleet-day hotspot study found
`ENRICH_HTML_MAINTEXT_MAX_CONCURRENCY=4` to be the strongest measured runtime
win for the current fleet setup: `706.11s -> 533.62s` (`-24.43%`) on the
accepted repeat.

For a one-off run:

```bash
ENRICH_HTML_MAINTEXT_MAX_CONCURRENCY=4 \
  uv run recoleta fleet run day --manifest /path/to/fleet.yaml
```

For a child config that should keep the tuning:

```yaml
enrich_html_maintext_max_concurrency: 4
```

The default is `1`, so omitting the setting keeps sequential behavior. Roll
back by unsetting `ENRICH_HTML_MAINTEXT_MAX_CONCURRENCY` or setting it back to
`1` in the environment or child config.

After enabling it, watch:

- `pipeline.enrich.failed_total`
- `pipeline.enrich.parallel.html_maintext.items_total`
- `pipeline.enrich.parallel.html_maintext.max_workers`
- source HTTP 429/5xx errors
- SQLite lock errors
- total enrich step duration from the workflow step metrics

If failures rise, source throttling appears, SQLite lock errors appear, or the
fleet workload is no longer comparable to the measured setup, roll back to `1`.
Use [`docs/design/performance-rollback-policy.md`](../design/performance-rollback-policy.md)
for the shared thresholds. The measured study is recorded in
[`docs/plans/2026-04-22-fleet-day-e2e-hotspot-study-stage-1.md`](../plans/2026-04-22-fleet-day-e2e-hotspot-study-stage-1.md).

## Controlled benchmark scripts

Two scripts under `scripts/` are kept as DFX tools for repeatable measurement:

- `scripts/bench_shadow_day_run.py`
- `scripts/bench_fleet_day_e2e.py`

Use `bench_shadow_day_run.py` for controlled A/B checks against one or more
instances. It restores a backup into a shadow workspace, deletes derived
outputs before each replay, runs the same date window, and writes comparable
timing artifacts.

Example:

```bash
uv run python scripts/bench_shadow_day_run.py \
  --manifest /path/to/fleet.yaml \
  --date 20260406 \
  --backup-root bench-out/e2e-20260406/backups \
  --output-dir bench-out/shadow-compare \
  --instances embodied_ai,software_intelligence
```

Use `bench_fleet_day_e2e.py` when you want a one-shot fleet report from a live
manifest run and do not need the stronger backup-restore controls of the shadow
harness.

Treat `bench-out*` directories as generated output. Do not keep experiment
results in the repo as source files.

## Safe replay pattern

For a fully settled historical window, start with the declarative workflow and
inspect the plan:

```bash
uv run recoleta fleet run week \
  --manifest /path/to/fleet.yaml \
  --date 2026-03-22 \
  --dry-run --json
```

If the plan shows the expected skips, run the same command without `--dry-run`.
Use `--skip` only as an advanced repair override when you need to suppress a
specific step despite planner output. For a true missing day with no corpus, run
the full day workflow instead.

## Deploy smoke

When you want to verify deploy behavior without touching the live remote, point
`fleet run deploy` at a local bare Git remote or a disposable checkout:

```bash
uv run recoleta fleet run deploy \
  --manifest /path/to/fleet.yaml \
  --repo-dir /tmp/recoleta-pages-smoke/repo \
  --remote origin \
  --branch gh-pages \
  --json
```

This is the safest way to check idempotency after schema or materialization
changes.

## Keep the old DB archived

The original shared DB still matters, but not as a write target.

Keep it for:

- migration audit
- legacy-history lookup
- disaster recovery

Do not upgrade it in place unless you deliberately want to retire the archive.
