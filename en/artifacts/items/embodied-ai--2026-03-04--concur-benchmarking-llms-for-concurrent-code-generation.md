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
- concurrency
- benchmark
- model-checking
- java
- evaluation
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# CONCUR: Benchmarking LLMs for Concurrent Code Generation

## Summary
CONCUR is a benchmark specifically designed to evaluate large language models’ ability to generate concurrent code, rather than only sequential code as in prior work. It elevates correctness evaluation for concurrent programs from surface similarity or ordinary unit tests to stricter verification based on model checking.

## Problem
- Existing code generation benchmarks mainly target sequential programs and cannot effectively measure LLMs’ ability to generate concurrent code.
- Concurrent programs are more complex and contain errors absent from sequential programs, such as deadlocks, race conditions, and starvation; ordinary unit tests struggle to systematically cover nondeterministic thread interleavings.
- Therefore, without a dedicated concurrency benchmark, LLMs’ code generation ability in real software engineering scenarios may be overestimated.

## Approach
- Build **CONCUR**: it includes **43** base problems drawn from a standard concurrency textbook, and based on a subset of them, **72** mutant variants were generated and manually validated, for a total of **115** problem instances.
- Each task is paired with a structured prompt, an executable Java 8 reference implementation, and uniform constraints (single file, no third-party libraries, must include `main`, and limits on thread count and iteration count).
- The evaluation process has two steps: first compile in a **Java 8** environment, then use **Java Pathfinder (JPF)** for model checking to systematically enumerate thread interleavings and detect concurrency bugs.
- The framework uses listeners to identify multiple error types, including **Deadlock, Race Condition, Starvation, Uncaught Exception, No Entry Method, Single Thread, Termination Error**.
- To control state explosion, the authors adopt a dual bounded strategy: at the task design level, they limit threads/iterations; at the verification level, they set `search.depth_limit` to **10x** the maximum execution depth of the reference solution and apply a uniform timeout (**9000 ms** in the example configuration).

## Results
- In terms of benchmark scale, CONCUR provides **115** concurrent code generation tasks, including **43** base problems and **72** manually validated mutants, explicitly covering multiple concurrency mechanisms such as locks, semaphores, atomic classes, blocking queues, and thread pools.
- In terms of evaluation scope, the authors used CONCUR to test **23** current mainstream LLMs (including closed-source APIs and open-source models), and pointed out clear limitations in these models’ concurrent code generation abilities.
- In terms of automated verification quality, the paper claims that its JPF-based error detection framework achieved **92% precision** under manual review.
- Methodologically, the authors explicitly state that the commonly used code evaluation metric **CodeBLEU** cannot reliably reflect concurrent program correctness; the excerpt does not provide finer-grained correlation coefficients or specific numerical comparisons.
- The excerpt does not provide complete pass rates for each model on CONCUR, distributions by error type, or quantitative head-to-head numbers versus existing benchmarks; the strongest quantitative claims are mainly the **115-task scale, 23 models, 92% precision, and a depth limit of 10x the reference solution**.

## Link
- [http://arxiv.org/abs/2603.03683v1](http://arxiv.org/abs/2603.03683v1)
