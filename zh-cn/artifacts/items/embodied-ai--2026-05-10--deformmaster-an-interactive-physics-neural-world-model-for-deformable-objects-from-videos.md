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
DeformMaster 从真实视频中学习可交互的可变形物体世界模型。它预测绳子、布料、包装物和软玩具在新动作下如何运动，并从新视角渲染预测的运动。

## 问题
- 可变形物体存在高维运动、接触、自接触和空间变化的材料行为，因此只从视频进行动作条件预测很难。
- 具身智能体需要能预测新交互效果的模型，不能只回放已观察到的运动或生成看起来合理的视频。
- 现有物理孪生模型可能漏掉真实世界效应，而学习式或生成式动力学在长时 rollout 中可能漂移，或缺少明确的动作控制。

## 方法
- DeformMaster 用材料粒子表示物体动力学，用 Gaussian 外观粒子进行渲染。
- Physics–Neural Particle-Grid Dynamics 先用可微 MPM 将状态向前推进，再应用有界的神经速度修正，以处理模拟器之外的效应。
- Distributed Compliant Actuators 将稀疏且有噪声的手部轨迹转换为软执行器-粒子力，并分布到局部接触邻域。
- Mixture of Constitutive Experts 以空间变化的权重和学习到的材料场混合 Neo-Hookean、corotated 和 StVK 材料定律。
- 预测的材料粒子运动通过线性混合蒙皮驱动 Gaussian Splatting，因此无需重新优化场景即可渲染新动作 rollout。

## 结果
- 在 20 个真实 PhysTwin 序列上，这些序列由 3 个 RGB-D 视角以 30 fps 采集，DeformMaster 达到 IoU 0.748、Chamfer 0.011、Track error 0.024、PSNR 25.41、SSIM 0.936 和 LPIPS 0.061。
- 相比 PhysTwin，它将 IoU 从 0.734 提高到 0.748，将 Chamfer 从 0.012 降到 0.011，但 Track error 略差，为 0.024，而 PhysTwin 为 0.023。
- 相比 Spring-Gaus，它将 IoU 从 0.464 提高到 0.748，将 Chamfer 从 0.062 降到 0.011，将 Track error 从 0.094 降到 0.024，并将 PSNR 从 22.49 提高到 25.41。
- 相比 GS-Dynamics，它将 IoU 从 0.498 提高到 0.748，将 Chamfer 从 0.041 降到 0.011，将 Track error 从 0.070 降到 0.024，并将 PSNR 从 22.54 提高到 25.41。
- 按物体类型看，它将绳子的 IoU 从 0.658 提高到 0.721，将 Chamfer 从 0.007 降到 0.005，并将 Track error 从 0.013 降到 0.010；在平面物体上，Track error 比 PhysTwin 差，为 0.032，而 PhysTwin 为 0.028。
- 该系统支持超过 15 fps 的在线交互式 rollout，并展示了新动作、材料尺度和新视角查询，包括当材料场缩放到 0.3× 时的断裂行为。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.09586v1](https://arxiv.org/abs/2605.09586v1)
