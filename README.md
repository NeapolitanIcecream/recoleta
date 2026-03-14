<p align="center">
  <img src="./docs/assets/Recoleta-3.jpeg" alt="Project Name Banner"/>
</p>

<!-- Badges (replace with your links) -->
<!-- [![CI](...)](...) -->
<!-- [![PyPI](...)](...) -->
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.14%2B-blue.svg)](#recoleta-installation)

Recoleta is a **research intelligence funnel** that ingests noisy sources, runs **structured LLM analysis**, and publishes high-signal outputs to **local Markdown by default** (with optional **Obsidian** and **Telegram** integrations) — so you can keep up with research without drowning in tabs.

## 📚 Contents

- [Overview](#recoleta-overview)
- [Features](#recoleta-features)
- [Installation](#recoleta-installation)
- [Docker / Compose](#recoleta-docker)
- [Usage](#recoleta-usage)
- [Configuration & CLI API](#recoleta-configuration)
- [Contributing](#recoleta-contributing)
- [License](#recoleta-license)

<a id="recoleta-overview"></a>
## 👀 Overview

Recoleta is local-first: it stores durable state in a local **SQLite** index and treats notes/messages as derived artifacts. A single instance can now run one or more **topic streams** so different topic domains can share ingest/enrich state while keeping analyze/publish outputs isolated.

```mermaid
flowchart LR
  Sources[Sources] --> Prepare["Prepare (recoleta ingest)"]
  Prepare --> Analyze["Analyze (LLM, recoleta analyze)"]
  Analyze --> Publish[Publish]
  Publish --> Markdown[Local Markdown output]
  Publish --> Obsidian["Obsidian Markdown notes (optional)"]
  Publish --> Telegram["Telegram messages (optional)"]
  Prepare --> SQLite[(SQLite index)]
  Analyze --> SQLite
  Publish --> SQLite
```

<a id="recoleta-features"></a>
## ✨ Features

- **Multi-source, stateful ingestion**: arXiv, Hacker News RSS, Hugging Face Daily Papers, OpenReview, and custom RSS feeds, with saved pull state for incremental runs.
- **Incremental & idempotent pipeline**: SQLite-backed state machine prevents duplicates and re-sends.
- **Structured LLM outputs**: JSON-only analysis validated by Pydantic (summary/tags/scores).
- **Topic streams**: one Recoleta instance can host multiple virtual topic-specific pipelines with separate analysis scopes and delivery sinks.
- **Semantic triage before LLM (optional)**: pre-rank (and optionally filter) candidates by topic similarity to improve LLM ROI under backlog.
- **Outputs where you read**: local Markdown output (default) + optional Obsidian notes + optional curated Telegram digest.
- **Trend surfaces with retrieval context**: trend generation can enrich prompts with semantic overview packs, representative source docs, bounded peer-history windows, browser-rendered PDFs, and a deployable static website.
- **Follow-on opportunity mining**: `recoleta ideas` can derive evidence-grounded why-now ideas from existing trend synthesis outputs without rerunning the full trend agent.
- **Operationally friendly**: structured logs, per-run metrics in SQLite, optional scrubbed debug artifacts.

<a id="recoleta-installation"></a>
## 📦 Installation

### Prerequisites

- **Python**: >= 3.14
- **Package manager**: [`uv`](https://docs.astral.sh/uv/) (recommended)
- **LLM provider** supported by LiteLLM (e.g. OpenAI / Anthropic)
- **Pandoc** (recommended): used to generate `html_document_md` from arXiv `html_document` when available
- **Optional integrations**:
  - Obsidian Vault (for writing notes directly into Obsidian)
  - Telegram Bot token + destination chat ID (for mobile digest)
  - Chromium-compatible browser for browser-rendered trend PDFs (`uv run playwright install chromium` is a good fallback when no system browser is available)

### Install (from source)

```bash
git clone https://github.com/NeapolitanIcecream/recoleta.git
cd recoleta
uv sync
uv run recoleta --help
```

<a id="recoleta-docker"></a>
## 🐳 Docker / Compose

Recoleta now ships an official multi-target `Dockerfile`.

- `runtime`: the default CLI image for the full command surface, including ingest/analyze/publish/run plus trends, site, RAG, DB, and maintenance commands
- `runtime-full`: extends `runtime` with Pandoc and Chromium for `html_document_md`, browser-rendered trend PDFs, and richer trend/web publishing flows

The Docker build uses `uv.lock` plus BuildKit cache mounts, so rebuilds should be materially faster after the first dependency sync when only application code changes.

The official container filesystem contract is:

- `/data/recoleta.db`
- `/data/outputs/`
- `/data/artifacts/`
- `/data/lancedb/`
- `/config/recoleta.yaml`

These are already wired through the image defaults:

```bash
RECOLETA_DB_PATH=/data/recoleta.db
MARKDOWN_OUTPUT_DIR=/data/outputs
ARTIFACTS_DIR=/data/artifacts
RAG_LANCEDB_DIR=/data/lancedb
RECOLETA_CONFIG_PATH=/config/recoleta.yaml
```

Build the core image:

```bash
docker build --target runtime -t recoleta:runtime .
```

Build the richer PDF/browser image:

```bash
docker build --target runtime-full -t recoleta:runtime-full .
```

`runtime-full` is intentionally much heavier because it installs Chromium. In practice, `runtime` is the better default for regular local/CI verification, while `runtime-full` fits release-time or explicitly manual builds.

Run a one-shot pipeline:

```bash
docker run --rm \
  --env-file .env \
  -v "$(pwd)/data:/data" \
  -v "$(pwd)/config:/config:ro" \
  recoleta:runtime run --once
```

Or use the included Compose example:

```bash
mkdir -p config data
cp recoleta.example.yaml config/recoleta.yaml
docker compose up -d
```

`.env` is optional for Compose itself, but is still the recommended place to provide LLM and delivery secrets.

The Compose service defaults to `recoleta run` and uses the read-only healthcheck:

```bash
recoleta doctor --healthcheck
```

For a read-only operational snapshot, use:

```bash
recoleta stats --json
```

If the container needs browser/PDF-capable trend surfaces, change the Compose build target from `runtime` to `runtime-full`.

<a id="recoleta-usage"></a>
## 🧰 Usage

### 🚀 Quick Start

Create a non-secret config file (all sources are disabled by default and must be explicitly enabled).

```bash
# Option A: copy the full example config and edit it
cp recoleta.example.yaml recoleta.yaml

# Option B: create a minimal config from scratch
cat <<'YAML' > recoleta.yaml
# NOTE: This file must NOT contain secrets. Keep tokens/API keys in env only.

recoleta_db_path: "~/.local/share/recoleta/recoleta.db"

# LiteLLM model naming: <provider>/<model-identifier>
# Examples:
# - openai/gpt-4o-mini
# - anthropic/claude-3-5-sonnet-20241022
llm_model: "openai/gpt-4o-mini"

# Publish targets (default: ["markdown"])
# Allowed: markdown, obsidian, telegram
publish_targets:
  - markdown

# Local Markdown output directory (default: platform-specific user data dir + /outputs)
markdown_output_dir: "~/.local/share/recoleta/outputs"

# Optional: language for summary text and trend notes.
# JSON keys stay in English and topics remain English tags.
llm_output_language: "Chinese (Simplified)"

topics:
  - agents
  - ml-systems

# Optional: instead of one global topic list, define multiple topic streams.
# topic_streams:
#   - name: agents_lab
#     topics: ["agents", "tooling"]
#     publish_targets: ["markdown", "telegram"]
#     telegram_bot_token_env: "AGENTS_LAB_TELEGRAM_BOT_TOKEN"
#     telegram_chat_id_env: "AGENTS_LAB_TELEGRAM_CHAT_ID"
#   - name: bio_watch
#     topics: ["biology", "therapeutics"]
#     publish_targets: ["markdown"]

sources:
  hn:
    enabled: true
    rss_urls:
      - "https://news.ycombinator.com/rss"
  rss:
    enabled: true
    feeds:
      - "https://example.com/feed.xml"

# Optional knobs
min_relevance_score: 0.6
max_deliveries_per_day: 10
write_debug_artifacts: false
YAML
```

Create a `.env` file for secrets and the config pointer.

```bash
cat <<'ENV' > .env
RECOLETA_CONFIG_PATH="./recoleta.yaml"

# Preferred: Recoleta-scoped LLM connection overrides
RECOLETA_LLM_API_KEY="sk-replace-me"
# RECOLETA_LLM_BASE_URL="http://localhost:4000/v1"

# Backward-compatible provider credentials (still supported)
# OPENAI_API_KEY="sk-replace-me"

# Optional: Telegram publishing (env-only)
# TELEGRAM_BOT_TOKEN="123456789:replace-me"
# TELEGRAM_CHAT_ID="@replace_me"
ENV
```

Run the pipeline end-to-end.

```bash
uv run recoleta ingest
uv run recoleta analyze --limit 50
uv run recoleta publish --limit 20
```

Or run the full pipeline once (no scheduler):

```bash
uv run recoleta run --once --analyze-limit 50 --publish-limit 20
```

For targeted catch-up or replay of one UTC day, pass `--date` to the stage command or the one-shot pipeline:

```bash
uv run recoleta ingest --date 2026-01-02
uv run recoleta analyze --date 2026-01-02 --limit 50
uv run recoleta publish --date 2026-01-02 --limit 20
uv run recoleta run --once --date 2026-01-02 --analyze-limit 50 --publish-limit 20
```

Command intent:
- `recoleta ingest`: prepare backlog (ingest + enrich + optional semantic triage)
- `recoleta analyze`: Stage 4 only (LLM on prepared items)
- `recoleta publish`: deliver analyzed items
- `recoleta run --once`: run `ingest -> analyze -> publish` once and exit

Incremental pull behavior:

- `--date` scopes `ingest`, `analyze`, `publish`, and `run --once` to one UTC day.
- When `--date` is omitted, source connectors reuse persisted pull state such as watermarks and conditional fetch headers where supported.
- Source-level diagnostics are recorded in SQLite metrics, including counts like `filtered_out_total`, `in_window_total`, and `not_modified_total`.

Where to look next:

- **Local Markdown**: `MARKDOWN_OUTPUT_DIR/latest.md` and `MARKDOWN_OUTPUT_DIR/Inbox/`
- **Topic streams**: when `topic_streams` is configured, Markdown output defaults to `MARKDOWN_OUTPUT_DIR/Streams/<stream>/`
- **Topic stream trends**: trend notes also follow stream-local output roots, e.g. `MARKDOWN_OUTPUT_DIR/Streams/<stream>/Trends/`
- **Ideas briefs**: opportunity notes write to `MARKDOWN_OUTPUT_DIR/Ideas/`, or `MARKDOWN_OUTPUT_DIR/Streams/<stream>/Ideas/` in topic-stream mode
- **Obsidian notes (optional)**: `OBSIDIAN_VAULT_PATH/OBSIDIAN_BASE_FOLDER/Inbox/`
- **Telegram (optional)**: messages are sent to `TELEGRAM_CHAT_ID`
- **SQLite index**: `RECOLETA_DB_PATH` (safe to re-run; deliveries are idempotent)

### 📈 Trend analysis (daily / weekly / monthly)

Recoleta can generate **trend notes** as a standalone stage:

```bash
uv run recoleta trends
```

Key behaviors:

- **Time windows**: `--date` is an anchor date in **UTC** (`YYYY-MM-DD` or `YYYYMMDD`).
  - `day`: the UTC calendar day of `--date`
  - `week`: ISO week (Monday start) containing `--date`
  - `month`: calendar month containing `--date`
- **Corpus sources**:
  - `day` trends are generated from **analyzed items** in that day.
  - `week` trends are generated from existing **day trend documents** in that week.
  - `month` trends are generated from existing **week trend documents** in that month.
- **Optional auto-backfill**: `--backfill` can auto-generate missing lower-granularity trends before generating `week`/`month` trends.
  - `week --backfill`: generates missing `day` trends for the week first.
  - `month --backfill`: generates missing `week` trends for the month first.
- **Token-safe**: if the corpus is empty, Recoleta **skips the LLM call** and emits a placeholder trend document.

Examples:

```bash
# Daily trend for today (UTC)
uv run recoleta trends --granularity day

# Daily trend for a specific day (UTC)
uv run recoleta trends --granularity day --date 2026-03-02

# Weekly trend (by default, requires daily trends for that week)
uv run recoleta trends --granularity week --date 2026-03-02

# Weekly trend with automatic daily backfill (missing days only)
uv run recoleta trends --granularity week --date 2026-03-02 --backfill

# Shortcut: weekly trend + backfill
uv run recoleta trends-week --date 2026-03-02

# Rebuild all daily trends for the week, then generate the weekly trend
uv run recoleta trends-week --date 2026-03-02 --backfill-mode all

# Monthly trend (requires weekly trends for that month)
uv run recoleta trends --granularity month --date 2026-03-02

# Monthly trend with automatic weekly backfill (missing weeks only)
uv run recoleta trends --granularity month --date 2026-03-02 --backfill

# Override the LLM model used for trend generation
uv run recoleta trends --granularity week --model "openai/gpt-4o-mini"
```

Outputs:

- **SQLite**: a durable `trend` document is persisted into `RECOLETA_DB_PATH`.
- **Local Markdown** (when `PUBLISH_TARGETS` includes `markdown`): `MARKDOWN_OUTPUT_DIR/Trends/` (canonical source for downstream PDF/site rendering)
- **Obsidian** (when `PUBLISH_TARGETS` includes `obsidian`): `OBSIDIAN_VAULT_PATH/OBSIDIAN_BASE_FOLDER/Trends/`
- **Telegram PDF** (when `PUBLISH_TARGETS` includes `telegram` and the corpus is non-empty): `<trend-note>.pdf`, rendered from the canonical markdown note

When `topic_streams` is configured, `recoleta trends` and `recoleta trends-week` run once per stream. Their outputs move under each stream root instead:

- Markdown: `MARKDOWN_OUTPUT_DIR/Streams/<stream>/Trends/`
- Obsidian: `OBSIDIAN_BASE_FOLDER/Streams/<stream>/Trends/`
- CLI summary: one aggregate line plus one `stream -> doc_id` line per stream

### 💡 Opportunity ideas from trend outputs

Recoleta can run a separate **ideas pass** on top of existing trend synthesis outputs:

```bash
uv run recoleta ideas --granularity day --date 2026-03-09
```

Key behaviors:

- **Upstream dependency**: `recoleta ideas` requires a matching `trend_synthesis` pass output for the same `day|week|month` window. It does not rerun `recoleta trends` automatically.
- **Same window semantics**: `--date` uses the same UTC anchor-date rules as `recoleta trends`.
- **Evidence-first output**: the ideas pass treats the upstream trend payload as the primary frame, then uses the active local corpus to verify and sharpen candidate opportunities.
- **Safe suppression**: when the window has too little evidence for reliable ideas, the pass returns `status=suppressed` instead of padding with generic suggestions.
- **Separate publication**: successful runs write an ideas brief under `MARKDOWN_OUTPUT_DIR/Ideas/` or `MARKDOWN_OUTPUT_DIR/Streams/<stream>/Ideas/`.

Examples:

```bash
# Generate daily ideas from an existing daily trend synthesis output
uv run recoleta ideas --granularity day --date 2026-03-09

# Generate weekly ideas from an existing weekly trend synthesis output
uv run recoleta ideas --granularity week --date 2026-03-02

# Override the LLM model used for ideas generation
uv run recoleta ideas --granularity day --date 2026-03-09 --model "openai/gpt-4o-mini"
```

Outputs:

- **SQLite**: the canonical `trend_ideas` pass output is persisted in `pass_outputs`.
- **Local Markdown**: a successful note is written to `MARKDOWN_OUTPUT_DIR/Ideas/`.
- **Topic streams**: when `topic_streams` is configured, `recoleta ideas` runs once per stream and the CLI prints one aggregate line plus one per-stream `status + pass_output_id` line.

Semantic context knobs (env or config):

- `RAG_LANCEDB_DIR`: where trend-search vectors and indices are stored (default: platform user data dir + `/lancedb`)
- `TRENDS_EMBEDDING_MODEL`, `TRENDS_EMBEDDING_DIMENSIONS`
- `TRENDS_EMBEDDING_BATCH_MAX_INPUTS`, `TRENDS_EMBEDDING_BATCH_MAX_CHARS`
- `TRENDS_EMBEDDING_FAILURE_MODE` (`continue|fail_fast|threshold`) and `TRENDS_EMBEDDING_MAX_ERRORS` (required when `threshold`)
- `TRENDS_SELF_SIMILAR_ENABLED`: build an overview pack from semantically related summaries / lower-level trend docs and attach representative source documents to clusters
- `TRENDS_RANKING_N`: top semantic matches per retrieval query used when filling clusters
- `TRENDS_OVERVIEW_PACK_MAX_CHARS`: size budget for the overview pack injected into the trend prompt
- `TRENDS_ITEM_OVERVIEW_TOP_K`, `TRENDS_ITEM_OVERVIEW_ITEM_MAX_CHARS`: how much per-item summary context is folded into day-trend overview packs
- `TRENDS_REP_MIN_PER_CLUSTER`: minimum cluster representatives to preserve after normalization/backfill
- `TRENDS_PEER_HISTORY_ENABLED`: add prior peer windows to the prompt so the trend payload can emit evolution notes
- `TRENDS_PEER_HISTORY_WINDOW_COUNT`, `TRENDS_PEER_HISTORY_MAX_CHARS`
- `TRENDS_EVOLUTION_MAX_SIGNALS`: cap the number of evolution signals kept after normalization

Manual RAG maintenance is optional. Normal trend runs can populate vectors on demand, but these commands help when you want to prewarm or repair the search corpus:

```bash
# Prebuild item-summary vectors for a date range
uv run recoleta rag sync-vectors \
  --doc-type item \
  --period-start 2026-03-01T00:00:00+00:00 \
  --period-end 2026-03-08T00:00:00+00:00

# Rebuild ANN / scalar indices after a large backfill
uv run recoleta rag build-index
```

PDF behavior:

- Telegram trend delivery renders the PDF from the canonical markdown note under `MARKDOWN_OUTPUT_DIR/Trends/`, or `MARKDOWN_OUTPUT_DIR/Streams/<stream>/Trends/` in topic-stream mode.
- The renderer uses `backend="auto"`: browser rendering via Playwright/Chromium first, then a `PyMuPDF Story` fallback if browser rendering is unavailable.
- Telegram uses a browser-rendered `continuous` page mode by default to avoid A4 page breaks in the mobile reading surface.
- `uv run recoleta trends --granularity day --debug-pdf` writes a debug bundle to `MARKDOWN_OUTPUT_DIR/Trends/.pdf-debug/<pdf-stem>/` containing the source markdown, normalized markdown, HTML, CSS, manifest, and per-page PNG previews.

### 🌐 Static trends site

Recoleta can turn trend notes into a deployable static website:

```bash
# Build and serve a local preview from trend markdown notes
uv run recoleta site serve

# Push a dedicated GitHub Pages branch without polluting main
uv run recoleta site gh-deploy
```

Behavior:

- `recoleta site serve` builds the site by default, then serves `MARKDOWN_OUTPUT_DIR/site` on `127.0.0.1:8000`.
- `recoleta site build` writes a clean static site to `MARKDOWN_OUTPUT_DIR/site` by default.
- `recoleta materialize outputs` backfills `Inbox/` item notes and rerenders trend markdown from existing DB trend documents without rerunning ingest/analyze; add `--site` and/or `--pdf` when you want to refresh derived HTML/PDF outputs in the same pass.
- `recoleta materialize outputs --scope <stream> --granularity week` is the targeted repair path when only one stream or one trend level needs to be regenerated.
- `recoleta site gh-deploy` builds the site into a temporary directory, commits it to a dedicated branch (default: `gh-pages`), and pushes that branch to the selected remote.
- `recoleta site gh-deploy` keeps the checked-out worktree on your source branch and skips the push when the generated snapshot is unchanged.
- In topic-stream mode, both commands automatically aggregate every `MARKDOWN_OUTPUT_DIR/Streams/<stream>/Trends/` directory.
- The static site now exposes a `Streams` navigation surface so mixed-domain trend notes are not silently flattened together.
- `recoleta site stage` remains available when you want a repo-local content snapshot for custom CI or non-GitHub hosting.
- All four commands treat their output directories as managed artifacts and clear stale files before writing when they rebuild site output.

Recommended GitHub Pages flow:

```bash
uv run recoleta site gh-deploy \
  --branch gh-pages \
  --pages-config auto
```

What `gh-deploy` does:

1. Builds the public site from your current trend markdown notes.
2. Creates or updates a dedicated deployment branch (default: `gh-pages`).
3. Force-pushes that derived branch by default, similar to `mkdocs gh-deploy`.
4. Tries to configure the repository Pages source to that branch when `gh` is authenticated or `GH_TOKEN` / `GITHUB_TOKEN` is available.

This keeps `main` free of `site-content/` snapshots and Pages-specific workflow YAML.

If you want explicit control over Pages configuration:

- `--pages-config auto`: best-effort; skip configuration if GitHub API credentials are unavailable
- `--pages-config always`: require automatic Pages source configuration, or fail
- `--pages-config never`: only push the deployment branch

If you prefer custom CI or another static host, `recoleta site stage` and `recoleta site build --input-dir ... --output-dir ...` still work with explicit paths and without loading the full runtime config.

### 🗓️ Run continuously (built-in scheduler)

```bash
uv run recoleta run
```

Tune the intervals via:

- `INGEST_INTERVAL_MINUTES`
- `ANALYZE_INTERVAL_MINUTES`
- `PUBLISH_INTERVAL_MINUTES`

### 🧪 Run manually (cron / launchd / systemd-friendly)

```bash
uv run recoleta run --once
```

Use explicit stage commands only when you intentionally want per-stage control:

```bash
uv run recoleta ingest
uv run recoleta analyze
uv run recoleta publish
```

Read-only operator checks:

```bash
# healthcheck-style contract; add freshness gating when needed
uv run recoleta doctor --healthcheck --max-success-age-minutes 180

# machine-readable backlog / lease / size snapshot
uv run recoleta stats --json
```

### 🧱 Deployment recipes

Recommended deployment split:

- use `uv run recoleta run` for a local always-on process
- use `uv run recoleta run --once` for cron, launchd, systemd timers, and scheduled containers
- use `uv run recoleta doctor --healthcheck` for supervisor/container liveness checks
- use `uv run recoleta stats --json` for dashboards, ad hoc inspections, or periodic snapshots

Minimal cron example:

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

### 🧹 Maintenance and recovery

Routine maintenance commands:

```bash
# prune expired debug artifacts, old runs, and old metrics
uv run recoleta gc

# additionally prune rebuildable caches such as inactive vector tables and derived PDFs
uv run recoleta gc --prune-caches

# compact the SQLite file after large cleanup windows
uv run recoleta vacuum
```

DB-scoped backup and restore:

```bash
# create a timestamped bundle under <db-dir>/backups/ by default
uv run recoleta backup

# restore from a specific bundle; requires explicit confirmation
uv run recoleta restore --bundle /path/to/backup-bundle --yes
```

Workspace reset helpers:

```bash
# Remove only trend/item document corpus rows and chunks; keep items, contents, analyses
uv run recoleta db reset --trends-only --yes

# Delete the SQLite DB and sidecars for a full clean slate
uv run recoleta db clear --yes
```

Scope notes:

- `backup` / `restore` operate on the SQLite state store only
- `db reset --trends-only` is useful when trend markdown/PDF/site output should be regenerated from fresh trend runs without losing ingest/analyze history
- `recoleta materialize outputs` is the safer repair path when the stored DB trend payloads are still authoritative and only filesystem outputs have drifted
- markdown outputs, artifacts, and LanceDB directories should still be protected by normal filesystem backups when they matter
- default GC is conservative; cache pruning is explicit so old canonical notes are not deleted by surprise

<a id="recoleta-configuration"></a>
## ⚙️ Configuration & CLI API

### Configuration sources & precedence

Recoleta loads typed settings from:

1. **Init args** (rare; mainly for tests)
2. **Environment variables**
3. **`.env`** in the working directory
4. **Config file** pointed to by `RECOLETA_CONFIG_PATH` (`.yaml`/`.yml`/`.json`)
5. Defaults (for optional fields)

**Secrets rule**: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, and `RECOLETA_LLM_API_KEY` are forbidden in the config file and must come from environment variables only.

### Settings reference

Required:

- `RECOLETA_DB_PATH` / `recoleta_db_path` (SQLite file path)
- `LLM_MODEL` / `llm_model` (LiteLLM model, format: `<provider>/<model>`)
- `PUBLISH_TARGETS` / `publish_targets` (default: `["markdown"]`)
- `MARKDOWN_OUTPUT_DIR` / `markdown_output_dir` (default: platform-specific data dir + `/outputs`)

Conditionally required:

- `OBSIDIAN_VAULT_PATH` / `obsidian_vault_path` (required when `PUBLISH_TARGETS` includes `obsidian`)
- `TELEGRAM_BOT_TOKEN` (env-only, required when `PUBLISH_TARGETS` includes `telegram`)
- `TELEGRAM_CHAT_ID` (env-only, required when `PUBLISH_TARGETS` includes `telegram`)

Common optional knobs:

- **Recoleta-scoped LLM connection**:
  - `RECOLETA_LLM_API_KEY` (env-only)
  - `RECOLETA_LLM_BASE_URL` / `llm_base_url`
- **LLM output language**:
  - `LLM_OUTPUT_LANGUAGE` / `llm_output_language` (applies to `summary` and trend notes; JSON keys and `topics` stay English)
- **Sources**: `SOURCES` / `sources`
  - `hn.enabled`, `hn.rss_urls`
  - `rss.enabled`, `rss.feeds`
  - `arxiv.enabled`, `arxiv.queries`, `arxiv.max_results_per_run`
  - `arxiv.enrich_method`, `arxiv.enrich_failure_mode`
  - `arxiv.html_document_max_concurrency`, `arxiv.html_document_requests_per_second`
  - `arxiv.html_document_log_sample_rate`
  - `openreview.enabled`, `openreview.venues`
  - `hf_daily.enabled`
- **Relevance & filtering**:
  - `TOPICS` / `topics`
  - `ALLOW_TAGS` / `allow_tags`
  - `DENY_TAGS` / `deny_tags`
  - `MIN_RELEVANCE_SCORE` / `min_relevance_score`
  - `MAX_DELIVERIES_PER_DAY` / `max_deliveries_per_day`
- **Analysis content truncation**:
  - `ANALYZE_CONTENT_MAX_CHARS` / `analyze_content_max_chars` (default: `32768`, set to `0` to disable truncation)
- **Semantic triage (pre-ranking before LLM)** (runs only when `TRIAGE_ENABLED=true` and `TOPICS` is non-empty):
  - `TRIAGE_ENABLED` / `triage_enabled`
  - `TRIAGE_MODE` / `triage_mode` (`prioritize|filter`)
  - `TRIAGE_EMBEDDING_MODEL` / `triage_embedding_model`
  - `TRIAGE_EMBEDDING_DIMENSIONS` / `triage_embedding_dimensions`
  - `TRIAGE_EMBEDDING_BATCH_MAX_INPUTS` / `triage_embedding_batch_max_inputs`
  - `TRIAGE_EMBEDDING_BATCH_MAX_CHARS` / `triage_embedding_batch_max_chars`
  - `TRIAGE_QUERY_MODE` / `triage_query_mode` (`joined|max_per_topic`)
  - `TRIAGE_CANDIDATE_FACTOR` / `triage_candidate_factor`
  - `TRIAGE_MAX_CANDIDATES` / `triage_max_candidates`
  - `TRIAGE_ITEM_TEXT_MAX_CHARS` / `triage_item_text_max_chars`
  - `TRIAGE_MIN_SIMILARITY` / `triage_min_similarity` (filter mode only)
  - `TRIAGE_EXPLORATION_RATE` / `triage_exploration_rate`
  - `TRIAGE_RECENCY_FLOOR` / `triage_recency_floor`
- **Execution limits**:
  - `ANALYZE_LIMIT` / `analyze_limit` (default Stage 4 batch size; also used as Stage 3.5 selection limit)
- **Dedup**:
  - `TITLE_DEDUP_THRESHOLD` / `title_dedup_threshold`
  - `TITLE_DEDUP_MAX_CANDIDATES` / `title_dedup_max_candidates`
- **Outputs**:
  - `PUBLISH_TARGETS` / `publish_targets`
  - `MARKDOWN_OUTPUT_DIR` / `markdown_output_dir`
  - `OBSIDIAN_BASE_FOLDER` / `obsidian_base_folder`
  - `ARTIFACTS_DIR` / `artifacts_dir` (required if `WRITE_DEBUG_ARTIFACTS=true`)
- **Browser PDF rendering**:
  - `RECOLETA_PLAYWRIGHT_EXECUTABLE_PATH`
  - `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH`
  - `GOOGLE_CHROME_BIN`
  - `CHROME_BIN`
- **Scheduling**:
  - `INGEST_INTERVAL_MINUTES`, `ANALYZE_INTERVAL_MINUTES`, `PUBLISH_INTERVAL_MINUTES`
- **Logging & diagnostics**:
  - `LOG_LEVEL` / `log_level`
  - `LOG_JSON` / `log_json`
  - `WRITE_DEBUG_ARTIFACTS` / `write_debug_artifacts`

### LiteLLM provider credentials

Recoleta delegates LLM calls to LiteLLM and PydanticAI. Preferred configuration is to use Recoleta-scoped overrides:

- `RECOLETA_LLM_API_KEY`
- `RECOLETA_LLM_BASE_URL`

These overrides are passed directly into Recoleta's own LLM calls and avoid collisions with other tools in the same shell session that also use `OPENAI_API_KEY` or `OPENAI_BASE_URL`.

Backward-compatible provider envs remain supported:

- OpenAI: `OPENAI_API_KEY`
- Anthropic: `ANTHROPIC_API_KEY`
- OpenRouter: `OPENROUTER_API_KEY`
- Custom OpenAI-compatible endpoints (including LiteLLM Proxy): `OPENAI_API_BASE` or `OPENAI_BASE_URL`
- Custom OpenRouter endpoints: `OPENROUTER_API_BASE` or `OPENROUTER_BASE_URL`

### Debug artifacts & metrics (optional)

Enable scrubbed debug artifacts:

- Set `WRITE_DEBUG_ARTIFACTS=true`
- Set `ARTIFACTS_DIR=/absolute/path/to/artifacts`

Recoleta writes per-run/per-item JSON artifacts (e.g. failure context and LLM request/response payloads) and **scrubs known secrets** before persisting them.

Recoleta also records lightweight, machine-readable **metrics** into the SQLite `metrics` table (e.g. stage durations, LLM call counts, publish outcomes).

### CLI commands

Recoleta's current CLI surface includes:

- `recoleta ingest --date 2026-01-02`: prepare one UTC day of source material (or the latest incremental backlog when `--date` is omitted)
- `recoleta analyze --limit 100 --date 2026-01-02`: run structured LLM analysis for prepared items
- `recoleta publish --limit 50 --date 2026-01-02`: write Markdown/Obsidian notes and send Telegram deliverables
- `recoleta run`: schedule ingest/analyze/publish periodically
- `recoleta run --once --date 2026-01-02`: execute a one-shot UTC-day pipeline
- `recoleta trends --granularity week --date 2026-03-02`: generate a trend note (day/week/month)
- `recoleta ideas --granularity week --date 2026-03-02`: derive evidence-grounded opportunity ideas from an existing trend synthesis output
- `recoleta trends-week --date 2026-03-02`: shortcut for weekly trends with lower-level backfill
- `recoleta trends --granularity day --debug-pdf`: generate a trend note and export a PDF debug bundle for the rendered Telegram PDF
- `recoleta site build`: render a static site from trend markdown notes
- `recoleta site gh-deploy`: build the site and push a dedicated GitHub Pages branch
- `recoleta site stage`: mirror trend markdown/PDF artifacts into a repo-local snapshot for custom CI or non-GitHub hosting
- `recoleta materialize outputs --site --pdf`: rerender item notes, trend notes, optional PDFs, and optional site output from existing DB state
- `recoleta rag sync-vectors --period-start ... --period-end ...`: prewarm or rebuild trend-search vectors in LanceDB
- `recoleta rag build-index`: build ANN/scalar indices for the current LanceDB embedding table
- `recoleta db reset --trends-only --yes`: clear trend corpus/documents without deleting items, contents, or analyses
- `recoleta db clear --yes`: delete the SQLite DB and sidecar files
- `recoleta stats --json`: emit a machine-readable workspace snapshot
- `recoleta doctor --healthcheck`: run a read-only healthcheck
- `recoleta gc`, `recoleta vacuum`, `recoleta backup`, `recoleta restore --bundle ... --yes`: maintenance and recovery commands

### Further reading

- [`docs/design/system-overview.md`](docs/design/system-overview.md) — goals, non-goals, and the end-to-end workflow
- [`docs/design/architecture.md`](docs/design/architecture.md) — module boundaries, pipeline stages, storage, and observability
- [`docs/design/configuration.md`](docs/design/configuration.md) — full configuration reference and rules
- [`docs/design/semantic-pre-ranking.md`](docs/design/semantic-pre-ranking.md) — semantic triage before LLM (pre-ranking and optional filtering)
- [`docs/plans/2026-03-14-ideas-real-data-smoke-and-calibration.md`](docs/plans/2026-03-14-ideas-real-data-smoke-and-calibration.md) — first real-data audit of the `ideas` pass and the current prompt baseline
- [`docs/design/outputs.md`](docs/design/outputs.md) — publish targets and local Markdown layout
- [`docs/design/trend-surfaces.md`](docs/design/trend-surfaces.md) — canonical trend markdown, browser PDF rendering, debug bundles, and static site deployment
- [`docs/design/llm-output-language.md`](docs/design/llm-output-language.md) — configurable analysis language behavior
- [`docs/design/data-model.md`](docs/design/data-model.md) — SQLite schema and Obsidian note layout
- [`docs/adr/`](docs/adr/) — architecture decision records (SQLite, LiteLLM, config file, Telegram delivery)

<a id="recoleta-contributing"></a>
## 🤝 Contributing

Install dev dependencies and run checks:

```bash
uv sync --group dev
uv run pytest
uv run ruff check .
```

<a id="recoleta-license"></a>
## 📄 License

Licensed under the **Apache License 2.0**. See [`LICENSE`](LICENSE).
