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
这一时期的机器人研究把可靠性当作一个可测量的控制问题来处理。Vision-Language-Action（VLA）策略加入恢复训练、由不确定性触发的搜索，以及面向门店的动作数据。RePO-VLA、CAPS 和 SABER 给出了最强的定量信号。

## Clusters

### VLA failure recovery and long-horizon control
两篇论文直接处理执行漂移。RePO-VLA 用成功、失败和恢复轨迹分别训练，再在部署时使用固定的高 value 条件，不用在线失败检测器。它报告的对抗成功率平均从 20% 提高到 75%，FRBench-Sim 覆盖 46 个任务中的 23,453 个双臂 episode。

CAPS 保持基础 VLA 策略不变，只在不确定性上升时增加推理开销。它用幂分布采样未来动作块，并在熵超过阈值时使用 Metropolis-Hastings 搜索。在 RoboTwin 1.0 上配合 π0，平均成功率为 47.4%，而 π0 为 32.2%，π0 加 TACO 为 41.3%。在 Simpler-WindowX 上，它报告平均成功率 60.5%，领先 π0 和多个 VLA 基线。

#### Evidence
- [RePO-VLA: Recovery-Driven Policy Optimization for Vision-Language-Action Models](../Inbox/2026-05-10--repo-vla-recovery-driven-policy-optimization-for-vision-language-action-models.md): RePO-VLA method, FRBench-Sim scale, and adversarial success figures.
- [Drift is a Sampling Error: SNR-Aware Power Distributions for Long-Horizon Robotic Planning](../Inbox/2026-05-10--drift-is-a-sampling-error-snr-aware-power-distributions-for-long-horizon-robotic-planning.md): CAPS inference-time search method and benchmark results on RoboTwin and Simpler-WindowX.

### Domain-specific action data for real environments
SABER 用具体数字说明了零售机器人里的数据问题。这个数据集用了大约 100 小时的杂货店采集内容，把人类活动转换成 44.8K 个训练样本：25K 个 latent-action 序列、18.6K 个手部姿态轨迹和 1.2K 个全身运动序列。在这些数据流上后训练后的 GR00T N1.6 在 10 个 RoboBenchMart 任务上的平均成功率达到 29.3%，而只用仿真微调时为 13.4%。

DRIS 处理的是灵巧 sim-to-real 迁移中的另一类数据缺口。每个模拟 episode 都包含多个具有不同动力学的对象实例，并在同一个机器人动作下同时推进。论文声称它能对平板反应式接球实现零样本真实迁移，但可见摘录没有给出真实试验成功率，因此这里的证据更强的是训练设计，而不是部署结果。

#### Evidence
- [SABER: A Scalable Action-Based Embodied Dataset for Real-World VLA Adaptation](../Inbox/2026-05-10--saber-a-scalable-action-based-embodied-dataset-for-real-world-vla-adaptation.md): SABER dataset composition and RoboBenchMart success comparison.
- [Zero-Shot Sim-to-Real Robot Learning: A Dexterous Manipulation Study on Reactive Catching](../Inbox/2026-05-10--zero-shot-sim-to-real-robot-learning-a-dexterous-manipulation-study-on-reactive-catching.md): DRIS training setup and limits of the visible quantitative evidence.

### World models built for action rollout
世界模型论文关注的是能指导控制的预测。Sub-JEPA 通过低维高斯检验来正则化潜空间，而不是把整个潜向量强行约束成各向同性高斯。与 LeWorldModel 相比，它在报告的四个任务上都提高了规划成功率，包括 Two-Room 的 95.00±2.76% 和 OGB-Cube 的 76.33±5.99%。

DeformMaster 用从真实视频中学习到的物理-神经模型处理绳子、布料、包裹和软玩具。它用可微 MPM 推进材料粒子，加入有界的神经速度修正，再用 Gaussian Splatting 渲染新的动作轨迹。在 20 个真实 PhysTwin 序列上，它报告 IoU 0.748、Chamfer 0.011、PSNR 25.41，在线交互式 rollout 速度高于 15 fps。

#### Evidence
- [Sub-JEPA: Subspace Gaussian Regularization for Stable End-to-End World Models](../Inbox/2026-05-10--sub-jepa-subspace-gaussian-regularization-for-stable-end-to-end-world-models.md): Sub-JEPA regularization method and planning success results.
- [DeformMaster: An Interactive Physics-Neural World Model for Deformable Objects from Videos](../Inbox/2026-05-10--deformmaster-an-interactive-physics-neural-world-model-for-deformable-objects-from-videos.md): DeformMaster action-conditioned deformable-object model and evaluation metrics.
