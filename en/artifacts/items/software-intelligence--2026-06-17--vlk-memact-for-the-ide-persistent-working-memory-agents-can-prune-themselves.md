---
source: hn
url: https://github.com/aranajhonny/vlk
published_at: '2026-06-17T23:23:12'
authors:
- akatsutki
topics:
- code-intelligence
- ide-agents
- persistent-memory
- mcp-server
- agent-context-management
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# Vlk: MemAct for the IDE – persistent working memory agents can prune themselves

## Summary
Vlk is a Rust MCP server that gives IDE coding agents persistent SQLite memory and a tool for deleting stale memory entries while saving a new lesson. It targets failure loops and context bloat in long-running coding-agent sessions.

## Problem
- Long-running IDE agents can keep retry errors, dead ends, and stale context, which wastes tokens and can trap the agent in loops.
- Normal chat context often disappears after a restart, so coding agents lose useful lessons between sessions.
- The problem matters for coding agents in Zed, Cursor, and Claude Desktop because they need durable task memory without carrying every failed attempt forward.

## Approach
- Vlk exposes one MCP tool, `vlk_time_travel`, over stdio JSON-RPC.
- The agent calls the tool with `target_mem_ids` to remove and a `learning` string to keep.
- `vlk-core` performs an atomic SQLite operation: delete selected rows from `agent_history`, then insert the lesson.
- SQLite WAL stores the memory in `vlk.db`, so the IDE agent can reuse it after restarts.
- The design follows MemAct from Zhang et al. 2025, where memory editing is an action the agent can choose at runtime.

## Results
- The excerpt gives no benchmark, user study, task success rate, latency result, or token-savings measurement.
- It claims one exposed tool: `vlk_time_travel`.
- In the shown example, memory slots `5`, `6`, and `7` are deleted and replaced with the lesson `London API down, use cached 12°C`.
- The test command reports `1 slots pruned, N tokens saved`, but the excerpt does not give a concrete value for `N`.
- Supported clients named in the excerpt are Zed, Cursor, and Claude Desktop via MCP configuration.

## Link
- [https://github.com/aranajhonny/vlk](https://github.com/aranajhonny/vlk)
