---
kind: trend
trend_doc_id: 790
granularity: day
period_start: '2026-07-02T00:00:00'
period_end: '2026-07-03T00:00:00'
topics:
- robot learning
- vision-language-action policies
- world models
- test-time control
- robot data
run_id: materialize-outputs
aliases:
- recoleta-trend-790
tags:
- recoleta/trend
- topic/robot-learning
- topic/vision-language-action-policies
- topic/world-models
- topic/test-time-control
- topic/robot-data
language_code: zh-CN
---

# 机器人策略正在围绕控制环证据重建

## Overview
机器人学习正被放到控制环中评估。表现最强的论文加入未来变化先验、漂移监测器、critic、世界模型 rollout 和更便宜的运动数据，让视觉-语言-动作（VLA）策略能应对接触、相机变化和有限示范。Bridge-WA、VLA-Corrector 和 TAP 给出了最清楚的实测主张。

## Clusters

### 未来变化与运动预测
几篇论文把预测做得更贴近具体动作。Bridge-WA 将一个 5B 的未来变化教师模型蒸馏为未来 token、变化图和运动流图，并在部署时移除教师模型。它在 VLABench 上报告的平均成功率为 52.8%，高于所列最强成功率基线的 43.1%；在 Dobot hard-track 中，面对干扰物、光照变化和桌布变化时也有更强结果。

PhysMani 把同样的要求用于动态 3D 操作。它用 30,000 个 3D Gaussian 建模场景，并为移动目标预测局部速度场。在 PhysMani-Bench 上，它报告的平均仿真成功率为 45.9%，领先于所列 3D 策略和 Gaussian 基线，但在 Insert Peg 等部分任务上仍然落后。

#### Evidence
- [Bridge-WA: Predicting Where and How the World Changes for Robotic Action](../Inbox/2026-07-02--bridge-wa-predicting-where-and-how-the-world-changes-for-robotic-action.md): Bridge-WA 的摘要、方法，以及 VLABench/Dobot 结果。
- [PhysMani: Physics-principled 3D World Model for Dynamic Object Manipulation](../Inbox/2026-07-02--physmani-physics-principled-3d-world-model-for-dynamic-object-manipulation.md): PhysMani 的摘要、3D Gaussian 方法、基准结果和任务限制。

### 动作块和计划的测试时引导
推理时控制是一个主要主题。VLA-Corrector 冻结 VLA 主干，监测预期视觉潜变量变化与观测视觉潜变量变化，截断过期动作块，并引导下一步 flow-matching 去噪。在 MetaWorld 上，pi0.5 的平均成功率从 48.70% 升至 64.35%；horizon 为 10 时，SmolVLA 提高成功率，同时减少策略调用。

Guided Action Flow 使用学到的动作块 critic 来引导冻结的 SmolVLA 采样器。增益在局部设置中最强：一个 LIBERO 空间任务提高 14 个百分点，而锁定 held-out 测试的增益为 2.5 个百分点。ACID 为世界模型规划加入单独检查，判断预测的潜变量转移是否与条件动作一致；它无需重新训练世界模型，就提高了 Le-WM 和 PLDM 操作任务的成功率。

#### Evidence
- [VLA-Corrector: Lightweight Detect-and-Correct Inference for Adaptive Action Horizon](../Inbox/2026-07-02--vla-corrector-lightweight-detect-and-correct-inference-for-adaptive-action-horizon.md): VLA-Corrector 的检测与纠正方法，以及 MetaWorld/LIBERO 结果。
- [Guided Action Flow: Q-Guided Inference for Flow-Matching Vision-Language-Action Policies](../Inbox/2026-07-02--guided-action-flow-q-guided-inference-for-flow-matching-vision-language-action-policies.md): Guided Action Flow 的 critic 引导推理，以及 LIBERO 验证/held-out 结果。
- [ACID: Action Consistency via Inverse Dynamics for Planning with World Models](../Inbox/2026-07-02--acid-action-consistency-via-inverse-dynamics-for-planning-with-world-models.md): ACID 的逆动力学一致性代价，以及跨世界模型的规划结果。

### 更低成本的机器人经验
研究正在用无标签运动和生成 rollout 降低数据成本。TAP 先在任务无关轨迹上用逆动力学预训练 VLA，再进行语言条件行为克隆。在 SIMPLER 中，TAP-20k 达到 33.32% Avg-All 成功率；同一架构使用标准行为克隆训练时为 23.15%。在真实 WidowX 测试中，它在背景和视角变化下改进了 push-pumpkin 任务。

WorldSample 用真实 rollout 初始化局部动作扰动，使用经过适配的 Cosmos-Predict2.5 世界模型生成未来观测，用奖励模型打标签，并把选出的合成转移输入真实机器人强化学习。在五个操作任务上，它报告的平均成功率为 82%，高于 HIL-SERL 的 56%，同时把平均训练步数从 56K 降至 23K。

#### Evidence
- [Learning to Move Before Learning to Do: Task-Agnostic pretraining for VLAs](../Inbox/2026-07-02--learning-to-move-before-learning-to-do-task-agnostic-pretraining-for-vlas.md): TAP 的任务无关预训练方法，以及 SIMPLER/真实世界结果。
- [WorldSample: Closed-loop Real-robot RL with World Modelling](../Inbox/2026-07-02--worldsample-closed-loop-real-robot-rl-with-world-modelling.md): WorldSample 的真实-合成训练循环、成功率和训练步数减少。

### 相机和布局泛化数据
The Moving Eye 分离了 VLA 训练数据中的相机捷径和物体位置捷径。它的双臂设置用一个机器人执行操作，另一个机器人作为移动环境相机，然后把移动相机 episode 与静态多视角 episode 混合。在 pen 任务上，固定视角训练达到 85.0% 的分布内成功率，但在移动相机评估下只有 43.0%。混合数据达到 86.0% 的分布内成功率，在移动相机测试下达到 83.0%。

物体位置测试显示了相同模式。移动 holder 后，multi-fixed 基线从 95.0% 降至 71.9%，而 mixed 1:3 设置报告为 91.9% 和 90.6%。摘录中 Gr00t pen-task 的最佳比例是 Moving:Multi-Fixed = 1:3。

#### Evidence
- [The Moving Eye: Enhancing VLA Spatial Generalization via Hybrid Dynamic Data Collection](../Inbox/2026-07-02--the-moving-eye-enhancing-vla-spatial-generalization-via-hybrid-dynamic-data-collection.md): The Moving Eye 的数据设置、捷径分析、移动相机结果和物体位置结果。
