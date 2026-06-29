---
source: arxiv
url: http://arxiv.org/abs/2604.11623v3
published_at: '2026-04-13T15:35:55'
authors:
- Charafeddine Mouzouni
topics:
- agentic-ai
- context-orchestration
- enterprise-governance
- access-control
- rag-systems
relevance_score: 0.85
run_id: materialize-outputs
language_code: en
---

# Context Kubernetes: Declarative Orchestration of Enterprise Knowledge for Agentic AI Systems

## Summary
This paper proposes Context Kubernetes, a Kubernetes-style orchestration layer for enterprise knowledge used by AI agents. It focuses on governance, permissions, freshness, and auditability rather than agent reasoning itself.

## Problem
- Enterprises can run a single AI agent against local files, but scaling to many agents across an organization creates coordination and governance problems: which knowledge reaches which agent, under what permissions, with what freshness, and with what audit trail.
- Existing agent platforms have weak or vendor-specific governance layers, and standard RBAC for humans does not fully address autonomous agents that act on a user's behalf.
- This matters because stale, over-permitted, or poorly routed context can cause data leaks, wrong actions, and failed enterprise deployments.

## Approach
- The paper treats organizational knowledge like a schedulable resource and adapts two Kubernetes ideas: declarative desired state in YAML manifests and a reconciliation loop that checks real state against declared state and fixes drift.
- It defines six main abstractions: context units, domains, stores, endpoints, a Context Runtime Interface for connectors, and domain-specific context operators.
- Agents request knowledge by intent rather than source location. A router resolves the request to allowed sources, filters by permissions, checks freshness, and fits the response into a token budget.
- The key governance mechanism is a three-tier permission model where agent authority must be a strict subset of the human user's authority. High-risk actions require out-of-band approval with a separate factor.
- The prototype includes a Context Router, Permission Engine, connectors, reconciliation loop, audit log, FastAPI service, and 92 automated tests.

## Results
- The evaluation includes 8 experiments: 5 correctness experiments and 3 value experiments.
- On 200 benchmark queries over synthetic seed data, the paper compares four governance setups: ungoverned RAG, ACL-filtered retrieval, RBAC-aware routing, and the full architecture. It claims each added layer contributes a distinct capability.
- In 5 attack scenarios, flat permissions block 0/5 attacks, basic RBAC blocks 4/5, and the three-tier model blocks 5/5.
- With no freshness monitoring, stale and deleted content can be returned silently. With reconciliation, staleness is detected in under 1 ms.
- The correctness tests report zero unauthorized context deliveries and zero permission invariant violations.
- TLA+ model checking explored 4.6 million reachable states and found zero safety violations. The paper also claims no surveyed enterprise platform enforces its out-of-band approval isolation design.

## Link
- [http://arxiv.org/abs/2604.11623v3](http://arxiv.org/abs/2604.11623v3)
