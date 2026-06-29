---
source: hn
url: https://capframe.ai
published_at: '2026-05-19T23:46:47'
authors:
- euan21
topics:
- ai-agent-security
- mcp
- capability-tokens
- tool-use
- policy-enforcement
- prompt-injection
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Show HN: Capframe – capability tokens for AI agent tool calls

## Summary
Capframe is a local Rust toolkit that maps MCP tool access, issues scoped capability tokens, and enforces deterministic policies on AI agent tool calls. It targets indirect prompt-injection and excessive-authority risks in agents that can call external tools.

## Problem
- AI agents connected through MCP can reach many tools, endpoints, and parameters, which makes their real authority hard to inspect.
- Unconstrained tool inputs and indirect-injection surfaces can let hostile content affect tool calls or push an agent beyond intended permissions.
- Security teams need audit evidence mapped to OWASP LLM Top 10, NIST AI RMF, and MITRE ATLAS.

## Approach
- `find` walks MCP servers and tool endpoints, records parameters, flags unconstrained inputs and indirect-injection surfaces, and writes `capframe.findings.json`.
- `bind` issues scoped, revocable capability tokens with macaroon-style attenuation, ed25519 holder-of-key binding, limits such as `max_refund=50`, and signed denial receipts using HMAC-SHA256.
- `guard` evaluates every tool call against YAML policy at runtime with deterministic Rust code, so allow and deny decisions do not depend on an LLM.
- `report` exports HTML or PDF evidence mapped to OWASP LLM, NIST AI RMF, and MITRE ATLAS controls.

## Results
- Example scan mapped 14 tools across 2 MCP servers and found 3 tools with unconstrained input tied to OWASP LLM01.
- A second example also found 1 indirect-injection surface tied to OWASP LLM01 and MITRE ATLAS T0051.
- Example token scoped `shopify-bot` to 2 tools, 2 limits, and a 24-hour TTL; concrete limits include `max_refund≤50` and `region=eu`.
- Guard backtest reports 247/247 corpus cases passing across 14 rules and 3 categories, with a 0.0% false-positive rate.
- The report example shows OWASP LLM Top 10 coverage of 4/10 items, 2 open findings, 2 MITRE techniques flagged, and 0 active exploits.
- Runtime policy evaluation is claimed to run in single-digit microseconds.

## Link
- [https://capframe.ai](https://capframe.ai)
