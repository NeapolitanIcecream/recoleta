---
source: arxiv
url: https://arxiv.org/abs/2607.11498v1
published_at: '2026-07-13T12:50:32'
authors:
- Byungkun Lee
- Dongyoon Hwang
- Dongjin Kim
- Hojoon Lee
- Minho Park
- Jaegul Choo
topics:
- vision-language-action
- robot-centric-geometry
- pointmaps
- viewpoint-generalization
- 3d-manipulation
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# See like a Robot: Robot-Centric Pointmaps for Vision-Language-Action Models

## Summary
## 摘要
以机器人为中心的点图为 VLA 提供与机器人动作使用的坐标系一致的稠密三维场景坐标。这样可以减少视角变化带来的坐标系不匹配，同时继续使用预训练的二维视觉编码器。

## 问题
- VLA 通常在相机坐标系中观察场景，却在机器人坐标系中预测动作，因此策略需要学习从相机坐标系到机器人坐标系的变换。
- 当示范使用不同的相机位置，或部署时采用训练中未见过的视角时，这一问题会加重。
- 相机感知输入、深度图和点云要么把坐标变换交给策略学习，要么丢失预训练 VLA 所使用的图像网格。

## 方法
- 将每个 RGB-D 像素提升到三维空间，把它从相机坐标系转换到机器人基座坐标系，再减去当前末端执行器的位置。
- 将得到的 XYZ 坐标存储在具有图像形状的点图中，使其 H×W 布局与 RGB 图像一致。
- 使用从 RGB 编码器初始化的视觉塔对点图进行编码，然后将其 token 逐元素加到 RGB token 上。
- 这种方法在不使用点云编码器、体素化、额外 token 序列或推理时渲染阶段的情况下，加入了机器人坐标系中的度量几何信息。

## 结果
- 在 RoboCasa 上，π₀.₅ 的 24 任务平均成功率从 55.3% 提高到 62.9%，增加 7.6 个百分点；SmolVLA 从 37.2% 提高到 41.4%，增加 4.2 个百分点。
- π₀.₅ 点图模型的得分为 62.9%，高于 KYC 的 59.1%、PointVLA 的 57.3% 和 GeoVLA 的 57.1%。
- 在受控的 RoboCasa 研究中，RGB + 点图的成功率为 34.7%，RGB 加 Plücker 射线和深度为 31.6%；加入末端执行器居中后，成功率提高到 36.9%。
- 随着训练相机视角变化增加，RGB 的成功率下降 9.6 个百分点，从 34.5% 降至 24.9%；点图模型仅下降 1.8 个百分点，从 37.6% 降至 35.8%。
- 在真实机器人 Franka 实验中，与 RGB 模型相比，使用训练时相机位置的性能提升为 5.0 个百分点；使用训练中未见过的相机位置时，提升扩大到 11.7 个百分点。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.11498v1](https://arxiv.org/abs/2607.11498v1)
