---
source: arxiv
url: http://arxiv.org/abs/2604.05013v1
published_at: '2026-04-06T16:36:21'
authors:
- Yingwei Ma
- Yue Liu
- Xinlong Yang
- Yanhao Li
- Kelin Fu
- Yibo Miao
- Yuchong Xie
- Zhexu Wang
- Shing-Chi Cheung
topics:
- coding-agents
- reinforcement-learning
- software-engineering
- code-intelligence
- generalization
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# Scaling Coding Agents via Atomic Skills

## Summary
This paper argues that coding agents generalize better when trained on a small set of reusable software engineering skills instead of end-to-end task benchmarks. It defines five atomic skills and trains one shared agent with joint reinforcement learning across all of them.

## Problem
- Current coding agents are often trained on composite tasks such as bug fixing, and the paper claims this leads to task-specific overfitting and weak transfer to other software engineering tasks.
- Composite tasks are hard to scale with RL because the task space is broad and reward design for each new task is costly and inconsistent.
- The authors want a training target that is easier to evaluate, reusable across workflows, and more likely to transfer to unseen tasks.

## Approach
- The paper defines five atomic skills: code localization, code editing, unit-test generation, issue reproduction, and code review.
- Each skill has a concrete input-output format and an execution-based reward: exact file-match for localization, all-tests-pass for editing, bug-detecting tests for unit-test generation, correct binary judgment for review, and pre-patch fail plus post-patch pass for issue reproduction.
- A single shared policy is initialized with light SFT on 1,500 verified trajectories, 300 per skill, using GLM-4.5-Air-Base as the starting model.
- The agent is then trained with joint RL over a unified task buffer, using GRPO to compare multiple sampled outputs for the same input and reduce reward-scale mismatch across skills.
- Training runs in sandboxed environments with only bash and str_replace tools, 10,000+ concurrent sandboxes, and 25,000+ pre-built Docker images.

## Results
- The main claim is an average **18.7%** performance gain across **10 tasks**: **5 atomic skills** and **5 composite tasks**.
- On atomic skills (Avg@3), the SFT+RL model improves over SFT on all five skills: code localization **0.665 -> 0.712**, code editing **0.458 -> 0.611**, issue reproduction **0.542 -> 0.605**, unit-test generation **0.359 -> 0.472**, and code review **0.563 -> 0.622**.
- On unseen composite tasks (Avg@3), SFT+RL improves over SFT on all five benchmarks: SWE-bench Verified **0.507 -> 0.585**, SWE-bench Multilingual **0.300 -> 0.389**, Terminal-Bench 2.0 **0.151 -> 0.182**, Code Refactoring **0.146 -> 0.171**, and SEC-Bench **0.136 -> 0.169**.
- Averaged over all reported tasks, joint RL reaches **0.452 Avg@3** versus **0.383** for the SFT model and **0.416** for GLM-4.5-Air.
- Against GLM-4.5-Air on atomic skills, the joint RL model is higher on localization **0.712 vs 0.666**, editing **0.611 vs 0.556**, issue reproduction **0.605 vs 0.555**, unit-test generation **0.472 vs 0.423**, and review **0.622 vs 0.536**.
- On composite benchmarks versus GLM-4.5-Air, the joint RL model is higher on SWE-bench Verified **0.585 vs 0.559**, SWE-bench Multilingual **0.389 vs 0.358**, Code Refactoring **0.171 vs 0.159**, and SEC-Bench **0.169 vs 0.163**, but lower on Terminal-Bench 2.0 **0.182 vs 0.187**.

## Link
- [http://arxiv.org/abs/2604.05013v1](http://arxiv.org/abs/2604.05013v1)
