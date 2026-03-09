# Dependency Selection

This document lists the proposed dependencies for Recoleta v0 and why each is used.

## Principles

- Prefer widely used, modern libraries.
- Avoid overlapping stacks (choose one primary HTTP client).
- Make observability first-class (structured logs + durable state in SQLite).

## Runtime dependencies

### CLI and UX

- `typer`: ergonomic CLI with subcommands and nice help output.
- `rich`: progress bars and readable console output.

### Logging / observability

- `loguru`: structured logging with `logger.bind(module=...)`. Avoid sensitive data and high-cardinality binding keys.

### Config

- `pydantic` + `pydantic-settings`: typed settings, environment validation, and safe defaults.
- `platformdirs`: OS-appropriate default locations for app data (SQLite, artifacts).

### Networking and retries

- `httpx`: primary HTTP client for all outbound HTTP calls (async-friendly).
- `tenacity`: retry/backoff for transient failures.

Note on `aiohttp`:
- We **standardize on `httpx`** for Recoleta code.
- `aiohttp` may still exist as a **transitive dependency** (e.g. from other libraries). We should avoid using it directly unless a library requires it.

### Source ingestion

- `feedparser`: parse RSS feeds (HN RSS, newsletters).
- `arxiv`: arXiv API wrapper.
- `openreview-py`: OpenReview API client.
- `huggingface-hub`: access Hugging Face endpoints (papers/datasets/models metadata when applicable).

### Content extraction and Markdown

- `trafilatura`: extract main text from web pages.
- `beautifulsoup4`: optional HTML cleanup and fallback parsing.
- `markdownify`: convert HTML fragments to Markdown.
- `pymupdf4llm`: PDF-to-Markdown extraction (non-OCR). `pdf_text` enrich fails when PDFs have no readable text layer.
- `pyyaml`: emit YAML frontmatter reliably.
- `python-slugify`: stable, filesystem-safe note filenames.

### LLM

- `litellm`: unified model calling across providers using an OpenAI-compatible interface; supports structured output (`response_format`).
- `openai` + `anthropic`: official SDKs (useful for provider-specific features and compatibility).

### Embeddings (optional)

Semantic pre-ranking (triage) can reuse existing dependencies:

- `litellm`: call `litellm.embedding()` with an embedding model such as `text-embedding-3-small` (OpenAI) or a provider-specific embedding model.

Optional alternatives (not required for v0):

- `sentence-transformers`: fully local embeddings and cross-encoder reranking (higher footprint; commonly depends on `torch`).

### Local index (SQLite)

- `sqlmodel`: combines Pydantic + SQLAlchemy for a simple SQLite-based state store.

### Dedup / similarity

- `rapidfuzz`: fast string similarity for title deduplication.

### Telegram delivery

- `python-telegram-bot`: async bot client with built-in patterns for flood-limit avoidance and error handling.

### Optional (recommended for `recoleta run`)

- `apscheduler`: lightweight in-process scheduler for interval jobs.

### Optional (quality-of-life)

- `orjson`: fast JSON for debug artifacts (when enabled).

## Long-running operations additions

The current long-running design should stay conservative about new dependencies. The preference order is:

- use the standard library when it is sufficient
- reuse existing dependencies when they already solve the problem cleanly
- add one focused dependency only when it clearly replaces fragile custom code

### Runtime lock

Current selected direction for the current stage:

- use a SQLite-backed lease and keep the coordination logic in the existing state store

Fallback direction if that proves awkward in practice:

- `filelock`

Why `filelock` is a reasonable candidate:

- mainstream and lightweight
- actively used in Python tooling ecosystems
- much smaller design surface than introducing a broader coordination stack

Why not choose something heavier yet:

- the project is still single-user and single-writer
- we do not need distributed coordination semantics

### Backup and maintenance

Preferred direction:

- standard library first

Examples:

- SQLite backup APIs and file copies for backup/restore
- `shutil`, `pathlib`, and normal filesystem operations for pruning/cache cleanup

No extra maintenance dependency is justified yet.

### Migration support

Preferred direction for the current stage:

- no migration framework dependency yet
- use SQLite `PRAGMA user_version` before introducing any migration-specific library

Rationale:

- the immediate need is schema versioning and incompatibility detection, not a full migration ecosystem
- `alembic` is mainstream and modern enough, but still heavier than the current stage requires

Revisit `alembic` when:

- schema rewrites become frequent
- hand-maintained migration code becomes error-prone
- the project begins to need a real migration history rather than a small compatibility layer

### Container packaging

Preferred direction for the current stage:

- no extra Python runtime dependency for container support
- rely on Docker multi-target builds rather than introducing an in-app deployment abstraction

## Dev dependencies

- `pytest`, `pytest-asyncio`: testing async ingestion and delivery code paths.
- `respx`: mock `httpx` requests in tests.
- `ruff`: linting and formatting.
- `alembic` (deferred optional): reconsider only if schema evolution outgrows a lightweight in-repo approach.
