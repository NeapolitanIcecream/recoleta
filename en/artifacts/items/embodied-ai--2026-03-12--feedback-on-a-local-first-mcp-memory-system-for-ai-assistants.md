---
source: hn
url: https://github.com/ptobey/local-memory-mcp
published_at: '2026-03-12T23:32:30'
authors:
- ptobey
topics:
- local-rag
- mcp-tools
- assistant-memory
- chromadb
- local-first
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Feedback on a local-first MCP memory system for AI assistants?

## Summary
This is a local-first personal memory system for AI assistants that uses MCP tools to quickly provide user context from a local vector database to new LLM sessions. It emphasizes self-hosting, versioned memory, lightweight metadata, and model-friendly warning-based write feedback, rather than complex human knowledge management structures.

## Problem
- It addresses the problem that newly started LLM sessions cannot reliably recover a user's long-term context; otherwise, assistants struggle to consistently remember preferences, constraints, schedules, and past decisions.
- Existing memory solutions often depend on cloud/SaaS or heavyweight schema design, which is unfavorable for technical users who want to self-host and control private data, and may not suit how LLMs consume context.
- Memory writes are also prone to overwrites, conflicts, and contamination from outdated information, leading to unreliable retrieval quality and assistant behavior.

## Approach
- It uses local ChromaDB to store text chunks and a small amount of metadata, representing memory as "clear text snippets + a few state fields" rather than complex document structures.
- It exposes tools such as `store`, `search`, `update`, `delete`, `get_chunk`, and `get_evolution_chain` through MCP so that new sessions can directly retrieve and recover context.
- During retrieval, it ranks results by combining semantic similarity with lightweight lexical signals and recency, while hiding deprecated chunks by default to reduce interference from outdated information.
- Updates use version chains and `supersedes` relationships, with soft delete by default to preserve history instead of destructive overwrites, making memory evolution easier to track.
- The write path adds heuristic conflict detection, structured `warnings[]` and self-heal hints, as well as health checks, helping the model self-correct when write risk is high.

## Results
- The text does not provide standard benchmark tests, public dataset experiments, or quantitative metrics, so there are **no reportable quantitative results**.
- It explicitly states that this is currently an "early but usable v1 release," sufficient to support "personal self-hosted workflows," though the API and internal heuristic rules may still change in later minor versions.
- It has implemented 6 core MCP tools: `store`, `search`, `update`, `delete`, `get_chunk`, `get_evolution_chain`.
- It supports 2 transport methods: stdio and SSE; SSE provides 3 authentication modes: `none`, `bearer`, `oauth`.
- It uses the local embedding model `all-MiniLM-L6-v2` and the local ChromaDB persistence directory `./chroma_db`, emphasizing that no cloud backend is required and data is stored locally by default.
- The strongest concrete claim is that version chains, conflict logs, warning-first write responses, and default hiding of deprecated chunks improve "practical retrieval quality and reliable AI behavior," but the text does not provide percentage improvements relative to a baseline.

## Link
- [https://github.com/ptobey/local-memory-mcp](https://github.com/ptobey/local-memory-mcp)
