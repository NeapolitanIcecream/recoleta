---
source: hn
url: https://mcplexer.com
published_at: '2026-06-24T23:08:50'
authors:
- maxrev17
topics:
- mcp-runtime
- agent-orchestration
- code-intelligence
- multi-agent-systems
- human-ai-interaction
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# Show HN: Mcplexer.com

## Summary
MCPlexer is an open-source cross-harness MCP runtime that gives coding agents one small tool surface plus routed access to workers, memory, browser control, approvals, audit, workspaces, and servers. It targets teams using multiple AI coding clients and shared controls across real software projects.

## Problem
- AI coding clients often load large static tool lists into context, which wastes context and makes tool access harder to control.
- Work split across Claude Code, Codex, Cursor, Gemini, and similar clients can lose task state, memory, approvals, and audit history.
- Powerful MCP servers for GitHub, databases, email, calendars, browsers, and deployment tools need routing, secrets, sandboxing, and review before they are safe in real repos.

## Approach
- MCPlexer exposes a small universal surface, centered on `mcpx__search_tools`, `mcpx__execute_code`, and secret refs, instead of exposing every downstream tool directly.
- It routes tool calls through workspace policy, auth scopes, approvals, audit logging, restrictions, and sandbox controls.
- It adds agent coordination primitives: delegations, workers, task ledgers, leases, offers, assignments, context packets, attachments, and persistent memory.
- It provides browser control through a visible Chrome/Playwright layer that can be used by different harnesses and workers.
- It lets agents configure servers, routes, auth scopes, audit, and approvals inside `~/.mcplexer`, while ordinary project repos only see the slim surface.

## Results
- The excerpt reports no benchmark results, user study, latency numbers, safety evaluation, or cost comparison.
- It claims support for 7 named MCP clients: Claude Code, Codex, OpenCode, Cursor, Grok, Pi, and Gemini, plus other MCP clients.
- It lists 15 feature areas: delegations, workers, tasks, memory, browser, workspaces, restrictions, approvals, audit, servers, secrets, mesh, skills, models, and dashboard.
- It names at least 11 downstream service targets: GitHub, Linear, Slack, Gmail, Calendar, Postgres, Vercel, WordPress, WooCommerce, Reddit, and Telegram, plus browsers and custom servers.
- Its strongest concrete claim is operational, not experimental: one routed MCP layer can give multiple coding harnesses the same delegation, memory, browser, approval, audit, workspace, sandbox, and secret-handling behavior.

## Link
- [https://mcplexer.com](https://mcplexer.com)
