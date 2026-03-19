---
source: arxiv
url: http://arxiv.org/abs/2603.03394v1
published_at: '2026-03-03T11:01:56'
authors:
- Muhammad Waseem
- Md Aidul Islam
- Md Nasir Uddin Shuvo
- Md Mahade Hasan
- Kai-Kristian Kemell
- Jussi Rasku
- Mika Saari
- Vilma Saari
- Roope Pajasmaa
- Markku Oivo
- Pekka Abrahamsson
topics:
- ai-governance
- sandbox-platform
- multi-tenant-architecture
- audit-logging
- access-control
relevance_score: 0.06
run_id: materialize-outputs
language_code: en
---

# Engineering a Governance-Aware AI Sandbox: Design, Implementation, and Lessons Learned

## Summary
This paper proposes and implements a “governance-aware” multi-tenant AI Sandbox for industry-academia collaboration, enabling AI experimentation under controlled permissions, organizational isolation, and traceable workflows. Its core contribution is embedding approval processes, access control, and audit logging directly into the experimentation platform architecture to improve the reusability and comparability of evaluation evidence.

## Problem
- Early-stage evaluation of AI technologies is often **informal and fragmented**, making results difficult to compare and evidence hard to reuse across different teams, tools, and use cases.
- In real organizational environments, AI experimentation is also constrained by **governance, compliance, data management, and human oversight**; if these constraints are not systematically incorporated into the platform, organizations will struggle to decide whether to adopt AI based on reliable evidence.
- Existing sandbox research focuses more on **regulatory or institutional aspects**, but lacks engineering guidance on how to actually build a **multi-tenant, governance-aware, operationalized** experimentation platform.

## Approach
- Based on Finland’s SW4E ecosystem, the authors collected and validated requirements with 3 industrial partners through **semi-structured interviews + biweekly iterative reviews**, then gradually developed a reference architecture and MVP prototype.
- The core mechanism is a **layered architecture**: a front-end multi-tenant workspace + a backend control plane + an independent AI execution layer + a data storage layer; the control plane centrally manages identity, approvals, collaboration, experiment orchestration, and policy enforcement.
- The platform turns governance into a system mechanism: using **JWT + RBAC + ABAC**, organization/project-level isolation, approval workflows, and audit logs, it records “who can access what, who approved what, and what experiments were conducted” as persistent governance artifacts.
- AI capabilities are integrated through **backend-hosted adapters** to external services (such as Hugging Face and OpenAI), preventing the front end from directly handling keys or external interfaces; hardware resources are governed through **quotas and approval workflows** rather than direct bare access to clusters.
- The prototype is implemented with Next.js + Express + SQLite and supports containerized deployment to Kubernetes/OpenShift-like environments, with a focus on validating **governance correctness and architectural feasibility** rather than large-scale performance.

## Results
- The paper’s main outputs are a **reference architecture + open-source prototype + deployment lessons learned**; it provides an open-source repository and online demo, but **does not report quantitative performance results on standard benchmark datasets**.
- The empirical process includes **3 stages** (requirements gathering, architecture design, and prototype development with iterative validation), and involved interviews with **3 industrial partners**; each interview lasted about **1 hour**, and iterations were advanced through **structured reviews every two weeks**.
- The core workflows covered by testing include user registration, approval handling, role-based dashboard access, project creation, AI service invocation, and hardware request submission; the authors claim that **governance constraints at API boundaries were correctly enforced** in these workflows.
- Access control testing was validated by attempting **privileged management operations, cross-organization access, and unauthorized service invocation**; the paper claims that middleware-level **RBAC/permission checks successfully rejected invalid requests**, and that audit logs captured security-relevant events, but it does not provide figures for rejection rate, latency, or coverage.
- Regarding automated testing, the authors explicitly state that there is **no complete end-to-end automated test suite for the main front end and back end**; only lightweight CI exists for build consistency and container integrity checks, indicating that the current work is more of an **engineering prototype validation** than a mature product evaluation.
- The strongest concrete claim is that the platform can achieve **governed onboarding, project collaboration, controlled AI service access, and traceable experiment records** in a multi-tenant environment, while preserving approval decisions and audit logs as evaluation evidence that can be reused across projects and stakeholders.

## Link
- [http://arxiv.org/abs/2603.03394v1](http://arxiv.org/abs/2603.03394v1)
