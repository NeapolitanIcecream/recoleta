---
source: arxiv
url: http://arxiv.org/abs/2603.11073v1
published_at: '2026-03-10T20:20:33'
authors:
- Md Nasir Uddin Shuvo
- Md Aidul Islam
- Md Mahade Hasan
- Muhammad Waseem
- Pekka Abrahamsson
topics:
- ai-assisted-coding
- vibe-coding
- software-architecture
- rag-systems
- multi-tenancy
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Context Before Code: An Experience Report on Vibe Coding in Practice

## Summary
This is an experience report on using "vibe coding" to develop real, deployable systems. The paper's core conclusion is that AI-generated code is very good at accelerating scaffolding and routine implementation, but still depends heavily on human architectural design and auditing for production-grade constraints such as multi-tenant isolation, access control, and asynchronous processing.

## Problem
- The paper addresses the question: **what can conversational code generation do, and what can it not do, under production environment constraints**, especially for key architectural requirements such as multi-tenant isolation, access control, retrieval scope restrictions, and asynchronous tasks.
- This matters because existing research focuses more on productivity and subjective experience, while **less often analyzing the reliability and architectural suitability of AI-assisted programming in deployable systems**.
- If these constraints are not implemented correctly, systems may suffer from **cross-project data leakage, permission errors, blocking processing, and technical debt**, directly affecting production readiness.

## Approach
- The authors conduct a retrospective experience study based on two real cases: a **multi-project agent learning platform** and an **academic document RAG system**.
- The development workflow follows "**context before code**": first clarify functional requirements and non-functional architectural constraints, then use large models to generate APIs, data models, utility functions, and frontend components.
- Put simply, the core mechanism is: **let AI write localized functional code first, while humans define boundary conditions, correct architectural errors, and add system-level constraints**.
- The authors verify whether tenant isolation, role permissions, retrieval scope, citation alignment, and asynchronous execution truly hold through **manual testing, code inspection, runtime logs, and background task monitoring**.
- The paper further identifies a class of "**non-delegation zones**," meaning architectural tasks that current conversational code generation cannot reliably handle, such as isolation policies, permission policies, infrastructure orchestration, and validation logic.

## Results
- The paper **does not provide strict quantitative experimental metrics**, nor does it report percentage productivity gains, defect-rate reductions, or numerical comparisons with baseline tools.
- Across **2 deployable systems**, the authors observe that vibe coding significantly accelerates development of **scaffolding, CRUD, basic routing, serialization utilities, and UI templates**.
- But in both cases, AI-generated code repeatedly omitted critical constraints: for example, early routes in the learning platform **lacked project-level filtering**, creating a risk of cross-project access; the memory update workflow was also initially implemented as **synchronous execution**, violating the asynchronous requirement.
- In the RAG system, early generated versions would **output citations without verifying whether answers were aligned with retrieved passages**; the first version of document embedding also used **synchronous processing**, leading to excessively long response times when uploading large files.
- The authors' strongest empirical conclusion is that engineering work did not disappear; rather, it shifted from **boilerplate coding** to **architectural design, isolation auditing, policy definition, validation, and monitoring**. Table 1 explicitly lists this task redistribution.
- The paper's main claimed contribution is not a new algorithm or benchmark SOTA, but a clear practical conclusion: **under production constraints, AI-assisted development is best suited as a tool for accelerating implementation within clearly defined architectural boundaries, rather than replacing system-level design.**

## Link
- [http://arxiv.org/abs/2603.11073v1](http://arxiv.org/abs/2603.11073v1)
