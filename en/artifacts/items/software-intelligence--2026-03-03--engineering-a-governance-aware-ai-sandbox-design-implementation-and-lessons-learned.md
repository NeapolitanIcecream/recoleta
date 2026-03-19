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
- ai-sandbox
- governance-aware-architecture
- multi-tenant-systems
- access-control
- auditability
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# Engineering a Governance-Aware AI Sandbox: Design, Implementation, and Lessons Learned

## Summary
This paper proposes and implements a governance-aware multi-tenant AI Sandbox for industry-academia collaboration, designed to conduct AI experiments under controlled conditions and accumulate reusable evaluation evidence. Its core value is that access control, approval workflows, and audit logging are built directly into the experimentation platform architecture rather than added as an after-the-fact remedy.

## Problem
- Early evaluation of AI technologies in real organizations is often **informal, fragmented, and not comparable**, making results hard to reuse and leaving insufficient evidence for adoption decisions.
- Industry-academia collaboration scenarios must simultaneously satisfy **rapid experimentation** and **governance constraints**: organizational isolation, permission control, compliance, data management, human oversight, and traceability.
- Existing research on regulatory sandboxes or AI governance focuses more on institutional goals, and **lacks practical guidance on how to engineer a multi-tenant, governance-aware experimentation platform**.

## Approach
- Proposes a **layered reference architecture**: multi-tenant frontend layer + backend control plane + independent AI execution layer + data storage layer, with a gateway connecting the control plane and execution plane to isolate governance logic from compute/model execution.
- Makes governance the “default path” in the backend control plane: using **JWT + RBAC + ABAC**, organization/project-level scopes, approval workflows, and audit logs, policies are enforced before requests enter business logic.
- Designs the system around **persistent governance artifacts**: users, roles, organizations, projects, service permissions, hardware quotas, approval records, and audit records are all stored in structured form, making experiment context and governance decisions traceable, comparable, and reusable.
- Developed through a **requirements-driven, iterative validation** method: conducted approximately 1-hour semi-structured interviews with 3 industrial partners, followed by prototype reviews every two weeks to continuously refine requirements, architecture, and implementation.
- Implements a deployable prototype: the frontend is based on Next.js/React, the backend on Express/Node.js, the database uses SQLite, AI capabilities are integrated through backend adapters for Hugging Face/OpenAI, and it includes an independent Python anonymization microservice.

## Results
- The paper’s main outputs are **architecture, prototype, and lessons learned**, rather than SOTA performance or model quality; it **does not provide quantitative performance metrics on benchmark datasets**, nor systematic benchmark numbers such as throughput, latency, or accuracy.
- The industrial research process involved **3 industry partners** (Bittium, Q4US, Solita), with **semi-structured interviews of about 1 hour each**, and **structured prototype reviews every two weeks** during development.
- The prototype claims to have validated several key governance workflows: user registration, approval handling, role-based dashboard access, project creation, AI service invocation, hardware request submission workflows, and blocking unauthorized access across roles/organizations.
- Test results are mainly **qualitative validation**: the authors state that middleware-level RBAC and permission checks can reject illegal requests, and audit logs can record security-related events; however, they also explicitly note that **a complete automated test suite was not implemented**.
- On the engineering side, the system supports **Kubernetes-compatible** deployment, local orchestration with Docker Compose, and backend-hosted integration with Hugging Face/OpenAI; governance of hardware resources is currently a **logical simulation** rather than real cluster orchestration.
- The paper’s strongest “breakthrough” claim is not a numerical improvement, but that it provides an open-source, runnable **reference architecture and prototype for a governance-aware AI Sandbox**, while clearly distinguishing between a “technical sandbox” and a “regulatory sandbox” in the sense of Article 53 of the EU AI Act.

## Link
- [http://arxiv.org/abs/2603.03394v1](http://arxiv.org/abs/2603.03394v1)
