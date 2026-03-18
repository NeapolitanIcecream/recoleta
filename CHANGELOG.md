# Changelog

This file tracks user-visible changes by release.

The format follows Keep a Changelog, and tagged releases follow Semantic
Versioning.

## [Unreleased]

### Added

- `recoleta doctor llm` for effective LLM config inspection and optional probe
  checks.
- `recoleta doctor why-empty` for machine-readable empty-corpus diagnostics.
- `recoleta repair-streams` for stream-state repair by UTC day.
- `recoleta runs show` and `recoleta runs list` for aggregated run inspection.
- `--json` output for `analyze`, `publish`, `trends`, `trends-week`, `ideas`,
  `materialize outputs`, `site build`, `site stage`, and `site gh-deploy`.

### Changed

- Explicit stream reruns no longer depend on the global `items.state` being
  below `analyzed`.
- `401` and `403` auth failures are now classified as retryable for stream
  recovery.
- Runs now persist minimal context such as command, scope, granularity, and
  period bounds.
- Artifacts now persist lightweight structured failure summaries alongside
  artifact paths.

## [0.1.0] - 2026-03-16

First public release.

### Added

- A local-first research pipeline backed by SQLite.
- Multi-source ingest for arXiv, Hacker News RSS, Hugging Face Daily Papers,
  OpenReview, and RSS feeds.
- Structured LLM analysis with topic scoring and relevance filtering.
- Markdown-first publishing with optional Obsidian and Telegram delivery.
- Trend briefs, idea briefs, browser-rendered PDFs, and static site export.
- Docker images, a Compose workflow, healthchecks, and JSON workspace stats.
- Starter presets for `agents-radar`, `robotics-radar`, and `arxiv-digest`.
- Static-site repo-return calls to action.
- A shorter README plus dedicated usage and first-output guides.
- GitHub contribution templates and release-handoff docs.
- Sample screenshots and preset-to-demo mapping for first-run validation.

### Notes

- `0.1.0` is the first public baseline for the current repo surface.
- GitHub release notes can be generated from
  [`docs/releases/v0.1.0-draft.md`](docs/releases/v0.1.0-draft.md).
