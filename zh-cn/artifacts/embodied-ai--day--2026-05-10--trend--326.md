---
kind: trend
trend_doc_id: 326
granularity: day
period_start: '2026-05-10T00:00:00'
period_end: '2026-05-11T00:00:00'
topics:
- robotics
- VLA
- failure recovery
- long-horizon planning
- world models
- sim-to-real
- embodied datasets
run_id: materialize-outputs
aliases:
- recoleta-trend-326
tags:
- recoleta/trend
- topic/robotics
- topic/vla
- topic/failure-recovery
- topic/long-horizon-planning
- topic/world-models
- topic/sim-to-real
- topic/embodied-datasets
language_code: zh-CN
---

# 机器人论文聚焦失败恢复、领域数据和动作条件预测

## Overview
这一时期的机器人研究把可靠性作为可测量的控制问题来处理。Vision-Language-Action (VLA) 策略加入了恢复训练、不确定性触发搜索和门店专用动作数据。RePO-VLA、CAPS 和 SABER 给出了最强的定量信号。

## Clusters

### VLA 失败恢复和长时程控制
两篇论文直接处理执行漂移。RePO-VLA 使用成功、失败和恢复 rollout 训练，并分别打标签；部署时使用固定的高 value 条件，不使用在线失败检测器。论文报告的对抗成功率平均从 20% 提高到 75%，FRBench-Sim 覆盖 46 个任务中的 23,453 个双臂 episode。

CAPS 不改变基础 VLA 策略，只在不确定性升高时增加推理开销。它用幂分布采样未来 action chunk，并在熵超过阈值时使用 Metropolis-Hastings 搜索。在 RoboTwin 1.0 上配合 π0 时，平均成功率为 47.4%；相比之下，π0 为 32.2%，π0 加 TACO 为 41.3%。在 Simpler-WindowX 上，它报告的平均成功率为 60.5%，高于 π0 和多个 VLA 基线。

#### Evidence
- [RePO-VLA: Recovery-Driven Policy Optimization for Vision-Language-Action Models](../Inbox/2026-05-10--repo-vla-recovery-driven-policy-optimization-for-vision-language-action-models.md): RePO-VLA 方法、FRBench-Sim 规模和对抗成功率数据。
- [Drift is a Sampling Error: SNR-Aware Power Distributions for Long-Horizon Robotic Planning](../Inbox/2026-05-10--drift-is-a-sampling-error-snr-aware-power-distributions-for-long-horizon-robotic-planning.md): CAPS 的推理时搜索方法，以及在 RoboTwin 和 Simpler-WindowX 上的基准结果。

### 面向真实环境的领域专用动作数据
SABER 用具体数字展示了零售机器人中的数据问题。该数据集使用约 100 小时的杂货店采集数据，把人类活动转换为 44.8K 个训练样本：25K 条潜在动作序列、18.6K 条手部姿态轨迹和 1.2K 条全身运动序列。在这些数据流上对 GR00T N1.6 做后训练后，它在 10 个 RoboBenchMart 任务上的平均成功率达到 29.3%；相比之下，仅用仿真微调的平均成功率为 13.4%。

DRIS 处理灵巧操作仿真到现实迁移中的另一类数据缺口。每个仿真 episode 包含多个动态参数不同的物体实例，并在同一个机器人动作下同步推进。论文声称在平板反应式接球任务上实现零样本现实迁移，但可见摘录没有给出现实试验成功率，因此证据对训练设计的支持强于对部署结果的支持。

#### Evidence
- [SABER: A Scalable Action-Based Embodied Dataset for Real-World VLA Adaptation](../Inbox/2026-05-10--saber-a-scalable-action-based-embodied-dataset-for-real-world-vla-adaptation.md): SABER 数据集组成，以及 RoboBenchMart 成功率对比。
- [Zero-Shot Sim-to-Real Robot Learning: A Dexterous Manipulation Study on Reactive Catching](../Inbox/2026-05-10--zero-shot-sim-to-real-robot-learning-a-dexterous-manipulation-study-on-reactive-catching.md): DRIS 训练设置，以及可见定量证据的局限。

### 为动作 rollout 构建的世界模型
世界模型论文关注可用于指导控制的预测。Sub-JEPA 通过低维高斯检验正则化潜在空间，避免把整个潜在向量强制成各向同性高斯分布。与 LeWorldModel 相比，它在报告的四个任务上都提高了规划成功率，包括 Two-Room 的 95.00±2.76% 和 OGB-Cube 的 76.33±5.99%。

DeformMaster 用从真实视频学习到的物理-神经模型处理绳子、布料、包装和软玩具。它用可微 MPM 推进材料粒子，加入有界神经速度校正，并用 Gaussian Splatting 渲染新的动作 rollout。在 20 条真实 PhysTwin 序列上，它报告 IoU 为 0.748、Chamfer 为 0.011、PSNR 为 25.41，并支持超过 15 fps 的在线交互式 rollout。

#### Evidence
- [Sub-JEPA: Subspace Gaussian Regularization for Stable End-to-End World Models](../Inbox/2026-05-10--sub-jepa-subspace-gaussian-regularization-for-stable-end-to-end-world-models.md): Sub-JEPA 正则化方法和规划成功率结果。
- [DeformMaster: An Interactive Physics-Neural World Model for Deformable Objects from Videos](../Inbox/2026-05-10--deformmaster-an-interactive-physics-neural-world-model-for-deformable-objects-from-videos.md): DeformMaster 的动作条件可变形物体模型和评估指标。
