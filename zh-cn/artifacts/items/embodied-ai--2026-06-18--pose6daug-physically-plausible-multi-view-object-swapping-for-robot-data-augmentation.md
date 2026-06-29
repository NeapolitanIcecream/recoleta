---
source: arxiv
url: https://arxiv.org/abs/2606.20118v1
published_at: '2026-06-18T11:41:25'
authors:
- Jonghoon Lee
- Seong Hyeon Park
- Byungwoo Jeon
- Minha Lee
- Jinwoo Shin
topics:
- vision-language-action
- robot-data-augmentation
- multi-view-consistency
- object-swapping
- robot-data-scaling
- manipulation
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Pose6DAug: Physically Plausible Multi-view Object Swapping for Robot Data Augmentation

## Summary
## 摘要
Pose6DAug 通过在成功的多视角 episode 中用新的 3D 物体替换原物体来增强机器人操作数据，同时保留原始机器人运动和接触几何。

## 问题
- GR00T-1.5 等 VLA 策略可能在形状或外观不同的新物体上失败。
- 为每个失败物体重新采集多视角遥操作数据既慢又贵。
- 2D 视频编辑可能破坏跨相机几何、物体身份一致性以及夹爪-物体接触关系，给策略提供带噪声的训练数据。

## 方法
- 该方法从一个成功的机器人 episode 开始，并保留记录下来的动作轨迹。
- 它重建或提供目标物体网格，从每个相机视角中移除原物体，并对背景进行补全。
- 它在共享世界坐标系中将原物体的 6D 位姿轨迹转移到目标网格，然后把同一个目标物体渲染到所有已标定的相机视角中。
- 它把机器人和夹爪掩码恢复到渲染物体之上，使遮挡关系保持一致。
- 它加入基于 3D 的扰动：物体旋转、沿夹爪接近轴的平移，以及用于保持物体可抓取的缩放。

## 结果
- 在使用 GR00T-1.5 的 RoboCasa365 Counter-to-Cabinet 失败 episode 上，Pose6DAug 的平均成功率为 22.8%，VACE 为 16.4%，MimicGen 为 15.8%，基础策略为 0.0%。
- 在同一失败 episode 设置下，Pose6DAug 的平均 turnover ratio 为 24.5%，VACE 为 18.2%，MimicGen 为 17.2%。
- 对于分布内失败物体，Pose6DAug 的成功率为 21.2%，VACE 为 12.8%，MimicGen 为 14.7%。
- 对于分布外失败物体，Pose6DAug 的成功率为 24.7%，VACE 为 21.2%，MimicGen 为 17.3%。
- 在包含 8 个未见过的分布外网格的困难物体测试中，仅用增强 episode 训练时，Pose6DAug 的成功率为 21.2%，VACE 为 15.0%，MimicGen 为 5.7%。
- Pose6DAug 恢复了 8 个困难物体中的 7 个，VACE 为 8 个中的 5 个，MimicGen 为 8 个中的 2 个；它像 VACE 一样生成了 176 个增强 episode，而 MimicGen 在 rollout 失败后只保留了 33 个有效 rollout。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.20118v1](https://arxiv.org/abs/2606.20118v1)
