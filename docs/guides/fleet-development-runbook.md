# Fleet Development Runbook

Use this guide after you have migrated a shared `topic_streams` deployment to
an instance-first fleet.

This is the development-mode operating model:

- run the fleet by hand from one fleet manifest
- keep each child instance isolated
- keep the old shared DB as a read-only archive
- do not wire the fleet into an automatic scheduler until you are ready

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
