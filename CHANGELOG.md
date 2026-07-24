# Changelog

This file tracks user-visible changes by release.

The format follows Keep a Changelog, and tagged releases follow Semantic
Versioning.

## [Unreleased]

### Fixed

- Trend emails now keep the title-rule gap on the content-bearing title cell,
  avoiding a standalone full-width spacer surface that Outlook could repaint.

## [0.6.1] - 2026-07-24

### Fixed

- Updated the standard Huldra dependency to 0.4.1 so Fleet maintenance can
  reclaim queue items after their durable HTTP 429 cooldown or transient
  backoff expires.

## [0.6.0] - 2026-07-22

### Changed

- Enabled arXiv sources now default to Huldra-backed pool mode. Huldra ships in
  the standard installation; the built-in direct adapter and local SQLite pool
  are deprecated, explicit rollback paths with no automatic fallback.
- The deprecated direct arXiv adapter now lazy-loads the `arxiv` SDK from the
  `legacy-arxiv` extra, so standard Huldra deployments no longer install or
  import it.
- Scheduled day, week, and month workflows now target only closed UTC periods
  and reconcile a bounded number of missed windows oldest first.
- Trend emails now use a clearer title hierarchy with Outlook-safe spacing and
  explicit background colors.

### Added

- `recoleta fleet daemon start --manifest ...` with top-level fleet schedules
  and one crash-safe host-local lease around each complete catch-up sequence.
- Bounded automatic Huldra pre-sync for missing mature workflow windows.
- Cross-process SQLite admission and cooldown for arxiv.org HTML, PDF, and
  e-print content fetches. A content 429 is not retried immediately and does not
  trigger an HTML-to-PDF fallback request.

### Fixed

- Fleet and single-instance dry-runs no longer evaluate Huldra readiness or
  submit missing windows, preserving the zero-side-effect dry-run contract.
- Translation payloads retain their validated model field order so complex
  fields cannot cause later top-level fields to be emitted at the wrong level.
- Analyze budget receipts now fingerprint Stage 4 semantics instead of broad,
  unrelated settings while retaining trusted legacy receipt compatibility.
- Installed CLI entrypoints now use Typer's public context type and remain
  compatible with unlocked dependency resolution through Typer 0.27.

## [0.5.0] - 2026-07-17

### Added

- Optional stage-specific LLM settings for analyze, trends, ideas, and
  translation, with `--model` overrides and provenance-aware refresh behavior.
- Exact evidence-read traces and independent-source quality gates for generated
  Trends and Ideas. JSON command output now reports whether an artifact
  succeeded or was suppressed through `artifact_status`.
- Analyze budget receipts so bounded day workflows can skip a completed
  analysis budget while still reporting the remaining backlog.
- Static pagination for generated Trends, Ideas, Topics, Archive, and topic
  detail collections without changing existing first-page URLs.
- Inline and display mathematics on generated web pages through semantic
  MathML, with readable TeX retained in email output.
- A no-model artifact quality evaluator for comparing generated output and
  detecting evidence, repetition, and lifecycle regressions.

### Changed

- Low-evidence Trend and Idea windows are now suppressed instead of padded with
  unsupported prose. Suppression also invalidates derived Ideas and removes
  stale Markdown, presentation, PDF, and debug projections.
- The generated site and trend email use a simpler reading layout, localized
  interface copy, semantic item metadata, deduplicated sources, accessible
  email markup, and a plain-text email alternative.
- Trend and Idea generation now checks recent outputs for repeated titles,
  openings, summaries, and boilerplate before accepting new artifacts.
- The optional Huldra dependency now pins the reviewed `huldra-arxiv` 0.3.0
  commit.

### Fixed

- Forced standalone translation reruns now stay within their requested scope,
  and dated translation commands default to day granularity.
- Outlook email calls to action use the corrected VML alignment and the site
  color palette.
- Translation metrics are aggregated in bounded batches and flushed when a
  batch is interrupted; noisy dependency logs are routed through Recoleta's
  logging policy.
- Artifact garbage collection retains unsafe or unresolved records, keeps runs
  referenced by skipped artifacts, and unlinks artifact symlinks without
  deleting their targets.

## [0.4.0] - 2026-06-02

### Added

- Idempotent ensure/backfill planning for `recoleta run day|week|month` and
  the matching fleet workflows.
- Dry-run JSON plan output for day, week, and month workflows, including step
  decisions, skip reasons, and planned expensive-step counts.

### Changed

- Week and month workflows now skip recursive lower-granularity trend and idea
  generation when that lower-granularity task set already exists in the parent
  window. Use `--force` for intentional regeneration.
- Pydantic AI RAG, trend, and idea agents now use `RECOLETA_LLM_API_KEY` and
  `RECOLETA_LLM_BASE_URL` consistently with the LiteLLM-backed stages.
- The `huldra` optional extra now installs the `huldra-arxiv` package from the
  pinned Huldra repository revision.

### Fixed

- Fleet deploy refreshes the email-ready site before manual trend email
  delivery.
- Manual trend email calls to action render more reliably in Outlook.
- Manual trend email summary excerpts now show when the text was truncated.
- Lower-granularity trend backfill now fills only untouched lower-level outputs
  instead of regenerating existing daily or weekly trend work during a parent
  window replay.

## [0.3.0] - 2026-05-22

### Added

- Optional Huldra-backed arXiv pool mode for workspaces that need arXiv
  metadata served from a shared pool instead of fetched by each instance.
- `recoleta arxiv-pool sync|backfill|worker`, `recoleta inspect arxiv-pool
  freshness`, and `recoleta admin arxiv-pool gc` for managing pool-backed
  arXiv metadata.
- Pool readiness checks for single-instance and fleet workflows, including
  maturity lag, `off|warn|strict` gating, structured readiness payloads, and
  fleet pre-sync behavior.
- Huldra-backed arXiv pool settings in starter presets, the example config,
  and the main operator docs.
- `recoleta inspect localization` for checking localized output coverage before
  previewing or publishing multilingual surfaces.
- Workflow timing metrics and benchmark/comparison helpers for fleet day runs.
- Batch-first manual trend email runs that can cover multiple configured
  granularities.

### Changed

- Presets that include arXiv now use Huldra-backed pool mode by default.
- Freshness reporting now separates run freshness, data freshness, derived
  windows, and backup recovery points more consistently.
- Refactor-audit guidance now uses the released `cremona` package and the
  repo's checked-in structural-debt baseline.

### Fixed

- arXiv HTML enrichment now respects conservative fetch-rate limits more
  consistently.
- Huldra-backed arXiv pool sync rejects unsupported force-refresh paths and
  reports structured skip or block reasons.

## [0.2.1] - 2026-04-10

### Added

- Manual trend email preview/send via `recoleta run email preview|send` and
  `recoleta fleet run email preview|send`.
- `EMAIL` config plus env-only `RECOLETA_RESEND_API_KEY` for Resend-backed
  manual trend email delivery.
- Private site email link-map companion artifacts to support site-first link
  resolution for manual trend email batches.
- Batch-oriented manual email send safety checks: public trend page
  reachability, recipient deduplication, and mixed resend protection unless
  `--force-batch`.

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
