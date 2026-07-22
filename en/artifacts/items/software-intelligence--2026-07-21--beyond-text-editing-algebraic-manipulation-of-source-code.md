---
source: arxiv
url: https://arxiv.org/abs/2607.18742v1
published_at: '2026-07-21T06:05:17'
authors:
- Kevin Pulo
topics:
- code-intelligence
- automated-software-production
- llm-coding-agents
- semantic-code-editing
- program-transformation
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Beyond Text Editing: Algebraic Manipulation of Source Code

## Summary
The paper proposes source code algebra: representing code changes as deterministic, semantic operations instead of low-level text edits. A proof-of-concept suggests that LLM coding agents can perform a non-local change more successfully while using one to two orders of magnitude fewer tokens, although the evidence is preliminary.

## Problem
- Text-based editing forces programmers and LLM agents to identify and update every affected location, increasing context requirements and the risk of syntax, semantic, merge, and logic errors.
- This matters for agentic software development because a high-level coding plan must otherwise be converted into dispersed, low-level edits across a codebase.

## Approach
- Source code algebra treats the codebase as a structured object that can be transformed through logical operations such as `AddParam`, `Rename`, `MakeCond`, `MoveParam`, and `TupleToStruct`.
- Each operation is intended to make the complete set of changes required for one semantic modification, producing deterministic and syntactically and semantically valid output.
- Operations can be composed into higher-level operations, such as `MakeOptional`, and can expose properties including completeness, composability, nullipotency, pluripotency, and commutativity.
- The Source Code Algebraic System (SCAS) parses code with tree-sitter, enriches its syntax tree with semantic information, stores the result in MongoDB, and exposes composable operations as tools for LLM agents.

## Results
- A feasibility probe used ReAct agents with SCAS on a cross-file Java method-symbol rename in a synthetic codebase of approximately 5.5k lines, 500 KB, 200k tokens, and 8 files.
- The task used deliberately ambiguous symbol names, making naive text replacement unreliable.
- The abstract reports higher success rates for algebraic editing than text-based baselines, but the excerpt does not provide the exact success percentages or sample sizes.
- SCAS required one to two orders of magnitude fewer tokens than text-based baselines for the demonstrated non-local change.
- The results support feasibility and motivate further work, but the evaluation is explicitly preliminary and does not establish broad performance across languages, tasks, or codebases.

## Link
- [https://arxiv.org/abs/2607.18742v1](https://arxiv.org/abs/2607.18742v1)
