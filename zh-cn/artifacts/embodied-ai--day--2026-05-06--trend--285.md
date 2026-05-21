---
kind: trend
trend_doc_id: 285
granularity: day
period_start: '2026-05-06T00:00:00'
period_end: '2026-05-07T00:00:00'
topics:
- robot learning
- Vision-Language-Action
- latent actions
- visual foresight
- model predictive control
- world models
run_id: materialize-outputs
aliases:
- recoleta-trend-285
tags:
- recoleta/trend
- topic/robot-learning
- topic/vision-language-action
- topic/latent-actions
- topic/visual-foresight
- topic/model-predictive-control
- topic/world-models
language_code: zh-CN
---

# 机器人策略正在用紧凑前瞻和可部署控制来衡量

## Overview
当前重点是让机器人策略在部署约束下保留有用的内部状态。Vision-Language-Action (VLA) 工作集中在紧凑空间 token、潜在动作监督和测试时视觉校正。Dream-MPC 将同一压力带到连续控制：在线规划，同时减少模型调用。

## Clusters

### 用于 VLA 操作的紧凑空间前瞻
ConsisVLA-4D 将空间一致性当作推理预算问题处理。它保留 32 个与指令相关的视觉 token，在多个相机视角之间对齐这些 token，并用紧凑的潜在 token 存储几何信息。报告的收益同时来自准确率和速度：在 LIBERO 上，相比 OpenVLA 性能提升 21.6%，推理速度提高 2.3×；在真实机器人平台上，性能提升 41.5%，推理速度提高 2.4×。

T³VF 处理视觉前瞻 VLA 模型中的另一个失效点。它将预测的未来图像与随后观测到的图像进行比较，并且只在动作方差较低时更新可学习的查询 token。在带扰动训练的 LIBERO-Plus 上，它将 Mantis 的平均成功率从 49.3% 提高到 52.1%，在相机和光照扰动上的增益更大。

#### Evidence
- [ConsisVLA-4D: Advancing Spatiotemporal Consistency in Efficient 3D-Perception and 4D-Reasoning for Robotic Manipulation](../Inbox/2026-05-06--consisvla-4d-advancing-spatiotemporal-consistency-in-efficient-3d-perception-and-4d-reasoning-for-robotic-manipulation.md): 概述 ConsisVLA-4D 的 token 压缩、多视角 3D 感知、未来场景推理，以及报告的 LIBERO 和真实世界增益。
- [Test-Time Training for Visual Foresight Vision-Language-Action Models](../Inbox/2026-05-06--test-time-training-for-visual-foresight-vision-language-action-models.md): 概述 T³VF 的测试时训练机制、筛选式更新，以及 LIBERO-Plus 扰动结果。

### 作为 VLA 监督的潜在动作 token
这项潜在动作研究给出了许多 VLA 论文缺少的受控比较。它使用一个基于 Qwen3-VL-2B 的基线，在四种集成方法上测试基于图像的潜在动作和基于动作的潜在动作。最强结果取决于任务类型。LA-Direct 在 LIBERO-Long 上达到 96.6%，比基线高 10.8 个百分点。LA-Tok 在 RoboTwin 2.0 上达到 78.0% 的平均成功率，高 17.5 个百分点，并将 Move Can Pot 等偏重运动控制的任务从 46% 提高到 70%。

实际含义是：潜在动作在匹配监督问题时有用。图像派生 token 有助于长时程场景推理。动作派生 token 有助于在异构机器人数据中归一化运动控制。

#### Evidence
- [From Pixels to Tokens: A Systematic Study of Latent Action Supervision for Vision-Language-Action Models](../Inbox/2026-05-06--from-pixels-to-tokens-a-systematic-study-of-latent-action-supervision-for-vision-language-action-models.md): 概述统一的 VLA 基线、四种潜在动作监督策略，以及 LIBERO、LIBERO-Long 和 RoboTwin 2.0 结果。

### 潜在世界模型中的低成本在线规划
Dream-MPC 将部署约束下的思路用于连续控制。它只从策略先验中采样五个候选动作序列，在学习得到的潜在世界模型中进行 rollout，并使用预测奖励和终止价值执行一步梯度更新。不确定性惩罚会压低进入模型误差区域的计划，动作复用则在模型预测控制步骤之间保留优化工作。

效率数据很具体。在报告的设置中，Dream-MPC 每个时间步使用 15 次世界模型评估；引用的 MPPI 配置需要 9,216 次。在 24 个连续控制任务上配合 BMPC 时，它将 IQM 归一化分数提高 26.7%，将平均归一化分数提高 20.5%。配合 TD-MPC2 时，它优于仅用策略的基线，但没有稳定达到 TD-MPC2 加 MPPI 的水平。

#### Evidence
- [Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination](../Inbox/2026-05-06--dream-mpc-gradient-based-model-predictive-control-with-latent-imagination.md): 概述 Dream-MPC 方法、规划器设置、评估次数和基准结果。
