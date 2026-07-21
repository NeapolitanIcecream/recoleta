---
source: arxiv
url: https://arxiv.org/abs/2607.17521v1
published_at: '2026-07-20T03:56:07'
authors:
- Songyan Zhang
- Jinyuan Tian
- Hanbing Li
- Daqi Liu
- Hao Chen
- Wenhui Huang
- Fang Li
- Guang Chen
- Hangjun Ye
- Long Chen
- Kuiyuan Yang
- Chen Lv
topics:
- world-model
- autonomous-driving
- 3d-geometry
- trajectory-planning
- vision-action
- future-prediction
relevance_score: 0.66
run_id: materialize-outputs
language_code: zh-CN
---

# GeoWorldAD: Geometry World Action Model for Autonomous Driving

## Summary
## 摘要
GeoWorldAD 使用当前场景中显式的、与自车对齐的三维几何，以及预测短期未来演化的潜在几何标记来规划自动驾驶轨迹。该方法在 NAVSIM v1 和 v2 上报告了当前最优的闭环得分，表明以几何为中心的未来引导能够在保持安全性的同时提升驾驶进度。

## 问题
- 基于视觉和视频动作的规划器可以根据图像预测驾驶动作，但通常缺乏显式的几何基础，这使得在动态三维场景中兼顾碰撞规避与高效行驶更加困难。
- 仅使用当前几何可能导致过于保守的行为，而像素空间世界模型提供的未来引导存在冗余，且空间指向性较弱。
- 该问题之所以重要，是因为安全的自动驾驶既需要准确的空间约束，也需要预判在规划时域内周围车辆和可行驶空间将如何变化。

## 方法
- GeoWorldAD 使用 EgoStreamVGGT（StreamVGGT 的自车对齐变体）提取多尺度当前场景几何标记，并估计四维重建、深度和相机运动。
- 一种 Q-Former 风格的几何世界模型结合自车状态与当前几何，生成未来 4 个片段的潜在几何标记，覆盖 2 秒时间；未来深度预测用于提供监督信号。
- 轨迹动作模型在 4 秒规划时域内生成 64 个候选轨迹，每个候选轨迹包含 8 个航点，并通过 4 个当前几何阶段和 1 个未来几何阶段逐步进行细化。
- 训练联合优化重建损失、未来深度损失、轨迹损失和候选轨迹评分损失；候选轨迹得分结合无责碰撞、可行驶区域遵循度、自车行驶进度、碰撞时间和舒适性。

## 结果
- 在 NAVSIM v1 的 navtest 划分上，GeoWorldAD 报告的 PDMS 为 91.0，高于 DVGT-2 的 90.3 和 EponaV2 的 90.4；同时报告 NC 99.0、DAC 97.8、TTC 95.8、舒适性 99.9 和 EP 85.9。
- 在 NAVSIM v2 的 navtest 划分上，GeoWorldAD 报告的 EPDMS 为所列最高值 90.4，高于 DVGT-2 的 89.6 和 EponaV2 的 88.9。
- 在 NAVSIM v2 上，其组成得分包括 NC 99.0、DAC 97.8、DDC 99.6、交通法规遵循度 99.7、EP 89.1 和 TTC 98.6。
- 该模型使用连续 4 帧输入进行训练，预测 2 秒内的 4 帧未来深度，并规划 4 秒内的 8 个航点；所提供的摘录不包含完整的消融实验表，因此无法量化当前几何与未来几何各自的独立贡献。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.17521v1](https://arxiv.org/abs/2607.17521v1)
