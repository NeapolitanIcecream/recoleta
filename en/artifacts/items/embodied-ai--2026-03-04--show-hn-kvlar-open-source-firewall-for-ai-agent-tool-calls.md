---
source: hn
url: https://github.com/kvlar-io/kvlar
published_at: '2026-03-04T23:16:30'
authors:
- kvlar
topics:
- ai-agent-security
- tool-call-firewall
- policy-engine
- mcp
- runtime-guard
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Show HN: Kvlar – Open-source firewall for AI agent tool calls

## Summary
Kvlar is an open-source security layer and policy engine for AI agent tool calls, performing policy-based checks on every tool call, data access, and operation before execution. It aims to solve the lack of a unified security firewall when agents can directly access code, databases, and production systems.

## Problem
- AI agents are gaining the ability to execute code, send emails, access databases, and operate production systems, but there is a **lack of a standardized security layer** between agents and tools.
- Without unified policy checks, agents may perform unauthorized actions; this matters because once connected to real systems, erroneous or malicious calls can directly create security and compliance risks.
- A mechanism is needed that is secure by default, auditable, and testable, making deterministic allow/deny decisions before every tool call.

## Approach
- Kvlar inserts a runtime proxy layer between the agent and the MCP tool server, intercepting each tool call and evaluating it with a policy engine before execution.
- The core mechanism is simple: write security rules as **human-readable YAML policies**; each action is matched against the policy, and if it hits an allow rule it is permitted, otherwise it is denied by default (fail-closed).
- It is **native to the MCP protocol**, designed for the Model Context Protocol (spec 2024-11-05), supports stdio and TCP, and communicates via JSON-RPC 2.0 / newline-delimited JSON.
- The system consists of several parts: `kvlar-proxy` handles forwarding and interception, `kvlar-core` handles policy evaluation, and `kvlar-audit` handles structured audit logs.
- It also provides policy testing tools, allowing YAML test cases to verify whether a given operation should be allow or deny, and supports CLI, verbose, and JSON output for CI.

## Results
- The text **does not provide academic benchmarks or performance metrics** such as latency, throughput, false positive rate, or interception rate.
- The most specific quantitative information provided is engineering validation: the project states support for **MCP spec 2024-11-05**, uses **JSON-RPC 2.0** as the protocol, and supports **2** transport types (primarily stdio and TCP).
- Repository-level validation information includes: the workspace has **80 tests**, and provides `cargo test --workspace` for testing.
- The explicitly tested compatible environments include **Claude Desktop** and **@modelcontextprotocol/server-filesystem**.
- The main claimed advances are engineering and security properties: **fail-closed by default**, **deterministic decisions** (same action + same policy = same result), **auditable** (every decision includes full-context logs), and the maintainability of **policy-as-code**.

## Link
- [https://github.com/kvlar-io/kvlar](https://github.com/kvlar-io/kvlar)
