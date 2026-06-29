---
source: arxiv
url: http://arxiv.org/abs/2604.23073v1
published_at: '2026-04-24T23:57:45'
authors:
- Charles Xu
- Jost Tobias Springenberg
- Michael Equi
- Ali Amin
- Adnan Esmail
- Sergey Levine
- Liyiming Ke
topics:
- vision-language-action
- online-reinforcement-learning
- real-robot-manipulation
- sample-efficient-rl
- dexterous-manipulation
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# RL Token: Bootstrapping Online RL with Vision-Language-Action Models

## Summary
## 摘要
RLT 通过暴露一个紧凑的“RL token”，并在其上训练一个小型 actor-critic，用在线强化学习对预训练的视觉-语言-动作模型进行微调，且在真实机器人上完成。这个方法的目标是在保留 VLA 通用能力的同时，在几分钟到几小时的机器人练习内提升任务特定的精度和速度。

## 问题
- 预训练的 VLA 模型可以完成许多操作任务，但在精细执行的最后一毫米经常失败，小误差、停顿和重试会导致变慢或失败。
- 对大型 VLA 模型做完整的 RL 微调成本太高，而且样本效率太低，不适合真实世界的机器人训练，因为可用交互时间可能只有几小时。
- 小型真实世界 RL 策略可以快速适应，但通常会放弃 VLA 强大的视觉和行为先验。

## 方法
- 论文给冻结的预训练 VLA 加了一个 **RL token**。这个 token 是一个紧凑向量，通过学习重建 VLA 的内部嵌入来得到，因此它把与任务相关的信息保留在一个适合 RL 的小状态表示里。
- 在少量针对任务的示范适配之后，VLA 和 RL-token 模块都被冻结。在线学习只更新一个轻量级 actor 和 critic。
- actor 不会从头规划动作。它接收 RL token、机器人本体感知，以及从 VLA 采样得到的一个 **参考动作块**，然后学习如何调整这个动作块。
- critic 使用分块动作和稀疏二元成功标签进行离策略训练，这比单步控制缩短了决策时域。
- 一个正则项让 actor 保持接近 VLA 动作，**参考动作 dropout** 则防止 actor 只复制 VLA 而不学习。

## 结果
- 在 **四个真实机器人精细任务** 上，**螺丝安装、扎带固定、充电器插入和以太网插入**，该方法在 **几分钟到几小时** 的在线练习后同时提升了成功率和执行速度。
- 在最难的任务阶段，RLT 的执行速度最高提升了 **3 倍**。
- 在一个有挑战的 **螺丝插入** 设置中，成功率从 **20% 提高到 65%**。
- 论文声称，在最需要灵巧操作的任务片段之一上，学到的策略可以在保持可靠性的同时 **超过专家人工遥操作的速度**。
- 摘要没有给出每个任务的完整指标表、数据集规模，或更细的逐基线数值。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.23073v1](http://arxiv.org/abs/2604.23073v1)
