---
source: hn
url: https://news.ycombinator.com/item?id=47343785
published_at: '2026-03-11T23:15:53'
authors:
- TaxFix
topics:
- agent-auditing
- headless-browser
- cryptographic-provenance
- mcp-tools
- ai-agents
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# Show HN:Conduit–Headless browser with SHA-256 hash chain - Ed25519 audit trails

## Summary
Conduit is a headless browser auditing tool for AI agents that records web actions into a verifiable cryptographic evidence chain. It attempts to solve the trust problem of being unable to prove after the fact what happened when an agent browses, clicks, fills forms, and scrapes.

## Problem
- Web actions performed by AI agents typically leave only screenshots or ordinary logs, which are **easy to fake, tamper with, or edit after the fact**, making accountability difficult when something goes wrong.
- In scenarios such as compliance, data collection, and litigation support, **independently verifiable execution evidence** is needed, rather than relying only on vendor claims or platform trust.
- For software agents / LLM tool calls, the lack of **native auditability** limits adoption in high-risk automated workflows.

## Approach
- Built on **Playwright** as a headless browser, recording each step such as browse, click, fill, and screenshot.
- Each action is hashed together with the previous record using **SHA-256**, forming a chained tamper-evident hash chain; if any intermediate step is altered, the rest of the chain becomes invalid.
- At the end of a session, the full result is signed with **Ed25519** to generate a proof bundle, which includes the action log, hash chain, signature, and public key.
- Any third party can independently verify the bundle’s integrity and origin **without trusting the producer**.
- The tool is also exposed as an **MCP server**, allowing Claude, GPT, and other LLM agents to use the browser directly through tool calls while automatically generating audit evidence.

## Results
- The text **does not provide standard benchmarks, public datasets, or quantitative experimental results**, so no precise performance gains or comparison figures can be reported.
- The core paper-style claimed result is that each browsing session can produce **1 proof bundle (JSON)** at the end, containing at least **4 types of content**: action log, hash chain, signature, and public key.
- It claims that anyone can perform **independent verification** of the bundle without trusting the log producer; compared with ordinary screenshots/logs, this provides stronger tamper-resistance guarantees.
- The supported target scenarios include **4 categories**: AI agent auditing, compliance automation, web scraping provenance, and litigation support.
- From an engineering deployment perspective, it shows strong usability signals: **MIT license, pure Python, no account/API key/telemetry required**, and provides `pip install conduit-browser` and MCP integration.

## Link
- [https://news.ycombinator.com/item?id=47343785](https://news.ycombinator.com/item?id=47343785)
