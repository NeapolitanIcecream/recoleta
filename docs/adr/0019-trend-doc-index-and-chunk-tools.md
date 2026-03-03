---
title: "ADR 0019: Trend doc index + chunk tools"
status: Accepted
---

## Context
Recoleta needs daily/weekly/monthly trend analysis with model-driven exploration over the local corpus, while staying local-first and SQLite-backed.

## Decision
Add a SQLite-backed **document + chunk index** (`documents`, `document_chunks`) with **FTS5** (`chunk_fts`) for lexical search. Use an embedded vector store (**LanceDB**) for semantic search over summary chunks. Expose these via tool-style APIs so the model can navigate by **position** (doc_id/chunk_index) and optionally use text/semantic search.

## Consequences
Trend generation is implemented as a tool-calling agent with typed output validation, and weekly/monthly aggregation can reuse the same mechanism over lower-level trend documents. SQLite remains the source of truth; LanceDB is a derived index; filesystem notes (Markdown/Obsidian) are derived outputs.

