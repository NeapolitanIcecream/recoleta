---
source: arxiv
url: https://arxiv.org/abs/2605.07728v1
published_at: '2026-05-08T13:34:36'
authors:
- Gaston Besanson
topics:
- agentic-ai
- runtime-governance
- ai-compliance
- multi-agent-systems
- auditability
- human-ai-interaction
relevance_score: 0.63
run_id: materialize-outputs
language_code: en
---

# SARC: A Governance-by-Architecture Framework for Agentic AI Systems

## Summary
SARC turns regulatory and operational obligations for tool-using agents into runtime checks placed inside the agent loop. The paper’s main claim is architectural: constraints should block, monitor, audit, or escalate actions while the system runs.

## Problem
- Tool-using agents can call APIs, sub-agents, and external services before prompt rules, dashboards, or post-hoc audits catch violations; in regulated deployments, that timing can allow an inadmissible action to execute.
- Regulatory duties such as human oversight, traceability, and post-market monitoring need executable checks because documentation alone cannot stop a bad tool call.
- Finite reward penalties cannot always replace hard constraints: the paper gives a two-state example where any finite penalty still lets a high-reward risky action remain optimal when violation probability is small enough.

## Approach
- SARC specifies an agent as `<S,A,R,C>`: state, action space, reward or objective, and constraints.
- Each constraint records `src`, `class`, `pred`, `verif`, `resp`, and an operating point. Classes are hard constraints, soft constraints, and escalation constraints.
- The specification compiles checks into four runtime sites: Pre-Action Gate, Action-Time Monitor, Post-Action Auditor, and Escalation Router.
- A prototype checker tests finite SARC specifications and traces for specification-trace correspondence: which constraints applied, where they were evaluated, what result they produced, and what response followed.
- The multi-agent extension propagates constraints across agents, intersects delegated authority, and keeps attribution-preserving trace trees for cross-agent workflows.

## Results
- In a synthetic procurement task over 50 seeds, SARC produced zero hard-constraint violations under exact predicates.
- The Post-Action Auditor throttling response reduced soft-window overages by 89.5% relative to the policy-as-code-only baseline.
- The evaluation compares SARC with 4 baselines: post-hoc audit, output filtering, workflow rules, and policy-as-code-only.
- The paper reports 95% confidence intervals for the synthetic evaluation, but the excerpt does not provide the interval values.
- Predicate-noise and enforcement-failure sweeps support the claim that residual hard violations under SARC scale with enforcement-stack error rather than environmental violation opportunity.
- The authors limit the result to controlled synthetic procurement runs and do not claim deployment-grade procurement performance.

## Link
- [https://arxiv.org/abs/2605.07728v1](https://arxiv.org/abs/2605.07728v1)
