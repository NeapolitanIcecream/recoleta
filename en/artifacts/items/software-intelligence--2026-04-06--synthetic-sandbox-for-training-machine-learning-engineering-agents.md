---
source: arxiv
url: http://arxiv.org/abs/2604.04872v1
published_at: '2026-04-06T17:19:29'
authors:
- Yuhang Zhou
- Lizhu Zhang
- Yifan Wu
- Jiayi Liu
- Xiangjun Fan
- Zhuokai Zhao
- Hong Yan
topics:
- machine-learning-agents
- on-policy-rl
- code-execution
- synthetic-data
- ml-engineering
- multi-agent-systems
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Synthetic Sandbox for Training Machine Learning Engineering Agents

## Summary
SandMLE makes on-policy reinforcement learning practical for machine learning engineering agents by replacing slow real MLE tasks with synthetic micro-scale sandboxes that keep the task structure but cut execution time. The paper claims this leads to better MLE performance than supervised fine-tuning and transfers across different agent scaffolds.

## Problem
- Training MLE agents with on-policy RL is expensive because each rollout step may need full data preprocessing, model training, and evaluation on large datasets.
- In standard MLE settings, one code execution averages nearly 200 seconds, while RL needs many multi-step trajectories and grouped samples per update.
- Prior work often falls back to supervised fine-tuning or offline/proxy-reward RL, which reduces exploration and weakens generalization.

## Approach
- The main idea is to generate synthetic MLE tasks with very small datasets, 50 to 200 training samples, so the full pipeline still looks like an MLE task but runs fast enough for trajectory-wise on-policy RL.
- SandMLE uses four LLM roles to build each task: a Data Strategist defines the task structure and hidden rules, an ML Developer generates data and baseline methods, an MLOps Engineer builds the evaluator, and a Technical Writer produces the final task spec.
- The system keeps tasks verifiable by creating a hidden test set, deterministic evaluation code, and milestone thresholds based on baseline methods. It filters out corrupted tasks with an automated sanity check on metric ordering.
- Training uses trajectory-level GRPO in a ReAct-style loop, with dense rewards made of format compliance, successful execution, and milestone-based score thresholds.
- The policy gradient is applied only to the model’s own action and reasoning tokens, while environment outputs are masked; trajectories that exceed time limits are also masked.

## Results
- SandMLE cuts average execution time by more than 13x, from standard problems with code execution around 200 seconds to synthetic tasks under 15 seconds.
- From 60 seed tasks, the pipeline builds 848 synthetic training tasks and 64 held-out synthetic validation tasks.
- On MLE-bench-lite, SandMLE-trained models beat SFT baselines on Qwen3-8B, Qwen3-14B, and Qwen3-30B-A3B, with relative gains in Any Medal rate ranging from 20.3% to 66.9%.
- On MLE-Dojo, the trained policy generalizes to unseen agent scaffolds and improves HumanRank by up to 32.4% relative.
- Evaluation covers 22 unseen MLE-bench-lite tasks from the Easy split and 62 MLE-Dojo tasks.
- The excerpt does not provide full per-model absolute scores, full baseline tables, or training cost totals.

## Link
- [http://arxiv.org/abs/2604.04872v1](http://arxiv.org/abs/2604.04872v1)
