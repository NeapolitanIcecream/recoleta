---
source: arxiv
url: https://arxiv.org/abs/2606.03108v1
published_at: '2026-06-02T03:47:48'
authors:
- Guhong Chen
- Yingcheng Shi
- Yongbin Li
- Binhua Li
- Xander Xu
- Hu Wei
- Shiwen Ni
- Min Yang
- Jieping Ye
topics:
- agentic-rl
- code-intelligence
- software-engineering-agents
- autonomous-training
- llm-reinforcement-learning
- diagnostic-harness
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# EvoTrainer: Co-Evolving LLM Policies and Training Harnesses for Autonomous Agentic Reinforcement Learning

## Summary
EvoTrainer trains LLM agents by evolving both the policy and the diagnostic code that decides what to try next. It reports the largest gain on repository-level SWE, where SWE-9B reaches 38.16 Avg@8 BC% versus 33.77 for a human-engineered RL setup.

## Problem
- Agentic RL runs can fail in ways a scalar score hides: reward leakage, zero-variance rollout groups, behavior collapse, or misleading high scores.
- Fixed training diagnostics make it hard to decide whether to promote, prune, or revise a training branch as bottlenecks change across versions.
- This matters for code and SWE agents because long tool-use trajectories need evidence about search, edit, test, and reward behavior; final pass rates alone are too coarse.

## Approach
- EvoTrainer keeps versioned policy branches and applies mostly single-factor interventions to rewards, data filters, rollout settings, optimizer choices, or tool-use behavior.
- A trainer agent, implemented with Claude Sonnet 4.6 in the experiments, reads metrics, rollouts, configs, logs, and code diffs, then proposes keep, prune, revert, or merge decisions.
- The diagnostic harness changes over time by adding metrics, analyzers, backtests, search procedures, and external evidence when current evidence cannot explain outcomes.
- Persistent memory stores version lineage, failed cases, reusable analyzer skills, and search traces so later domains can reuse tested fixes.
- The SWE instantiation uses GRPO-style training with group-relative advantages, asymmetric Clip-Higher bounds, weak KL regularization, behavior-sensitive rewards, and variance-aware group filtering.

## Results
- Main table: EvoTrainer is the top row in every reported column. Versus no-RL, it reaches SWE-4B 31.49 vs 24.68 Avg@8 BC% (+6.81), SWE-9B 38.16 vs 30.19 (+7.97), AIME 2024 84.17 vs 77.50 (+6.67), AIME 2025 73.33 vs 67.50 (+5.83), CNMO 2024 81.94 vs 75.00 (+6.94), and Coding 51.29 vs 46.71 (+4.58).
- Against human-engineered RL, EvoTrainer improves SWE-9B by +4.39 BC%: 38.16 vs 33.77, with 95% CI [+2.61, +6.34] and p<0.001.
- Against human-engineered RL on Math, the paper reports +2.88 aggregate Avg@8 with p<0.001; it matches the human reference within bootstrap CI on SWE-4B and Coding, with p>0.1.
- Against AutoResearch, EvoTrainer is higher in all shown settings: SWE-4B 31.49 vs 28.41, SWE-9B 38.16 vs 33.33, AIME 2024 84.17 vs 78.33, AIME 2025 73.33 vs 70.42, CNMO 2024 81.94 vs 78.47, and Coding 51.29 vs 45.51.
- It also beats the strongest algorithmic baseline, RAGEN v2 SNR Filtering, in every table column, including SWE-9B 38.16 vs 35.74 and Coding 51.29 vs 49.86.
- The evaluation uses one random seed, seed 42, and Avg@8, so the strongest support comes from paired tests and reported confidence intervals, with less evidence about run-to-run training stability.

## Link
- [https://arxiv.org/abs/2606.03108v1](https://arxiv.org/abs/2606.03108v1)
