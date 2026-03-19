---
source: hn
url: https://github.com/baristaGeek/open-source-postman-for-mcp
published_at: '2026-03-02T23:40:15'
authors:
- baristaGeek
topics:
- model-context-protocol
- developer-tools
- api-testing
- stdio-transport
- debugging
relevance_score: 0.05
run_id: materialize-outputs
language_code: en
---

# Show HN: Open-Source Postman for MCP

## Summary
This is an open-source debugging and testing tool for Model Context Protocol (MCP) servers, positioned as a “Postman for MCP.” It primarily addresses the poor support that existing API clients provide for stdio-based MCP servers, as well as shortcomings in visualization and debugging experience.

## Problem
- The MCP server testing workflow is cumbersome: developers often need to manually inspect JSON-RPC logs, repeatedly re-enter requests, and switch between multiple terminals.
- Most existing API tools are oriented toward HTTP, while the text explicitly states that **most MCP servers use stdio transport**, making mainstream tools difficult to adapt directly.
- The lack of schema inspection, request history, and visual forms makes it inefficient to understand tool parameters, reproduce requests, and troubleshoot failures, which slows development and debugging across the MCP ecosystem.

## Approach
- Provides a desktop-style GUI that unifies connection to **stdio, HTTP, and SSE** MCP transport modes, with particular emphasis on native support for stdio.
- Reads tool schemas and automatically generates input forms and a schema inspector, so users can understand parameter requirements without digging through source code.
- Includes built-in request execution, response viewing, error display, latency display, and SQLite-based request history with one-click replay.
- Adds AI-assisted capabilities: users can describe intent in natural language, Claude automatically selects the tool and parameters, and summarization is also supported.
- On the implementation side, the system is built with Next.js 15, React 19, Prisma, SQLite, TypeScript, and the Anthropic SDK; backend routes separately handle stdio process management, HTTP/SSE forwarding, history, and summaries.

## Results
- The text **does not provide formal benchmark tests, user studies, or quantitative experimental results**, so there are no reportable figures for accuracy, speed improvements, or numerical comparisons against baseline tools.
- The strongest concrete functional conclusion is that the tool claims to support **3 transport types** (stdio, HTTP, SSE), with stdio as a core focus, which the author argues is a capability broadly missing from existing API clients.
- The tool provides **1-click** request execution and **1-click replay** for history, aiming to significantly reduce the manual work of copying JSON-RPC payloads and repeatedly entering parameters, but the text does not quantify the savings.
- The text explicitly states that **SSE transport is currently still stubbed out (not fully implemented)**, so although multi-transport support is claimed, the level of completeness is not fully consistent.
- The author’s core claim is that it fills a missing part of the MCP ecosystem’s developer tooling and can serve as a standardized entry point for testing, debugging, exploring schemas, and replaying requests for MCP servers, but this remains a product claim rather than a paper-style empirical result."

## Link
- [https://github.com/baristaGeek/open-source-postman-for-mcp](https://github.com/baristaGeek/open-source-postman-for-mcp)
