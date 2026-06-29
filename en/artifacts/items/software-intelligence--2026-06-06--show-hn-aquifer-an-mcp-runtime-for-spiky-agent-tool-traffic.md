---
source: hn
url: https://github.com/rjpruitt16/aquifer
published_at: '2026-06-06T23:08:44'
authors:
- rjpruitt16
topics:
- mcp-runtime
- agent-tooling
- rate-limiting
- durable-queues
- webhooks
- traffic-control
relevance_score: 0.62
run_id: materialize-outputs
language_code: en
---

# Show HN: Aquifer – an MCP runtime for spiky agent tool traffic

## Summary
Aquifer is a self-hosted MCP and HTTP runtime that turns bursty agent tool calls into durable, rate-controlled jobs. It matters for agent systems that overload local backends or hit 429s from external APIs.

## Problem
- Distributed agents can send tool and API requests in bursts, causing inbound overload, outbound 429s, and failures when one dependency slows down.
- Agent teams need a coordination layer that lets the backend or upstream API set the safe request pace.
- The tool targets single-machine sidecar deployments where teams want persistence without adding an external database.

## Approach
- Agents submit jobs through an MCP tool or HTTP endpoint; Aquifer returns a job ID, stores the job in SQLite, and dispatches it later.
- A per-upstream worker sends requests at configured RPS and concurrency limits, with jitter and live rate reduction from `X-Aquifer-*` response headers.
- Results are delivered through webhooks, while Server-Sent Events provide live job status, queue position, and catch-up events for late subscribers.
- The runtime core handles idempotency, persistence, dispatch, SSE events, L8 signing, webhook delivery, and metrics; adapters expose that core through MCP stdio, HTTP, or custom Go integrations.
- L8 v0.1 signs webhooks with Ed25519 after a one-time public-key challenge, avoiding stored shared HMAC secrets.

## Results
- The excerpt gives no benchmark for throughput, latency, queue durability, or failure recovery, so it does not support a measured performance breakthrough claim.
- Config examples show per-upstream limits such as `api.openai.com` at 10 RPS with 3 max concurrent requests, `api.stripe.com` at 20 RPS with 5 max concurrent requests, and an internal backend at 50 RPS with 10 max concurrent requests.
- Webhook delivery retries 4 times with exponential backoff at 1 s, 2 s, 4 s, and 8 s.
- Queue position events are emitted every 2 seconds while a job waits.
- In-flight jobs older than 5 minutes are reset to `queued`, and queued jobs are re-dispatched after restart from SQLite.
- The L8 protocol version is 0.1; the excerpt claims webhook verification is one local Ed25519 `verify()` call against a cached public key.

## Link
- [https://github.com/rjpruitt16/aquifer](https://github.com/rjpruitt16/aquifer)
