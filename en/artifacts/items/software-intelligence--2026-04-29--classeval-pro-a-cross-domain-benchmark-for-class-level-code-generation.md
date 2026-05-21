---
source: arxiv
url: https://arxiv.org/abs/2604.26923v1
published_at: '2026-04-29T17:38:37'
authors:
- Yeheng Chen
- Chaoxiang Xie
- Yuling Shi
- Wenhao Zeng
- Yongpan Wang
- Hongyu Zhang
- Xiaodong Gu
topics:
- code-generation
- code-benchmark
- class-level-synthesis
- llm-evaluation
- software-engineering
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# ClassEval-Pro: A Cross-Domain Benchmark for Class-Level Code Generation

## Summary
ClassEval-Pro is a 300-task benchmark for generating complete Python classes from specifications. It targets class-level code generation, where models must coordinate methods, shared state, and domain logic.

## Problem
- Current code benchmarks focus on isolated functions or repository issue fixes, so they miss from-scratch class construction.
- Class-level generation matters because object-oriented software often needs multiple methods to share state and call each other correctly.
- Existing class-level benchmarks are small, manually curated, and older, which raises cost and training-contamination concerns.

## Approach
- The benchmark builds 300 class-level tasks across 11 domains, with 233 cross-domain tasks and 67 same-domain tasks.
- The pipeline collects Python classes from GitHub repositories created on or after January 1, 2025, then filters for standard-library-only, self-contained classes with at least 5 methods and 40 to 800 lines.
- It merges class structures with AST-guided prompts to create harder class skeletons that combine domain logic.
- It generates tests with LLMs, uses three LLM judges to check skeleton-test alignment, and keeps only cases where at least two judges give full marks.
- It keeps only tasks whose reference solution compiles, passes all tests, and reaches more than 90% line coverage.

## Results
- ClassEval-Pro contains 300 tasks across 11 domains. The source pool had 206 repositories, 1,114 extracted classes, and 383 classes after filtering.
- The new tasks are larger than ClassEval: average LOC is 117.0 for cross-domain tasks and 122.0 for same-domain tasks, compared with 45.7 in ClassEval.
- The new tasks have higher structure metrics: average dependency depth is 3.01 for cross-domain and 2.85 for same-domain tasks, compared with 1.77 in ClassEval; average method count is 9.53 and 8.60, compared with 4.97.
- Under holistic generation, class-level Pass@1 ranges from 27.9% to 45.6% across five LLMs, a 17.7-point spread.
- Strategy choice has large effects: bottom-up generation improves weaker models by up to 9.4 percentage points, while compositional generation drops as low as 1.3% class-level Pass@1.
- In 500 manually annotated failures, logic errors account for 56.2% and dependency errors account for 38.0%, showing that cross-method coordination is the main failure source.

## Link
- [https://arxiv.org/abs/2604.26923v1](https://arxiv.org/abs/2604.26923v1)
