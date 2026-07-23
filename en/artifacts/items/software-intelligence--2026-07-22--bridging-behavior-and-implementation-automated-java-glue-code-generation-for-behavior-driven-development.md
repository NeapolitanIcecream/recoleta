---
source: arxiv
url: https://arxiv.org/abs/2607.19703v1
published_at: '2026-07-22T03:06:45'
authors:
- Xinyu Shi
- Zhou Yang
- An Ran Chen
topics:
- code-intelligence
- automated-software-production
- multi-agent-software-engineering
- behavior-driven-development
- code-generation
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# Bridging Behavior and Implementation: Automated Java Glue Code Generation for Behavior-Driven Development

## Summary
AutoGlue generates Java BDD glue code by combining scenario-level behavior interpretation with retrieval from related BDD artifacts and the target project codebase. On 1,307 steps from eight open-source Java projects, it outperformed prompting baselines and produced directly usable code for 46.1% of steps.

## Problem
- BDD scenarios make requirements executable, but developers must manually connect each natural-language step to project APIs through glue code.
- This work matters because steps are often underspecified, relevant implementation details are scattered across large codebases, and requirement changes make glue-code creation and maintenance labor-intensive.

## Approach
- AutoGlue uses a hierarchical multi-agent workflow with three stages: behavior interpretation, context retrieval, and glue-code generation.
- A Behavior Interpreter determines a step's intent from its enclosing feature and scenario rather than treating the step in isolation.
- A Developer agent coordinates separate BDD Context Retriever and Project Context Retriever agents to find similar steps, existing glue code, relevant Java classes, methods, and APIs.
- The final generator produces Java glue code grounded in both the interpreted behavior and retrieved project context, including framework-specific annotations, parameters, and project calls.

## Results
- The evaluation used 1,307 step–glue-code pairs from eight open-source Java projects.
- Compared with few-shot prompting, AutoGlue improved API F1 by 58.7% and CodeBLEU by 43.7%; the paper also reports consistent gains over plain prompting.
- An LLM-as-a-Judge assessment found that 46.1% of generated implementations were directly usable without modification.
- Most partially correct outputs needed minor edits, especially adding missing actions or refining parameters.
- Ablations showed that behavior interpretation and project-aware context retrieval each substantially improved generation quality, although execution-based validation was limited by environment dependencies and the lack of reliable step-level oracles.

## Link
- [https://arxiv.org/abs/2607.19703v1](https://arxiv.org/abs/2607.19703v1)
