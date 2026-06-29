---
source: hn
url: https://role-model.dev/
published_at: '2026-06-28T22:16:36'
authors:
- handfuloflight
topics:
- ai-routing
- model-orchestration
- capability-aware-routing
- llm-infrastructure
- agent-runtime
relevance_score: 0.66
run_id: materialize-outputs
language_code: en
---

# Role-model: protocol for assigning the right AI model for the right job

## Summary
role-model proposes an open protocol and reference runtime for routing AI requests to endpoints based on task needs, capabilities, policy, and measured performance. It matters for systems that use many models because routing decisions need to be inspectable, portable, and tied to concrete endpoint behavior.

## Problem
- Multi-model systems need a durable way to state what a request requires, which roles and tasks apply, which endpoints can do the work, and which policies allow the call.
- Routing by a model label gives weak control over capability fit, cost, locality, tools, modality, and fallback behavior.
- Operators need an audit trail that explains why an endpoint was chosen or excluded.

## Approach
- Requests carry task type, required capabilities, modalities, tool needs, constraints, and policy context.
- The protocol describes roles, tasks, endpoint identities, endpoint profiles, routing policies, and observability artifacts as separate inspectable objects.
- The reference router filters endpoints by role, task, policy scope, capability, modality, tool support, locality, budget, and binding rules.
- Eligible endpoints are scored with measured quality, latency, throughput, cost, reliability, and preference data, with declared data and neutral defaults used when measurements are missing.
- The runtime returns a RouterDecision with the chosen endpoint, fallbacks, exclusions, and selection reasons.

## Results
- The excerpt reports 0 quantitative benchmark results: no accuracy, latency, throughput, cost, reliability, or routing-quality measurements are provided.
- The claimed output is a packaged reference runtime plus an open routing protocol that can be inspected by clients and operators.
- The router uses a 5-stage decision flow: normalize intent, narrow candidates, apply eligibility checks, score endpoints, and emit a decision.
- The first-run setup lists 7 operational steps: install runtime, connect endpoints, activate models and roles, run benchmark, review results, choose strategy, and validate a routed request.
- The strongest concrete claim is explainable routing across concrete endpoints using roles, tasks, declared capability, policy, and observed performance.

## Link
- [https://role-model.dev/](https://role-model.dev/)
