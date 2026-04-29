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
## 概要
Move-Then-Operate 是一种视觉-语言-动作策略，把机器人操作分成两个阶段：先移动到目标附近，再执行需要精确接触的操作。在 RoboTwin2 上，这种分阶段设计比单体的 pi_0 策略高出一大截，并且用更少的数据和更少的训练步数就取得了很强的结果。

## 问题
- 标准的 VLA 操作策略用一个策略同时学习粗略到达和精细接触控制，尽管这两类行为的动作尺度和动力学不同。
- 论文认为，move 片段在数据和梯度中占主导，这会让较小但对接触至关重要的 operate 动作更难学好。
- 这对高精度操作很重要，因为失败通常发生在最后的接触阶段，在这个阶段，微小的动作误差就可能导致任务失败。

## 方法
- 该方法引入了双专家策略：一个专家负责 **move**，一个专家负责 **operate**。一个轻量路由器为每个动作块选择一个专家。
- 两个专家都使用 Conditional Flow Matching 来生成动作，但它们的参数彼此独立，因此粗略移动和精细操作不会共享同一个底层动作头。
- 训练时，路由器用阶段标签进行监督，每个样本只更新对应的专家。这样可以让梯度更新保持阶段专属。
- 阶段标签通过基于 MLLM 的分段流水线自动生成，该流水线使用视频、语言指令、子任务分解，以及末端执行器速度等线索。
- 该模型建立在预训练的 pi_0-base 主干之上，并为两个专家以及共享的视觉-语言主干分别使用独立的 LoRA 适配器。

## 结果
- 在 8 个 RoboTwin2 任务上，使用 **每个任务 50 个演示** 和相同训练步数时，该方法取得了 **68.88% 的平均成功率**，而 **pi_0** 为 **44.75%**，**RDT** 为 **35.63%**，**ACT** 为 **31.63%**。相比 pi_0 提高了 **24.13 个百分点**。
- 相比 **pi_0** 的单任务提升包括：**Click Alarmclock 88% vs 63% (+25)**、**Click Bell 99% vs 44% (+55)**、**Move Pillbottle pad 37% vs 21% (+16)**、**Place Bread Basket 34% vs 17% (+17)**、**Place Cans Plasticbox 79% vs 34% (+45)**、**Place Empty Cup 55% vs 37% (+18)**、**Place Burger Fries 89% vs 80% (+9)**、**Press Stapler 70% vs 62% (+8)**。
- 与使用 **10 倍更多数据** 训练的数据充足基线相比，该方法在若干任务上具有竞争力：**Click Bell 99%**，而 **pi_0.5*** 为 **75%**、**GO-1*** 为 **98%**；**Press Stapler 93%**，而两者分别为 **80%** 和 **66%**。
- 摘要称，该模型达到峰值性能所需的训练步数比标准完整训练预算少 **40%**。
- 摘录给出了基准成功率和部分基线对比的具体数字，但没有提供 10 倍数据对比表的完整总体平均值，也没有给出训练效率曲线的详细数值。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.23620v1](http://arxiv.org/abs/2604.23620v1)
