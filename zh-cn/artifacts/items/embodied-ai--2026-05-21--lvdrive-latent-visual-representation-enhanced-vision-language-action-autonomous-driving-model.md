---
source: arxiv
url: https://arxiv.org/abs/2605.22089v1
published_at: '2026-05-21T07:31:49'
authors:
- Xiaodong Mei
- Diankun Zhang
- Hongwei Xie
- Guang Chen
- Hangjun Ye
- Dan Xu
topics:
- vision-language-action
- autonomous-driving
- latent-world-model
- trajectory-planning
- closed-loop-evaluation
relevance_score: 0.72
run_id: materialize-outputs
language_code: zh-CN
---

# LVDrive: Latent Visual Representation Enhanced Vision-Language-Action Autonomous Driving Model

## Summary
## 摘要
LVDrive 是一个用于自动驾驶的 VLA 模型，它在潜在空间中预测未来场景特征，并用这些特征修正规划轨迹。在 Bench2Drive 上，它在所列的纯摄像头驾驶方法中报告了最高的 Driving Score 和 Success Rate。

## 问题
- 现有的 VLA 驾驶模型主要从稀疏动作标签中学习，因此对场景动态和未来风险的监督有限。
- 基于图像重建的 world model 提供了更密集的监督，但像素生成会把模型容量花在纹理上，而不是与规划相关的语义上。
- 自回归的未来帧或动作 token 生成会增加推理开销，这在闭环驾驶中很重要。

## 方法
- LVDrive 在 VLA 模型中加入未来场景预测任务，用潜在视觉特征作为监督，而不是重建的 RGB 帧。
- 一个冻结的预训练视觉模型提供目标未来视觉嵌入；模型预测 6 个未来时间步，每个未来帧对应 256 个潜在 token。
- 未来场景 token 和规划 token 在共享的连续嵌入空间中一次前向传播生成。
- 规划器先从规划嵌入中解码出粗轨迹，再由一个 transformer 精修器通过对预测的未来场景嵌入做交叉注意力，生成最终轨迹。
- 训练使用视觉潜在预测损失、粗轨迹和精修轨迹损失、结构化视图特征损失，以及占位 token 序列的交叉熵损失。

## 结果
- 在 Bench2Drive 的闭环评估中，LVDrive 报告的 Driving Score 为 80.71，Success Rate 为 58.26%。
- 与所列最强的图像重建 world model 基线 UniDrive-WM-AR+Diff 相比，LVDrive 的 Driving Score 从 79.31 提升到 80.71，Success Rate 从 56.42% 提升到 58.26%。
- 与它所基于的 VLA 基线 ORION 相比，LVDrive 的 Driving Score 从 77.74 提升到 80.71，Success Rate 从 54.62% 提升到 58.26%。
- 与所列最强的传统端到端方法 Raw2Drive 相比，LVDrive 的 Driving Score 从 71.36 提升到 80.71，Success Rate 从 50.24% 提升到 58.26%。
- 在开放环评估中，Avg. L2 为 0.63，与 UniDrive-WM-AR+Diff 的 0.63 持平，好于 ORION 的 0.68；DriveMoE 在所列结果中的 Avg. L2 更低，为 0.38。
- LVDrive 只使用摄像头输入进行模仿学习；它在 Bench2Drive 上报告的 Efficiency 为 155.77，Comfortness 为 14.34.

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.22089v1](https://arxiv.org/abs/2605.22089v1)
