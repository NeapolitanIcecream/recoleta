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
- agentic-search
- llm-finetuning
- hpc
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# ParEVO: Synthesizing Code for Irregular Data: High-Performance Parallelism through Agentic Evolution

## Summary
ParEVO aims to enable large models to automatically generate high-performance parallel code for irregular data structures, addressing the difficulty of guaranteeing both concurrency correctness and performance at the same time. It combines domain-specific fine-tuning with evolutionary agent search, iteratively repairing and accelerating code using feedback from compilers, race detectors, and profilers.

## Problem
- Irregular parallel tasks (such as sparse graphs, unbalanced trees, and nonuniform meshes) are difficult to schedule statically and are prone to race conditions, deadlocks, and load imbalance, making parallel code both hard to write and hard to optimize.
- General-purpose LLMs exhibit a clear "sequential bias" and often generate incorrect OpenMP/concurrent code for these tasks, sometimes even slower than serial code.
- This matters because modern performance gains increasingly depend on parallel computing, and irregular parallelism is a core challenge in both HPC and real-world software systems.

## Approach
- Build the **Parlay-Instruct** dataset: synthesize samples through a Teacher-Student-Critic / Critic-Refine-style pipeline and apply strict execution-based validation, yielding **13,820** compiled and test-passing parallel programming samples, with a focus on ParlayLib primitives and performance optimization trajectories.
- Perform domain-specific fine-tuning on models such as **DeepSeek, Qwen, and Gemini** so they learn to map natural-language requirements to high-level parallel primitives like ParlayLib / Rust RPB, rather than directly writing fragile low-level thread synchronization code.
- Propose the **Evolutionary Coding Agent (ECA)**: generate multiple candidate programs at once, then after compiling and running them, use compiler errors, unit test results, dynamic race detection, and runtime/profile measurements as "fitness" signals, followed by continued mutation and selection.
- During search, combine **MAP-Elites** to preserve candidate diversity, and use features such as code length, cyclomatic complexity, and synchronization primitive usage frequency to avoid search collapse.
- The core mechanism can be understood simply as: first teach the model the "right parallel building blocks," then let the agent keep trial-and-erroring on real machine feedback until the code is both correct and fast.

## Results
- On the **ParEval** benchmark, ParEVO reports an **average 106× speedup** and a **maximum 1103× speedup** across the full task suite.
- On highly complex irregular graph problems, it achieves **13.6× speedup** and claims to outperform commercial models such as **GPT-5-Thinking** and **Gemini-3-Pro**.
- Compared with expert hand-written baselines, it can reach up to **4.1× speedup** on certain highly irregular kernels (such as **Maximal Independent Set**).
- The paper also reports an "alignment tax" in concurrent programming: after fine-tuning, **Pass@1 rises from 0.42 to 0.76**, but peak performance **Speedup drops from 21.7× to 13.6×**, indicating that safer high-level primitives sacrifice some ultimate speed.
- In terms of dataset scale, the final retained set contains **13,820** validated samples, split into **13,120** training samples and **700** test samples.
- The excerpt does not provide a more complete per-model breakdown table, but the strongest quantitative claim is that ParEVO significantly surpasses general-purpose LLMs in both correctness and irregular parallel performance, and on some tasks reaches or exceeds expert implementations.

## Link
- [http://arxiv.org/abs/2603.02510v1](http://arxiv.org/abs/2603.02510v1)
