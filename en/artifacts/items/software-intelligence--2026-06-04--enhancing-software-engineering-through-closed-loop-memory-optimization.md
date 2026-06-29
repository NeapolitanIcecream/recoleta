---
source: arxiv
url: https://arxiv.org/abs/2606.05646v1
published_at: '2026-06-04T03:17:21'
authors:
- Xuehang Guo
- Zora Zhiruo Wang
- Qingyun Wang
- Graham Neubig
- Xingyao Wang
topics:
- software-engineering-agents
- agent-memory
- code-intelligence
- swe-bench
- reinforcement-learning
- llm-finetuning
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Enhancing Software Engineering Through Closed-Loop Memory Optimization

## Summary
MemOp trains a memory model for software-engineering agents by keeping only memories that improve downstream task metrics. The paper claims better SWE-Bench Verified success and efficiency, with lower compute cost.

## Problem
- Software-engineering agents solve each issue as a separate episode, so they rediscover repository structure, repeat bad edits, and spend tokens rebuilding context.
- Existing memory methods lack a task-agnostic utility test, so a stored note may be useful, redundant, or harmful without a clear measurement.
- The problem matters because repository tasks share conventions and failure patterns; reusable memory can raise solve rate and cut agent iterations.

## Approach
- MemOp defines memory utility by downstream effect: run the agent with a candidate memory and compare it with a no-memory baseline across 10 metrics, including success rate, localization accuracy, resolve efficiency, and localization efficiency.
- A memory is accepted when every metric is at least unchanged and at least one metric improves. Failed candidates become rejected examples.
- The system uses trajectory-based rejection sampling on SWE-Bench Verified to build training data; the paper reports 3,200 memory candidates from 10 repositories, 100 task samples, 4 trajectories per task, and 4 memories per trajectory.
- Training has two stages: supervised finetuning on accepted memories, then reinforcement learning with rewards based on measured metric gains over the no-memory baseline.
- Evaluation covers single-episode reuse and cross-episode memory evolution, using Devstral-Small-2507 and Qwen3-Coder-30B-A3B as SE agents with several small memory-model backbones.

## Results
- In single-episode memory augmentation, MemOp reports absolute gains up to +5.25 percentage points in success rate and +4.63 points in resolve efficiency over no-memory baselines.
- In cross-episode memory evolution, it reports gains up to +3.00 points in success rate and +3.17 points in localization accuracy over no-memory baselines.
- Across SE agents and memory-model backbones, the paper reports up to +9.00 points in success rate and +5.24 points in resolve efficiency for Devstral-Small-2507, and up to +6.75 points in success rate and +7.45 points in resolve efficiency for Qwen3-Coder-30B-A3B.
- Compute cost drops by at least 9.79% relative to baselines, according to the paper.
- Finetuned MemOp variants beat Claude-4-Sonnet memory generation by up to +3.25 points in single-episode success rate and +1.75 points in cross-episode success rate.
- With GRPO, DAPO, and GSPO, MemOp reports gains up to +3.50 points in success rate and +4.03 points in localization accuracy.

## Link
- [https://arxiv.org/abs/2606.05646v1](https://arxiv.org/abs/2606.05646v1)
