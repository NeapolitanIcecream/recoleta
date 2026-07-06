---
kind: ideas
granularity: day
period_start: '2026-07-03T00:00:00'
period_end: '2026-07-04T00:00:00'
run_id: 7bc8b7b8-ee57-4728-abe2-91cc491dd455
status: succeeded
topics:
- agent identity
- OAuth
- LLM agents
- credential security
- mTLS
tags:
- recoleta/ideas
- topic/agent-identity
- topic/oauth
- topic/llm-agents
- topic/credential-security
- topic/mtls
language_code: en
pass_output_id: 301
pass_kind: trend_ideas
upstream_pass_output_id: 300
upstream_pass_kind: trend_synthesis
---

# Agent credential containment

## Summary
Enterprise agent security work is ready for narrow pilots around token brokers, API proxies, and certificate-bound agent credentials. The clearest starting point is a broker-and-proxy flow that prevents reusable OAuth tokens from entering the agent container. Teams that already issue workload certificates can add mTLS checks. SaaS integrations need early adapter tests because login flows and opaque tokens vary by provider.

## Broker-and-proxy OAuth flow for email, calendar, and GitHub agents
Security teams can pilot a central OAuth broker for agents that need email, calendar, GitHub, or internal API access. The broker runs the browser login flow and receives the real OAuth token. It gives the agent a signed JWT that copies nonsecret claims and stores the real token as an encrypted claim. The agent sends API calls through a proxy, and the proxy verifies the broker signature, decrypts the embedded token, swaps it into the `Authorization` header, and forwards the request.

A useful first test is small: put the flow in front of one high-risk agent and instrument the container filesystem, tool outputs, logs, and repository writes. The pass condition is that the upstream OAuth token never appears in the agent runtime while the agent can still inspect scope-like claims and complete normal API calls. The same pilot should record latency and failure modes because the source proposal gives architecture, not deployment measurements.

### Evidence
- [Securing Agentic Identity](../Inbox/2026-07-03--securing-agentic-identity.md): Summarizes the broker and proxy design, target services, and lack of quantitative deployment data.
- [Securing Agentic Identity](../Inbox/2026-07-03--securing-agentic-identity.md): Describes the broker-minted JWT with an encrypted copy of the real token and the proxy header swap.
- [Securing Agentic Identity](../Inbox/2026-07-03--securing-agentic-identity.md): Names the operational risk: agent-held credentials can be written to disk, committed to repositories, or exfiltrated.

## mTLS certificate binding for broker-issued agent tokens
Teams that already give agent workloads client certificates can bind broker-issued JWTs to the agent environment. The agent presents a client certificate when it asks the broker for a token. The broker embeds a representation of that certificate in the JWT. The proxy then requires mTLS and checks that the live client certificate matches the embedded certificate before decrypting the real OAuth token.

The practical security test is to copy a broker-issued JWT out of one agent environment and try to use it through the proxy from another environment. The expected result is proxy rejection unless the caller also has the private key for the original environment. Hardware-backed or hypervisor-backed private keys make that check more meaningful. This can be adopted even when the upstream identity provider has no support for RFC 8705 token binding.

### Evidence
- [Securing Agentic Identity](../Inbox/2026-07-03--securing-agentic-identity.md): Explains presenting a client certificate to the broker, embedding it in the minted token, and enforcing mTLS at the proxy.
- [Securing Agentic Identity](../Inbox/2026-07-03--securing-agentic-identity.md): Connects the design to SPIFFE-style workload identity and notes stateless broker and proxy operation.

## Adapter tests for third-party login flows and opaque access tokens
Agent teams integrating with GitHub and other SaaS APIs should test broker adapters before committing to a shared production path. The broker may need provider-specific handling where login does not run through the enterprise identity provider. Opaque access tokens also need coverage: the broker can wrap the opaque token inside a new JWT as an encrypted claim, and the proxy can present the opaque token only after the mTLS check passes.

A practical adoption check is a provider matrix covering login flow, token type, claim visibility, refresh behavior, proxy header rewrite, and mTLS enforcement. GitHub is a good first case because the source calls out provider-specific login friction. Passing the matrix for two or three common SaaS services would show whether the broker can stay small or needs a larger adapter layer.

### Evidence
- [Securing Agentic Identity](../Inbox/2026-07-03--securing-agentic-identity.md): Notes that third-party services and GitHub-style login flows may require vendor-specific broker knowledge.
- [Securing Agentic Identity](../Inbox/2026-07-03--securing-agentic-identity.md): States that opaque tokens can be carried as encrypted claims and released only after mTLS binding is verified.
