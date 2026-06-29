---
source: arxiv
url: https://arxiv.org/abs/2604.26855v2
published_at: '2026-04-29T16:20:25'
authors:
- Frank Ginac
topics:
- ai-assisted-coding
- software-engineering
- code-review
- human-ai-interaction
- software-reliability
- model-collapse
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# Cognitive Atrophy and Systemic Collapse in AI-Dependent Software Engineering

## Summary
This position paper argues that heavy reliance on LLM coding agents can weaken engineers' mental models and make software failures harder to diagnose. It proposes stricter training, review, and data controls for AI-generated code.

## Problem
- LLM coding can separate code production from human understanding, creating "epistemological debt": the gap between what a system does and what maintainers can explain.
- The paper says this matters because engineers who accept AI patches without tracing the logic may fail during outages, security incidents, or dependency failures.
- Recursive training and reuse of synthetic code may narrow the range of code patterns and spread insecure or average solutions.

## Approach
- The paper defines epistemological debt as a human-system interface cost, distinct from technical debt in the codebase.
- It builds the argument with Polanyi's tacit knowledge, "vibe coding," "mechanized convergence," and model collapse from recursively generated data.
- It uses Amazon Q Developer and reported 2026 Amazon incidents as a case study for AI-assisted code review risk.
- It recommends "no-vibe coding" in core education, senior review for AI-assisted production changes, specification-to-code traceability, property-based testing, dependency impact audits, performance profiling, and curated human-written code corpora.

## Results
- The paper reports that Amazon Q Developer migrated 30,000 production applications to Java 17, with estimated savings of 4,500 developer-years and $260 million in annual costs.
- It cites a 79% acceptance rate for auto-generated code reviews without manual modification, using this as evidence of a rubber-stamp review pattern.
- It claims two 2026 Amazon incidents: a six-hour primary e-commerce storefront outage and a 13-hour AWS cost-management service disruption linked to GenAI-assisted changes.
- It cites Shukla et al. for a 37.6% increase in critical security vulnerabilities after five iterations of AI code generation without rigorous human intervention.
- The paper does not present a new controlled experiment or benchmark; its main contribution is a conceptual risk model and a set of governance recommendations.

## Link
- [https://arxiv.org/abs/2604.26855v2](https://arxiv.org/abs/2604.26855v2)
