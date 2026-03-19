---
source: hn
url: https://github.com/agent-browser-io/browser
published_at: '2026-03-02T23:07:05'
authors:
- dokdev
topics:
- browser-agents
- ascii-wireframes
- token-efficiency
- mcp-tools
- playwright
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Show HN: AgentBrowser Token-efficient browser for AI agents via ASCII wireframes

## Summary
This is a “real browser” control tool for AI agents that exposes web pages to models through ASCII wireframes rather than rich visual pages, thereby reducing the token cost of browser interaction. It is more like an engineering system release than an academic paper, with the focus on providing a unified browser toolchain across MCP/SDK/CLI.

## Problem
- Existing AI agents operating browsers often rely on screenshots, HTML, or complex DOM/visual representations, which lead to long context windows and high token overhead.
- High token costs limit the scalability and stability of multi-step web tasks, especially during repeated interactions such as navigation, clicking, typing, and scrolling.
- What is needed is an interface that still lets models operate a real browser, but represents page state in a more compact textual form; this is important for building practical web agents.

## Approach
- The core mechanism is to convert web page state into an **ASCII wireframe**: interactive elements and text content on the page are numbered and linearized, and the model uses those numbers to understand the page and decide the next action.
- The system still connects to a **real browser**, using Playwright underneath to execute operations such as `launch`, `navigate`, `click`, `type`, `scroll`, and `screenshot`, so it is not a purely simulated environment.
- It provides a unified tool interface that can be exposed to clients like Cursor and Claude Desktop via **MCP**, or called directly in code through the **Vercel AI SDK**.
- The interaction flow is simple: start the browser, open a web page, get the wireframe, and then perform actions such as clicking, typing, and selecting based on numbered elements.
- In essence, this design replaces an “expensive visual/page representation” with a “compact text UI” to improve the token efficiency of agentic browsing.

## Results
- The text **does not provide formal paper-style quantitative results**; it does not report metrics such as success rate, token savings percentage, benchmark datasets, or numerical comparisons with other browser agents.
- The strongest concrete claim is that the system supports a complete browser toolset, with **14 action tools**: `launch`, `navigate`, `getWireframe`, `click`, `type`, `fill`, `dblclick`, `hover`, `press`, `select`, `check`, `uncheck`, `scroll`, `screenshot`, `close` (the text lists 15 names, covering the main browser operations).
- The document gives an ASCII wireframe example for Hacker News, in which page elements are numbered to at least **[137]**, showing that this representation can compress a fairly complex web page into a single text view for model consumption.
- In terms of compatibility, the authors claim it can be used with **MCP clients** (such as Cursor and Claude Desktop), the **Vercel AI SDK**, and the **CLI**, and that it requires **Node 18+** while browser automation is based on **Playwright**.
- In the example agent workflow, the model is constrained to **20 steps** (`stepCountIs(20)`) to visit Hacker News, inspect the top 3 stories, and summarize their content, but this is only a usage example and does not constitute benchmark evidence.

## Link
- [https://github.com/agent-browser-io/browser](https://github.com/agent-browser-io/browser)
