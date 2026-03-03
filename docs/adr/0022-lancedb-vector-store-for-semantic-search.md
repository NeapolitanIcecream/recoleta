---
title: "ADR 0022: LanceDB vector store for semantic search"
status: Accepted
---

## Context
Semantic search over tens of thousands of chunks is too slow with per-query SQLite reads and Python-side cosine sorting.

## Decision
Use **LanceDB** as an embedded vector store for summary chunk embeddings, keyed by `chunk_id` and made idempotent by `text_hash`. SQLite remains the durable source of truth for documents and chunks.

## Consequences
Semantic search becomes an ANN query with server-side filtering, and embeddings are no longer persisted as JSON in SQLite for query-time retrieval. A rebuild/sync step keeps LanceDB aligned with the SQLite corpus.

