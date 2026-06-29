---
source: arxiv
url: https://arxiv.org/abs/2605.29710v1
published_at: '2026-05-28T10:10:19'
authors:
- Sergey Arkhangelskiy
topics:
- vision-language-action
- robot-benchmark
- real-robot-evaluation
- time-to-success
- robot-policy-ranking
- human-relative-throughput
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# PhAIL: A Real-Robot VLA Benchmark and Distributional Methodology

## Summary
PhAIL is a real-robot benchmark and evaluation method for vision-language-action policies. It measures full time-to-success distributions instead of only fixed-time success rates, so close policy comparisons can be tested with fewer rollouts.

## Problem
- Real-robot VLA papers often report binary success at one timeout with N≤25 rollouts per condition, usually without confidence intervals or paired tests.
- Binary success can miss speed, hard failures, and tail behavior, so two policies can look tied or swap order depending on the chosen scalar metric.
- The problem matters because real-robot rollouts are expensive, and weak evaluation can rank generalist robot policies from noise.

## Approach
- PhAIL uses the time-to-success CDF as the main evaluation object: each operation contributes a completion time, and unrecoverable failures are added as T=∞ events.
- It estimates the CDF with Kaplan-Meier survival analysis and reports 95% episode-clustered bootstrap confidence intervals.
- It separates scoring from significance testing. Scoring uses Human-Relative Throughput, the ratio of human-reference RMST to model RMST on the same fixture.
- Significance testing uses a per-object Kolmogorov-Smirnov statistic on the CDFs, then macro-averages across objects.
- The benchmark runs on a Franka FR3 with a Robotiq 2F-85 gripper, external and wrist RGB cameras, four object types, public rollout artifacts, and a reference implementation.

## Results
- The benchmark includes about 995 analyzed episodes, including 396 same-fixture human teleoperation rollouts, across four objects: wooden spoons, towels, scissors, and batteries.
- Four VLAs were evaluated after fine-tuning on the same 449-episode, about 13-hour demonstration set: OpenPI π0.5, NVIDIA GR00T N1.6, ACT, and SmolVLA.
- Human teleoperation reached RMST 10.5 s [10.3, 10.8]. OpenPI reached RMST 77.7 s [69.2, 87.0] and HRT 13.8% [12.2, 15.7]; GR00T reached RMST 77.2 s [69.0, 86.4] and HRT 13.3% [12.0, 15.2].
- ACT reached RMST 100.9 s [85.8, 117.6] and HRT 10.5% [9.2, 13.2]. SmolVLA reached RMST 165.8 s [147.0, 185.6] and HRT 6.4% [5.7, 7.5].
- The best evaluated VLA is about 7× slower than the human reference by RMST ratio, and no inference model exceeds 19% HRT on any single object.
- Macro-averaged KS resolves GR00T vs. ACT at N=25 and OpenPI vs. ACT at N=30 rollouts per model-object cell; OpenPI vs. GR00T remains unresolved. The paper compares this with a binary McNemar baseline needing 600–1500 paired rollouts per cell for a 5 percentage-point paired difference.

## Link
- [https://arxiv.org/abs/2605.29710v1](https://arxiv.org/abs/2605.29710v1)
