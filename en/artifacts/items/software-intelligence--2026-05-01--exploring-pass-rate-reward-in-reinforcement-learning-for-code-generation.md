---
source: arxiv
url: https://arxiv.org/abs/2605.02944v1
published_at: '2026-05-01T10:26:43'
authors:
- Xin-Ye Li
- Ren-Biao Liu
- Yun-Ji Zhang
- Hui Sun
- Zheng Xie
- Ming Li
topics:
- code-generation
- reinforcement-learning
- unit-test-feedback
- reward-design
- grpo
- rloo
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# Exploring Pass-Rate Reward in Reinforcement Learning for Code Generation

## Summary
This paper tests whether test-case pass-rate rewards improve critic-free RL for code generation. Its main finding is negative: pass-rate rewards give denser feedback, but they do not beat binary pass-all-tests rewards on final pass@k.

## Problem
- RL fine-tuning for code generation often uses a binary unit-test reward: a solution gets reward 1 only if it passes every test.
- Binary rewards can be sparse on hard programming tasks, so many runs use test-case pass rate as a denser reward.
- The paper asks whether denser partial-credit rewards actually improve full-correctness performance, which matters because code generation benchmarks care about passing all tests, not passing some tests.

## Approach
- The authors compare binary reward, raw pass-rate reward, difficulty-reweighted pass-rate reward, and a two-stage pass-rate-to-binary schedule.
- They train DeepSeek-R1-Distill-Qwen-7B, Qwen3-4B, and Qwen2.5-7B-Instruct with critic-free RL methods GRPO and RLOO.
- Training uses 768 update steps, 64 problems per batch, 16 rollouts per problem, learning rate 1e-6, temperature 1.0, no KL regularization, and strict on-policy updates.
- Evaluation uses pass@1, pass@4, pass@8, and pass@16 on LiveCodeBench and LeetCodeDataset test splits.
- The analysis checks reward density and probes whether pass-rate gradients increase the log-probability of a known full-pass solution.

## Results
- On DeepSeek-R1-Distill-Qwen-7B with GRPO, pass-rate reward is only +0.3 points over binary on average pass@1, but is worse at pass@4, pass@8, and pass@16: -0.6, -1.2, and -2.0 points.
- On DeepSeek-R1-Distill-Qwen-7B with RLOO, pass-rate reward trails binary on average pass@1/pass@4/pass@8/pass@16 by -0.2, -0.4, -0.8, and -1.7 points.
- On Qwen3-4B with GRPO, binary reward beats pass-rate reward across all average metrics: pass@1 46.4% vs. 44.2%, pass@16 59.1% vs. 56.8%.
- On Qwen2.5-7B-Instruct with GRPO, pass-rate reward gives no average gain: pass@1 22.8% vs. 22.9% for binary, and pass@16 28.8% vs. 30.5%.
- Task-level training-set outcomes for DeepSeek-R1-Distill-Qwen-7B + GRPO agree on 97% of tasks: 2,650 solved by both rewards, 774 failed by both, and only 97 differ.
- Pass-rate feedback is dense: 77.5% of effective groups contain 3 or more distinct reward values, and 47.2% of samples have intermediate pass-rate values, yet gradient probes on 392 tasks show weak movement toward full-pass solutions when no full-pass rollout is present.

## Link
- [https://arxiv.org/abs/2605.02944v1](https://arxiv.org/abs/2605.02944v1)
