---
source: arxiv
url: https://arxiv.org/abs/2606.20517v1
published_at: '2026-06-18T17:35:57'
authors:
- Maria Ivanova
- Pavel Zadorozhny
- Rodion Levichev
- Ivan Petrov
- Adamenko Pavel
- Ivan Lopatin
- Alexey Kutalev
- Dmitrii Babaev
topics:
- code-generation-benchmark
- multilingual-code
- livecodebench
- llm-evaluation
- pass-at-1
- code-intelligence
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Multi-LCB: Extending LiveCodeBench to Multiple Programming Languages

## Summary
Multi-LCB extends LiveCodeBench code-generation evaluation from Python to 12 programming languages while keeping LCB's release-date filtering and hidden-test protocol. The paper shows that Python scores can give a poor estimate of model performance in other languages.

## Problem
- LiveCodeBench is widely used for code generation, but it only tests Python, so it misses failures in C++, Java, Rust, Go, JavaScript, and other languages used in software work.
- Python-only evaluation can hide Python overfitting and language-specific data leakage.
- Cross-language comparison matters because the same algorithmic task can expose different compiler, type-system, runtime, and syntax failures.

## Approach
- Multi-LCB reuses the LCB code-generation task pool from LeetCode, AtCoder, and Codeforces, including release dates for contamination-aware filtering.
- It evaluates the same tasks in 12 languages: Python, C++, C#, Java, Rust, Go, TypeScript, JavaScript, Ruby, PHP, Kotlin, and Scala.
- AtCoder and Codeforces tasks already use STDIN/STDOUT, so their tests pass directly into the evaluator.
- LeetCode functional tasks are converted into STDIN/STDOUT format, including public examples and hidden tests, so one evaluator can run all languages.
- Models receive zero-shot prompts that specify the target language, then generated programs are compiled or interpreted in sandboxed containers and scored with Pass@1.

## Results
- The study evaluates 24 LLMs ranging from 7B to 685B parameters across 12 languages, using Pass@1 averaged over 10 runs.
- GPT-OSS-120B (Medium) has the best reported average in the excerpt: 67.8 ± 5.9 Pass@1 across 12 languages, with 71.1 ± 2.1 in Python, 72.3 ± 1.9 in C++, 70.4 ± 3.0 in Java, and 54.1 ± 3.0 in Scala.
- Qwen3-235B-A22B-Thinking-2507 scores higher than GPT-OSS-120B (Medium) on Python and C++ at 74.0 ± 3.7 and 75.8 ± 2.4, but its average is 64.0 ± 9.4 because it drops to 47.7 ± 2.8 in Rust, 49.4 ± 3.2 in Ruby, and 56.7 ± 2.0 in Go.
- DeepSeek-R1-0528 reports 63.1 ± 3.8 average Pass@1, with 66.3 ± 2.0 in Python, 68.0 ± 1.6 in C++, 67.8 ± 1.8 in Java, and 55.0 ± 3.0 in Go.
- OpenReasoning-Nemotron-32B shows a large Python-to-other-language gap: 64.4 ± 3.6 in Python, 44.2 ± 5.2 in C++, 11.5 ± 4.2 in Go, 10.8 ± 6.9 in JavaScript, 2.8 ± 1.5 in Rust, and 22.7 ± 18.5 average.
- The authors manually inspected about 500 tasks and report no language-dependent inconsistencies in the converted tasks; they also claim evidence of language-specific contamination, but the excerpt does not give a contamination-rate metric.

## Link
- [https://arxiv.org/abs/2606.20517v1](https://arxiv.org/abs/2606.20517v1)
