---
source: arxiv
url: http://arxiv.org/abs/2604.14820v1
published_at: '2026-04-16T09:41:47'
authors:
- Hao Han
- Jin Xie
- Xuehao Ma
- Weiquan Zhu
- Ziyao Zhang
- ZhiLiang Long
- Hongkai Chen
- Qingwen Ye
topics:
- software-engineering-agents
- process-reward-model
- test-time-scaling
- swe-bench
- long-horizon-reasoning
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# SWE-TRACE: Optimizing Long-Horizon SWE Agents Through Rubric Process Reward Models and Heuristic Test-Time Scaling

## Summary
SWE-TRACE is a training and inference pipeline for software engineering agents that tries to make long bug-fixing trajectories shorter, easier to learn from, and cheaper to run. It combines filtered supervision data, step-level reward signals, and guided search at inference time.

## Problem
- Long-horizon SWE agents waste tokens on redundant exploration, repeated tool calls, and noisy debugging traces, which weakens supervised training.
- Final test pass/fail is a sparse reward for reinforcement learning, so the agent gets little signal about which intermediate actions helped.
- Common test-time scaling methods sample many full trajectories and rerank them, which raises latency and compute cost on repository-level tasks.

## Approach
- Build a large executable training set by screening more than 1,000 GitHub repositories, keeping 77 that can build and run tests, generating about 140K candidate bug instances, and filtering them down to 60K high-quality samples.
- Use test-aware bug synthesis: map tests to relevant functions, inject bugs only in test-linked code regions, and condition generation on the related tests so the issues and fixes stay executable and verifiable.
- Distill shorter supervised trajectories with LLM multi-task cascading: at each step, generate action candidates for modes such as localize, inspect, edit, validate, and summarize, then use an oracle verifier to pick the best next action and compress away redundant steps.
- Train with a rubric-based process reward model that gives dense step-level feedback on progress, patch direction, useful information gain, token cost, and redundant actions, instead of relying only on final execution reward.
- Reuse that process reward model at inference time to score and prune weak action candidates early, and use it to keep a memory buffer of high-value past steps when context grows too long.

## Results
- Test-aware bug synthesis raises benchmark construction success from 35.0% to 50.7% on 25 repositories, with filtered samples increasing from 20,638 to 24,995.
- The data pipeline produces about 140K candidate bug issues across 77 repositories and keeps 60K filtered training instances.
- The paper claims state-of-the-art gains on standard SWE benchmarks, including SWE-bench Verified, and says the method improves both 4B and 30B models while reducing token use and inference latency.
- The provided excerpt does not include the main benchmark tables or exact resolution-rate numbers for SWE-bench Verified, so the core quantitative claim beyond data construction is not available here.

## Link
- [http://arxiv.org/abs/2604.14820v1](http://arxiv.org/abs/2604.14820v1)
