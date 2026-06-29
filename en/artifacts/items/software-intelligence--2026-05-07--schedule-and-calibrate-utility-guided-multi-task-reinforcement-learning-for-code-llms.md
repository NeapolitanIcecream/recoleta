---
source: arxiv
url: https://arxiv.org/abs/2605.06111v1
published_at: '2026-05-07T12:24:53'
authors:
- Yujia Chen
- Yang Ye
- Xiao Chu
- Yuchi Ma
- Cuiyun Gao
topics:
- code-llms
- multi-task-rl
- reinforcement-learning
- code-intelligence
- automated-software-engineering
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Schedule-and-Calibrate: Utility-Guided Multi-Task Reinforcement Learning for Code LLMs

## Summary
ASTOR trains one code LLM with reinforcement learning across four coding tasks by using task utility to choose data and tune KL regularization. The paper claims one shared model beats both task-specific RL specialists and standard multi-task RL baselines on Qwen2.5-Coder-7B and Qwen3-8B.

## Problem
- Code RL specialists work well on their own task, but deploying one model per task raises memory and compute cost as the task count grows.
- A single specialist transfers poorly to other coding tasks, so code understanding, code generation, unit test generation, and commit message generation need better joint training.
- Existing multi-task RL methods use fixed or uniform task mixing and one shared update policy, which misses task difficulty, prompt value, and cross-task gradient effects.

## Approach
- ASTOR defines task utility from two signals: rollout reward variance for learning potential and gradient cosine similarity for cross-task synergy.
- It assigns each task a training quota with a temperature-scaled softmax over utility, then samples prompts inside each task using prompt utility based on reward variance and recent reward progress.
- It builds on GRPO and gives each task its own KL coefficient, with a dynamic multiplier tied to the current task utility.
- The reward setup covers four tasks: Code I/O Prediction, Code Generation, Unit Test Generation, and Commit Message Generation, each with task-specific verifiable or metric-based rewards plus a format reward.
- Experiments use Qwen2.5-Coder-7B and Qwen3-8B, a global batch size of 128, 8 rollouts per sample, 400 training steps, and 32 Ascend 910B-B3 NPUs.

## Results
- On Qwen2.5-Coder-7B, ASTOR reaches an average score of 38.65, beating the best task-specific specialist by 9.0% and Joint Learning by 12.8%.
- On Qwen3-8B, ASTOR reaches an average score of 44.29, beating the best task-specific specialist average of 40.43 by 9.5% and Joint Learning by 7.5%.
- Against multi-task baselines on Qwen2.5-Coder-7B, ASTOR improves over Joint Learning by 12.8%, Curriculum Learning by 16.8%, and Model Merging by 19.2%.
- ASTOR is best on 8 of 10 metrics for Qwen2.5-Coder-7B and all 10 metrics for Qwen3-8B.
- Example Qwen3-8B task results: CRUXEval Input/Output accuracy 61.5/65.1, Aider-Polyglot pass@1/pass@2 51.1/54.8, Defects4J line/branch coverage 38.1/32.0 with 56.6 compile rate, and MCMDEval+ BLEU/ROUGE/METEOR 41.2/22.5/20.0.
- Ablations show both scheduling and KL calibration matter: for Qwen2.5-Coder-7B, removing task and prompt scheduling drops results such as Code Gen pass@1 from 41.5 to 31.9 and MCMDEval+ METEOR from 20.2 to 16.6.

## Link
- [https://arxiv.org/abs/2605.06111v1](https://arxiv.org/abs/2605.06111v1)
