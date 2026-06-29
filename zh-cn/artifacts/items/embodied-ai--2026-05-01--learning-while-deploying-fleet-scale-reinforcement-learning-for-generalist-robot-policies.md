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
LWD 在部署期间训练一个单一的 VLA 机器人策略，把离线机器人数据和新的车队 rollout 混合起来。它在 16 台双臂机器人和 8 个真实世界操作任务上运行，经过几小时的在线交互后，平均成功率达到 95%。

## 问题
- 离线 VLA 预训练会错过部署后出现的分布偏移、长尾失败、任务变体和人工纠正。
- 纯模仿学习不能把失败的自主试验、部分进展、稀疏奖励和恢复过程当作 RL 信号来用。
- 现有机器人 RL 往往只改进一个短时域或任务特定策略，所以它不能解决共享通用策略的持续后训练。

## 方法
- 从一个预训练的、基于 flow 的 Vision-Language-Action 策略开始，它会根据观测和语言指令输出动作块。
- 将当前检查点部署到共享车队，收集自主 rollout 和可选的人类干预，把这些数据加入在线回放缓冲区，再用离线和在线回放的混合数据重新训练。
- 使用分布式隐式价值学习：先在回放数据的动作价值上拟合一个分布，再用高分位数作为 TD bootstrap 目标，而不是标量 expectile 价值。
- 根据价值分布熵调整分位数水平；当价值分布更分散时，采用更低的乐观程度。
- 用通过伴随匹配的 Q-learning 提取策略，它把 critic 的动作梯度转成 flow 动作生成器的局部训练目标。

## 结果
- 真实世界评估使用 16 台双臂机器人，覆盖 8 个操作任务。
- 任务集合包括语义杂货补货，以及功夫茶、鸡尾酒和果汁等长时域任务，这些长时域任务的执行时间报告为 3–5 分钟。
- 一个单一的通用策略在所有任务上的平均成功率达到 95%。
- 论文说 LWD 比预训练的 VLA 有提升，也以较大幅度超过了相关基线，但摘录没有给出基线成功率。
- 最大的提升出现在长时域任务上，因为稀疏奖励可以通过动态规划在部分进展之间传播。
- 在线改进阶段据称只需要几小时的真实世界交互。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.00416v1](https://arxiv.org/abs/2605.00416v1)
