---
source: arxiv
url: http://arxiv.org/abs/2604.04990v1
published_at: '2026-04-05T07:32:37'
authors:
- Phongsakon Mark Konrad
- Tim Lukas Adam
- Riccardo Terrenzi
- Serkan Ayvaz
topics:
- ai-coding-agents
- software-architecture
- prompt-engineering
- code-generation
- multi-agent-software-engineering
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Architecture Without Architects: How AI Coding Agents Shape Software Architecture

## Summary
This position paper argues that AI coding agents already make software architecture decisions, often without review or recorded rationale. It introduces a model of how prompts drive infrastructure choices and shows, with a small case study, that changing prompt wording alone can produce different system architectures.

## Problem
- The paper studies how coding agents choose frameworks, databases, integrations, and decomposition strategies during code generation, even when teams do not treat those choices as architecture decisions.
- This matters because those decisions happen fast, arrive bundled, and often leave no ADRs, design docs, or review trail, which creates governance, security, and maintenance risk.
- The paper also argues that prompt features such as structured output, tool access, and retrieval requirements can force extra infrastructure, so a prompt can act as an architecture specification.

## Approach
- The authors identify **five mechanisms** of agent-driven architectural choice from a survey of coding tools: model selection, task decomposition, default configuration, scaffolding/autonomous generation, and integration protocols.
- They propose **six prompt-architecture coupling patterns** grouped into constraint, capability, and context patterns: structured output, few-shot selection, function calling, ReAct reasoning, RAG, and context reduction.
- They classify these couplings as **contingent** when stronger model capabilities may reduce the extra infrastructure, or **fundamental** when the infrastructure is logically required, such as tool orchestration.
- They run an illustrative case study with three independently generated customer-service chatbot variants using Claude Code with default settings, while keeping the runtime model fixed at GPT-4o-mini and changing only the prompt wording.
- They use the case study to trace how prompt specificity changes components, dependencies, and failure modes, then discuss review practices, ADR generation, and architecture-aware governance tooling.

## Results
- The main concrete result is architectural divergence from prompt wording alone on the same task: Variant A (“answer product questions from a FAQ”) produced **141 LoC, 2 files**; Variant B (structured JSON with schema validation) produced **472 LoC, 4 files**; Variant C (tool access) produced **827 LoC, 6 files**.
- Relative to Variant A, the most complex variant grew by about **5.9x in code size** (**141 → 827 LoC**) and **3x in file count** (**2 → 6 files**).
- Structured output added concrete components absent in the simpler prompt: **Zod schema, retry handler, fallback generator**. Tool access added **tool registry, agent loop, SQLite state store**.
- The paper claims **five agent decision mechanisms** and **six recurring coupling patterns**, but these are analytical contributions, not empirically validated benchmarks.
- There are **no quantitative accuracy or benchmark results** on datasets, task success, or comparisons against baselines such as human-designed architectures or other agents. The evidence is a tool survey plus a single illustrative case study.

## Link
- [http://arxiv.org/abs/2604.04990v1](http://arxiv.org/abs/2604.04990v1)
