---
source: arxiv
url: https://arxiv.org/abs/2607.19653v1
published_at: '2026-07-22T01:19:42'
authors:
- Ryan Deng
- Yuanzhe Liu
- Bastian Lipka
- Yao Ma
- Xuhao Chen
- Tim Kaler
- Jatin Ganhotra
topics:
- code-intelligence
- automated-software-production
- repository-optimization
- software-agents
- profiler-guided-optimization
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# PerfAgent: Profiler-Guided Iterative Refinement for Repository-Level Code Optimization

## Summary
PerfAgent improves repository-level code optimization by giving coding agents profiler summaries, iterative speedup feedback, and targeted correctness checks. On GSO and SWE-fficiency-Lite, it more than doubles the rate of patches matching expert performance compared with OpenHands using GPT-5.1.

## Problem
- General-purpose coding agents often optimize visible Python code while missing bottlenecks across abstraction layers or inside native extensions.
- They may stop after the first passing patch and test too narrowly, producing modest speedups or correctness regressions.
- The problem matters because repository-level optimization requires preserving behavior while approaching expert performance, not merely passing tests.

## Approach
- PerfAgent uses the low-overhead `py-spy` sampling profiler to identify hotspots in Python and native code, then converts raw samples into a concise summary containing locations, call context, self-time, total-time, and runtime share.
- An objective-driven controller intercepts the agent's stop signal, rebuilds and validates each patch, re-profiles the workload, and asks the agent to continue for up to 5 iterations.
- A best-patch selector retains the fastest correct patch rather than the last submitted patch.
- Selective validation with `pytest-testmon` runs tests affected by the changes and returns build or test failures as feedback without requiring the full repository test suite.

## Results
- With GPT-5.1, the rate of expert-matching patches increased from 19.6% to 39.2% on GSO and from 26% to 74% on SWE-fficiency-Lite, relative to OpenHands.
- On GSO, the benchmark contains 102 tasks across 10 repositories; average harmonic-mean speedup rose from 2.5x at turn 1 to 6.4x at turn 5, while validation failures fell from 53 to 5 instances.
- PerfAgent reached low-level C, C++, Cython, or Rust code on 48 GSO instances, compared with 31 for OpenHands, including 21 cases where OpenHands changed only Python.
- Selective testing reduced the number of tests run by 66%–99% on GSO and 47%–98% on SWE-fficiency-Lite compared with full-suite testing.
- A traced NumPy string-replacement example reached a 5.87x speedup; the controller retained this fourth-turn patch over a slightly slower 5.85x fifth-turn patch.
- The paper reports that PerfAgent surpassed an oracle best-of-five baseline at substantially lower cost, although the excerpt does not provide the exact cost or score values; results on SWE-fficiency-Lite later in the loop are limited by its $5 per-task budget.

## Link
- [https://arxiv.org/abs/2607.19653v1](https://arxiv.org/abs/2607.19653v1)
