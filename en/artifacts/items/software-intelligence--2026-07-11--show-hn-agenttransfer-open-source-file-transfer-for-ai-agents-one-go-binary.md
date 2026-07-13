---
source: hn
url: https://github.com/shehryarsaroya/agenttransfer
published_at: '2026-07-11T22:52:52'
authors:
- tomatoes2026
topics:
- agent-infrastructure
- file-transfer
- multi-agent-coordination
- mcp
- agent-identity
- self-hosting
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# Show HN: AgentTransfer – open-source file transfer for AI agents (one Go binary)

## Summary
AgentTransfer gives AI agents their own identities, inboxes, storage, and verified file-transfer workflows in one self-hostable Go binary. It connects file delivery, integrity checks, agent discovery, coordination, MCP, email, and optional app hosting without requiring a human for each handoff.

## Problem
- Existing file tools assume a human creates accounts, manages credentials, shares links, and confirms delivery.
- Large files can be awkward or unsafe to move through email or an AI model's context window.
- Agents need recipient identity, delivery state, integrity metadata, access control, and audit evidence rather than storage alone.

## Approach
- An agent signs up with one `POST /v1/agents` call and receives an email address, API key, inbox, folder, and 400 MB scratch quota. Files expire after 24 hours by default until the owner's mailbox is verified.
- Agents send named recipients structured offers containing a download link, file size, SHA-256 hash, expiry, and message metadata. HTTPS streams file bytes directly between the client and server, while the CLI and MCP bridge verify downloads.
- Ed25519-signed, hash-chained receipts record transfers and app lifecycle events. Operators and clients can verify an individual agent's records or the complete instance chain offline.
- The same static Go binary provides the server, CLI, local MCP bridge, REST API, optional email and webhook delivery, discovery cards, shared spaces, client-side encryption, and a separate Docker-facing app runner.
- Human mailbox verification unlocks outbound email, a permanent 20 GB folder with 5 GB per-file limits, and optional static or container app hosting. Quotas, recipient limits, quarantine, rate limits, and SSRF checks constrain abuse.

## Results
- The offline demo completes a 1 MiB `alice` to `bob` handoff through upload, send, long-poll, download, SHA-256 verification, and signed receipt-chain verification without an account or network.
- A new agent can operate immediately with 400 MB of temporary storage and 24-hour file expiry; verified agents receive 20 GB of persistent storage and can upload files up to 5 GB each.
- The project claims support for streaming 5 GB transfers through the local MCP bridge without placing file contents in the model context window. The excerpt provides no throughput, latency, reliability, or benchmark comparison against existing tools.
- AgentTransfer v0.6.0 includes open signup, inbox delivery, discovery, spaces, local and hosted MCP, client-side symmetric and sealed encryption, signed receipts, webhooks, verified-agent static sites, container apps, and tunnel-based Connect hosting.
- Self-hosting requires a Linux VPS, domain, outbound relay key, and Go 1.25+ or Docker; the core deployment needs no separate database, object store, or reverse proxy.

## Link
- [https://github.com/shehryarsaroya/agenttransfer](https://github.com/shehryarsaroya/agenttransfer)
