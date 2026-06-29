---
source: arxiv
url: https://arxiv.org/abs/2605.13757v1
published_at: '2026-05-13T16:38:05'
authors:
- Bin Yu
- Shijie Lian
- Xiaopeng Lin
- Zhaolong Shen
- Yuliang Wei
- Changti Wu
- Hang Yuan
- Haishan Liu
- Bailing Wang
- Cong Huang
- Kai Chen
topics:
- vision-language-action
- robot-policy
- frame-selection
- robot-data-scaling
- dexterous-manipulation
- dataloader-training
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# FrameSkip: Learning from Fewer but More Informative Frames in VLA Training

## Summary
## 摘要
FrameSkip 是一种在训练阶段进行帧选择的方法，用于 VLA 策略。它在主设置中保留 20% 的唯一轨迹帧，并报告在 RoboCasa-GR1、SimplerEnv 和 LIBERO 上的成功率高于使用全部帧训练。

## 问题
- 稠密的机器人演示包含许多变化很小的帧，因此均匀采样会把大量训练预算分给接近、搬运和其他平滑片段。
- 对齐、接触、夹爪闭合和释放等关键事件很稀疏，这会让 VLA 策略在决定任务成功的步骤上表现薄弱。
- 这会影响机器人数据扩展，因为大规模遥操作数据集即使持续变大，也未必能在操控关键转换上提供相应比例的监督。

## 方法
- FrameSkip 用动作变化、视觉-动作一致性、任务进度先验和夹爪或末端执行器转换来给每一帧打分。
- 动作变化使用局部动作变化和短期前瞻变化；视觉-动作一致性使用 DINOv2 视觉特征变化除以局部动作变化。
- 任务进度使用两种方式之一：基于标注的关键阶段位置构建、可适应数据集的高斯混合模型，或更简单的轨迹中段高斯先验。
- dataloader 在目标保留比例下保留得分最高的帧，同时保留首尾帧、夹爪转换帧和动作变化位于前十分位的帧。
- VLA 模型、动作头、损失函数、优化器配置和推理路径保持不变；训练在 warmup 后使用 5:1 的裁剪 minibatch 与全帧锚点 minibatch 混合。

## 结果
- 主设置中，FrameSkip 保留 20% 的唯一帧，并将 RoboCasa-GR1、SimplerEnv 和 LIBERO 上的宏平均成功率从全帧训练的 66.50% 提升到 76.15%。
- RoboCasa-GR1：24 个任务的平均成功率从全帧训练的 47.8% 提高到 FrameSkip 的 59.5%；训练集使用 24K GR1 遥操作仿真演示。
- SimplerEnv：4 个留出 WidowX 任务的平均成功率从 55.2% 提高到 71.55%。
- SimplerEnv 的任务提升包括 Stack Green Block on Yellow Block 从 29.2% 提高到 45.59%，以及 Put Eggplant in Yellow Basket 从 54.2% 提高到 95.83%。
- 报告中的宏平均值，以及展示的 RoboCasa-GR1 和 SimplerEnv 平均值，意味着如果三个基准的平均值等权，FrameSkip 的 LIBERO 平均值约为 97.4%，全帧训练约为 96.5%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.13757v1](https://arxiv.org/abs/2605.13757v1)
