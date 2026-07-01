---
source: arxiv
url: https://arxiv.org/abs/2606.31767v1
published_at: '2026-06-30T14:54:25'
authors:
- Khashayar Etemadi
- Zhendong Su
topics:
- java-performance
- software-benchmarking
- automated-program-repair
- code-agents
- test-generation
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# JETO-Bench: A Reproducible Benchmark for Execution Time Improvement Patches in Java

## Summary
JETO-Bench is a reproducible Java benchmark for execution time improvement patches, built with the JETO-Mine collection and evaluation tool. It targets automated repair and coding-agent evaluation for performance fixes rather than functional bugs.

## Problem
- Existing execution-time patch benchmarks mainly cover Python, C++, or .NET, while Java has fewer reproducible datasets.
- Java timing is hard to measure because JIT compilation, garbage collection, class loading, and JVM warm-up can distort execution-time comparisons.
- Fixed benchmark datasets cannot collect new real-world patches with user-chosen filters, build settings, or statistical thresholds.

## Approach
- JETO-Mine crawls GitHub Java repositories and filters commits or PRs by project activity, Java version, Maven Wrapper use, changed files, and issue links.
- An LLM-based classifier checks whether the linked issue is mainly about execution-time improvement.
- The dynamic phase builds Docker images for original and patched versions, runs a warm-up round, then runs tests repeatedly under the same JVM setup.
- It uses paired one-sided binomial tests to decide whether a patched version is faster under user-set thresholds, with defaults of 30 timed runs, 5% minimum improvement, and p-value 10%.
- The evaluation harness applies generated patches or tests inside the Docker environment, runs project tests, extracts timings, and reports build, test, and speed results.

## Results
- JETO-Mine scanned 3,686 repositories and 1,769,958 commits across 11 years of open-source Java history, up to 2025-11-28.
- JETO-Bench contains 660 identified execution time improvement patches and 91 manually verified executable ETIPs from 174 Java repositories.
- The repository pool had at least 20 stars by default; observed stars ranged from 20 to 93,448, with a median of 53.
- Commit counts per considered repository ranged from 1 to 55,824, with a median of 58.
- OpenHands fixed 14.3% of the manually verified executable tasks, or 13 out of 91.
- The paper reports that open-source Java projects often lack tests that show execution-time improvements, which limits automatic validation and points to a test-generation gap.

## Link
- [https://arxiv.org/abs/2606.31767v1](https://arxiv.org/abs/2606.31767v1)
