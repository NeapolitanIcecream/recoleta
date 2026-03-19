---
source: hn
url: https://github.com/baristaGeek/open-source-postman-for-mcp
published_at: '2026-03-02T23:40:15'
authors:
- baristaGeek
topics:
- mcp
- developer-tools
- code-intelligence
- debugging
- agent-tooling
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# Show HN: Open-Source Postman for MCP

## Summary
This is an open-source debugging and testing tool for Model Context Protocol (MCP) servers, positioned as a kind of “Postman for MCP.” It primarily addresses the problem that most MCP servers rely on stdio transport, making visual debugging difficult with existing API clients.

## Problem
- The MCP server testing experience is poor: developers are often limited to viewing JSON-RPC logs in the terminal and manually constructing requests, which makes debugging costly.
- Existing tools mainly support HTTP, but the text claims that **90% of MCP servers use stdio**, which means mainstream API clients cannot directly support the most common usage scenario.
- The lack of schema inspection, request history, and replay capabilities makes it hard for developers to understand tool parameters, reproduce issues, and improve iteration efficiency.

## Approach
- Provides a desktop/GUI-style MCP client that can connect through **stdio, HTTP, and SSE**, with particular emphasis on stdio process management.
- Uses a **schema inspector + auto-generated forms** to convert MCP tool JSON schemas into fillable interfaces, reducing the need to hand-write JSON-RPC requests.
- Provides **persistent request history**, saving requests to SQLite and supporting one-click replay for easier debugging and reproduction.
- Integrates Anthropic-based **AI auto-select**: users describe their needs in natural language, and the model automatically selects the appropriate tool and parameters.
- At the system level, it uses Next.js 15/React 19, Prisma + SQLite, TypeScript, and API routes to organize stdio, HTTP/SSE, history, and summarization functionality.

## Results
- The project's core outcome is the delivery of a working open-source tool rather than a paper-style benchmark evaluation; **the text does not provide quantitative experimental results such as standard datasets, accuracy, success rate, or speed**.
- The strongest quantitative/specific claims in the text include: **90% of MCP servers use stdio**, and the tool supports **3 transport types** (stdio, HTTP, SSE).
- Key GUI-supported capabilities include: auto-generated input forms, full JSON schema viewing, request history saved to SQLite, one-click replay, and display of errors and timing.
- The author claims the tool significantly improves the MCP development experience by avoiding the inefficient workflow of “running the server in one terminal, the client in another, and manually copying JSON-RPC.”
- There are still limitations: **SSE transport is currently stubbed out**, indicating that multi-transport support is not yet fully mature; future plans include exporting collections, environment variables, batch/scripted requests, and desktop app packaging.

## Link
- [https://github.com/baristaGeek/open-source-postman-for-mcp](https://github.com/baristaGeek/open-source-postman-for-mcp)
