---
source: hn
url: https://codon.org.uk/~mjg59/blog/p/securing-agentic-identity/
published_at: '2026-07-03T23:38:15'
authors:
- edward
topics:
- agent-identity
- oauth-security
- llm-agents
- mtls
- credential-management
- enterprise-security
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# Securing Agentic Identity

## Summary
The post proposes a token-broker and proxy design that keeps real OAuth tokens out of LLM agent environments. It targets enterprise agents that need email, calendar, GitHub, or other API access without leaving reusable credentials on disk.

## Problem
- LLM agents often get access tokens for sensitive services, and those tokens can be written to disk, committed to repositories, or exfiltrated.
- Common device-code login gives the identity provider limited visibility into the security posture of the agent host.
- Simple placeholder-token proxy designs can require a secret store for token mappings, and a compromised proxy can turn stolen placeholders into usable access.

## Approach
- A central broker runs the user login flow and receives the real token after browser authentication.
- The broker returns a new JWT to the agent, signed by the broker, with the real token stored as an encrypted claim and nonsecret claims copied for local inspection.
- The agent calls APIs through a proxy with that JWT in the `Authorization` header; the proxy verifies the broker signature, decrypts the real token, and replaces the header before forwarding the request.
- The design adds mTLS binding: the agent presents a client certificate, the broker records that certificate in the minted JWT, and the proxy checks that the live mTLS certificate matches before it decrypts the embedded token.
- The same pattern works for opaque access tokens by encrypting the opaque token inside the broker-minted JWT.

## Results
- No quantitative evaluation is provided: no benchmarks, latency numbers, incident data, or deployment-scale measurements.
- The main claimed security result is that the real access token never enters the agent environment.
- The main claimed operational result is stateless scaling: the broker and proxy need encryption keys, but no persistent token-mapping database or distributed secret store.
- The mTLS variant claims stronger containment by binding token use to the agent environment’s private key, ideally backed by hardware or a hypervisor.
- The post cites RFC 8705 and says Fly.io had a similar idea about 3 years earlier, so the author presents the contribution as a practical adaptation for agentic identity rather than a wholly new protocol.

## Link
- [https://codon.org.uk/~mjg59/blog/p/securing-agentic-identity/](https://codon.org.uk/~mjg59/blog/p/securing-agentic-identity/)
