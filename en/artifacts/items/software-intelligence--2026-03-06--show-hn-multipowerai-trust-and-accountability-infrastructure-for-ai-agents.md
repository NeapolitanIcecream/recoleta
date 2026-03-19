---
source: hn
url: https://multipowerai-trust.vercel.app
published_at: '2026-03-06T23:24:31'
authors:
- rogergrubb
topics:
- ai-agents
- trust-infrastructure
- auditability
- agent-commerce
- human-in-the-loop
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Show HN: MultiPowerAI – Trust and accountability infrastructure for AI agents

## Summary
MultiPowerAI proposes a “trust and accountability infrastructure” for AI agents, aiming to add an identity, audit, and risk-control layer when agents gain real execution capabilities such as making payments, calling tools, and hiring other agents. It is more of a product/platform solution than an academic paper, with the focus on making agent behavior verifiable, accountable, and stoppable.

## Problem
- Existing AI agents can already spend money, send emails, and execute transactions, but they usually lack **authentication, authorization boundaries, and liability attribution**. When something goes wrong, it is difficult to prove “who did what, and whether it was authorized.”
- In multi-agent collaboration scenarios, calls, purchases, and delegations between agents lack a **unified ledger, receipts, and audit trail**, so post-incident reconstruction often depends only on logs, which is unreliable.
- Prompt injection, malicious inputs, model drift, or account abuse can cause agents to act beyond their permissions; without **real-time monitoring, pause switches, and human approval**, losses can escalate quickly.

## Approach
- Assign each agent a **verifiable cryptographic identity**, keys, wallet, and permission policies, forming a foundational identity layer and authorization boundary.
- Apply **signatures, timestamped records, and encrypted auditing** to all agent actions and transactions, generating a complete provable audit trail from the first call to the final result.
- Introduce a **dynamic trust score (0–100)** and behavioral profiling to detect anomalous patterns such as spending spikes, access to unfamiliar endpoints, and activity at unusual times, with support for automatic pauses.
- Provide **human-in-the-loop approval** for high-risk operations, multi-signature/quorum approval, and **escrow settlement** for inter-agent transactions to reduce the execution risk of high-value actions.
- Offer a **verified skills marketplace** and a multi-model aggregated query interface, enabling agents to discover capabilities, purchase services, and make more robust decisions in a controlled, auditable environment.

## Results
- The clearest quantified capability given in the text is **sub-200ms merchant verification**.
- The platform claims to provide a **dynamic trust score of 0–100** for continuously assessing agent state and trustworthiness.
- The skills marketplace currently claims to have **12 live skills**, covering categories such as finance, coding, research, and security.
- The multi-model query interface claims it can **query 5 models in parallel in a single call** (Claude, GPT, Gemini, DeepSeek, and one composite-result workflow), then generate a weighted synthesized answer.
- In terms of revenue sharing, the platform says skill publishers can receive **80% of sales revenue**.
- It does not provide standard academic benchmarks, controlled experiments, or public dataset results; its strongest concrete claims are low-latency verification, end-to-end encrypted auditing, anomaly-detection-based auto-pausing, and inter-agent escrow and multi-signature governance capabilities.

## Link
- [https://multipowerai-trust.vercel.app](https://multipowerai-trust.vercel.app)
