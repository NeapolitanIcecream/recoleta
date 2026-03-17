# Data Model (SQLite + LanceDB + Markdown)

This document defines the current logical data model used by Recoleta: the SQLite truth store, the rebuildable LanceDB trend-search cache, and the Markdown/Obsidian output layout. The schema is scope-aware so one workspace can host multiple topic streams.

## SQLite tables (logical)

### `runs`

Tracks each managed run for auditing, leases, and freshness checks.

- `id` (PK, text): run id (UUID)
- `started_at` (datetime)
- `heartbeat_at` (datetime): refreshed while long-running commands hold the workspace lease
- `finished_at` (datetime, nullable)
- `status` (text): `running|succeeded|failed`
- `config_fingerprint` (text): hash of effective config (excluding secrets)

### `workspace_leases`

Single-row lease records that prevent concurrent writers from corrupting one workspace.

- `name` (PK, text): logical lease name
- `owner_token` (text)
- `run_id` (text, nullable)
- `command` (text)
- `pid`, `hostname` (nullable)
- `acquired_at`, `heartbeat_at`, `expires_at`

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
- `state` (text): `ingested|enriched|triaged|analyzed|published|retryable_failed|failed`
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
- `content_type` (text): `html_maintext|pdf_text|latex_source|html_document|markdown`
- `text` (text, nullable): short/medium content
- `artifact_path` (text, nullable): filesystem path for large blobs
- `content_hash` (text): sha256(text or file bytes)
- `created_at`

### `analyses`

LLM outputs (validated structured payload).

- `id` (PK, integer)
- `item_id` (FK -> items.id)
- `scope` (text): topic stream / publish scope (`default` in single-stream mode)
- `model` (text): e.g. `openai/gpt-5.4`
- `provider` (text): LiteLLM provider label
- `summary` (text)
- `topics_json` (text): list[string]
- `relevance_score` (real): 0..1
- `novelty_score` (real, nullable): 0..1
- `cost_usd` (real, nullable)
- `latency_ms` (integer, nullable)
- `created_at`

Constraint / index:

- unique `(item_id, scope)`

### `item_stream_states`

Per-stream item state machine. This lets one ingested item participate in several topic streams without duplicating the raw item row.

- `id` (PK, integer)
- `item_id` (FK -> items.id)
- `stream` (text)
- `state` (text)
- `created_at` / `updated_at`

### `deliveries`

Records outbound item deliveries for idempotency and audit.

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

### `trend_deliveries`

Records outbound trend deliveries (currently Telegram PDF sends) separately from item deliveries.

- `id` (PK, integer)
- `doc_id` (FK -> documents.id)
- `channel`, `destination`, `message_id`
- `content_hash`: hash of the generated trend delivery payload/PDF
- `status`: `sent|skipped|failed`
- `error` (nullable)
- `sent_at` (nullable)

Constraint / index:

- unique `(doc_id, channel, destination)`

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

Common metric names (non-exhaustive):

- `pipeline.triage.candidates_total`
- `pipeline.triage.selected_total`
- `pipeline.triage.embedding_calls_total`
- `pipeline.triage.failed_total`
- `pipeline.triage.duration_ms`

### `artifacts`

Optional debug artifacts (mainly for failures and LLM calls).

- `id` (PK, integer)
- `run_id` (FK -> runs.id)
- `item_id` (FK -> items.id, nullable)
- `kind` (text): `error_context|llm_request|llm_response|embedding_request|embedding_response|triage_summary|raw_html|raw_pdf`
- `path` (text): relative path under artifact root
- `created_at`

### `source_pull_states`

Persists incremental-ingest watermarks and conditional-fetch metadata per source/feed/query scope.

- `id` (PK, integer)
- `source` (text)
- `scope_kind`, `scope_key`
- `etag`, `last_modified` (nullable)
- `watermark_published_at` (nullable)
- `cursor_json`
- `created_at` / `updated_at`

Constraint / index:

- unique `(source, scope_kind, scope_key)`

### `documents`

Canonical trend/RAG document registry used by trend generation, materialization, and semantic search.

