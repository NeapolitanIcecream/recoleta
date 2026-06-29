---
source: hn
url: https://www.quandri.io/engineering-blog/mcp-is-dead
published_at: '2026-05-29T22:56:49'
authors:
- nadis
topics:
- mcp
- claude-code
- developer-tools
- code-agents
- cli-automation
- tool-use
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# MCP is dead?

## Summary
The article argues that MCP adds too much context cost, latency, and workflow fragility for many developer tools. It recommends CLI/API access with on-demand Skills when a CLI already exists.

## Problem
- MCP loads tool schemas into the LLM context, so common tools can consume space before the user asks for them.
- Extra MCP server processes add latency and can fail during initialization or mid-session.
- This matters for software agents because wasted context, slower calls, and brittle tool setup reduce the amount of code, logs, and task state the model can handle.

## Approach
- The authors measured JSON tool schemas from MCP servers loaded in their Claude Code setup, using the tool name, description, and parameters.
- They compared a Linear issue lookup through MCP with a direct `curl` call to the Linear GraphQL API.
- Their proposed mechanism is simple: use existing CLIs or APIs first, then store short usage instructions in Claude Skills so the model loads them only when needed.
- They still keep MCP for cases where it solves a real need, such as services without a good CLI, shared authentication, or safer database access.

## Results
- In their 4-server Claude Code setup, MCP tool definitions used 10.5% of the context window before any tool call.
- Linear alone loaded 42 tool definitions and about 12,807 tokens, even for a task that needed only an issue lookup.
- The same Linear issue lookup used about 200 tokens with a CLI/API call and about 12,957 tokens with MCP, a roughly 65x token increase.
- The referenced Jira benchmark found MCP was 3x slower per call than the REST API and 9.4x slower on the first call when initialization was included.
- Replacing MCP servers with Skills that wrap CLIs freed about 21K context tokens in Quandri's workflow and removed their daily MCP initialization failures.
- The update says Claude Code Tool Search with Deferred Loading now cuts MCP context use by 85%+, so the context-bloat result applies less to current Claude Code users.

## Link
- [https://www.quandri.io/engineering-blog/mcp-is-dead](https://www.quandri.io/engineering-blog/mcp-is-dead)
