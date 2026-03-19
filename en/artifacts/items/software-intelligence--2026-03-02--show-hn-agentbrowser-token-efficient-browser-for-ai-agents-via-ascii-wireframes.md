---
source: hn
url: https://github.com/agent-browser-io/browser
published_at: '2026-03-02T23:07:05'
authors:
- dokdev
topics:
- browser-automation
- ai-agents
- token-efficiency
- ascii-ui
- mcp-tools
relevance_score: 0.89
run_id: materialize-outputs
language_code: en
---

# Show HN: AgentBrowser Token-efficient browser for AI agents via ASCII wireframes

## Summary
AgentBrowser is a real browser control tool for AI agents. It represents pages using ASCII wireframes instead of full webpage content, thereby reducing token consumption. It primarily serves MCP clients and Vercel AI SDK use cases, enabling agents to perform web navigation and interaction in a lighter-weight way.

## Problem
- When existing AI agents operate browsers, they typically need to process full DOMs, screenshots, or rich-text page representations, leading to **high token overhead** and severe context waste.
- For agent tasks that require multi-step web interactions, high-cost page representations limit scalability, responsiveness, and automation stability.
- This matters because browser interaction is a key interface for code agents, automation assistants, and general software agents to carry out real-world tasks.

## Approach
- The core mechanism is to convert webpages into numbered **ASCII wireframes**: elements such as links, buttons, and text are presented in simplified text form, and the agent understands the page and performs actions such as clicking, typing, and scrolling through the numbering.
- The system exposes a unified set of browser tools, such as `launch`, `navigate`, `getWireframe`, `click`, `type`, `scroll`, and `screenshot`, allowing the model to complete tasks through sequences of tool calls.
- Actual browser execution is driven by a **Playwright** backend, so the agent is still controlling a real browser rather than a simulated page.
- It provides two main integration methods: one is via **MCP** into clients such as Cursor and Claude Desktop; the other is as tools embedded in applications through the **Vercel AI SDK**.

## Results
- The text does not provide standard academic evaluations, benchmark data, or ablation studies, so there are **no quantitative results** available for comparing performance gains.
- The strongest concrete claim is that the system enables AI agents to control a real browser in a **token-efficient** way, and to perform navigation, clicking, typing, hovering, selecting, checking, scrolling, screenshotting, and closing through ASCII wireframes.
- The provided toolset includes at least **14 operations**: `launch`, `navigate`, `getWireframe`, `click`, `type`, `fill`, `dblclick`, `hover`, `press`, `select`, `check`, `uncheck`, `scroll`, `screenshot`, `close`.
- The text gives an example agent workflow of up to **20 steps** (`stopWhen: stepCountIs(20)`), showing that the model can access Hacker News, open the top 3 news items, and summarize their contents, but this is only a usage example, not a formal experimental result.
- In terms of environment compatibility, the project requires **Node 18+** and states that it can be used in Cursor/Claude Desktop via MCP over JSON-RPC over stdio.

## Link
- [https://github.com/agent-browser-io/browser](https://github.com/agent-browser-io/browser)
