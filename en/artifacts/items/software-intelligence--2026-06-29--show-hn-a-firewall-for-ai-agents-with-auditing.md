---
source: hn
url: https://github.com/beebeeVB/trajeckt/
published_at: '2026-06-29T23:52:48'
authors:
- beebeeVB
topics:
- ai-agent-security
- runtime-enforcement
- mcp
- data-exfiltration
- audit-logging
- tool-governance
relevance_score: 0.68
run_id: materialize-outputs
language_code: en
---

# Show HN: A Firewall for AI agents with auditing

## Summary
trajeckt is a runtime gateway for MCP-speaking AI agents that blocks unsafe multi-step tool sequences using a sealed pre-session commitment graph and data-flow tracking. It matters because per-tool authorization can allow a sensitive read followed by an external write, even when each call looks allowed alone.

## Problem
- Agent security checks often decide on one call at a time, such as `(agent, tool, arguments)`, so they can miss violations created by call order and data movement.
- A sensitive database read followed by summarization and an external email can leak data while each individual tool call passes a local policy check.
- The agent context is treated as untrusted, so enforcement state needs to sit outside the agent and fail closed when no approved plan exists.

## Approach
- Before execution, trajeckt creates or accepts a sealed `CompiledGraph` (`Gτ`) that declares allowed tools, order, data sinks, scopes, and budgets. The graph is sealed with an HMAC and installed for a session.
- Each tool call is checked against the current reachable frontier of the sealed graph. Calls outside the graph, sessions without an installed graph, and mismatched session IDs are refused.
- The gateway tracks provenance and taint so sensitive data cannot flow into forbidden sinks, even through intermediate tools such as summarizers.
- When an operator opts out of committed mode, a heuristic safety floor blocks known patterns such as `ReadSensitive → ExternalWrite` and `ShellExec → NetworkEgress`.
- The system exposes block reasons, stable `reason_code` values, per-session decision history, and signed corpus events for audit.

## Results
- The README claims deterministic enforcement in about `1.6 ms` per check, outside the agent's control.
- In the included smoke test, `read_database` is allowed, `summarize` is allowed, and `send_email_external` is blocked with HTTP `403` when it completes an exfiltration path.
- A session that reaches `tools/call` without an installed commitment is blocked before evaluation with `no_commitment_installed`; `require_commitment_before_tools` defaults to `true` in the described gateway path.
- The MCP gateway implements the Streamable HTTP transport non-streaming profile for protocol version `2025-11-25` and advertises `2025-11-25`, `2025-06-18`, and `2025-03-26`.
- The audit endpoint returns the last `100` enforcement decisions per session, and `/corpus/stream` sends signed events over SSE with `Last-Event-ID` support.
- Evaluation evidence is limited: the README reports one ClawTrojan end-to-end case, `cs_delay_002`, with trusted-instruction false-positive guard coverage; suite-wide measurement across all `20` ClawTrojan trajectories is not done.

## Link
- [https://github.com/beebeeVB/trajeckt/](https://github.com/beebeeVB/trajeckt/)
