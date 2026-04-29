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
RLT 通过暴露一个紧凑的“RL token”并在其上训练一个小型 actor-critic，用在线强化学习在真实机器人上微调预训练的视觉-语言-动作模型。该方法的目标是在保留 VLA 通用技能的同时，用几分钟到几小时的机器人练习提升特定任务的精度和速度。

## 问题
- 预训练 VLA 模型能执行许多操作任务，但在精确执行的最后一毫米阶段常常失败，此时微小误差、停顿和重试会导致变慢或失败。
- 对大型 VLA 模型做完整的 RL 微调成本过高，样本效率也太低，不适合真实机器人训练，因为通常只有几小时的交互时间可用。
- 小型真实世界 RL 策略可以快速适应，但通常会丢掉 VLA 强大的视觉和行为先验。

## 方法
- 论文在一个冻结的预训练 VLA 中加入一个 **RL token**。这个 token 是一个紧凑向量，通过学习重建 VLA 的内部嵌入来保留任务相关信息，作为 RL 的小型状态表示。
- 在少量任务特定的演示适配之后，VLA 和 RL-token 模块都会被冻结。在线学习只更新一个轻量级的 actor 和 critic。
- actor 不从零开始规划动作。它接收 RL token、机器人的本体感觉信息，以及一个从 VLA 采样得到的 **reference action chunk**，然后学习如何调整这个动作块。
- critic 在分块动作上用稀疏的二元成功标签进行离策略训练，相比单步控制缩短了决策时域。
- 一个正则项让 actor 保持接近 VLA 动作，**reference action dropout** 则防止 actor 只复制 VLA 而不学习。

## 结果
- 在 **四个真实机器人精密任务**——**螺丝安装、扎带紧固、充电器插入和以太网线插入**——上，该方法经过 **几分钟到几小时** 的在线练习后，同时提升了成功率和执行速度。
- 在任务中最难的阶段，RLT 将执行速度提升了 **最高 3×**。
- 在一个有挑战性的 **螺丝插入** 设置中，成功率从 **20% 提升到 65%**。
- 论文称，在一个对灵巧性要求最高的任务片段上，学到的策略在保持可靠性的同时，速度可以 **超过专家人工遥操作**。
- 这段摘录没有提供完整的各任务指标表、数据集规模，或除上述示例之外更详细的逐个基线对比数字。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.23073v1](http://arxiv.org/abs/2604.23073v1)
