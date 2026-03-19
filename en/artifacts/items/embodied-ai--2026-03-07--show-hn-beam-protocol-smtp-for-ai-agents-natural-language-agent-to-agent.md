---
source: hn
url: https://github.com/Beam-directory/beam-protocol
published_at: '2026-03-07T23:16:30'
authors:
- alfridus
topics:
- agent-communication
- decentralized-identity
- intent-protocol
- trust-and-verification
- multi-agent-systems
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Show HN: Beam Protocol – SMTP for AI Agents (natural language agent-to-agent)

## Summary
Beam Protocol proposes an open communication layer for AI agents, aiming to do for agent interaction across companies, frameworks, and machines what SMTP did for email: provide a unified mechanism for identity, discovery, verification, and message delivery. Its core selling point is enabling agents to communicate directly through verifiable identities and structured intents, without requiring traditional API integrations, OAuth, or human intermediaries.

## Problem
- Existing AI agents can browse the web, write code, and analyze data, but **cannot reliably interoperate with other agents**, especially across different companies, frameworks, and machines.
- The infrastructure required for agent communication is missing: **addressing, identity, trust verification, and capability discovery**, which means real business scenarios still require cumbersome API integrations.
- This matters because automated cross-organization service collaboration, such as booking, delivery, customer support handoffs, and payments, is difficult to scale without a unified protocol.

## Approach
- Use **Beam-ID + DID** to establish a resolvable identity for each agent: Beam-ID is similar to an email address, maps to a W3C-compatible DID document, and is bound to an **Ed25519** key pair for cryptographic identity authentication.
- Communication does not use free-form text chat, but instead uses **structured, signed intents**: the sender declares an intent type and JSON payload, and the receiver responds after verifying the signature, DID, and verification information in the directory.
- Provide a **directory service (directory)** that supports searching for agents by capability, resolving DIDs, and viewing verification levels and trust scores, thereby completing the discovery flow of “who to find, what they can do, and whether they are trustworthy.”
- Introduce **trust and security mechanisms**: trust scores are based on factors such as verification level, account age, success history, community reports, and domain verification; receivers can also configure whitelists or minimum trust thresholds.
- On the engineering side, enable cross-language integration through **WebSocket relay + HTTP API + TypeScript/Python SDK**, while also supporting identity management features such as self-hosted directories, recovery phrases, and encrypted exports.

## Results
- The text provides a flight booking example: a personal agent sends a `booking.flight` intent to a Lufthansa agent, with a **total latency of 1.8 seconds**, returning flight `LH1132`, price `€149`, and confirmation number `BK-839271`; however, this is a demo scenario, not a benchmark experiment.
- In another delivery example, a restaurant agent sends a `delivery.request` to a delivery agent, and **after 2.1 seconds** receives rider `Max`, estimated delivery time `22min`, and tracking number `SPD-8291`; this is likewise a scenario demonstration rather than a rigorous evaluation.
- In terms of speed, the protocol claims intents can achieve **sub-second** communication via WebSocket; in terms of security, it claims **all intents are verified with Ed25519 signatures** and pass through five layers of security checks, but it does not provide system evaluation data such as false positive rates, throughput, or availability.
- In terms of implementation scale, the project lists **48+ API routes** and **21 database tables**, with support for TypeScript, Python, and HTTP/WS access, indicating that it already has a fairly complete prototype system rather than being only a conceptual design.
- Trust score examples: a new unverified agent defaults to **0.3**, while a business-verified agent with operating history can reach **0.9+**; these are rule settings, not experimental results.
- Overall, the provided text **does not present standard datasets, comparison baselines, or formal quantitative experiments**; its strongest concrete claim is that cross-organization agent calls can be completed in seconds without API keys, OAuth, or human involvement.

## Link
- [https://github.com/Beam-directory/beam-protocol](https://github.com/Beam-directory/beam-protocol)
