---
source: arxiv
url: https://arxiv.org/abs/2605.18743v2
published_at: '2026-05-18T17:58:51'
authors:
- Kunqi Xu
- Jitao Li
- Jianglong Ye
- Tianshu Tang
- Isabella Liu
- Sifei Liu
- Xueyan Zou
topics:
- world-model
- actionable-object-representation
- 3d-occupancy
- articulated-objects
- rgb-d-reconstruction
- robotics
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# WorldString: Actionable World Representation

## Summary
## 摘要
WorldString 学习一个可控的 3D 物体模型，以稀疏的物体状态关键点作为输入，并预测被占据的 3D 形状。论文把它定位为物理世界模型的基础模块，并在刚体、可动关节、蒙皮和软体对象上做了测试。

## 问题
- 机器人和物理世界模型需要物体状态，这些状态可以被动作改变、在 3D 中查询，并用于预测或控制。
- 视频生成器可以生成看起来合理的滚动结果，但通常缺少 3D 一致性和直接的状态控制。
- 传统模型把刚体关节、蒙皮或软体形变分开处理，这让真实世界里混合类型的物体很难用同一种方法建模。

## 方法
- WorldString 存储一个可学习的规范物体嵌入，并用稀疏状态关键点进行条件控制，这些关键点可以是关节或跟踪到的表面锚点。
- State Transformer 通过交叉注意力把关键点状态注入规范物体嵌入。
- Object Transformer 将局部关键点效应扩散到整个物体，使完整的形变状态被编码。
- Voxel Transformer 查询 3D 坐标并预测占据情况，输出形变后的物体形状，形式可以是体素或点云。
- 对于 RGB-D 视频，数据管线使用 Grounded-SAM2 生成掩码，使用 CoTracker 做稠密跟踪，使用 TRELLIS 生成初始网格，用最远点采样选取关键点，并把形变后的网格体素化作为训练目标。

## 结果
- 在刚体形状重建上，WorldString 在 Utah Teapot 的 IoU/F1 为 92.17/95.92，在 Stanford Bunny 上为 75.38/85.96，在 Armadillo 上为 67.36/80.50，在 Lucy 上为 70.20/82.49。
- 在四个可动关节物体上，WorldString 的平均 IoU 为 86.61，平均 F1 为 92.73。基线方法的平均值分别是 NN 的 53.61/67.81、Optimized NN 的 47.62/62.18，以及 Dr. Robot 的 44.79/60.73。
- 在 Robot 1 Hand 上，WorldString 达到 90.28 IoU 和 94.89 F1，而表中最好的基线是 73.41 IoU 和 84.58 F1。
- 在 Robot 2 Arm 上，WorldString 达到 77.00 IoU 和 87.01 F1，而 Dr. Robot 为 57.43 IoU 和 72.94 F1。
- 在 IKEA 风格家具案例上，WorldString 在 Furniture 21 的 IoU/F1 为 90.17/94.83，在 Furniture 09 上为 88.98/94.17；表中最好的基线 IoU 分别是 74.21 和 49.21。
- 摘要声称覆盖可动关节、蒙皮和软体对象，但给出的正文只包含刚体和可动关节案例的完整定量表。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.18743v2](https://arxiv.org/abs/2605.18743v2)
