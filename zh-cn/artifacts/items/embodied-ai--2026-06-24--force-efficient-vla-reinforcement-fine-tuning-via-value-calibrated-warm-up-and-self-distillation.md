---
source: arxiv
url: https://arxiv.org/abs/2606.26006v1
published_at: '2026-06-24T16:23:18'
authors:
- Shuyi Zhang
- Yunfan Lou
- Hongyang Cheng
- Yichen Guo
- Chuyao Fu
- Yaoxu Lyu
- Xiaojie Zhang
- Haoran Li
- Pengwei Wang
- Zhongyuan Wang
- Shanghang Zhang
topics:
- vision-language-action
- robot-rl-finetuning
- offline-to-online-rl
- value-guided-distillation
- robot-manipulation
- sample-efficiency
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# FORCE: Efficient VLA Reinforcement Fine-Tuning via Value-Calibrated Warm-up and Self-Distillation

## Summary
## 摘要
FORCE 是一种用于 VLA 机器人策略的三阶段 RL 微调方法，目标是在无需人工干预的情况下超过模仿学习。它处理离线到在线机器人学习中的样本效率问题和训练早期崩溃问题。

## 问题
- 通过模仿训练的 VLA 策略可能继承演示中的较弱或不一致动作，部署后任务成功率会受限。
- 直接在机器人上进行 RL 微调可能浪费样本，因为在线 rollout 开始时 critic 校准不佳，导致早期性能下降。
- 在线探索会产生许多低价值动作，以往的真实机器人方法常用人工纠正来保证训练安全且有效。

## 方法
- FORCE 先在专家演示上使用离线 Cal-QL，训练保守 critic 和带行为正则化的 actor。
- 随后进行 value-calibrated warm-up：当前策略收集一小批 on-policy rollout，在更新 actor 前，先用混合的离线数据和 rollout 数据更新 critic。
- 在线微调期间，它保留一个专家缓冲区和一个策略缓冲区，并从两者采样，使策略在从新 rollout 学习的同时保留有用的演示行为。
- 它的 Value-Guided Policy Self-Distillation 会采样候选动作，用 critic 打分，保留高于状态级平均 Q 基线的动作，并训练策略趋向这些更高价值动作。
- 该方法使用 one-step consistency policy actor，以降低 diffusion 或 flow 风格动作生成的成本，并让 Q 引导的更新更容易应用。

## 结果
- 在 ManiSkill 仿真的 6 个任务中，使用 Octo backbone 的 FORCE 达到 82.3% 的平均成功率；相比之下，无 human-in-the-loop 的 ConRFT 为 71.1%，PA-RL 为 50.2%，Cal-QL 为 45.2%，Octo 行为克隆为 3.58%。
- 使用 pi0 backbone 时，FORCE 在相同 ManiSkill 任务上的平均成功率达到 86.9%，其中 PullCube 和 PushCube 为 100%，PlaceSphere 为 97.5%，PickCube 为 94.1%。
- 论文称，成功率绝对提升 79 个百分点，相比以往 RL 方法提升 10 个百分点，训练速度提高 32.5%。
- 在 6 个真实世界 Franka 任务上，平均成功率从行为克隆的 45.0% 提高到 FORCE 在线微调后的 98.3%。
- 真实世界平均执行步数从行为克隆的 112.8 降至 FORCE 微调后的 38.9；任务结果包括 Open Drawer 成功率从 35% 到 100%，Insert USB 从 75% 到 100%，Stack Cube 从 40% 到 100%。
- 报告中的真实世界训练在在线微调期间未使用人工干预。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.26006v1](https://arxiv.org/abs/2606.26006v1)
