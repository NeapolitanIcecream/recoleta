---
source: arxiv
url: https://arxiv.org/abs/2606.12329v1
published_at: '2026-06-10T17:02:56'
authors:
- Ripon Chandra Malo
- Tong Qiu
topics:
- code-intelligence
- ai-coding-agents
- project-memory
- mcp
- event-sourcing
- agent-guardrails
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# PROJECTMEM: A Local-First, Event-Sourced Memory and Judgment Layer for AI Coding Agents

## Summary
PROJECTMEM adds persistent project memory and a deterministic pre-action warning layer to AI coding agents. It targets repeated failed fixes and repeated context reconstruction across coding sessions.

## Problem
- AI coding agents lose project-specific state between sessions, so they re-read files, re-derive decisions, and may try fixes that already failed.
- The paper estimates that rebuilding project context can cost 5,000-20,000 tokens per session, which raises cost and wastes time.
- Repeated failed fixes matter because they can send an agent through the same debugging path without new evidence or tests.

## Approach
- PROJECTMEM records development history as an append-only plain-text event log with typed events: issue, attempt, fix, decision, and note.
- It rebuilds AI-readable summaries deterministically from the log, so the agent reads compact project memory without vector search, embeddings, or LLM fact extraction.
- It exposes memory through MCP with read and write tools, plus CLI commands and a Markdown bridge for tools without MCP support.
- Its precheck_file(path) gate checks the log before an edit and warns about prior failed attempts, open issues, or high-churn files tied to that path.
- It runs locally with no telemetry or cloud dependency, redacts secrets before writing events, and can promote library-level gotchas into a machine-wide local store.

## Results
- The released implementation is a Python package with 3 runtime dependencies, a footprint under 5 MB, 14 MCP tools, 19 CLI commands, and 37 automated tests.
- The paper evaluates usage through a 2-month self-study across 10 projects with 207 logged events.
- The system reports estimated savings through pjm score, including hours, tokens, and dollars, but the excerpt does not give measured savings values.
- The paper claims context rebuilding can cost 5,000-20,000 tokens per session, while memory reads have a more fixed cost after events are written.
- The capability table compares PROJECTMEM with 13 named systems and claims it is the only listed system with all six target properties: local-first, plain-text without vector DB, event-sourced immutable storage, pre-action judgment, MCP-native access, and cross-project memory.
- The paper does not report a controlled benchmark for coding task success rate, bug-fix accuracy, or head-to-head agent performance.

## Link
- [https://arxiv.org/abs/2606.12329v1](https://arxiv.org/abs/2606.12329v1)
