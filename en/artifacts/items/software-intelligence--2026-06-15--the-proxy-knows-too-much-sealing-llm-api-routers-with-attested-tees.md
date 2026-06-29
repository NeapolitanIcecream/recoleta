---
source: arxiv
url: https://arxiv.org/abs/2606.16358v1
published_at: '2026-06-15T07:55:13'
authors:
- Sipeng Xie
- Qianhong Wu
- Hengrun Lu
- Ziliang Sun
- Qi Wu
- Bo Qin
- Qin Wang
topics:
- llm-api-router
- agent-security
- trusted-execution-environments
- remote-attestation
- code-agent-security
- api-gateway-security
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# The Proxy Knows Too Much: Sealing LLM API Routers with Attested TEEs

## Summary
Aegis is an attested TEE-based LLM API router that keeps prompts, tool calls, responses, and secrets out of the router host's plaintext memory. The client verifies the enclave before sending the request body, so the host can route and bill requests without reading or changing the interaction.

## Problem
- LLM API routers terminate client TLS and open a new upstream TLS session, which gives the router plaintext access to prompts, tool definitions, tool outputs, provider responses, and secrets.
- A malicious router can rewrite coding-agent tool calls, swap dependencies for typosquatted packages, trigger attacks only under selected conditions, or scan traffic for credentials.
- This matters because coding agents may execute shell commands and install packages on a developer machine, so one tampered tool call can lead to code execution or supply-chain compromise.

## Approach
- Aegis moves only the request/response data path into a hardware enclave. Authentication, scheduling, account selection, accounting, and management stay on the untrusted host.
- The client sidecar checks the enclave attestation and measurement before it releases the plaintext body.
- TLS to the client terminates inside the enclave, and the enclave opens the provider HTTPS session to fixed, measured destinations.
- The host passes control data such as account choice and provider credential, but the control channel cannot carry body bytes or host-chosen network destinations.
- The enclave relays provider-native API bytes without translating the request or response format.

## Results
- In the plaintext-access baseline, all 4 malicious-router attack classes succeed: tool-call rewrite, typosquat package swap, trigger-gated attack, and passive secret exfiltration.
- Aegis blocks all 4 attack classes in the authors' tests, including adaptive tests against the same trust boundary.
- The trusted data path is 851 lines of code.
- The implementation carries 3 provider-native APIs without format conversion.
- Under real-provider workload and concurrency, every request completed through the verified path.
- The reported local relay overhead is about 6 ms per request, and a seeded audit pilot had two commodity coding agents find 8/10 and 10/10 planted invariant violations.

## Link
- [https://arxiv.org/abs/2606.16358v1](https://arxiv.org/abs/2606.16358v1)
