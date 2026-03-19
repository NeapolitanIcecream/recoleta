---
source: hn
url: https://github.com/ptobey/local-memory-mcp
published_at: '2026-03-12T23:32:30'
authors:
- ptobey
topics:
- local-rag
- mcp
- ai-memory
- vector-database
- self-hosting
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Feedback on a local-first MCP memory system for AI assistants?

## Summary
This is a local-first personal memory system for AI assistants that uses MCP tools to quickly provide user context from a local vector database to new LLM sessions. It emphasizes self-hosting, traceable version history, and context organization that is friendly to models, rather than complex human knowledge taxonomies.

## Problem
- It addresses the problem that newly started LLM sessions cannot reliably inherit a user's long-term context, causing assistants to forget preferences, constraints, plans, and historical decisions.
- Existing memory solutions often rely on cloud/SaaS or complex document structures, making them unsuitable for technical users who prioritize privacy, self-hosting, and controllable data flow.
- Memory writes are also prone to conflicts, overwrites, and contamination from stale information, which harms retrieval quality and the reliability of subsequent agent behavior.

## Approach
- It adopts a local-first RAG approach: storing text chunks and a small amount of metadata in local ChromaDB, then exposing tools such as `store/search/update/delete/get_chunk/get_evolution_chain` to AI assistants via MCP.
- The core mechanism is simple: split user context into clear text fragments for storage; when a new session needs memory, perform semantic retrieval and rerank using a small number of lexical and recency signals.
- It uses lightweight metadata instead of a heavy schema: including timestamps, confidence, `supersedes` version chains, and deprecation flags, in order to preserve history and hide deprecated content by default.
- It performs heuristic reconciliation on writes; when overlap or conflicts are detected, it returns structured `warnings[]` and self-heal hints so the model can adjust its write behavior instead of silently overwriting.
- It uses soft delete by default and versioned updates (`strategy="version"`), supplemented by health checks, conflict logs, backup/restore, and two MCP transport modes: stdio and SSE.

## Results
- The text does not provide standard paper-style quantitative evaluation results, so there are **no reportable accuracy, recall, or benchmark comparison figures**.
- The clearly claimed deliverable is an “early but usable v1” for “personal self-hosted workflows,” and it already supports 6 core MCP tools: `store`, `search`, `update`, `delete`, `get_chunk`, and `get_evolution_chain`.
- On the retrieval side, it claims to support semantic search and to blend similarity, lightweight lexical signals, and recency in ranking; deprecated chunks are hidden by default to improve current context quality.
- On the write side, it claims to support heuristic conflict detection, conflict logging, warning-first responses, and self-heal fields to improve reliability when models write memory.
- In terms of engineering delivery, it provides 2 runtime paths (Docker or local Python), 2 MCP transports (stdio, SSE), and 3 SSE authentication modes (`none`, `bearer`, `oauth`).

## Link
- [https://github.com/ptobey/local-memory-mcp](https://github.com/ptobey/local-memory-mcp)
