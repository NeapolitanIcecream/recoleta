---
source: arxiv
url: https://arxiv.org/abs/2605.04973v1
published_at: '2026-05-06T14:28:28'
authors:
- Julius Irion
- Moritz Leugers
- Paul Hartwig
- Simon Kling
- Tachmyrat Annayev
- Alexander Schwind
- Maria C. Borges
- Sebastian Werner
topics:
- ai-assisted-development
- service-scaffolding
- rag
- platform-engineering
- backstage
- software-architecture
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# Architectural Constraints Alignment in AI-assisted, Platform-based Service Development

## Summary
AI-assisted service scaffolding often fails when generated code has to meet company-specific deployment, CI/CD, security, and platform constraints. The paper claims that RAG over approved Backstage templates plus a short clarification chat produces more deployable service starts than open-ended Copilot-style generation.

## Problem
- General LLM coding tools can generate prototypes, but they lack access to organization-specific architecture rules, infrastructure dependencies, and deployment standards.
- This matters because production services must fit existing CI/CD, security policies, Kubernetes setup, and platform templates, or developers spend time debugging generated infrastructure code.
- The paper compares this issue against “vibe coding,” where users repeatedly prompt an AI coding tool until the service appears to work.

## Approach
- The system ingests approved Backstage service templates that include boilerplate code, configuration, CI/CD pipelines, and security policies.
- It embeds those templates with `all-MiniLM-L6-v2` and stores them in Chroma for semantic search.
- A GPT-4o-mini clarification loop asks users for missing requirements such as service purpose, tech stack, database, API style, and CI/CD needs.
- If a user cannot answer a technical question, the system can infer from the remaining context instead of blocking retrieval.
- The final user requirements are embedded and matched against the template catalog; the system recommends the closest pre-approved scaffold.

## Results
- In the RAG template-selection test, the system chose the correct ground-truth template in 10/10 runs, for a 100% success rate.
- In the vibe-coding user study, 7 participants used Visual Studio Code with GitHub Copilot powered by GPT-5-mini; only 2/7 passed all deployment quality gates.
- Average quality-gate success was 43% for vibe coding versus 100% for the RAG system.
- Vibe coding required a mean of 22 prompts, 941k input tokens, 12.1k output tokens, and about $0.26 per run; the RAG system used a median of 3 prompts, 3.2k input tokens, 0.26k output tokens, and about $0.001 per run.
- All vibe-coding participants hit about a 45-minute cap, while the RAG interaction took under 5 minutes.
- The study is small: 7 academic participants, 1 vibe-coding task, and no full functional test beyond deployment checks and pod logs.

## Link
- [https://arxiv.org/abs/2605.04973v1](https://arxiv.org/abs/2605.04973v1)
