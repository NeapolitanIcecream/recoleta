---
source: arxiv
url: http://arxiv.org/abs/2603.02510v1
published_at: '2026-03-02T20:41:07'
authors:
- Liu Yang
- Zeyu Nie
- Andrew Liu
- Felix Zou
- "Deniz Altinb\xFCken"
- Amir Yazdanbakhsh
- Quanquan C. Liu
topics:
- code-generation
- parallel-computing
- irregular-data
- program-synthesis
- evolutionary-search
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# ParEVO: Synthesizing Code for Irregular Data: High-Performance Parallelism through Agentic Evolution

## Summary
ParEVO targets parallel code generation for irregular data, aiming to enable large models not only to write parallel programs that run, but also to produce implementations that are truly high-performance and free of data races. It combines domain-specific fine-tuning with evolutionary search driven by compilation, race detection, and performance profiling, targeting hard HPC problems such as graphs and sparse structures.

## Problem
- The paper addresses how to automatically synthesize **correct and high-performance** parallel code for **irregular data structures** (such as graphs, sparse matrices, and nonuniform meshes).
- This matters because modern performance gains increasingly depend on parallel computing, but these tasks have uneven workloads and dynamically changing dependencies, making manual concurrent programming difficult, while LLMs often fail due to **race conditions, deadlocks, and incorrect synchronization**.
- Existing LLMs show a clear “sequential bias,” often just wrapping a serial program with an outer parallel loop, leading to errors or even worse performance.

## Approach
- It first builds an execution-validated training set, **Parlay-Instruct**: starting from 593 human seed examples and DMOJ problems, it uses a “Teacher-Student-Critic”/“Critic-Refine” pipeline to generate and filter samples, ultimately producing **13,820** parallel task examples that compile and pass tests.
- The core idea is to teach the model **high-level parallel primitives** rather than low-level threading details: mapping natural-language requirements to ParlayLib primitives such as `filter`, `scan`, `reduce`, and `sort`, making it easier to obtain parallel algorithms that are “structurally correct.”
- At the model level, the authors fine-tuned specialized models, including **DeepSeek-6.7B**, **Qwen3-30B** (C++/Rust), and an adapted version of **Gemini-2.5-Pro**, so they better understand ParlayLib semantics, parallel patterns, and Rust safe-concurrency practices.
- At inference time, they use an **Evolutionary Coding Agent (ECA)**: generating a batch of candidate programs, evaluating them with **compilers, unit tests, dynamic race detectors, and performance profilers**, and then performing “mutation/crossover/repair” based on feedback from these external tools to optimize code generation by generation.
- The search combines **performance-optimal selection** with **MAP-Elites** diversity maintenance; if a candidate program fails to compile, fails tests, or triggers a data race/deadlock, its fitness is set directly to 0.

## Results
- On the **ParEval** benchmark, ParEVO reports an **average 106× speedup**, with a maximum of **1103×**, indicating that its generated parallel implementations can achieve very large acceleration relative to the baseline.
- On **highly complex irregular graph problems**, it reports an **average 13.6× speedup**, and claims to outperform commercial models such as **GPT-5-Thinking** and **Gemini-3-Pro**.
- Compared with expert human baselines, the evolutionary method achieves up to a **4.1× speedup** on some highly irregular kernels; the paper gives **Maximal Independent Set** as an example.
- The authors also report a “correctness-speed” tradeoff: after fine-tuning, **Pass@1 rises from 0.42 to 0.76**, but peak speed drops from **21.7×** to **13.6×**, because the model becomes more inclined to use safe high-level primitives rather than aggressive but riskier atomic operations.
- On the dataset side, the training corpus contains **13,820** validated instruction-tuning samples, of which **13,120** are used for training and **700** are held out for testing; samples are included in the performance-comparison set only if the optimized version achieves at least a **1.2×** speedup.

## Link
- [http://arxiv.org/abs/2603.02510v1](http://arxiv.org/abs/2603.02510v1)
