---
source: arxiv
url: http://arxiv.org/abs/2603.03683v1
published_at: '2026-03-04T03:22:26'
authors:
- Jue Huang
- Tarek Mahmud
- Corina Pasareanu
- Guowei Yang
topics:
- llm-code-generation
- concurrent-programming
- benchmarking
- model-checking
- code-evaluation
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# CONCUR: Benchmarking LLMs for Concurrent Code Generation

## Summary
CONCUR is a benchmark and validation framework specifically designed to evaluate large language models' ability to generate concurrent code, filling the gap left by existing code generation benchmarks that mainly target sequential programs. It combines a dataset of concurrency problems with model-checking-based automatic assessment to more rigorously detect errors such as deadlocks, race conditions, and solutions that "appear concurrent but are actually single-threaded."

## Problem
- Existing code generation benchmarks mostly evaluate **sequential code**, and cannot effectively measure LLMs' ability to generate **concurrent programs**.
- Concurrent code is more difficult because it can exhibit errors that do not exist in sequential programs, such as **deadlock, race condition, starvation**, and traditional static similarity metrics or unit tests struggle to cover different thread interleavings.
- Without a dedicated benchmark, it is impossible to truly understand the upper bounds and shortcomings of LLMs in generating concurrent code for software engineering, which is important for code intelligence and automated software production.

## Approach
- Build the **CONCUR** dataset: **43** foundational concurrency problems were compiled from a classic concurrency textbook, and **72** manually validated mutant variants were added, for a total of **115** tasks, each paired with a structured prompt and a Java ground-truth implementation.
- Use **structured prompts** to constrain output to a single Java 8 file, limit the number of threads and iterations, and prohibit third-party libraries, thereby ensuring compilability and suitability for formal verification.
- Use **Java Pathfinder (JPF)** for model checking instead of relying only on unit tests: systematically explore bounded thread interleavings and detect issues such as **deadlock, race condition, starvation, uncaught exception**.
- Add custom listeners and rules to map errors to fixed labels, including **No Entry Method**, **Single Thread**, **Termination Error**, etc., with special handling to identify pseudo-concurrent solutions that use concurrency libraries but do not actually create concurrent execution.
- Adopt a dual-bounded strategy to ensure scalability: at the problem level, limit threads/iterations; at the verification level, set the JPF depth limit to **10x** the maximum depth of the ground-truth program, and apply a uniform timeout.

## Results
- Benchmark scale: **43** base problems + **72** mutants = **115** concurrent code generation tasks; the authors describe it as the **first** specialized benchmark for LLM concurrent code generation.
- Evaluation scope: experiments were conducted on **23** current LLMs (including closed-source APIs and open-source models), and the paper says the results reveal clear limitations of existing models in concurrent code generation.
- Effectiveness of automatic verification: the JPF-based error detection framework achieved **92% precision** in manual validation, indicating relatively high reliability in automatically discovering concurrency bugs.
- Example verification settings: the JPF configuration uses a **9000 ms** time limit and sets `search.depth_limit` to **10x** the depth of the corresponding ground-truth program; this reflects its "bounded but systematic" concurrency verification strategy.
- The paper explicitly claims that the common code generation metric **CodeBLEU** cannot reliably reflect the correctness of concurrent programs, but the provided passage does not give the corresponding correlation coefficient or numerical comparison for that conclusion.
- The provided text **does not** give the exact pass rates of individual models on CONCUR, per-model rankings, or relative baseline improvement figures; the strongest quantitative claims are mainly the dataset size, the number of evaluated models, and the **92%** manual-validation precision.

## Link
- [http://arxiv.org/abs/2603.03683v1](http://arxiv.org/abs/2603.03683v1)
