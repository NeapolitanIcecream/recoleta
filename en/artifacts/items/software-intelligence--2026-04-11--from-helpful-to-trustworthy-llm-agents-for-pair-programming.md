---
source: arxiv
url: http://arxiv.org/abs/2604.10300v1
published_at: '2026-04-11T17:39:57'
authors:
- Ragib Shahariar Ayon
topics:
- llm-agents
- pair-programming
- formal-specification
- software-verification
- code-intelligence
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# From Helpful to Trustworthy: LLM Agents for Pair Programming

## Summary
This paper proposes a multi-agent pair-programming workflow for LLMs that aims to make code generation more trustworthy by turning intent into explicit specifications and checking outputs with deterministic tools. It is a doctoral research plan, supported by early results from the author's prior specification-generation systems.

## Problem
- LLM coding agents can produce code, tests, and docs that look plausible but do not match developer intent.
- Free-form agent review is hard to audit, so developers still need to inspect outputs closely in real projects.
- Software changes over time through refactoring, API migration, and documentation updates, and current agent workflows give limited evidence that behavior stayed correct.

## Approach
- Use a driver agent to propose artifacts and a navigator agent to critique them in a pair-programming loop, with separate roles and shared project context.
- Constrain the navigator to output machine-checkable contracts and formal specifications instead of open-ended judgments.
- Validate those specifications and later code/test changes with deterministic verifiers and SMT-backed counterexamples, so review relies on external evidence rather than one model judging another.
- Study three stages: converting informal problem statements into standards-aligned requirements and formal specs, refining tests and implementations with automated feedback, and handling maintenance tasks while preserving validated behavior.
- Measure trustworthiness through concrete signals such as pass rates, inconclusive outcomes, reproducibility of failures, and regression prevention during maintenance.

## Results
- The paper itself is a research proposal and does not report end-to-end results yet for the full pair-programming workflow.
- It cites initial results from **AutoReSpec** on a **72-program benchmark**: **67 programs verified**, **58.2% success probability**, **69.2% completeness**, and **26.89% lower average evaluation time** than prior methods.
- It cites initial results from **AutoJML** on a **120-program benchmark**: **109 programs verified** and **79.3% average completeness**.
- AutoJML also reports strong results on harder control-flow cases: **81.48%** completeness for **multi-path loops** and **85.71%** for **nested loops**, compared with state-of-the-art baselines, though exact baseline numbers are not given in the excerpt.
- The claimed advance is an evidence-driven pair-programming setup where requirements, specifications, tests, and solver feedback act as auditable artifacts for code generation and maintenance.

## Link
- [http://arxiv.org/abs/2604.10300v1](http://arxiv.org/abs/2604.10300v1)
