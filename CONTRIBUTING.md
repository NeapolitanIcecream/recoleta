# Contributing

Use this guide when you want to send a pull request, file a bug, or propose a
new preset.

## Local setup

```bash
uv sync --group dev
uv run ruff check .
uv run pytest
```

When you are iterating on one area, run a focused test too:

```bash
uv run pytest tests/test_trends_static_site.py -q
```

## Refactor Audit

Use the audit workflow when you want to check whether the current scope is
drifting into structural debt before you start or while you are iterating on a
refactor.

```bash
uv sync --group dev
uv run python scripts/refactor_audit.py
uv run python scripts/refactor_audit.py recoleta/pipeline recoleta/site.py
```

`output/refactor-audit/` is temporary local output and remains ignored.
`quality/refactor-baseline.json` is the checked-in baseline used to spot
regressions without pretending that the existing hotspot backlog is already
gone.

## How to make changes easier to review

- Keep one pull request focused on one behavior change or one user-facing
  improvement.
- Add or update tests whenever behavior changes, especially around pipeline
  stages, site rendering, storage, trends, and ideas.
- Keep config files free of secrets. Put API keys and delivery credentials in
  environment variables.
- Update docs and presets when the first-run experience changes.

## Pull requests

Include these points in the PR description:

- what changed
- why it matters to a user or operator
- which commands you ran locally
- sample output when the change affects README text, site rendering, or
  published artifacts

Use the PR template in `.github/pull_request_template.md`.

## Issues and preset requests

Use the issue templates for bug reports and preset requests.

If you are proposing a new preset, include:

- who it is for
- which sources it should watch
- which topics it should track
- what output shape you expect
