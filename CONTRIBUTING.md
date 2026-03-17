# Contributing

Recoleta is easiest to review when each change is small, behavior-driven, and
backed by tests or concrete output examples.

## Local setup

```bash
uv sync --group dev
uv run ruff check .
uv run pytest
```

Use focused tests while iterating:

```bash
uv run pytest tests/test_trends_static_site.py -q
```

## Contribution guidelines

- Keep changes scoped to one behavior or one user-facing improvement.
- Add or update tests for behavior changes, especially around pipeline stages,
  site rendering, storage, trends, and ideas.
- Keep config files non-secret. API keys and delivery credentials stay in env.
- Prefer updating docs and presets when the first-run experience changes.

## Pull requests

Include:

- what changed
- why the change matters to a user or operator
- commands you ran locally
- representative output when the change affects README copy, site rendering, or
  published artifacts

Use the PR template in `.github/pull_request_template.md`.

## Issues

Use the issue templates for:

- bug reports
- preset requests

If you are proposing a new preset, include the target user, sources, topics,
and the output shape you expect.
