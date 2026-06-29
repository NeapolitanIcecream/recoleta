---
source: hn
url: https://github.com/wkdomains/macos-app
published_at: '2026-05-02T23:12:14'
authors:
- fcpguru
topics:
- coding-agents
- browser-automation
- mcp
- human-ai-interaction
- code-intelligence
- developer-tools
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Mac browser for a human that also gives coding agents local APIs

## Summary
wkdomains is a macOS browser that lets a human use a live logged-in page while a coding agent reads structured local browser state through APIs. Its main value is reducing the gap between what the human sees in the browser and what the agent can inspect.

## Problem
- Coding agents often need page context, login state, network calls, DOM structure, and domain metadata, but screenshots alone are incomplete and Playwright flows require the agent to recreate the browsing session.
- Developers working with Codex, Claude Code, Cursor, or similar tools need a way to share the exact page state they are viewing without copying data between browser, terminal, and chat.
- This matters for web debugging, API discovery, UI investigation, and authenticated request replay, where missing browser context can lead agents to guess.

## Approach
- The app keeps browsing under human control and exposes the current page state on a local API, defaulting to `http://localhost:9001`.
- The agent can request screenshots, URL and viewport data, visible DOM, links, console messages, resources, XHR/fetch summaries, cookies, localStorage, and sessionStorage.
- wkdomains scans domain entry points such as `/llms.txt`, `/openapi.json`, `/.well-known/agent-card.json`, `/sitemap.xml`, and `/robots.txt` when the agent terminal opens.
- A right-side browser terminal sends human questions as MCP human requests, so a separate watcher agent can inspect the page and reply inside the app.
- Viewport modes change what the APIs report, with desktop mode plus mobile widths of 700 px and 390 px.

## Results
- The excerpt reports no benchmark, user study, latency result, accuracy metric, or comparison against Playwright, browser DevTools, or agent-only browsing.
- The system exposes at least 8 named local API routes shown by examples: `/screenshot`, `/page`, `/dom`, `/links`, `/console`, `/resources`, `/xhr`, and `/cookies`.
- It checks 9 likely agent or developer entry points: `/llms.txt`, `/llms-full.txt`, `/openapi.json`, `/swagger.json`, `/.well-known/openapi.json`, `/.well-known/ai-plugin.json`, `/.well-known/agent-card.json`, `/sitemap.xml`, and `/robots.txt`.
- The interface can split the window into a 75% browser area and a 25% terminal panel for page-aware agent questions.
- It supports multiple app instances by changing ports, with examples using the default `9001` and a second instance on `9003`.
- The strongest concrete claim is workflow support: a human can stay logged in and browse normally while a watcher agent reads live page data, network shapes, storage, and discovered domain files without rebuilding the login flow.

## Link
- [https://github.com/wkdomains/macos-app](https://github.com/wkdomains/macos-app)
