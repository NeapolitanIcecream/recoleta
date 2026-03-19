---
source: hn
url: https://github.com/LvcidPsyche/auto-browser
published_at: '2026-03-12T23:56:26'
authors:
- Lvcid
topics:
- browser-agent
- mcp
- playwright
- human-in-the-loop
- auth-state
- workflow-automation
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Auto-Browser – An MCP-native browser agent with human takeover

## Summary
Auto-Browser is an open-source browser agent for authorized web workflows that packages real browser capabilities directly as an MCP server, while supporting human-in-the-loop takeover. Its core value is enabling LLMs/agents to continue working through brittle web flows without interruption, while preserving login-state reuse, security auditing, and controlled execution.

## Problem
- Existing browser automation or agent tools often fail in login flows, pop-ups, CAPTCHA-related pre-verification, and complex multi-tab workflows, and once purely automated execution gets stuck it tends to lose context or the session.
- For authorized scenarios such as internal admin systems, QA, export/download tasks, and account reuse, developers need more than just “automation”; they need browser-agent infrastructure that is **recoverable, supervisable, and auditable**.
- Many tools are not MCP-native, so integrating with MCP clients such as Claude Desktop and Cursor requires extra compatibility layers, increasing deployment and maintenance complexity.

## Approach
- Implement the “browser agent” as an **MCP-native server**: provide real JSON-RPC MCP transport via `/mcp`, and also expose `/mcp/tools` and REST interfaces for MCP clients, agent frameworks, or direct script invocation.
- Use **Chromium + Playwright + FastAPI** underneath, and return agent-oriented “screen-aware observations”: screenshots, interactable element IDs, DOM/accessibility summaries, and optional OCR text, so the model can act based on page state.
- When web flows become brittle, use **noVNC human takeover** so a person can manually recover within the same session and then hand control back to the agent, avoiding a “restart after failure” pattern.
- Enable “log in once, reuse later” through **named authentication profiles** and encrypted auth-state storage; also add security guardrails such as allowlists, upload approval, audit logs, operator identity, and rate limiting.
- Support shared browser nodes and `docker_ephemeral` session isolation, reverse SSH/remote takeover, and persistent job/session metadata, emphasizing deployability in real operational environments.

## Results
- The text **does not provide standard paper-style benchmark data** and does not report success rate, task completion rate, latency, or quantitative comparisons with other browser agents.
- Clearly stated engineering capabilities include support for **4 access modes/client types** (Claude Desktop, Cursor, any MCP JSON-RPC client, and direct REST calls).
- On the MCP side, it explicitly supports **6 JSON-RPC capability/method families**: `initialize`, `notifications/initialized`, `ping`, `tools/list`, `tools/call`, and `DELETE /mcp` session destruction; it also **rejects JSON-RPC batching**.
- At the action layer, browser capabilities added and unified into the shared schema include at least **7 operation types**: `hover`, `select_option`, `wait`, `reload`, `go_back`, `go_forward`, plus existing basic actions such as click/type.
- For security and operations, it specifies several concrete constraints/thresholds: in production mode, startup **fails closed** if required security configuration is missing; Codex host bridge requests time out after **55 seconds** by default; restoring authentication state performs `AUTH_STATE_MAX_AGE_HOURS` expiry checks; the metrics endpoint can be disabled via `METRICS_ENABLED=false` and will return **404**.
- The strongest practical claim is that the workflow of “**manual login once + save auth profile + reuse logged-in state in new sessions**” makes the system better suited than ordinary browser automation for day-to-day authorized web workflows, but this is a product claim rather than a quantified experimental conclusion.

## Link
- [https://github.com/LvcidPsyche/auto-browser](https://github.com/LvcidPsyche/auto-browser)
