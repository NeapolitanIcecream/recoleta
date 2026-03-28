<p align="center">
  <img src="./docs/assets/Recoleta-3.jpeg" alt="Project Name Banner"/>
</p>

[![CI](https://github.com/NeapolitanIcecream/recoleta/actions/workflows/ci.yml/badge.svg)](https://github.com/NeapolitanIcecream/recoleta/actions/workflows/ci.yml)
[![Live demo](https://img.shields.io/badge/demo-live-0b7a75)](https://neapolitanicecream.github.io/recoleta/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.14%2B-blue.svg)](#recoleta-installation)

Recoleta watches arXiv, Hacker News, OpenReview, Hugging Face Daily Papers, and
RSS from one local workspace. It keeps state in SQLite, writes Markdown first,
and can turn the same corpus into trend briefs, idea briefs, PDFs, and a static
site.

**Start here:** [Live demo](https://neapolitanicecream.github.io/recoleta/) · [5-minute quickstart](#recoleta-quickstart) · [First output tour](./docs/guides/first-output-tour.md) · [Fleet development runbook](./docs/guides/fleet-development-runbook.md) · [Preset gallery](./presets/README.md) · [CLI v2 migration](./docs/guides/cli-v2-migration.md)

- Run one instance or a fleet of isolated instances from one manifest.
- Keep SQLite as the source of truth and regenerate Markdown, site pages, and
  delivery outputs from stored state.
- Start from a preset if you want a smaller first run.

## 📚 Contents

- [Overview](#recoleta-overview)
- [Features](#recoleta-features)
- [Installation](#recoleta-installation)
- [Docker / Compose](#recoleta-docker)
- [Usage](#recoleta-usage)
- [Starter presets](#recoleta-presets)
- [Common commands](#recoleta-common-commands)
- [Guides & reference](#recoleta-guides)
- [Contributing](#recoleta-contributing)
- [License](#recoleta-license)

<a id="recoleta-overview"></a>
## 👀 Overview

Recoleta is local-first by design. The database is the durable record of what
was ingested, analyzed, and published. Markdown notes, PDFs, Telegram messages,
and site pages are rebuildable outputs on top of that state.

One workspace can run a single instance. A migrated deployment can also run a
fleet manifest that points at several isolated child instances. Each child keeps
its own config, DB, outputs, and delivery state.

<a id="recoleta-features"></a>
## ✨ Features

- Pull from arXiv, Hacker News RSS, Hugging Face Daily Papers, OpenReview, and
  custom RSS feeds.
- Reuse saved pull state so reruns stay incremental and idempotent.
- Validate JSON-only LLM analysis with Pydantic.
- Run several isolated child instances from one fleet manifest.
- Pre-rank items semantically before the LLM when backlog pressure matters.
- Publish to local Markdown by default, with optional Obsidian and Telegram
  delivery.
- Build trend briefs, idea briefs, PDFs, and a static site from stored local
  state.
- Inspect runs through structured logs, SQLite metrics, and optional debug
  artifacts.

<a id="recoleta-installation"></a>
## 📦 Installation

### Prerequisites

- Python 3.14+
- [`uv`](https://docs.astral.sh/uv/)
- An LLM provider supported by LiteLLM
- Pandoc if you want `html_document_md` output from arXiv `html_document`
- Optional integrations:
  - Obsidian vault for direct note writing
  - Telegram bot token and chat ID for chat delivery
  - Chromium-compatible browser for browser-rendered trend PDFs

### Install from source

```bash
git clone https://github.com/NeapolitanIcecream/recoleta.git
cd recoleta
uv sync
uv run recoleta --help
```

<a id="recoleta-docker"></a>
## 🐳 Docker / Compose

Use `runtime` for normal CLI usage. Use `runtime-full` when you need Pandoc or
browser-rendered PDFs.

- `runtime`: workflow-first CLI surface, stage primitives, inspection, repair,
  admin, and related utilities
- `runtime-full`: `runtime` plus Pandoc and Chromium

The image uses these default paths:

- `/data/recoleta.db`
- `/data/outputs/`
- `/data/artifacts/`
- `/data/lancedb/`
- `/config/recoleta.yaml`

They map to these environment variables:

```bash
RECOLETA_DB_PATH=/data/recoleta.db
MARKDOWN_OUTPUT_DIR=/data/outputs
ARTIFACTS_DIR=/data/artifacts
RAG_LANCEDB_DIR=/data/lancedb
RECOLETA_CONFIG_PATH=/config/recoleta.yaml
```

Build the default image:

```bash
docker build --target runtime -t recoleta:runtime .
```

Build the PDF/browser image:

```bash
docker build --target runtime-full -t recoleta:runtime-full .
```

Run the current UTC-day workflow once:

```bash
docker run --rm \
  --env-file .env \
  -v "$(pwd)/data:/data" \
  -v "$(pwd)/config:/config:ro" \
  recoleta:runtime run now
```

Or use the bundled Compose file for a long-running daemon:

```bash
mkdir -p config data
cp recoleta.example.yaml config/recoleta.yaml
# edit config/recoleta.yaml and enable workflows + daemon.schedules first
docker compose up -d
```

Compose runs `recoleta daemon start` by default. Set `workflows` and
`daemon.schedules` in `config/recoleta.yaml` before using `docker compose up -d`
for long-running execution. With the stock example file, the daemon will stay up
but no workflow will run until you enable at least one schedule.

The bundled healthcheck uses:

```bash
recoleta inspect health --healthcheck
```

For a machine-readable workspace snapshot:

```bash
recoleta inspect stats --json
```

If you want a one-shot test run from the same service definition:

```bash
docker compose run --rm recoleta run now
```

If you need browser/PDF output, switch the Compose build target from `runtime`
to `runtime-full`.

<a id="recoleta-usage"></a>
## 🧰 Usage

<a id="recoleta-quickstart"></a>
### 🚀 Quick start

#### Fastest local run with Docker Compose

This is the shortest path from clone to first local output:

```bash
mkdir -p config data
cp recoleta.example.yaml config/recoleta.yaml

cat <<'ENV' > .env
RECOLETA_CONFIG_PATH=/config/recoleta.yaml
RECOLETA_LLM_API_KEY="sk-replace-me"
ENV

docker compose run --rm recoleta run now
```

Check these paths after the run:

- `./data/outputs/latest.md`
- `./data/outputs/Inbox/`
- `./data/outputs/Trends/`
- `./data/outputs/site/index.html`
- `./data/recoleta.db`
- When the day has enough evidence: `./data/outputs/Ideas/`

Then open the [first output tour](./docs/guides/first-output-tour.md) to compare
your local files with sample output.

Use `docker compose up -d` later when you want the bundled `daemon start`
service to keep running from `daemon.schedules`.

#### Run from source

Create a non-secret config file. All sources are off until you enable them.

```bash
# Option A: copy the full example config and edit it
cp recoleta.example.yaml recoleta.yaml

# Option B: create a minimal config from scratch
cat <<'YAML' > recoleta.yaml
# Keep secrets in env, not in this file.

recoleta_db_path: "~/.local/share/recoleta/recoleta.db"

# LiteLLM model naming: <provider>/<model-identifier>
# Examples:
# - openai/gpt-5.4
# - anthropic/claude-3-5-sonnet-20241022
llm_model: "openai/gpt-5.4"

# Publish targets (default: ["markdown"])
# Allowed: markdown, obsidian, telegram
publish_targets:
  - markdown

# Local Markdown output directory
markdown_output_dir: "~/.local/share/recoleta/outputs"

# Optional: canonical language for newly generated summaries, trends, and ideas.
# JSON keys stay in English and topics remain English tags.
llm_output_language: "English"

# Optional: derive additional localized output trees and a multilingual site.
# localization:
#   source_language_code: "en"
#   site_default_language_code: "en"
#   legacy_backfill_source_language_code: "zh-CN"
#   targets:
#     - code: "zh-CN"
#       llm_label: "Chinese (Simplified)"

topics:
  - agents
  - ml-systems

sources:
  hn:
    enabled: true
    rss_urls:
      - "https://news.ycombinator.com/rss"
  rss:
    enabled: true
    feeds:
      - "https://example.com/feed.xml"

min_relevance_score: 0.6
max_deliveries_per_day: 10
write_debug_artifacts: false
YAML
```

Create `.env` for secrets and the config pointer:

```bash
cat <<'ENV' > .env
RECOLETA_CONFIG_PATH="./recoleta.yaml"

# Preferred: Recoleta-scoped LLM connection overrides
RECOLETA_LLM_API_KEY="sk-replace-me"
# RECOLETA_LLM_BASE_URL="http://localhost:4000/v1"

# Backward-compatible provider credentials
# OPENAI_API_KEY="sk-replace-me"

# Optional: Telegram publishing
# TELEGRAM_BOT_TOKEN="123456789:replace-me"
# TELEGRAM_CHAT_ID="@replace_me"
ENV
```

Run the default UTC-day workflow:

```bash
uv run recoleta run now
```

Use these commands when you want more control:

```bash
uv run recoleta run day --date 2026-01-02
uv run recoleta run week --date 2026-03-02
uv run recoleta run month --date 2026-03-02
```

Use `stage` only when you want one primitive without workflow orchestration:

```bash
uv run recoleta stage ingest --date 2026-01-02
uv run recoleta stage analyze --date 2026-01-02 --limit 50
uv run recoleta stage publish --date 2026-01-02 --limit 20
```

If `localization` is configured, derive translated reading surfaces after the
canonical outputs exist:

```bash
uv run recoleta run translate --include items,trends,ideas
```

If you are migrating a historical corpus that was written in another canonical
language, run the one-time backfill:

```bash
uv run recoleta stage translate backfill --all-history --include items,trends,ideas --emit-mirror-targets
```

How workflows behave:

- `recoleta run now`: run the current UTC day end to end
- `recoleta run day`: run one UTC day end to end
- `recoleta run week`: run one ISO week end to end, including day-level and
  week-level trends and ideas
- `recoleta run month`: run one month end to end, including day/week/month
  trends and ideas
- `recoleta run translate`, `recoleta run site build`, and
  `recoleta run deploy`: derived workflows from stored state
- `recoleta stage ...`: run one primitive only, with no recursive orchestration

How reruns work:

- `recoleta run day --date YYYY-MM-DD` replays one UTC day end to end.
- `recoleta stage ingest|analyze|publish|trends|ideas --date YYYY-MM-DD`
  reruns one primitive when you do not want the full workflow.
- Without `--date`, connectors reuse saved pull state such as watermarks and
  conditional fetch headers when available.
- Source diagnostics are written to SQLite metrics, including values such as
  `filtered_out_total`, `in_window_total`, and `not_modified_total`.

If you are coming from older CLI docs or automation, start with
[`docs/guides/cli-v2-migration.md`](./docs/guides/cli-v2-migration.md).

Where outputs go:

- Local Markdown: `MARKDOWN_OUTPUT_DIR/latest.md` and
  `MARKDOWN_OUTPUT_DIR/Inbox/`
- Trend briefs: `MARKDOWN_OUTPUT_DIR/Trends/`
- Idea briefs: `MARKDOWN_OUTPUT_DIR/Ideas/`
- Localized Markdown: `MARKDOWN_OUTPUT_DIR/Localized/<language>/Inbox/`,
  `Trends/`, and `Ideas/` when `localization` is configured
- Static site: `MARKDOWN_OUTPUT_DIR/site/`; multilingual builds emit
  `/<language>/...` roots and a root redirect page that remembers the browser's
  last language choice
- Obsidian notes: `OBSIDIAN_VAULT_PATH/OBSIDIAN_BASE_FOLDER/Inbox/`
- Telegram: sent to `TELEGRAM_CHAT_ID`

For a migrated fleet, each child instance gets its own `MARKDOWN_OUTPUT_DIR`.
The fleet manifest sits above those child output trees.
- SQLite state: `RECOLETA_DB_PATH`

<a id="recoleta-presets"></a>
### 🧭 Starter presets

Use a preset when you want working sources and output paths without editing the
full example config first.

- [`presets/agents-radar.yaml`](./presets/agents-radar.yaml): track agent
  tooling, code agents, and evals
- [`presets/robotics-radar.yaml`](./presets/robotics-radar.yaml): watch
  embodied AI, VLA, and robotics work
- [`presets/arxiv-digest.yaml`](./presets/arxiv-digest.yaml): start with a
  paper-only arXiv digest
- [`presets/README.md`](./presets/README.md): pick the right preset and see the
  matching guide
- [`docs/guides/first-output-tour.md`](./docs/guides/first-output-tour.md):
  compare your local output with screenshots and demo pages

<a id="recoleta-common-commands"></a>
### 🧰 Common commands

```bash
# run the current UTC day end to end
uv run recoleta run now

# run a migrated multi-instance deployment from one fleet manifest
uv run recoleta fleet run day --manifest ./fleet/fleet.yaml
uv run recoleta fleet run week --manifest ./fleet/fleet.yaml
uv run recoleta fleet run deploy --manifest ./fleet/fleet.yaml

# replay one UTC day, week, or month
uv run recoleta run day --date 2026-03-09
uv run recoleta run week --date 2026-03-02
uv run recoleta run month --date 2026-03-02

# rerun one primitive only
uv run recoleta stage trends --granularity day --date 2026-03-09
uv run recoleta stage ideas --granularity day --date 2026-03-09

# translate derived language variants
uv run recoleta run translate --include items,trends,ideas

# one-time backfill for historical canonical content
uv run recoleta stage translate backfill --all-history --include items,trends,ideas --emit-mirror-targets

# build, preview, or deploy the public site
uv run recoleta run site build
uv run recoleta run site serve
uv run recoleta run deploy --branch gh-pages --pages-config auto

# inspect or repair a workspace
uv run recoleta inspect health --healthcheck --max-success-age-minutes 180
uv run recoleta inspect stats --json
uv run recoleta inspect llm --json
uv run recoleta inspect why-empty --date 2026-03-15 --granularity day --json
uv run recoleta repair outputs --site --pdf --json
uv run recoleta inspect runs show --run-id <run-id> --json
uv run recoleta inspect runs list --limit 5 --json
```

When you are scripting a subcommand, check `--help` for its `--json` support.

For daemon schedules, translation backfills, repair workflows, and admin
commands, see [`docs/guides/usage-recipes.md`](./docs/guides/usage-recipes.md).

<a id="recoleta-guides"></a>
## 📚 Guides & reference

### User guides

- [`docs/guides/first-output-tour.md`](docs/guides/first-output-tour.md) -
  check what a good first run should create
- [`docs/guides/fleet-development-runbook.md`](docs/guides/fleet-development-runbook.md) -
  run a migrated fleet by hand and keep the old shared DB archived
- [`docs/guides/usage-recipes.md`](docs/guides/usage-recipes.md) - common CLI
  workflows, site tasks, and operator recipes
- [`docs/guides/cli-v2-migration.md`](docs/guides/cli-v2-migration.md) - map
  older command names to the workflow-first CLI surface
- [`presets/README.md`](presets/README.md) - choose a starter preset and follow
  its guide
- [`CONTRIBUTING.md`](CONTRIBUTING.md) - contribution, issue, and preset request
  guidance

### Release docs

- [`CHANGELOG.md`](CHANGELOG.md) - user-visible changes by release
- [`docs/releases/v0.1.0-draft.md`](docs/releases/v0.1.0-draft.md) - public
  release notes draft
- [`docs/releases/v0.1.0-launch-kit.md`](docs/releases/v0.1.0-launch-kit.md) -
  reusable launch copy

### Design reference

- [`docs/design/configuration.md`](docs/design/configuration.md) - full config
  reference and rules
- [`docs/design/system-overview.md`](docs/design/system-overview.md) - goals,
  non-goals, and end-to-end workflow
- [`docs/design/outputs.md`](docs/design/outputs.md) - output directories and
  publish target behavior
- [`docs/design/trend-surfaces.md`](docs/design/trend-surfaces.md) - trend
  markdown, PDFs, and static site behavior
- [`docs/design/architecture.md`](docs/design/architecture.md) - module
  boundaries, pipeline stages, storage, and observability
- [`docs/design/data-model.md`](docs/design/data-model.md) - SQLite schema and
  output layout
- [`docs/design/semantic-pre-ranking.md`](docs/design/semantic-pre-ranking.md) -
  semantic triage before LLM
- [`docs/design/llm-output-language.md`](docs/design/llm-output-language.md) -
  analysis language behavior
- [`docs/adr/`](docs/adr/) - architecture decision records

<a id="recoleta-contributing"></a>
## 🤝 Contributing

See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for PR expectations, issue templates,
and preset request guidance.

Install dev dependencies and run the standard checks:

```bash
uv sync --group dev
uv run pytest
uv run ruff check .
```

<a id="recoleta-license"></a>
## 📄 License

Licensed under the **Apache License 2.0**. See [`LICENSE`](LICENSE).
