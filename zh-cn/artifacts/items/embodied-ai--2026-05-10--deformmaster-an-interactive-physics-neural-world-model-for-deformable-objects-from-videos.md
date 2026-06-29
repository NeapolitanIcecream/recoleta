---
source: arxiv
url: https://arxiv.org/abs/2605.09586v1
published_at: '2026-05-10T14:55:54'
authors:
- Can Li
- Zhoujian Li
- Ren Li
- Jie Gu
- Lei Lei
- Jingmin Chen
- Lei Sun
topics:
- deformable-object-modeling
- physics-neural-world-model
- robot-interaction
- material-point-method
- gaussian-splatting
- sim2real
relevance_score: 0.62
run_id: materialize-outputs
language_code: zh-CN
---

# DeformMaster: An Interactive Physics-Neural World Model for Deformable Objects from Videos

## Summary
## 摘要
DeformMaster 从真实视频中学习一个面向可变形物体的交互式世界模型。它预测绳子、布料、包裹和软体玩具在新动作下的运动，并从新视角渲染预测结果。

## 问题
- 可变形物体具有高维运动、接触、自接触和空间变化的材料行为，只靠视频很难做动作条件预测。
- 具身智能体需要能预测新交互影响的模型，而不只是回放已观测到的运动或生成看起来合理的视频。
- 现有物理数字孪生会漏掉真实世界效应，学习式或生成式动力学在长时间展开时会漂移，或者缺少明确的动作控制。

## 方法
- DeformMaster 用材料粒子表示物体动力学，用高斯外观粒子表示渲染。
- Physics–Neural Particle-Grid Dynamics 先用可微分 MPM 推进状态，再加入有界的神经速度修正，处理模拟器之外的效应。
- Distributed Compliant Actuators 将稀疏、带噪声的手部轨迹转换为软执行器-粒子力，并分布到局部接触邻域中。
- Mixture of Constitutive Experts 以空间变化的权重和学习到的材料场，混合 Neo-Hookean、corotated 和 StVK 材料定律。
- 预测的材料粒子运动通过线性混合蒙皮驱动 Gaussian Splatting，因此新的动作展开可以直接渲染，不需要重新优化场景。

## 结果
- 在 20 个真实 PhysTwin 序列上测试，使用 3 个 RGB-D 视角、30 fps 采集，DeformMaster 达到 IoU 0.748、Chamfer 0.011、Track error 0.024、PSNR 25.41、SSIM 0.936 和 LPIPS 0.061。
- 与 PhysTwin 相比，IoU 从 0.734 提升到 0.748，Chamfer 从 0.012 降到 0.011，但 Track error 略差，为 0.024 对 0.023。
- 与 Spring-Gaus 相比，IoU 从 0.464 提升到 0.748，Chamfer 从 0.062 降到 0.011，Track error 从 0.094 降到 0.024，PSNR 从 22.49 提升到 25.41。
- 与 GS-Dynamics 相比，IoU 从 0.498 提升到 0.748，Chamfer 从 0.041 降到 0.011，Track error 从 0.070 降到 0.024，PSNR 从 22.54 提升到 25.41。
- 按物体类型看，绳子上的 IoU 从 0.658 提升到 0.721，Chamfer 从 0.007 降到 0.005，Track error 从 0.013 降到 0.010；在平面物体上，Track error 为 0.032，差于 PhysTwin 的 0.028。
- 该系统支持超过 15 fps 的在线交互式展开，并展示了新动作、材料尺度和新视角查询，包括把材料场缩放到 0.3× 时出现的断裂行为。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.09586v1](https://arxiv.org/abs/2605.09586v1)
