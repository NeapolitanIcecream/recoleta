---
source: hn
url: https://github.com/kvlar-io/kvlar
published_at: '2026-03-04T23:16:30'
authors:
- kvlar
topics:
- ai-agent-security
- mcp
- policy-engine
- runtime-guardrails
- tool-call-firewall
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Show HN: Kvlar – Open-source firewall for AI agent tool calls

## Summary
Kvlar is an open-source security layer for AI agent tool calls that checks every tool call, data access, and operation against YAML policies before execution. It aims to fill a gap in the MCP ecosystem with a runtime firewall that is fail-closed by default, auditable, and testable.

## Problem
- AI agents can already execute code, send emails, query databases, and operate production systems, but there is no unified security isolation layer between agents and tools.
- Without a standardized policy enforcement point, over-privileged calls, mistakes, and unauditable behavior are more likely, which matters for automated software production and agentic systems.
- What is needed is a predictable, verifiable mechanism that decides “allow or deny” before a tool actually executes.

## Approach
- Kvlar inserts a proxy layer between the agent and the MCP tool server, performing policy evaluation on each tool call / data access / operation before deciding whether to allow it.
- The core mechanism is simple: write security rules in readable YAML; if an action does not match an allow rule, it is denied by default under **fail-closed** behavior.
- The system emphasizes determinism: the same action plus the same policy always yields the same decision, making testing, reproduction, and auditing easier.
- It is native to the MCP protocol, supports stdio and TCP, uses JSON-RPC 2.0 over newline-delimited JSON, and provides `wrap`/`unwrap` to connect clients into existing MCP configurations.
- In addition to runtime interception, it provides policy testing and structured audit logs, with CLI and JSON output for CI integration.

## Results
- The text does not provide benchmark data, interception rates, performance overhead, or quantitative comparisons with other approaches.
- Explicitly claimed capabilities include: **deny by default** (deny when no matching rule exists), **auditable** (every decision records full context), and **deterministic decisions** (same action + same policy = same result).
- On the engineering validation side, the project provides **80 tests** (`cargo test --workspace`) as a signal of current implementation test coverage, but does not report further metrics beyond pass rate.
- Compatibility claims include: based on **MCP spec 2024-11-05**, supports **stdio** and **TCP**, and has been tested with **Claude Desktop** and `@modelcontextprotocol/server-filesystem`.
- Compared with “direct tool invocation without a security layer,” its main breakthrough claim is not higher task performance, but adding an open-source, policy-driven, runtime-enforced security control plane for AI agents.

## Link
- [https://github.com/kvlar-io/kvlar](https://github.com/kvlar-io/kvlar)
