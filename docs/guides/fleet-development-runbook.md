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
uv run recoleta fleet run deploy --manifest /path/to/fleet.yaml
```

Use `--date` when you want to replay a historical UTC window:

```bash
uv run recoleta fleet run day --manifest /path/to/fleet.yaml --date 2026-03-25
uv run recoleta fleet run week --manifest /path/to/fleet.yaml --date 2026-03-22
```

`fleet run day` defaults to the latest complete UTC day. Use an explicit date
for replays and backlog repair.

## Development rules

- Treat the fleet manifest as the only manual entry point for the migrated deployment.
- Do not keep running the old shared config after cutover.
- Do not point new writes at the archived shared DB.
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

## Safe replay pattern

For a fully settled historical window, prefer replaying only the stages that
need it. For example, if W12 already has item and analysis data, you can replay
the weekly layer without ingesting current upstream state:

```bash
uv run recoleta fleet run week \
  --manifest /path/to/fleet.yaml \
  --date 2026-03-22 \
  --skip ingest,analyze,publish,trends:day,ideas:day,translate,site-build
```

For a true missing day with no corpus, run the full day workflow instead.

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
