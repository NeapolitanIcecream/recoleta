---
source: arxiv
url: https://arxiv.org/abs/2607.18711v1
published_at: '2026-07-21T05:07:22'
authors:
- Ruogu Yang
- Yifeng He
- Yundi Xu
- Yuqing Wei
- Hao Chen
topics:
- code-intelligence
- automated-software-testing
- llm-test-generation
- functional-bug-detection
- program-invariants
- software-foundation-model
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# LLM-Based Invariant Testing for Software Functional Bugs

## Summary
LISA is an LLM-based invariant-testing framework for detecting functional bugs in C/C++ software libraries that do not necessarily cause crashes. It separates API-sequence exploration from documentation-grounded invariant generation, producing executable tests and high-confidence bug candidates for developer confirmation.

## Problem
- Manual unit tests require developers to specify API inputs, expected outputs, and call sequences, which is costly and requires detailed knowledge of API semantics.
- Conventional fuzzing mainly detects crashes and hangs, so it often misses functional bugs that return incorrect results without abnormal termination.
- Existing LLM test generators can produce unreliable input-output assertions, creating an oracle problem: a failed test may reflect a wrong generated oracle rather than a library bug.

## Approach
- LISA extracts API and type information with Clang, then uses an LLM to generate executable API-call sequences under library rules, examples, and lifecycle constraints.
- It iteratively repairs invalid sequences and uses API 3-gram feedback with adaptive energy condensation to balance exploration of new API combinations with reuse of successful patterns.
- It partitions validated sequences into semantically coherent chunks and asks a stronger LLM to insert invariants at chunk boundaries, using API documentation, mined contracts, and observed reference behavior.
- The invariants check properties such as state validity, value ranges, conservation relations, and documented semantic contracts; violations are reported as high-confidence candidates rather than proven bugs.

## Results
- On 7 real-world C/C++ libraries, LISA-generated tests achieve higher average library-level branch coverage than OSS-Fuzz, according to the paper; the excerpt does not provide the aggregate coverage values.
- On re-introduced historical functional bugs, LISA detects 9 more bugs than CITYWALK, the compared state-of-the-art LLM-based unit-testing framework.
- On zlib under a 3-hour budget, API 3-gram feedback with order N=3 produced 818 valid programs, 73.01% line coverage, and 60.01% branch coverage; N=2 produced 512 valid programs and 59.22% branch coverage, while N=4 produced 705 valid programs and 57.02% branch coverage.
- The reported evidence supports improved functional-bug detection and competitive coverage, but invariant soundness is not formally proved and every reported candidate requires developer confirmation.

## Link
- [https://arxiv.org/abs/2607.18711v1](https://arxiv.org/abs/2607.18711v1)
