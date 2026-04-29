---
source: arxiv
url: http://arxiv.org/abs/2604.22659v1
published_at: '2026-04-24T15:35:54'
authors:
- Jia Li
- Hongyi Deng
- Yiran Zhang
- Kechi Zhang
- Tianqi Shao
- Tiankuo Zhao
- Weinan Wang
- Zhi Jin
- Ge Li
- Yang Liu
- Yingtao Fang
- Yihong Dong
topics:
- repo-level-code-generation
- code-benchmark
- uml-guided-generation
- software-engineering
- llm-evaluation
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# RealBench: A Repo-Level Code Generation Benchmark Aligned with Real-World Software Development Practices

## Summary
RealBench is a repo-level code generation benchmark built to match how software teams usually work: code from requirements plus system design, not from text prompts alone. It adds UML-based specifications, real repositories, and test-backed evaluation, then shows that current LLMs still perform poorly on full-repository generation.

## Problem
- Existing code generation benchmarks such as HumanEval and EvoCodeBench mainly score models on natural-language-to-code tasks, often at function or small repo scope.
- In real software development, developers usually implement code from structured design artifacts such as package and class diagrams, so current benchmark scores can misstate practical automation value.
- Repo-level generation gets harder as repository size and dependency density grow, which makes realistic evaluation important for software engineering use cases.

## Approach
- The paper builds **RealBench**, a Python benchmark with **61 real-world repositories** from **20 programming domains**, selected from GitHub projects created in **2024.12-2025.05** to reduce contamination risk.
- Each task includes **natural language requirements** plus a **two-level UML design**: a package diagram for modules and dependencies, and a class diagram for classes, attributes, methods, and relationships.
- Repositories are grouped into **4 size levels**: **0-500 LOC**, **500-1000 LOC**, **1000-2000 LOC**, and **>=2000 LOC**.
- The authors add human-verified tests with **50.05 test cases per repository on average** and **79.76% average line coverage**.
- They evaluate **6 LLMs** under **3 generation strategies**: holistic generation of the full repo, incremental file-by-file generation, and retrieval-augmented generation using file dependency links from the design.

## Results
- RealBench is larger and more design-rich than prior repo benchmarks: **2,484 requirements**, **544 UML diagrams**, **538 files**, and **1,201 average LOC** per repository; Table 1 reports RealBench as the only listed benchmark with both repo-level tasks and diagram inputs.
- Current models perform poorly on this setting: the **best average Pass@1 is 19.39%** across all studied LLMs.
- Performance drops sharply with repository size: **Pass@1 is above 40%** for repositories with **<500 LOC** and **below 15%** for repositories with **>2000 LOC**.
- Benchmark complexity is substantial: only **44.73%** of methods/functions are standalone on average, and in level-4 repositories only **26.23%** are standalone, so most code has dependencies.
- The benchmark reports strong test support by size level: line coverage is **91.16%** for level-1, **81.07%** for level-2, **74.09%** for level-3, and **72.71%** for level-4 repositories.
- The paper claims that **holistic generation works best for smaller repositories (<1000 LOC)**, while **incremental generation works better for larger repositories (>1000 LOC)**, and that detailed UML design materially improves repo-level generation. The excerpt does not provide per-model score tables or exact gains from the ablation.

## Link
- [http://arxiv.org/abs/2604.22659v1](http://arxiv.org/abs/2604.22659v1)
