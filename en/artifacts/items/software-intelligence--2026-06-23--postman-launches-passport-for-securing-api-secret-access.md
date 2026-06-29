---
source: hn
url: https://blog.postman.com/postman-passport-secure-api-access-for-the-agentic-era/
published_at: '2026-06-23T23:23:22'
authors:
- paidsandserape
topics:
- api-security
- agentic-sdlc
- secret-management
- credential-broker
- secure-proxy
relevance_score: 0.66
run_id: materialize-outputs
language_code: en
---

# Postman launches passport for securing API secret access

## Summary
Postman Passport is a product design for letting humans, machines, and agents call APIs without receiving raw API keys. It matters because coding agents and CI workloads can multiply API calls and secret exposure across developer machines and tools.

## Problem
- API keys are copied into `.env` files, shell profiles, IDE configs, build outputs, Slack, Google Docs, and tool caches; Postman says each live secret appears in roughly 8 locations on the same machine.
- Agents in the SDLC can call APIs and spawn other agents, so direct key access creates leakage and over-permission risks.
- Existing vaults tend to protect production systems, while developer and agent access often resolves secrets on local machines or app runtimes.

## Approach
- Passport gives callers credential references instead of API keys; each reference is bound to the holder through a cryptographic token and a private key.
- Access requests flow through the Postman API Network, which connects to the customer’s vault; real keys stay in the vault.
- API requests route through the Secure Access Proxy inside the customer’s VPC; the proxy checks scope, resolves the secret, injects it into the request, and keeps it out of apps, logs, and Postman.
- Durable identities track longer-lived consumers, while ephemeral identities let agents delegate short-lived subset access to spawned agents.
- The Secure Access Proxy can enforce endpoint-level scopes beyond the original API permission set.

## Results
- The excerpt gives no benchmark, user study, incident reduction data, latency data, or production deployment numbers.
- Claimed demand driver: agents are projected to consume APIs at 1,000x the rate humans do today.
- Secret-sprawl measurement: each live secret appeared in roughly 8 locations on the same machine on average.
- Security claim: a stolen credential reference is useless without the matching holder private key.
- Deployment claim: the trust root is the customer’s certificate authority, and secret resolution runs inside the customer’s VPC.
- Control claim: the proxy checks scope on every request before it reaches the vault and can enforce endpoint-level access.

## Link
- [https://blog.postman.com/postman-passport-secure-api-access-for-the-agentic-era/](https://blog.postman.com/postman-passport-secure-api-access-for-the-agentic-era/)
