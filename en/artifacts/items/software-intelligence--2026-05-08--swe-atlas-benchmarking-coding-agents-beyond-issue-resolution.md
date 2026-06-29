---
source: arxiv
url: https://arxiv.org/abs/2605.08366v1
published_at: '2026-05-08T18:21:44'
authors:
- Mohit Raghavendra
- Soham Dan
- Miguel Romero Calvo
- Yannis Yiming He
- Johannes Baptist Mols
- Gautam Anand
- Cole McCollum
- Edgar Arakelyan
- Vijay Bharadwaj
- Andrew Park
- Jeff Da
- MohammadHossein Rezaei
- Bing Liu
- Brad Kenstler
- Yunzhong He
topics:
- coding-agents
- software-engineering-benchmark
- codebase-qa
- test-generation
- refactoring
- llm-evaluation
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# SWE Atlas: Benchmarking Coding Agents Beyond Issue Resolution

## Summary
SWE Atlas is a 284-task benchmark for coding agents on codebase Q&A, test writing, and refactoring across 18 active open-source repositories. It measures whether agents can handle engineering work that issue-resolution benchmarks often miss.

## Problem
- Existing coding-agent benchmarks focus on bug fixes and feature implementation, so they miss common software work such as understanding a codebase, writing useful tests, and refactoring safely.
- This matters because agents can pass functional checks while leaving weak tests, incomplete refactors, missed edge cases, or poor code hygiene.
- The paper targets under-specified tasks that require repository exploration, runtime evidence, and professional review criteria.

## Approach
- SWE Atlas contains 124 Codebase Q&A tasks, 90 Test Writing tasks, and 70 Refactoring tasks.
- Codebase Q&A tasks require agents to inspect repositories, run code, trace behavior, and answer developer-facing questions with evidence.
- Test Writing tasks require agents to add tests and submit a manifest; evaluation uses manifest checks, mutation checks, and rubric checks for coverage, placement, and conventions.
- Refactoring tasks require behavior-preserving code changes; evaluation uses regression tests, hidden tests, and rubrics for maintainability, cleanup, documentation, and anti-patterns.
- Expert software engineers wrote the tasks, reference solutions, and rubrics; three trusted experts audited each task and removed invalid or ambiguous rubric items.

## Results
- The benchmark has 284 tasks across 18 repositories, with average rubric counts of 10.5 for Q&A, 17.1 for Test Writing, and 17.4 for Refactoring; refactoring tasks average 18 tests each.
- On native scaffolds, GPT-5.4 Codex leads with 43.49 ± 3.32 Pass@1 and 29.2 Pass³; Opus 4.7 Claude Code follows with 41.89 ± 3.31 Pass@1 and 29.2 Pass³.
- GPT-5.4 scores 40.80 on Q&A, 44.36 on Test Writing, and 44.29 on Refactoring; Opus 4.7 scores 40.30, 38.51, and 48.57 on the same workflows.
- Under the common mini-SWE-agent scaffold, Opus 4.7 scores 38.94 ± 3.25 Pass@1 and GPT-5.4 scores 38.00 ± 3.26; GLM 5 is the best open-weight model listed at 24.03 ± 2.87.
- Even top systems are inconsistent: best Pass³ values are 29.2, about 30-50% below Pass@1 depending on configuration.
- Rubric checks expose gaps hidden by functional tests: refactoring has about a 15-40 point gap between regression-test pass rate and rubric pass rate, while test writing has about a 10-15 point gap between mutation pass rate and rubric pass rate.

## Link
- [https://arxiv.org/abs/2605.08366v1](https://arxiv.org/abs/2605.08366v1)
