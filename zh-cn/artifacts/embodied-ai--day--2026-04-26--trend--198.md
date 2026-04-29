---
kind: trend
trend_doc_id: 198
granularity: day
period_start: '2026-04-26T00:00:00'
period_end: '2026-04-27T00:00:00'
topics:
- robotics
- vision-language-action
- manipulation
- tactile sensing
- safety
run_id: materialize-outputs
aliases:
- recoleta-trend-198
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/manipulation
- topic/tactile-sensing
- topic/safety
language_code: zh-CN
---

# 接触时刻控制与 VLA 安全定义了当天的机器人论文主题

## Overview
这一天最突出的主题，是必须在接触时刻稳定工作的具身控制。两篇论文关注如何提升操作执行效果：Move-Then-Operate将接近阶段与接触阶段分开，TubeDiffusionPolicy则在动作时域内部加入逐步的视觉-触觉修正。

## Clusters

### 用于精确操作的行为分阶段
Move-Then-Operate 认为，当策略把接近运动和接触操作视为两种独立行为时，高精度操作会更好。它的双专家设计用一个专家负责移动，另一个专家负责操作，并由路由器为每个动作块选择所处阶段。在 RoboTwin2 的 8 个任务上、每个任务 50 条演示的设置下，它报告的平均成功率为 68.88%，高于 pi_0 的 44.75%、RDT 的 35.63% 和 ACT 的 31.63%。在接触密集型任务上的提升尤其明显，例如 Click Bell 为 99%，而 pi_0 为 44%；Place Cans Plasticbox 为 79%，而 pi_0 为 34%。论文还称，在训练步数减少 40% 的情况下就能达到峰值表现。

#### Evidence
- [Move-Then-Operate: Behavioral Phasing for Human-Like Robotic Manipulation](../Inbox/2026-04-26--move-then-operate-behavioral-phasing-for-human-like-robotic-manipulation.md): 分阶段操作策略的摘要和基准结果。

### 反应式视觉-触觉控制
Tube Diffusion Policy 聚焦于不确定条件下的高接触控制。它保留了用于动作块起始动作生成的 diffusion，然后加入一个学习得到的流式反馈流，让机器人能根据新的视觉和触觉输入，在每一步修正动作。论文报告称，它在 Push-T 和另外三个视觉-触觉任务上持续优于先前的模仿学习基线，并给出了两个真实世界实验，在扰动下表现出更强的反应能力。摘录没有提供精确的成功率，因此目前最可靠的结论是架构层面的：对于触觉操作，动作块内部的反应式修正正被视为核心控制需求。

#### Evidence
- [Tube Diffusion Policy: Reactive Visual-Tactile Policy Learning for Contact-rich Manipulation](../Inbox/2026-04-26--tube-diffusion-policy-reactive-visual-tactile-policy-learning-for-contact-rich-manipulation.md): 动作管方法的摘要和报告的实验范围。

### VLA 安全分类与评估范围
安全性正被视为 vision-language-action 模型中的一类核心研究问题，而不是附属于模型规模的边缘话题。VLA 安全综述给出了一个具体的威胁图谱，覆盖训练时与推理时攻击，以及训练时与运行时防御。它涵盖了数据投毒、后门、对抗补丁、跨模态扰动、越狱和 freezing attacks 等威胁，并将这些威胁与六个领域中的评估和部署问题联系起来。这篇论文是综述，不是新的基准测试报告，但它清楚表明，这个领域现在需要共享评估方法和运行时保护机制。

#### Evidence
- [Vision-Language-Action Safety: Threats, Challenges, Evaluations, and Mechanisms](../Inbox/2026-04-26--vision-language-action-safety-threats-challenges-evaluations-and-mechanisms.md): 含分类法、威胁类别和部署范围的综述摘要。
