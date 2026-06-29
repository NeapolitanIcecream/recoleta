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
本文提出了一个面向真实世界的人形操作系统，结合了稳定的全身控制、灵巧手和触觉感知。其核心模型 Humanoid Transformer with Touch Dreaming（HTD）把未来触觉预测加入行为克隆，并在接触丰富的任务上报告了显著提升。

## 问题
- 真实的人形行走式操作很难，因为机器人必须同时保持全身平衡、移动灵巧手，并对不断变化的接触作出反应。
- 只有视觉和本体感知时，会遗漏部分接触状态，影响插入、柔性物体操作、工具使用和双手搬运等任务表现。
- 以往的人形系统通常至少缺少其中一项：全身控制、完整的灵巧手控制、触觉感知或触觉建模。

## 方法
- 该系统使用一个通过强化学习训练的下半身控制器，负责稳定行走和躯干跟踪；同时结合 VR 遥操作、上半身逆运动学和灵巧手重定向，用于数据采集和执行。
- 策略模型 HTD 是一个多模态编码器-解码器 Transformer，输入多视角 RGB、本体感知、手关节力信号和触觉输入。
- 训练采用单阶段行为克隆，并加入辅助的“触觉梦境”损失。除了预测动作片段，模型还预测未来的手关节力和未来的触觉潜变量。
- 未来触觉目标来自 EMA 目标编码器，因此模型在没有单独触觉预训练阶段或推理时世界模型的情况下，学习潜在预测目标。
- 触觉输入按手部区域和手指区域编码，然后与其他模态一起融合到共享的 Transformer 主干中。

## 结果
- 在 5 个真实世界的接触丰富人形任务上，HTD 相比更强的 **ACT** 基线，在平均成功率上实现了 **90.9% 的相对提升**。
- 任务包括 **Insert-T**、**Book Organization**、**Towel Folding**、**Cat Litter Scooping** 和 **Tea Serving**。
- 论文在消融实验中指出，**潜空间触觉预测**优于**原始触觉预测**，成功率获得 **30% 的相对提升**。
- 该系统可以处理一个公差很紧的插入任务，间隙为 **3.5 mm**。
- 部署时，学习到的策略以 **30 Hz** 运行，而下半身控制器、IK 求解器和手部重定向器以 **50 Hz** 运行。
- 摘要未提供逐任务成功率、数据集规模或基线绝对数值，因此这里能确认的最强量化结论是平均 **90.9%** 的相对提升，以及消融实验中的 **30%** 提升。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.13015v2](http://arxiv.org/abs/2604.13015v2)
