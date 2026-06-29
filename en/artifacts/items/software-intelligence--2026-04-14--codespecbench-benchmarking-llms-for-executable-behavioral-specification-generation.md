---
source: arxiv
url: http://arxiv.org/abs/2604.12268v1
published_at: '2026-04-14T04:31:45'
authors:
- Zaoyu Chen
- Jianbo Dai
- Boyu Zhu
- Jingdong Wang
- Huiming Wang
- Xin Xu
- Haoyang Yuan
- Zhijiang Guo
- Xiao-Ming Wu
topics:
- code-benchmark
- specification-generation
- program-semantics
- repository-level-reasoning
- llm-evaluation
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# CodeSpecBench: Benchmarking LLMs for Executable Behavioral Specification Generation

## Summary
CodeSpecBench is a benchmark for testing whether LLMs can write executable preconditions and postconditions from natural-language software tasks. It shows that this is hard, especially in real repositories, where the best model reaches only a 20.2% pass rate.

## Problem
- The paper studies whether LLMs understand intended program behavior, not just whether they can produce code that passes tests.
- Prior benchmarks for specification generation are limited: many use static verifiers, simpler assertion forms, small datasets, or only function-level tasks.
- This matters because executable behavioral specifications can check semantic intent, support verification, and give a clearer interface for human and agent collaboration around code.

## Approach
- The benchmark asks models to generate two executable Python functions: a **precondition** that checks valid inputs and state before execution, and a **postcondition** that checks outputs and state after execution.
- It has two settings: **CodeSpecBench-Func** for self-contained function tasks and **CodeSpecBench-Repo** for real multi-file repository issues with code context.
- Evaluation is execution-based. A generated spec must accept all valid behaviors for **correctness** and reject all invalid behaviors for **completeness**; **pass rate** requires both.
- CodeSpecBench-Func contains **2,494** tasks built from LeetCodeDataset. The authors generate and validate large test sets, with **217.8 average tests per task**, **96.3%** average statement coverage, and **93.6%** average branch coverage.
- CodeSpecBench-Repo uses **500** SWE-bench Verified issues across **12** Python projects, with UTBoost-augmented tests and about **19.7k** prompt tokens on average, versus **520.7** for function-level tasks.

## Results
- The benchmark covers **2,494 function-level tasks** and **500 repository-level tasks**. Average tests per task are **217.8** for Func and **123.3** for Repo.
- On **CodeSpecBench-Func**, the best **pass rate** is **47.0%** by **GPT-5-mini**. Other strong results are **46.2%** by **Gemini-2.5-Pro** and **42.5%** by **GPT-OSS-120B**.
- On **CodeSpecBench-Repo**, performance drops hard. The best **pass rate** is **20.2%** by **Claude-4.5-Sonnet**, followed by **18.2%** by **Gemini-2.5-Pro** and **9.6%** by **GPT-5-mini**.
- Repo-level correctness/completeness for the top model are **37.4% correctness**, **57.2% completeness**, and **20.2% pass** for **Claude-4.5-Sonnet**. **Gemini-2.5-Pro** gets **30.8% / 53.0% / 18.2%**.
- Strong code-capable open models still struggle on repo tasks: **DeepSeek-V3.2** reaches **6.8%** repo pass, **QWQ-32B** **3.6%**, and **Qwen3-32B** with reasoning **2.0%**.
- The paper claims specification generation is harder than code generation, so high code-generation scores do not mean the model captures program semantics well. The excerpt does not include the comparison table with those code-generation numbers.

## Link
- [http://arxiv.org/abs/2604.12268v1](http://arxiv.org/abs/2604.12268v1)
