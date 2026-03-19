---
source: hn
url: https://news.ycombinator.com/item?id=47225418
published_at: '2026-03-02T22:56:56'
authors:
- genesalvatore
topics:
- ai-governance
- autonomous-agents
- deterministic-policy
- llm-safety
- audit-trail
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Show HN: We filed 99 patents for deterministic AI governance(Prior Art vs. RLHF)

## Summary
This piece proposes a **deterministic** architecture for governing autonomous agents, aiming to replace probabilistic safety approaches that rely on RLHF and prompts. The core claim is to demote the LLM from an “executable actor” to something that can only generate intent, with an external deterministic policy execution layer providing strict constraints and auditing.

## Problem
- Existing autonomous agent safety mainly relies on probabilistic alignment methods such as **RLHF, system prompt, constitutional training**; the author argues these methods fail under jailbreaks or context overflow.
- The author emphasizes that “a statistical disposition is not a security boundary”: if the model itself still holds execution power, it cannot provide a verifiable, enforceable governance mechanism.
- This is especially important for automated agents, because once an agent can actually call tools, take actions, or run continuously, loss-of-control risks expand into security, compliance, and ethics.

## Approach
- Proposes **Deterministic Policy Gates**: the LLM does not directly execute any action and can only output an **intent payload**.
- That payload is sent into a **process-isolated deterministic execution environment**, where an external rule system rather than the model’s probability distribution determines whether execution is allowed.
- The execution environment matches requests against a **cryptographically hashed constraint matrix** (which the author calls the constitution); if constraints are violated, the request is blocked directly.
- Every decision is recorded to a **Merkle-tree substrate (GitTruth)**, creating an immutable audit trail.
- The author also claims to write **humanitarian use restrictions** directly into patent claims, attempting to restrict use for autonomous weapons, mass surveillance, or exploitation at the IP layer.

## Results
- The text **does not provide experimental data, benchmark tests, or quantitative evaluation results**, so its effectiveness on specific datasets, task success rate, jailbreak interception rate, or performance overhead cannot be verified.
- The strongest concrete claim is that, starting from **2026-01-10**, the author filed **99 provisional patents** around this architecture.
- The paper/post claims that compared with **RLHF / system prompts / constitutional training**, this approach is closer to a “true security boundary,” because the model is stripped of execution authority and violating intents are intercepted by a deterministic policy layer.
- It also claims to achieve an “immutable audit trail” through **Merkle-tree** logging, but provides no figures for throughput, storage cost, or audit latency.
- It claims to include a **Peace Machine Mandate** in the patents to restrict certain misuse scenarios, but provides no data on legal enforceability or actual constraint effectiveness.

## Link
- [https://news.ycombinator.com/item?id=47225418](https://news.ycombinator.com/item?id=47225418)
