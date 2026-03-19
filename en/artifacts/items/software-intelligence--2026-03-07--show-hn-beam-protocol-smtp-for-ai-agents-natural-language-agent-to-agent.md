---
source: hn
url: https://github.com/Beam-directory/beam-protocol
published_at: '2026-03-07T23:16:30'
authors:
- alfridus
topics:
- agent-communication
- multi-agent-systems
- decentralized-identity
- protocol-design
- ai-infrastructure
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Show HN: Beam Protocol – SMTP for AI Agents (natural language agent-to-agent)

## Summary
Beam Protocol proposes an open communication layer for AI agents, aiming to do for agents what SMTP did for email: enable agents across different companies, frameworks, and machines to discover one another, verify identities, and communicate securely. Its core value is shifting agent collaboration from custom API integrations to standardized interactions based on identity, intent, and trust scores.

## Problem
- Existing AI agents, even if they can browse the web, write code, and analyze data, **cannot directly communicate with other agents across organizations**, because there is no unified addressing, identity, or trust mechanism.
- Inter-company agent collaboration typically requires **API keys, OAuth, webhooks, and long integration projects**, making automated service orchestration costly and slow to scale.
- The lack of verifiable identity and permission control creates risks of **impersonation, abuse, and low-trust interactions**, which is especially critical for real business workflows.

## Approach
- Use email-like **Beam-IDs** (such as `booking@lufthansa.beam.directory`) as agent addresses, mapped to **Ed25519 key pairs** and **W3C DIDs** to provide passwordless, verifiable identity.
- Rather than sending free-form chat messages, agents send **structured intents**: signed requests containing an intent type and JSON payload. The recipient first verifies the signature and parses the identity, then returns a structured result.
- Provide a **directory/registry** that supports searching agents by capability, resolving DID documents, and viewing verification levels and trust scores, so agents can first “discover” and then “communicate.”
- Compute trust scores using signals such as **verifiable credentials, email/DNS/business verification, historical successful interactions, and community reports**, combined with security policies like whitelist/open to control who can contact an agent.
- Use **WebSocket relay + HTTP API + TS/Python SDKs** to create a cross-language implementation, with the goal of turning agent interconnection from bespoke integration into a general protocol layer.

## Results
- The article gives two end-to-end example latencies: a flight-booking agent request completes in **1.8 seconds**, and a restaurant-to-delivery agent request completes in **2.1 seconds**; however, these are demo scenarios, not systematic benchmark evaluations.
- It claims the communication flow requires **no API keys, no OAuth, and no human intervention**, while applying **Ed25519 signature verification** to all intents.
- It provides implementation-scale metrics: **48+ API routes, 21 database tables**, supporting **WebSocket real-time relay**, DID resolution, verification, trust scoring, and multi-directory federation.
- Example trust scores: a newly created unverified agent starts at around **0.3**, while a business-verified agent with history can reach **0.9+**.
- It offers a runnable ecosystem: **TypeScript SDK, Python SDK, CLI, Docker/self-hosted directory**, and support for Stripe-powered paid upgrades; this suggests the project is more focused on protocol and productized infrastructure than on paper-style experimental results.
- **It does not provide standard datasets, comparison baselines, or formal quantitative experiments**. Therefore, its strongest concrete claim is that, through a standard identity + directory + signed-intent mechanism, it can reduce cross-organization agent integration time from “months of API integration” to plug-and-play interoperability.

## Link
- [https://github.com/Beam-directory/beam-protocol](https://github.com/Beam-directory/beam-protocol)
