---
source: hn
url: https://github.com/LvcidPsyche/auto-browser
published_at: '2026-03-12T23:56:26'
authors:
- Lvcid
topics:
- mcp
- browser-agent
- human-in-the-loop
- playwright
- auth-session-reuse
- agent-orchestration
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Auto-Browser – An MCP-native browser agent with human takeover

## Summary
Auto-Browser is an open-source browser agent system for authorized scenarios that wraps a real browser as an **MCP-native service** and supports human takeover when automation fails. It emphasizes "log in once, reuse later," auditability, safety guardrails, and local self-hosting, rather than stealth scraping or bypassing anti-bot systems.

## Problem
- Existing browser automation or LLM tool-calling often fails on real websites because of logins, pop-ups, complex flows, pre-CAPTCHA human-verification walls, or brittle UI flows, causing agents to be unable to complete tasks reliably.
- Many systems merely bolt a browser onto an agent framework, lacking a unified MCP interface, session persistence, human takeover, auditing, and approvals, which makes them hard to use for everyday authorized workflows.
- For real enterprise and personal scenarios, being able to safely reuse login state, avoid interrupting sessions when failures occur, and maintain traceability is important, because this directly determines whether a browser agent can enter production-assist workflows.

## Approach
- The core mechanism is to implement the browser agent as an **MCP server**: the control layer uses FastAPI + Playwright to drive Chromium, exposing a unified tool interface to models, and it can also be invoked via REST or MCP JSON-RPC.
- The system operates through an "observe + act" loop: it returns screenshots, interactable element IDs, DOM/accessibility summaries, and optional OCR text, allowing the model to perform clicks, typing, hovering, selecting, waiting, pagination, and other actions based on the screen and page structure.
- When web flows become brittle or require human handling, it uses noVNC for **human takeover**, letting a person directly take over the same browser session and then resume automation afterward without losing context.
- To support "log in once, reuse later," the system can save encrypted auth state and named auth profiles and restore them in new sessions; it also provides host allowlists, upload approvals, operator identity headers, audit logs, metrics, and durable job records.
- For stronger isolation requirements, it supports per-session browser isolation with docker_ephemeral, dedicated noVNC ports, optional reverse-SSH remote access, and two model-provider integration modes: CLI and API.

## Results
- The text **does not provide quantitative metrics on standard benchmark datasets**, nor does it report success rate, latency, cost, or public comparison figures against other browser agents.
- The strongest empirical claim made by the paper/project is runnable end-to-end capability: support for **Claude Desktop, Cursor, any MCP JSON-RPC client, and direct REST calls**, along with real MCP transport endpoints `/mcp` and convenient tool endpoints `/mcp/tools` and `/mcp/tools/call`.
- It provides several verifiable smoke-test flows, such as `make doctor` and `make release-audit`, as well as scripted smoke tests for **reverse-SSH, isolated sessions, and isolated session tunnels**; the text states that these tests validate specific flows such as `/readyz`, session creation, observe, agent-step, remote noVNC connectivity, and isolated container cleanup.
- In terms of interface capabilities, the system explicitly supports **1-step and multi-step agent orchestration**, background durable jobs, session-level download capture, tab control, social-page assistance, upload approval gates, and Prometheus-style `/metrics`, which together make up a more complete agent infrastructure than "pure Playwright scripts."
- The most prominent application example is Outlook: **log in once and save it as the `outlook-default` profile, then restore future new sessions directly from that auth profile**, presented as the core demonstration of being "more useful than ordinary browser automation," but without giving success-rate or time-saved numbers.

## Link
- [https://github.com/LvcidPsyche/auto-browser](https://github.com/LvcidPsyche/auto-browser)
