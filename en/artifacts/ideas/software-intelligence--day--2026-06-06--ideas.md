---
kind: ideas
granularity: day
period_start: '2026-06-06T00:00:00'
period_end: '2026-06-07T00:00:00'
run_id: ac979bdd-0081-4908-89bb-d2c300c37c07
status: succeeded
topics:
- agent control
- coding agents
- MCP
- desktop automation
- AI cost governance
- LLM safety
- context management
tags:
- recoleta/ideas
- topic/agent-control
- topic/coding-agents
- topic/mcp
- topic/desktop-automation
- topic/ai-cost-governance
- topic/llm-safety
- topic/context-management
language_code: en
pass_output_id: 235
pass_kind: trend_ideas
upstream_pass_output_id: 234
upstream_pass_kind: trend_synthesis
---

# Agent control layers

## Summary
Agent deployments are reaching the point where the missing work sits around the model call: queued tool execution, guarded desktop access, and budgeted context management. The concrete openings are small control layers that teams can test against existing agent failures: 429s, unsafe desktop actions, long runs filled with stale state, and review overload from large generated changes.

## Durable MCP queue for bursty agent tool calls
Agent teams with repeated 429s or overloaded internal services should put a small job queue between agents and shared APIs. Aquifer shows the shape of that layer: agents submit jobs through MCP or HTTP, the runtime stores them in SQLite, then per-upstream workers dispatch at configured request and concurrency limits. The example config sets `api.openai.com` at 10 RPS with 3 concurrent requests, `api.stripe.com` at 20 RPS with 5 concurrent requests, and an internal backend at 50 RPS with 10 concurrent requests.

A useful pilot would wrap one high-traffic agent tool behind a durable queue and measure failed calls, queue wait time, retries, and task completion. The test should include an upstream slowdown, since Aquifer’s design allows response headers to reduce the live rate under the configured ceiling. This is a practical support layer for teams whose agents already work but fail when many runs hit the same backend at once.

### Sources
- [Show HN: Aquifer – an MCP runtime for spiky agent tool traffic](../Inbox/2026-06-06--show-hn-aquifer-an-mcp-runtime-for-spiky-agent-tool-traffic.md): Aquifer queues MCP or HTTP jobs in SQLite, dispatches through per-upstream workers, supports live rate reduction, and gives concrete RPS and concurrency examples.
- [Show HN: Aquifer – an MCP runtime for spiky agent tool traffic](../Inbox/2026-06-06--show-hn-aquifer-an-mcp-runtime-for-spiky-agent-tool-traffic.md): The source describes distributed agents calling APIs in bursts and using Aquifer as a coordination layer before shared backends or external APIs.

## Accessibility-first MCP gateway for local desktop actions
Coding-agent users still hit workflows that leave the editor: browser dialogs, installers, native apps, and OS permission prompts. clawdcursor makes a concrete desktop-control pattern credible by exposing local desktop actions through one MCP entry, trying the accessibility tree before OCR or screenshots, and sending every call through a safety check. Its compact surface has 6 tool groups, while the 94-tool surface remains available for compatibility and debugging.

The first adoption test should focus on a narrow desktop workflow with clear stop conditions, such as filling a local app form, saving a file through a native dialog, or completing a browser-based admin task. The evaluation should log which actions used accessibility metadata, which fell back to OCR or screenshots, which actions needed confirmation, and whether batching reduced tool-call count. This keeps desktop automation close to named user tasks and makes safety prompts part of the workflow from the first trial.

### Sources
- [AI Can now control your desktop](../Inbox/2026-06-06--ai-can-now-control-your-desktop.md): clawdcursor exposes desktop control through MCP, uses accessibility before OCR and screenshots, has 6 compact tool groups, and gates destructive actions through confirmation.
- [AI Can now control your desktop](../Inbox/2026-06-06--ai-can-now-control-your-desktop.md): The source describes the compact grouped surface, cross-platform support, accessibility-first operation, and batched deterministic actions.

## Budget-capped context rewriting tests for long agent runs
Long-running coding and corpus-grounded agents need a way to shed stale files, failed paths, tool noise, and distractor evidence. Context Sculpting tested a two-model harness where an outer model can pass through, rewrite context, roll back, or terminate between inner-agent turns. The feasibility signal comes with a clear cost warning: in one coding repair example, the control run passed in 7 turns, 42.7 seconds, and about $0.015, while the harnessed run also passed but used 12 turns, 566.9 seconds, about $1.06, and hit a max-turn guardrail.

A practical test should allow context rewriting only under explicit caps: maximum rewrites, maximum added latency, maximum spend, and a hard stop after repeated non-improving edits. The evaluation should compare pass rate, total turns, cost, and reviewer-visible trace quality on tasks known to contain stale context or distracting files. This makes context editing a measured intervention for specific long-run failures, with policy limits set before the agent starts.

### Sources
- [Context Sculpting](../Inbox/2026-06-06--context-sculpting.md): Context Sculpting reports the two-model harness design, rewrite actions, pass-through results, active rewrite runs, and the coding repair cost and latency comparison.
