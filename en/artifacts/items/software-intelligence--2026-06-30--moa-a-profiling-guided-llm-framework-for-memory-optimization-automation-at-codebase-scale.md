---
source: arxiv
url: https://arxiv.org/abs/2606.31368v1
published_at: '2026-06-30T09:00:31'
authors:
- Jiaxi Liang
- Yuanxiang Shi
- Zezhou Yang
- Chenxiong Qian
topics:
- llm-code-agents
- memory-optimization
- static-analysis
- profiling-guided-repair
- automated-software-engineering
- c-cpp
relevance_score: 0.89
run_id: materialize-outputs
language_code: en
---

# MOA: A Profiling-Guided LLM Framework for Memory-Optimization Automation at Codebase Scale

## Summary
MOA automates memory-optimization work in large C/C++ codebases by turning profiling evidence into static checks and patches. On OpenHarmony, it reports 13 anti-patterns, 10,067 detected inefficiencies, 769 generated patches, and a 92.5% expert acceptance rate.

## Problem
- Memory bloat and allocation churn raise resource costs and slow production systems, but they often do not cause crashes, so teams find them late.
- Developers must connect profiler traces to source causes, write detection rules, and make semantics-preserving edits across files.
- Local profiler findings do not scale to a 100M+ LOC operating-system codebase without reusable pattern rules and automated repair.

## Approach
- The Analyzer agent loads profiling traces into a relational database, queries runtime evidence, inspects source code, and writes structured anti-pattern reports.
- An independent Reviewer checks whether each report has evidence, a distinct pattern, examples, detection logic, and an optimization strategy.
- The Checker Generator turns accepted reports into Clang Static Analyzer checkers using a fixed skeleton, compiler feedback, and example-based refinement.
- The Patcher groups detected targets into chunks, gathers symbol context with clangd, edits code, checks syntax, and rolls back to checkpoints when validation fails.

## Results
- On OpenHarmony 5.0, a C/C++ OS codebase with over 100 million lines, profiling 3 services produced 13 validated anti-patterns.
- 9 of the 13 anti-patterns, or 69.3%, had no matching Clang-Tidy performance check in the paper's comparison.
- The 13 anti-patterns covered 4 static-object-overuse patterns, 2 inefficient-string patterns, 4 redundant-copying patterns, and 3 const-heap-structure patterns.
- Candidate pattern reports had a 65% yield rate, with 1.5 refinement iterations per accepted pattern on average.
- The synthesized checkers detected 10,067 inefficiency instances across 7 services, and MOA generated 769 optimization patches with 92.5% expert acceptance.
- Accepted optimizations achieved 42.2% average heap reduction and 10.6% average binary-size reduction.

## Link
- [https://arxiv.org/abs/2606.31368v1](https://arxiv.org/abs/2606.31368v1)
