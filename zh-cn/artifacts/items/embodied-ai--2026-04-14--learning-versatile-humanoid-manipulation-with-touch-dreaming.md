---
source: arxiv
url: http://arxiv.org/abs/2604.13015v2
published_at: '2026-04-14T17:54:17'
authors:
- Yaru Niu
- Zhenlong Fang
- Binghong Chen
- Shuai Zhou
- Revanth Krishna Senthilkumaran
- Hao Zhang
- Bingqing Chen
- Chen Qiu
- H. Eric Tseng
- Jonathan Francis
- Ding Zhao
topics:
- humanoid-manipulation
- tactile-learning
- vision-language-action
- dexterous-manipulation
- sim2real
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Learning Versatile Humanoid Manipulation with Touch Dreaming

## Summary
## 摘要
这篇论文提出了一个面向真实世界的人形机器人操作系统，把稳定的全身控制、灵巧手和触觉感知结合在一起。其核心模型 Humanoid Transformer with Touch Dreaming（HTD）在行为克隆中加入了对未来触觉的预测，并在高接触任务上报告了明显的性能提升。

## 问题
- 真实人形机器人的移动操作很难，因为机器人必须同时保持全身平衡、控制灵巧手运动，并对不断变化的接触状态作出反应。
- 仅靠视觉和本体感觉无法完整覆盖接触状态，这会影响插入、可变形物体操作、工具使用和双手搬运等任务的表现。
- 以往的人形机器人系统通常至少缺少其中一项：全身控制、完整的灵巧手控制、触觉传感，或触觉建模。

## 方法
- 该系统包含一个用 RL 训练的下半身控制器，用于稳定行走和躯干跟踪；同时结合 VR 遥操作、上半身 IK 和灵巧手重定向来完成数据采集和执行。
- 策略模型 HTD 是一个多模态编码器-解码器 Transformer，输入包括多视角 RGB、本体感觉、手部关节力信号和触觉输入。
- 训练采用单阶段行为克隆，并加入辅助性的“touch dreaming”损失。模型除了预测动作块，还会预测未来的手部关节力和未来的触觉潜变量。
- 未来触觉目标来自 EMA 目标编码器，因此模型可以学习潜变量预测目标，而不需要单独的触觉预训练阶段，也不需要在推理时使用世界模型。
- 触觉输入按手部区域和手指区域编码，再与其他模态一起在共享的 Transformer 主干中融合。

## 结果
- 在 5 个真实世界的高接触人形机器人任务上，HTD 相比更强的 **ACT** 基线，报告了**平均成功率相对提升 90.9%**。
- 任务包括 **Insert-T**、**Book Organization**、**Towel Folding**、**Cat Litter Scooping** 和 **Tea Serving**。
- 论文称，在消融实验中，**潜空间触觉预测**优于**原始触觉预测**，带来**成功率相对提升 30%**。
- 该系统可以完成一个间隙仅 **3.5 mm** 的紧公差插入任务。
- 部署时，学习得到的策略以 **30 Hz** 运行，下半身控制器、IK 求解器和手部重定向器以 **50 Hz** 运行。
- 摘录中没有给出各任务成功率、数据集规模或基线的绝对数值，因此目前最强的定量结论是平均相对提升 90.9% 和消融中的 30% 提升。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.13015v2](http://arxiv.org/abs/2604.13015v2)
