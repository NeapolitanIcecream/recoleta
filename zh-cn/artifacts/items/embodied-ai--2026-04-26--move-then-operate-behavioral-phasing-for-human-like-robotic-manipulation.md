---
source: arxiv
url: http://arxiv.org/abs/2604.23620v1
published_at: '2026-04-26T09:28:10'
authors:
- Haoming Xu
- Lei Lei
- Jie Gu
- Chu Tang
- Jingmin Chen
- Ruiqi Wang
topics:
- vision-language-action
- robot-manipulation
- mixture-of-experts
- data-efficiency
- contact-rich-manipulation
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Move-Then-Operate: Behavioral Phasing for Human-Like Robotic Manipulation

## Summary
## 总结
Move-Then-Operate 是一种视觉-语言-动作策略，把机器人操作拆成两个阶段：先移动到目标附近，再做精细的接触操作。在 RoboTwin2 上，这种分阶段设计明显优于单一的 pi_0 策略，并且用更少的数据和更少的训练步骤就能达到很强的结果。

## 问题
- 标准的 VLA 操作策略用同一个策略同时学习粗略接近和精细接触控制，但这两类行为的动作尺度和动力学不同。
- 论文认为，move 段在数据和梯度中占主导，这会让模型更难学到更小、但对任务成败关键的 operate 动作。
- 这对高精度操作很重要，因为失败往往发生在最后的接触阶段，这时微小的动作误差就会破坏任务。

## 方法
- 该方法引入一个双专家策略：一个专家负责 **move**，另一个负责 **operate**。一个轻量路由器为每个动作块选择一个专家。
- 两个专家都用 Conditional Flow Matching 生成动作，但参数分开，因此粗运动和精细操作不会共享同一个低层动作头。
- 训练时，路由器用阶段标签进行监督，每个样本只更新匹配的专家。这样梯度更新就保持了阶段特异性。
- 阶段标签通过一个基于 MLLM 的分段流水线自动生成，使用视频、语言指令、子任务分解以及末端执行器速度等信号。
- 模型基于预训练的 pi_0-base 主干构建，为两个专家和共享的视觉-语言主干分别设置了 LoRA 适配器。

## 结果
- 在 8 个 RoboTwin2 任务上、每个任务 **50 个示范** 且训练步数相同的条件下，该方法达到 **68.88% 的平均成功率**，而 **pi_0** 为 **44.75%**，**RDT** 为 **35.63%**，**ACT** 为 **31.63%**。这比 pi_0 高 **24.13 个百分点**。
- 相比 **pi_0** 的单任务提升包括：**Click Alarmclock 88% 对 63%（+25）**、**Click Bell 99% 对 44%（+55）**、**Move Pillbottle pad 37% 对 21%（+16）**、**Place Bread Basket 34% 对 17%（+17）**、**Place Cans Plasticbox 79% 对 34%（+45）**、**Place Empty Cup 55% 对 37%（+18）**、**Place Burger Fries 89% 对 80%（+9）**、**Press Stapler 70% 对 62%（+8）**。
- 与使用 **10 倍更多数据** 训练的数据充足基线相比，该方法在多个任务上有竞争力：**Click Bell 99%**，而 **pi_0.5*** 为 **75%**、**GO-1*** 为 **98%**；**Press Stapler 93%**，而另外两者分别为 **80%** 和 **66%**。
- 摘要称，这个模型只用标准完整训练预算的 **40% 更少训练步数** 就达到峰值性能。
- 这段摘录给出了基准成功率和部分基线对比的具体数字，但没有给出 10 倍数据对比表的完整总体平均值，也没有给出训练效率曲线的详细数值。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.23620v1](http://arxiv.org/abs/2604.23620v1)
