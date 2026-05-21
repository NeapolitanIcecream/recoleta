---
source: arxiv
url: https://arxiv.org/abs/2605.13139v1
published_at: '2026-05-13T08:05:16'
authors:
- Hao Guan
- Lingyue Fu
- Shao Zhang
- Yaoming Zhu
- Kangning Zhang
- Lin Qiu
- Xunliang Cai
- Xuezhi Cao
- Weiwen Liu
- Weinan Zhang
- Yong Yu
topics:
- code-agents
- software-benchmarks
- issue-resolution
- agent-evaluation
- test-generation
- environment-reconstruction
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# SWE-Cycle: Benchmarking Code Agents across the Complete Issue Resolution Cycle

## Summary
SWE-Cycle is a 489-instance benchmark for testing whether code agents can resolve real GitHub issues end to end: set up the environment, change the code, and write verification tests. Its evaluator, SWE-Judge, combines code review with execution and aligns with human labels on more than 95% of sampled cases.

## Problem
- Existing SWE-bench-style evaluations give agents prebuilt environments and fixed tests, so they miss failures in dependency setup and test design.
- Static parsers and fixed unit-test scripts can reject valid patches, accept shallow test-hacking, and fail on autonomous agent trajectories.
- This matters because a useful coding agent must onboard a raw repository, implement a fix, and verify it without manual setup.

## Approach
- The authors build SWE-Cycle from SWE-bench Verified, SWE-bench Pro, and SWE-bench Multilingual, reducing 1,531 initial instances to 489 after contamination, complexity, and test-reliability filters.
- Each instance has three isolated tasks: Environment Reconstruction, Code Implementation, and Verification Test Generation.
- The FullCycle task gives the agent only a raw repository and issue description, then asks it to complete all three phases in one autonomous run.
- SWE-Judge scores outputs with static review plus dynamic execution, using 0-2 scores normalized to 0-1.
- In FullCycle evaluation, SWE-Judge checks the environment first, evaluates generated tests, refines poor tests when needed, then tests the submitted implementation.

## Results
- SWE-Judge matches human annotations at 99.3% on Env (N=143), 95.6% on Impl (N=113), 99.5% on TestGen (N=201), and 96.9% on FullCycle (N=489).
- On isolated tasks, the best reported solve rates are 78.12% for Env, 40.08% for Impl, and 67.28% for TestGen, all by Claude-Sonnet-4.6.
- FullCycle solve rates stay below 14% for every model in the excerpt; GLM-5.1 reaches 13.50% and Claude-Sonnet-4.6 reaches 12.27%.
- FullCycle average scores in the excerpt are 81.49 for GLM-5.1 and 80.52 for Claude-Sonnet-4.6, while strict solve rates are much lower, showing that partial progress does not translate into complete issue resolution.
- The benchmark evaluates six LLM-backed agents: GPT-5.4, Claude-Sonnet-4.6, Qwen-3.5, GLM-5.1, Kimi-K2.5, and MiniMax-M2.7.

## Link
- [https://arxiv.org/abs/2605.13139v1](https://arxiv.org/abs/2605.13139v1)
