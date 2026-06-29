---
source: arxiv
url: https://arxiv.org/abs/2606.01508v1
published_at: '2026-06-01T00:08:03'
authors:
- Ankur Sharma
- Deep Shah
topics:
- agent-operating-system
- agentic-control-plane
- os-security
- agent-governance
- tool-mediation
- auditability
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Agent Operating Systems (AOS): Integrating Agentic Control Planes into, and Beyond, Traditional Operating Systems

## Summary
The paper defines an Agent Operating System as a control plane for long-running AI agents that need scheduling, memory, permissions, policy checks, and audit trails beyond normal process management. It is a conceptual systems paper, with architecture and evaluation criteria rather than benchmark results.

## Problem
- Traditional OS abstractions such as processes, threads, files, syscalls, and static permissions do not capture agent intent, goal progress, delegated authority, tool use, or decision lineage.
- Production agent systems often put scheduling, memory, permissions, tool mediation, and audit in application code, which weakens enforcement and makes incident review harder.
- The problem matters because agents can take side-effecting actions across files, networks, APIs, and services while their reasoning remains probabilistic and may be wrong or manipulated.

## Approach
- The paper proposes an Agent Operating System layer above existing kernels, where agent identity, goals, task graphs, capability sets, context state, and execution records are first-class managed objects.
- It separates reasoning, execution, and policy: the model proposes actions, the policy layer authorizes or denies them, and the execution layer runs approved tool calls in controlled environments.
- The architecture includes lifecycle management, goal-aware scheduling, context and memory management, a tool and capability registry, deterministic policy enforcement, and append-only audit records.
- It maps AOS deployment paths to user-space runtimes, OS extensions, distributed control planes, and partial takeover of higher-level OS responsibilities while leaving kernel duties such as paging, drivers, and low-level CPU scheduling in the OS.
- It grounds the design in existing Linux and Windows mechanisms, including containers, cgroups, namespaces, seccomp, SELinux/AppArmor, eBPF, Windows policy controls, and audit streams.

## Results
- The excerpt reports no quantitative benchmark results, no prototype performance numbers, and no measured comparison against Linux, Windows, Kubernetes, or agent runtimes.
- The paper claims 6 main contributions: an AOS definition, component decomposition, integration models, Linux/Windows mappings, security analysis, and evaluation criteria.
- It defines 3 separated planes: reasoning, execution, and policy, with deterministic enforcement required before any side-effecting action runs.
- It lists 4 architectural invariants, including that no side-effecting action executes without a deterministic allow decision and that policy outcomes are recorded in append-only audit logs.
- It describes 4 integration models: user-space runtime, OS extension, distributed control plane, and selective takeover of higher-level OS responsibilities.
- It gives 4 memory classes for agents: ephemeral context, durable agent memory, retrieved knowledge, and execution records, each with different retention, provenance, and audit needs.

## Link
- [https://arxiv.org/abs/2606.01508v1](https://arxiv.org/abs/2606.01508v1)
