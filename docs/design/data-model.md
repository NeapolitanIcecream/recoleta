# Data Model (SQLite + Obsidian)

This document defines the SQLite schema (logical model) and the Obsidian note layout used by Recoleta.

## SQLite tables (logical)

### `runs`

Tracks each pipeline run for auditing and trend stats.

- `id` (PK, text): run id (UUID)
- `started_at` (datetime)
- `finished_at` (datetime, nullable)
- `status` (text): `running|succeeded|failed`
- `config_fingerprint` (text): hash of effective config (excluding secrets)

### `items`

Canonical normalized records for source items.

- `id` (PK, integer)
- `source` (text): `arxiv|hn|hf_daily|openreview|rss`
- `source_item_id` (text, nullable): stable id from the source (e.g., arXiv id)
- `canonical_url` (text)
- `canonical_url_hash` (text): sha256(canonical_url)
- `title` (text)
- `authors` (text, nullable): serialized list
- `published_at` (datetime, nullable)
- `raw_metadata_json` (text): source-specific metadata
- `state` (text): `ingested|enriched|analyzed|published|failed`
- `created_at` / `updated_at`

Constraints / indexes:
- unique `(source, source_item_id)` when `source_item_id` is not null
- unique `canonical_url_hash`
- index on `published_at`
- index on `state`

### `contents`

Stores extracted content and links to large artifacts.

- `id` (PK, integer)
- `item_id` (FK -> items.id)
- `content_type` (text): `html_maintext|pdf_text|markdown`
- `text` (text, nullable): short/medium content
- `artifact_path` (text, nullable): filesystem path for large blobs
- `content_hash` (text): sha256(text or file bytes)
- `created_at`

### `analyses`

LLM outputs (validated structured payload).

- `id` (PK, integer)
- `item_id` (FK -> items.id, unique)
- `model` (text): e.g. `openai.gpt-4o-mini`
- `provider` (text): LiteLLM provider label
- `summary` (text)
- `insight` (text)
- `idea_directions_json` (text): list[string]
- `topics_json` (text): list[string]
- `relevance_score` (real): 0..1
- `novelty_score` (real, nullable): 0..1
- `cost_usd` (real, nullable)
- `latency_ms` (integer, nullable)
- `created_at`

### `deliveries`

Records outbound deliveries for idempotency and audit.

- `id` (PK, integer)
- `item_id` (FK -> items.id)
- `channel` (text): `telegram`
- `destination` (text): chat id or channel name (masked or hashed)
- `message_id` (text, nullable)
- `status` (text): `sent|skipped|failed`
- `error` (text, nullable)
- `sent_at` (datetime, nullable)

Constraints / indexes:
- unique `(item_id, channel, destination)` to prevent re-sends

### `metrics`

Machine-readable operational metrics (lightweight for v0).

- `id` (PK, integer)
- `run_id` (FK -> runs.id)
- `name` (text): e.g. `pipeline.ingest.items_total`
- `value` (real)
- `unit` (text, nullable)
- `created_at`

Guideline:
- Avoid high-cardinality metrics (do not encode item_id/url as metric name/labels).

### `artifacts`

Optional debug artifacts (mainly for failures and LLM calls).

- `id` (PK, integer)
- `run_id` (FK -> runs.id)
- `item_id` (FK -> items.id, nullable)
- `kind` (text): `llm_request|llm_response|error_context|raw_html|raw_pdf`
- `path` (text): relative path under artifact root
- `created_at`

## Obsidian note layout

Recoleta writes user-facing notes into the configured Obsidian Vault.

Recommended folders:

- `Recoleta/Inbox/` (new items, one note per item)
- `Recoleta/Trends/` (weekly/monthly trend notes)
- `Recoleta/Artifacts/` (optional links to raw files)

### Note naming

- `YYYY-MM-DD--<slug>.md`
- Slug derived from the title (stable, filesystem-safe).

### YAML frontmatter fields

Minimal frontmatter:

- `source`: `arxiv|hn|hf_daily|openreview|rss`
- `url`: canonical URL
- `published_at`: ISO timestamp
- `authors`: list of strings
- `topics`: list of strings
- `relevance_score`: float
- `run_id`: UUID

Body sections (recommended):

- `## Summary`
- `## Insight`
- `## Ideas`
- `## Links` (canonical + PDF + related threads)

