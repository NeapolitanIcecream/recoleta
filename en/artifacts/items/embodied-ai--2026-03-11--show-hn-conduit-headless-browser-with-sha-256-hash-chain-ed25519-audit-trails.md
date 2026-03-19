---
source: hn
url: https://news.ycombinator.com/item?id=47343785
published_at: '2026-03-11T23:15:53'
authors:
- TaxFix
topics:
- ai-agent-auditing
- headless-browser
- cryptographic-provenance
- sha-256-hash-chain
- ed25519-signatures
- mcp-tools
relevance_score: 0.11
run_id: materialize-outputs
language_code: en
---

# Show HN:Conduit–Headless browser with SHA-256 hash chain - Ed25519 audit trails

## Summary
Conduit is a headless browser auditing tool for AI agents that uses cryptography to generate a verifiable chain of evidence for web actions. It aims to solve the trust and auditability problem of being unable to prove "what the agent actually did," and integrates with MCP so LLM agents can call it directly.

## Problem
- When AI agents browse web pages, click, fill forms, and scrape data, traditional screenshots and logs can be forged or tampered with, making it difficult to prove after the fact what really happened.
- In scenarios such as compliance, data provenance tracking, and litigation evidence collection, the lack of independently verifiable operational evidence creates unclear accountability and trust issues.
- This matters because as agents increasingly automate real-world web tasks, auditability and accountability will become foundational requirements for deployment and compliance.

## Approach
- The core mechanism is simple: each browser action is linked to the hash of the previous step, forming a SHA-256 hash chain; if any step in the middle is altered, the entire chain becomes invalid.
- At the end of the session, the result is signed with Ed25519 to generate a proof bundle containing the full action log, the hash chain, the signature, and the public key.
- Anyone can independently verify this JSON evidence bundle without having to trust the party that produced it.
- The implementation is based on a Playwright headless browser and packaged as a pure Python tool.
- It also provides an MCP server interface, allowing Claude, GPT, and other LLM agents to directly use capabilities such as browse, click, fill, and screenshot through tool calls, while the evidence bundle is automatically built in the background.

## Results
- The text does not provide standard paper-style quantitative experimental results; it does **not** include benchmark datasets, success rates, latency, overhead, or numerical comparisons with other auditing approaches.
- The strongest concrete claim is that each action is included in a **SHA-256** hash chain and signed with **Ed25519** at the end of the session, producing a "tamper-evident" auditable record.
- The output artifact is an independently verifiable **JSON proof bundle** containing four core components: **action log, hash chain, signature, public key**.
- Supported agent capabilities include **browse / click / fill / screenshot**, and it is claimed to be usable for **AI agent auditing, compliance automation, web scraping provenance, litigation support**.
- Specific engineering details include: **MIT license**, **pure Python**, **no accounts / no API key / no telemetry**, and installation via `pip install conduit-browser`.

## Link
- [https://news.ycombinator.com/item?id=47343785](https://news.ycombinator.com/item?id=47343785)
