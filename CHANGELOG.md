# Changelog

This file tracks user-visible changes by release.

The format follows Keep a Changelog, and tagged releases follow Semantic
Versioning.

## [Unreleased]

## [0.2.0] - 2026-04-09

### Added

- Workflow-first CLI entrypoints under `run`, `fleet`, `daemon`, `inspect`,
  `repair`, `stage`, and `admin`.
- `recoleta fleet run day|week|month|deploy` and `recoleta fleet site build`
  for manual multi-instance orchestration from one fleet manifest.
- `recoleta fleet site serve` for local aggregate-site preview from a fleet
  manifest.
- `recoleta inspect llm` for effective LLM config inspection and optional probe
  checks.
- `recoleta inspect why-empty` for machine-readable empty-corpus diagnostics.
- `recoleta inspect runs show` and `recoleta inspect runs list` for aggregated
  run inspection.
- `--json` output for `stage analyze`, `stage publish`, `stage trends`,
  `stage ideas`, `repair outputs`, `run site build`, `stage site stage`, and
  `run deploy`.
- Localized markdown output plus sibling presentation sidecars for translated
  trend and idea notes.

### Changed

- Multi-instance runtime is now instance-first: use child configs plus a fleet
  manifest instead of shared `topic_streams`.
- Config files, `.env`, or shell env containing `TOPIC_STREAMS` /
  `topic_streams` now fail fast.
- `run now|day|week|month|deploy` now act as the default workflow-first
  orchestration surface for end-to-end runs.
- Site export and translation now prefer sibling `.presentation.json` sidecars
  and fall back to markdown parsing only when needed.
- Runs now persist minimal context such as command, scope, granularity, and
  period bounds.
- Artifacts now persist lightweight structured failure summaries alongside
  artifact paths.

### Removed

- `recoleta repair streams`.
- Shared `TOPIC_STREAMS` / `topic_streams` runtime support and in-tree
  migration or recovery commands, including
  `recoleta admin migrate topic-streams-to-instances`.

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
