---
source: hn
url: https://github.com/Foued-pro/Mnemos
published_at: '2026-04-25T23:28:51'
authors:
- foufouadi
topics:
- code-intelligence
- memory-augmented-llm
- local-first-ai
- mcp
- retrieval-augmented-generation
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# I reverse-engineered Claude Desktop's storage to give it memory

## Summary
Mnemos gives Claude Desktop a local memory layer by reading Claude's on-disk conversation storage, indexing it, and exposing search through MCP. It aims to avoid long-context slowdown and confusion by retrieving relevant past fragments instead of keeping everything in one active chat.

## Problem
- Claude Desktop has no history or memory API, so past conversations are hard to reuse in a structured way.
- Very long chats can degrade model behavior as context grows, with slower responses, more confusion, and more hallucinations; the project describes this as context rot.
- Users who want persistent memory with privacy may not want cloud sync or external API calls.

## Approach
- Mnemos reverse-engineers Claude Desktop's local Chromium storage, watches files in real time, decompresses stored data, and parses conversation records from active sessions and history.
- It embeds messages locally with the ONNX version of MiniLM-L6-v2, then stores text and vectors in SQLite using FTS5 for keyword search and vector blobs for semantic search.
- It exposes retrieval back to Claude through an MCP server over JSON-RPC, so Claude can query relevant past snippets on demand.
- Search uses hybrid retrieval: BM25 keyword ranking from SQLite FTS5 plus cosine-similarity semantic ranking, merged with Reciprocal Rank Fusion.
- v1.1 adds a local GUI that lets users browse, search, and visualize conversation history with UMAP and K-Means in a 3D view.

## Results
- The system claims fully offline operation: no API calls, no cloud sync, and no data leaving the machine.
- It claims real-time indexing with OS file watchers and semaphore debouncing, with zero polling overhead.
- Embeddings use MiniLM-L6-v2 with 384-dimensional vectors, and the visualization projects those embeddings with UMAP plus K-Means clustering.
- The paper excerpt gives no benchmark numbers for retrieval quality, latency, memory savings, hallucination reduction, or user outcomes.
- The strongest concrete claim is architectural: hybrid search with Reciprocal Rank Fusion gives better recall than semantic search alone or keyword search alone, but no measured comparison is included in the excerpt.

## Link
- [https://github.com/Foued-pro/Mnemos](https://github.com/Foued-pro/Mnemos)
