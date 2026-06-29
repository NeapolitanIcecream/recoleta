---
source: arxiv
url: https://arxiv.org/abs/2606.12320v1
published_at: '2026-06-10T16:54:47'
authors:
- Krti Tallam
topics:
- ai-agent-governance
- runtime-policy
- multi-agent-security
- capability-attenuation
- enterprise-ai
- auditability
relevance_score: 0.62
run_id: materialize-outputs
language_code: en
---

# A Five-Plane Reference Architecture for Runtime Governance of Production AI Agents

## Summary
The paper proposes a five-plane runtime architecture for governing production AI agents that act through enterprise tools and connectors. It targets delegated action risk: authorized individual steps can combine into an unauthorized business process.

## Problem
- Enterprise security tools mainly check data movement or single requests, while production agents create multi-step plans that change systems of record.
- Standard policy engines evaluate atomic principals and Boolean allow/deny decisions; agent systems need stateful checks over delegation chains and session history.
- This matters because a compromised or misled agent can use permitted tools in sequence to exfiltrate data, overreach authority, or alter business processes.

## Approach
- The architecture splits governance into 5 planes: 1 reasoning plane that decides on intent, plus 4 enforcement planes for network, identity, endpoint, and data.
- The reasoning plane checks the agent plan, composite principal, delegation chain, capability set, and session state before action reaches infrastructure.
- Stop-anywhere mediation inserts checks at 7 points in the agent execution loop and supports 6 interruption primitives: pause, escalate, narrow, modify, defer, and rollback.
- Composite principals bind a delegation chain to attenuated capabilities; the effective authority is the intersection of unexpired capability sets along the chain.
- Audit records are structured and tamper-evident, so incident responders can reconstruct what was decided and how each plane enforced it.

## Results
- The paper claims foreclosure of 7 production-agent threats across a canonical workflow and 4 additional use cases: financial services, healthcare, software engineering, and customer operations.
- It states 4 correctness invariants: composed authority, mediation coverage, bounded composite authority, and evidence sufficiency; these are argued structurally, with no formal proof in the excerpt.
- A reference implementation of the policy-engine core reports attenuation correctness on every trial and evidence reconstructability on every trial; the excerpt does not give trial counts.
- Adjudication is reported to run in single-digit microseconds in the policy-engine core.
- The audit substrate's tamper-evidence is reported to behave as designed in the reference implementation.
- The paper does not report a full-system score on a live agent benchmark; it names that evaluation as future work.

## Link
- [https://arxiv.org/abs/2606.12320v1](https://arxiv.org/abs/2606.12320v1)
