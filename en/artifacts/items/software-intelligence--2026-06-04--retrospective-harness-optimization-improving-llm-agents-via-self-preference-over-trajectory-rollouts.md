---
source: arxiv
url: https://arxiv.org/abs/2606.05922v1
published_at: '2026-06-04T09:26:00'
authors:
- Wenbo Pan
- Shujie Liu
- Chin-Yew Lin
- Jingying Zeng
- Xianfeng Tang
- Xiangyang Zhou
- Yan Lu
- Xiaohua Jia
topics:
- llm-agents
- harness-optimization
- self-improvement
- software-engineering-agents
- trajectory-learning
- code-intelligence
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Retrospective Harness Optimization: Improving LLM Agents via Self-Preference over Trajectory Rollouts

## Summary
RHO improves an LLM agent harness from past trajectories without labeled validation data. It selects hard varied tasks, reruns them, asks the agent to compare its own rollouts, and keeps the best proposed harness update.

## Problem
- LLM agents depend on a harness of prompts, skills, workflows, and tools, and that harness needs updates after deployment.
- Many harness optimization methods need labeled validation sets, which are hard to collect for future task distributions.
- Past trajectories contain failures and useful behavior traces, but simple memory accumulation gives smaller and less consistent gains.

## Approach
- RHO first scores past trajectories for difficulty, embeds their failure descriptions, and uses a DPP coreset selector to choose 10 hard and varied tasks in the experiments.
- It reruns each selected task multiple times, with group size G=3 in the reported setup.
- The agent inspects each rollout for mistakes through self-validation, then compares rollouts for disagreement through self-consistency.
- Those diagnoses become instructions for generating candidate harnesses that can add skills, instructions, and executable tools.
- RHO samples N=3 candidate harnesses and chooses the one whose new rollouts are preferred over the baseline rollouts by pairwise self-preference.

## Results
- On SWE-Bench Pro, RHO raises held-out pass rate from 0.59 for Vanilla Codex to 0.78, an absolute gain of +0.19, with no external grading.
- On Terminal-Bench 2, pass rate rises from 0.71 to 0.76, a +0.05 gain.
- On GAIA-2, pass rate rises from 0.29 to 0.37, a +0.08 gain.
- RHO beats feedback-free baselines in the reported table: Dynamic Cheatsheet reaches 0.62/0.73/0.30, ReasoningBank reaches 0.61/0.73/0.28, and Sleep-time Compute reaches 0.64/0.73/0.32 on SWE-Bench Pro, Terminal-Bench 2, and GAIA-2.
- Against Meta-Harness on SWE-Bench Pro, RHO gets 0.78 with 103 optimization-time agent calls and no validation labels; Meta-Harness gets 0.62 in 1 round with labels and 41 calls, and 0.80 in 10 rounds with labels and 320 calls.
- The ablation excerpt reports full diagnosis at 0.78/0.76/0.37; removing self-consistency drops to 0.56/0.75/0.27, removing self-validation drops to 0.70/0.73/0.30, and using raw trajectories gives 0.60/0.75/0.29.

## Link
- [https://arxiv.org/abs/2606.05922v1](https://arxiv.org/abs/2606.05922v1)
