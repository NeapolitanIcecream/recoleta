---
source: arxiv
url: https://arxiv.org/abs/2605.00416v1
published_at: '2026-05-01T05:20:26'
authors:
- Yi Wang
- Xinchen Li
- Pengwei Xie
- Pu Yang
- Buqing Nie
- Yunuo Cai
- Qinglin Zhang
- Chendi Qu
- Jeffrey Wu
- Jianheng Song
- Xinlin Ren
- Jingshun Huang
- Mingjie Pan
- Siyuan Feng
- Zhi Chen
- Jianlan Luo
topics:
- vision-language-action
- generalist-robot-policy
- fleet-scale-rl
- robot-data-scaling
- offline-to-online-rl
- long-horizon-manipulation
relevance_score: 0.98
run_id: materialize-outputs
language_code: zh-CN
---

# Learning while Deploying: Fleet-Scale Reinforcement Learning for Generalist Robot Policies

## Summary
## 摘要
LWD 在部署期间训练单个 VLA 机器人策略，将离线机器人数据与新的机群 rollout 混合使用。在 16 台双臂机器人和 8 个真实世界操作任务上，论文报告称，经过数小时在线交互后，平均成功率达到 95%。

## 问题
- 离线 VLA 预训练无法覆盖部署后出现的分布偏移、长尾失败、任务变体和人工纠正。
- 纯模仿学习无法把失败的自主尝试、部分进展、稀疏奖励和恢复过程用作 RL 信号。
- 现有机器人 RL 通常只改进一个短时域或任务特定策略，因此不能解决共享通用策略的持续后训练问题。

## 方法
- 从一个预训练的基于流的 Vision-Language-Action 策略开始，该策略根据观测和语言指令输出动作块。
- 将当前 checkpoint 部署到共享机群，收集自主 rollout 和可选的人工干预，将它们加入在线回放缓冲区，并在混合的离线与在线回放数据上重新训练。
- 使用 Distributional Implicit Value Learning：拟合回放动作价值的分布，然后用高分位数作为 TD bootstrap 目标，而不是标量 expectile 价值。
- 根据价值分布熵调整分位数水平；当价值分布较分散时，降低乐观程度。
- 使用 Q-learning via Adjoint Matching 提取策略，该方法把 critic 的动作梯度转换为流式动作生成器的局部训练目标。

## 结果
- 真实世界评估使用 16 台双臂机器人，覆盖 8 个操作任务。
- 任务集包括语义化杂货补货，以及功夫茶、鸡尾酒和果汁等长时域任务；论文报告长时域任务的执行时间为 3–5 分钟。
- 单个通用策略在所有任务上的平均成功率达到 95%。
- 论文称 LWD 优于预训练 VLA，并以较大幅度超过相关基线，但摘录未提供基线成功率。
- 最大提升出现在长时域任务上；在这些任务中，稀疏奖励可以通过动态规划沿部分进展传播。
- 论文报告称，在线改进阶段只需要数小时真实世界交互。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.00416v1](https://arxiv.org/abs/2605.00416v1)
