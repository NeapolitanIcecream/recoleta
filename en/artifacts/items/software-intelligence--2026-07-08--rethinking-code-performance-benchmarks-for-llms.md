---
source: arxiv
url: https://arxiv.org/abs/2607.07619v1
published_at: '2026-07-08T16:36:03'
authors:
- Nhat Minh Le
- Yisen Xu
- Zhijie Wang
- Tse-Hsun
- Chen
topics:
- llm-code-generation
- code-performance-benchmarks
- performance-testing
- multi-agent-testing
- statistical-evaluation
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# Rethinking Code Performance Benchmarks for LLMs

## Summary
This paper finds that current function-level Python performance benchmarks often fail to show whether LLM-generated code is faster. It re-tests four benchmarks and proposes a multi-agent test-generation system that exposes more runtime differences.

## Problem
- Performance benchmarks for LLM code generation often compare generated code with canonical solutions, but their tests may be too small or too correctness-focused to expose speed differences.
- Single-run or low-run timing makes results sensitive to runtime noise from scheduling, cache state, and background processes.
- The issue matters because weak benchmarks can make efficient code look ordinary and can make benchmark claims about LLM code efficiency unreliable.

## Approach
- The authors re-evaluate 1,538 tasks from EffiBench, Enamel, EvalPerf, and Mercury.
- For each task, they run the canonical solution and the benchmark-provided performant implementation 30 times on the original benchmark tests.
- They use the Mann-Whitney U test with p < 0.05 for per-task runtime differences, Cliff’s delta for effect size, and Wilcoxon signed-rank tests for benchmark-level comparisons.
- They manually inspect 308 non-significant tasks and use DeepSeek-V3.1 and GPT-4o as judges to extend the analysis to the remaining non-significant tasks.
- They build a three-agent test-generation system: one agent generates performance-oriented tests, one diagnoses failures or weak tests, and one repairs tests while preserving functional correctness.

## Results
- On the original tests, only 94 of 1,538 benchmark-provided performant implementations are significantly faster than the canonical solutions, or 6.11% overall.
- Non-significant rates are high across all four benchmarks: EffiBench 944/1,000 tasks, Enamel 153/164, EvalPerf 102/118, and Mercury 245/256.
- Among significant tasks, 92 of 94 have large Cliff’s delta effect sizes; 1 has small effect size and 1 has medium effect size.
- In the manual sample of 308 non-significant tasks, 99 performant implementations contain no meaningful performance change, while 209 contain plausible performance improvements hidden by the original tests.
- DeepSeek-V3.1 and GPT-4o agree with human labels at Cohen’s Kappa 0.72 and 0.75, then label 76.06% and 73.94% of the remaining non-significant tasks as having potential performance impact.
- On 1,345 previously non-significant tasks, generated tests reveal significant improvements in 323 tasks with DeepSeek-V3.1 tests, or 24.01%, and 342 tasks with GPT-4o tests, or 25.43%; stronger tests also reveal significant gains in 22.19% of evaluated GPT-4o-mini, Claude-Sonnet-4.5, and Gemini-2.5-Flash outputs.

## Link
- [https://arxiv.org/abs/2607.07619v1](https://arxiv.org/abs/2607.07619v1)