- `id` (PK, integer)
- `doc_type`: `item|trend`
- `scope`: topic stream / trend scope
- `item_id` (nullable, for `doc_type=item`)
- `source`, `canonical_url`, `title`, `published_at` (nullable item metadata copied for retrieval/export)
- `granularity`, `period_start`, `period_end` (nullable trend metadata for `doc_type=trend`)
- `created_at` / `updated_at`

Constraints / indexes:

- unique `(doc_type, item_id, scope)` for item documents
- unique `(doc_type, scope, granularity, period_start, period_end)` for trend documents

### `document_chunks`

Chunked text attached to `documents`, used for trend prompting, FTS, and retrieval.

- `id` (PK, integer)
- `doc_id` (FK -> documents.id)
- `chunk_index`
- `kind`: `summary|content|meta`
- `text`
- `start_char`, `end_char` (nullable)
- `text_hash`
- `source_content_type` (nullable)
- `created_at`

Constraint / index:

- unique `(doc_id, chunk_index)`

Retrieval boundary:

- `kind=meta` is reserved for system-facing projection/provenance metadata
- `meta` chunks are persisted in SQLite but are not indexed into `chunk_fts`
- agent-visible lexical retrieval only searches `summary|content`
- semantic retrieval remains summary-only, so provenance does not enter the
  agent corpus through embeddings either

### `chunk_embeddings`

SQLite-side embedding cache keyed by document chunk and embedding model. LanceDB stores the searchable vector tables and indices, while this table records the per-chunk embedding payload and invalidates stale rows when chunk text changes.

- `id` (PK, integer)
- `chunk_id` (FK -> document_chunks.id)
- `model`
- `dimensions` (nullable)
- `vector_json`
- `text_hash`
- `created_at`

Constraint / index:

- unique `(chunk_id, model)`

## LanceDB workspace

Recoleta also maintains a rebuildable LanceDB directory under `RAG_LANCEDB_DIR`.

- Stores vector tables and ANN/scalar indices for semantic trend search.
- Acts as a cache over SQLite `documents` / `document_chunks`.
- Safe to rebuild from SQLite with `recoleta rag sync-vectors` and `recoleta rag build-index`.

## Obsidian note layout

Recoleta writes user-facing notes into the configured Obsidian Vault.

Recommended folders:

- `Recoleta/Inbox/` (new items, one note per item)
- `Recoleta/Trends/` (weekly/monthly trend notes)
- `Recoleta/Artifacts/` (optional links to raw files)

With `topic_streams`, the default layout becomes:

- `Recoleta/Streams/<stream>/Inbox/`
- `Recoleta/Streams/<stream>/Trends/`

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
- `## Links` (canonical + PDF + related threads)

Derived trend/idea notes may also include projection provenance fields in
frontmatter:

- `pass_output_id`
- `pass_kind`
- `upstream_pass_output_id`
- `upstream_pass_kind`

## Local Markdown output layout

Recoleta can also write user-facing Markdown notes to a normal filesystem directory (no Obsidian required).

Default layout under `MARKDOWN_OUTPUT_DIR`:

- `latest.md` (entry point for the most recent publish run)
- `Runs/<run_id>.md` (per-run index)
- `Inbox/` (one note per item, Markdown + YAML frontmatter)
- `Trends/` (canonical trend markdown notes and derived trend PDFs)
- `Ideas/` (idea briefs derived from canonical `trend_ideas` pass outputs)
- `Trends/.pdf-debug/<pdf-stem>/` (optional trend PDF render debug bundle)
- `site/` (optional static site export derived from `Trends/`)

With `topic_streams`, the default layout becomes:

- `Streams/<stream>/latest.md`
- `Streams/<stream>/Inbox/`
- `Streams/<stream>/Trends/`

Trend markdown notes are the canonical source for the richer trend surfaces:

- Telegram trend PDFs render from `Trends/*.md`
- the static site exporter renders from a trend markdown directory
- a repository can mirror selected trend notes into `site-content/` while preserving `Streams/<stream>/Trends/` when topic streams are enabled
