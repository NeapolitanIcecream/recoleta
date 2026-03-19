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
- vibe-coding
- ai-assisted-development
- software-architecture
- rag-systems
- multi-tenancy
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Context Before Code: An Experience Report on Vibe Coding in Practice

## Summary
This is an experience report on the use of “vibe coding” in real deployable systems. The authors find that AI-generated code can significantly accelerate scaffolding and routine implementation, but production-grade constraints such as multi-tenant isolation, access control, and asynchronous processing still require human-led design and auditing.

## Problem
- The paper addresses the question: under **production constraints**, can conversational code generation reliably build deployable systems rather than merely rapid prototypes? This matters because enterprise systems often require tenant isolation, permission control, traceable retrieval, and stable asynchronous task execution.
- Existing research focuses more on productivity, prompting techniques, or developer perceptions, and less on the actual performance of AI-generated code under **architecture-level constraints**.
- If these constraints are not implemented correctly, systems may face high-risk issues such as cross-project data leakage, improper permission access, untrustworthy citations, or synchronous blocking.

## Approach
- In the form of an **experience report**, the authors retrospectively analyze two deployable systems built using conversational/vibe coding: a multi-project agent learning platform and an academic RAG system.
- The core mechanism is simple: first clearly specify functional requirements and architectural constraints, then let a large model generate APIs, data models, utility functions, and frontend components; afterward, humans check whether the code actually satisfies requirements for isolation, permissions, retrieval scope, and asynchronous execution.
- Both systems follow a “**context before code**” approach: prompts explicitly include constraints such as project isolation, role separation, background tasks, retrieval scope, and citation tracing, rather than describing functionality alone.
- Evidence comes from commit records, issue discussions, prompt iterations, deployment logs, and implementation notes; validation methods include manual testing, code review, and runtime log analysis.
- The authors further identify several “**non-delegation zones**,” such as multi-tenant boundaries, access control policies, memory update policies, citation alignment checks, background task orchestration, and infrastructure design—areas that cannot safely be fully delegated to AI generation.

## Results
- The paper **does not provide controlled experiments or systematic quantitative metrics**; in “Threats to Validity,” the authors explicitly state that **no** quantitative comparison was conducted for productivity, code quality, or defect rate.
- The strongest experience-based conclusion is that, across **2** deployable system cases, vibe coding significantly accelerated scaffolding, CRUD, routing, utility functions, and UI template development, but key architectural constraints were often omitted.
- In Case 1 (the multi-project agent learning platform), early AI-generated routes **lacked project-level filtering**, creating a risk of cross-project access; the initial memory update also incorrectly used **synchronous execution**, ultimately requiring humans to add project ID checks and migrate it to a background worker.
- In Case 2 (the academic RAG system), the early implementation produced citations with **unchecked answer-citation alignment**, and embedding ingestion was also initially executed **synchronously**, slowing responses during large file uploads; developers later added citation alignment checks and changed it to asynchronous tasks.
- The paper presents a concrete table showing a shift in engineering effort: reduced work includes **4 categories** (boilerplate writing, CRUD scaffolding, basic routing, UI template creation), while increased work also includes **4 categories** (architecture design, isolation auditing, policy specification, validation and monitoring).
- The overall claim is that AI-assisted development is better suited as a tool for **accelerating implementation within clearly defined architectural boundaries**, rather than replacing system-level design; the real breakthrough lies not in full automation, but in identifying which production-grade tasks must still remain under human responsibility.

## Link
- [http://arxiv.org/abs/2603.11073v1](http://arxiv.org/abs/2603.11073v1)
