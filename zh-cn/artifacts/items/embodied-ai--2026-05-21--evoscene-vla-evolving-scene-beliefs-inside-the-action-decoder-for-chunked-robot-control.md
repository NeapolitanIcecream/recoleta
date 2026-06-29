---
source: arxiv
url: https://arxiv.org/abs/2605.21862v1
published_at: '2026-05-21T01:19:17'
authors:
- Chushan Zhang
- Ruihan Lu
- Jinguang Tong
- Xuesong Li
- Yikai Wang
- Hongdong Li
topics:
- vision-language-action
- generalist-robot-policy
- world-model
- robot-data-scaling
- sim2real
- embodied-foundation-model
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# EvoScene-VLA: Evolving Scene Beliefs Inside the Action Decoder for Chunked Robot Control

## Summary
## 摘要
EvoScene-VLA 是一种分块机器人 VLA 策略，会在控制调用之间保留一个由动作更新的场景状态。与采用深度监督的 LingBot-VLA 基线相比，它在 RoboTwin 上的平均成功率在固定场景下提高了 1.9 个百分点，在随机布局下提高了 2.4 个百分点。

## 问题
- 分块 VLA 策略会基于一次视觉更新预测多步机器人动作，因此接触、遮挡和物体移动会让后续动作使用过时的场景几何信息。
- 空间 VLA 改善了单帧几何信息，时间 VLA 保存了过去观测，但策略仍然缺少一个由自身最近动作更新的紧凑场景状态。
- 这对操作任务很重要，因为机器人会在一个分块期间改变场景，比如打开微波炉、堆叠积木，或把物体放进柜子里。

## 方法
- 该方法在 VLM 输入中加入一个递归场景前缀：观测槽位读取当前多视角图像，先前槽位携带上一分块的场景状态。
- VLM 用新观测修正携带来的先验，然后动作解码器在一次 flow-matching 去噪过程中同时预测下一段动作和未来场景标记。
- 最后一个预测的场景标记会成为下一次控制调用的先验，因此推理时不需要单独的场景预测器或记忆模块。
- 训练时使用 Local Anchor，通过冻结的单目深度教师进行掩码深度重建，并使用 Global Anchor 对齐冻结的 3D 基础模型特征。
- 仅用于训练的 Scene Predictor 将当前场景标记和动作映射到未来的场景标记目标，这些目标通过场景 flow-matching 损失蒸馏到动作解码器中。

## 结果
- 在 31 个 RoboTwin 任务上，EvoScene-VLA 在固定评测下把平均成功率从 87.2% 提高到 89.1%，比采用深度监督的 LingBot-VLA 基线高 1.9 个百分点。
- 在同样 31 个 RoboTwin 任务的随机初始位置和朝向设置下，平均成功率从 86.1% 提高到 88.5%，提升 2.4 个百分点。
- 与原始 LingBot-VLA 基线相比，报告的平均值在固定场景中从 85.3% 提高到 89.1%，在随机场景中从 84.1% 提高到 88.5%。
- 与 π0.5 相比，报告的平均值在固定场景中从 81.2% 提高到 89.1%，在随机场景中从 75.9% 提高到 88.5%。
- 相比采用深度监督的 LingBot-VLA 基线，示例任务提升包括：Open Microwave 固定成功率从 70% 提高到 82%，Place Dual Shoes 固定成功率从 75% 提高到 91%，Stack Blocks Three 随机成功率从 88% 提高到 95%。
- 摘要提到 Galaxea R1-Lite 真机实验优于所有基线，但没有给出真机表格中的数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.21862v1](https://arxiv.org/abs/2605.21862v1)
