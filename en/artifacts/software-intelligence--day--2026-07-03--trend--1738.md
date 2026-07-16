---
kind: trend
trend_doc_id: 1738
granularity: day
period_start: '2026-07-03T00:00:00'
period_end: '2026-07-04T00:00:00'
topics:
- agent identity
- OAuth
- LLM agents
- credential security
- mTLS
run_id: materialize-outputs
aliases:
- recoleta-trend-1738
tags:
- recoleta/trend
- topic/agent-identity
- topic/oauth
- topic/llm-agents
- topic/credential-security
- topic/mtls
language_code: en
pass_output_id: 300
pass_kind: trend_synthesis
---

# Agent identity work centers on keeping OAuth tokens out of LLM runtimes

## Overview
This day has one strong signal: enterprise LLM agents need delegated access without reusable OAuth tokens sitting in their runtimes. `Securing Agentic Identity` proposes a broker, proxy, and mutual TLS (mTLS) binding pattern for email, calendar, GitHub, and API access. The evidence is architectural, with no benchmark or deployment data yet.

## Findings

### Brokered tokens for agent API access
The proposal puts a broker between user login and the agent runtime. The broker receives the real OAuth token after browser authentication, then gives the agent a signed JSON Web Token (JWT). That JWT contains the real token only as an encrypted claim. The agent can inspect copied nonsecret claims, but the credential that remote services accept never lands in the agent environment.

The agent sends API calls through a proxy. The proxy verifies the broker signature, decrypts the embedded token, swaps it into the `Authorization` header, and forwards the request. This design targets a practical failure mode: agents with access to email, calendar, or source-control APIs can write tokens to disk, leak them through tools, or commit them to repositories.

#### Sources
- [Securing Agentic Identity](../Inbox/2026-07-03--securing-agentic-identity.md): Summary describes the broker, proxy, encrypted JWT claim, and target services.

### mTLS binding limits stolen-token reuse
The stronger version binds the broker-issued JWT to the agent environment’s client certificate. The agent presents a certificate when requesting a token. The broker records that certificate inside the minted JWT. Later, the proxy requires mTLS and checks that the live client certificate matches before it decrypts the embedded token.

This makes token theft less useful unless the attacker also controls the environment’s private key. The post recommends hardware-backed or hypervisor-backed private keys where possible. It also notes that the pattern can work even when the upstream identity provider does not support RFC 8705 token binding.

#### Sources
- [Securing Agentic Identity](../Inbox/2026-07-03--securing-agentic-identity.md): Content describes certificate embedding, proxy mTLS checks, and hardware or hypervisor-backed keys.

### Stateless operation, vendor friction, and missing measurements
The operational appeal is that the broker and proxy do not need a persistent token-mapping database. They need signing and encryption keys, and new instances can be started for scale or availability. That reduces the chance that a placeholder-token scheme turns into a distributed secret store.

The limits are also clear. Third-party services may use different login flows or opaque tokens, so the broker may need vendor-specific handling. The post gives no latency, reliability, incident, or deployment-scale measurements. Its contribution is a concrete security design for agentic identity, not a measured system result.

#### Sources
- [Securing Agentic Identity](../Inbox/2026-07-03--securing-agentic-identity.md): Content states the stateless scaling claim and cites similar prior work by Fly.io.
