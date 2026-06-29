---
source: hn
url: https://github.com/BetaBots-LLC/callimachus
published_at: '2026-06-20T23:00:27'
authors:
- arishaller
topics:
- code-intelligence
- coding-agents
- local-search
- developer-tools
- agent-memory
- human-ai-interaction
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Show HN: Callimachus – Local search across your AI coding-agent history

## Summary
Callimachus is a local app that indexes AI coding-agent conversations and makes them searchable from desktop, CLI, VS Code/Cursor, and MCP clients. It targets developers who use several coding agents and need prior decisions, TODOs, file mentions, and transcripts without sending the index to a cloud service.

## Problem
- AI coding-agent work is split across many tools, so past decisions, fixes, and TODOs are hard to find during later coding sessions.
- Lost thread history can cause repeated work, inconsistent project decisions, and weak context when switching between Claude Code, Codex, Cursor, Gemini CLI, and other tools.
- The tool matters because agent memory helps only when developers and agents can retrieve it inside the editor, terminal, or agent session where work happens.

## Approach
- It imports conversations from 11 coding-agent sources into one local SQLite database.
- Search combines SQLite FTS5/BM25 keyword ranking with on-device vector search through sqlite-vec, then merges rankings with Reciprocal Rank Fusion.
- A file-mention index maps paths to threads, so a query such as `file:embed/mod.rs` can find sessions that touched that file.
- Optional LLM passes extract decisions, gotchas, TODOs, summaries, conflicts, and cited answers over prior threads.
- The same index is exposed through a desktop app, `cal` CLI, VS Code/Cursor extension, provider-agnostic chat, and an MCP server that lets agents read and write project memory.

## Results
- Supports 11 sources: Claude Code, Codex, Cursor, Gemini CLI, Qwen Code, Goose, OpenCode, Continue, Cline, Roo Code, and Kilo Code.
- Ships 16 MCP tools, including thread search, current-project search, file-to-thread lookup, cited history Q&A, decision recall, gotcha recall, and memory writes.
- The CLI exposes 21 commands, including search, recent, export, ask, files, memory, done, remember, agents, and hook.
- The semantic index uses `bge-small-en-v1.5` embeddings with 384 dimensions and sqlite-vec KNN running locally.
- The author reports indexing a Claude corpus of about 90,000 messages in about 25 seconds, with later passes skipping unchanged files.
- No benchmarked retrieval accuracy, baseline comparison, or user-study result is reported in the provided text.

## Link
- [https://github.com/BetaBots-LLC/callimachus](https://github.com/BetaBots-LLC/callimachus)
