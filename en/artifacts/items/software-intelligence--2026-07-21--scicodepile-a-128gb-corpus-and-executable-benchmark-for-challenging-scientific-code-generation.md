---
source: arxiv
url: https://arxiv.org/abs/2607.19104v1
published_at: '2026-07-21T13:46:52'
authors:
- Weifeng Sun
- Ye Fan
- Yuchen Chen
- Gou Tan
- Jieke Shi
- Yuan Yidi
- Swee Liang Wong
- Jonathan Pan
- David Lo
topics:
- scientific-code-generation
- code-benchmarks
- executable-evaluation
- code-pretraining
- code-intelligence
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# SciCodePile: A 128GB Corpus and Executable Benchmark for Challenging Scientific Code Generation

## Summary
SciCodePile combines a 125GB scientific code corpus from 37,737 repositories with a 200-task executable benchmark for testing functional correctness. Its evaluations show that scientific code generation remains difficult, while continued pretraining and instruction tuning on the corpus substantially improve performance.

## Problem
- General code-generation benchmarks do not adequately test scientific software, which requires domain-specific semantics, numerical reasoning, dependencies, and runnable implementations.
- Existing scientific resources usually provide either small evaluation suites or domain-specific corpora, with limited repository-level context and executable verification.

## Approach
- Crawl GitHub using 198 scientific seed keywords expanded to 213 queries, then apply quality and LLM-based relevance filtering; 37,737 repositories remain from 1,311,568 candidates.
- Construct four aligned formats: 125GB of deduplicated code files, 37,737 README summaries, 500,000 function-level instruction instances, and 20,000 problem-solution pairs.
- Derive 200 HumanEval-style tasks from relevant Python functions, synthesize sandboxed environments and tests, and retain only instances that execute successfully; each test suite contains 7.3 assertions on average.
- Evaluate 15 open- and closed-source LLMs on prefix-to-suffix completion, fill-in-the-middle infilling, and executable instruction-following generation.

## Results
- The best CodeBLEU scores are 38.13 for prefix completion and 38.37 for fill-in-the-middle completion.
- On the 200-task executable benchmark, the strongest model reaches 12.30% Pass@1 and 15.50% Pass@5, indicating a substantial gap between textually plausible code and functionally correct scientific code.
- Continued pretraining of GPT-2 (124M) on SciCodePile improves scientific completion CodeBLEU by 2.84×.
- Instruction tuning Qwen2.5-Coder-0.5B on the constructed instruction data improves executable Pass@1 by 4.79×, from 1.90% to 9.10%.
- The benchmark is deliberately limited to pure Python functions with stubbed dependencies, so its executable results do not fully represent multi-file or production scientific workflows.

## Link
- [https://arxiv.org/abs/2607.19104v1](https://arxiv.org/abs/2607.19104v1)
