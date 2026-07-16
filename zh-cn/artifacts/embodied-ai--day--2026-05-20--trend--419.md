---
kind: trend
trend_doc_id: 419
granularity: day
period_start: '2026-05-20T00:00:00'
period_end: '2026-05-21T00:00:00'
topics:
- embodied AI
- vision-language-action
- robot manipulation
- 3D perception
- dexterous hands
- world models
- robot evaluation
run_id: materialize-outputs
aliases:
- recoleta-trend-419
tags:
- recoleta/trend
- topic/embodied-ai
- topic/vision-language-action
- topic/robot-manipulation
- topic/3d-perception
- topic/dexterous-hands
- topic/world-models
- topic/robot-evaluation
language_code: zh-CN
---

# 机器人研究把 3D 接触和真实测试平台当作主要证据

## 概览
具身 AI 是中心。视觉-语言-动作（VLA）论文现在主要看 3D 接触线索、真实硬件、扰动测试和可重复评测。GaussianDream、PointACT 和 VLA-REPLICA 给出的信号最强。

## 研究发现

### 3D-aware VLA control
几篇机器人论文把几何信息更直接地放到动作输出附近。GaussianDream 用 3D Gaussian 重建和短时域场景流预测训练一个 VLA 策略，然后在推理时去掉解码头，只保留学到的前缀 token。它在 LIBERO 上的平均成功率是 98.4%，在 RoboCasa Human-50 上是 52.6%。

PointACT 让动作解码器关注多尺度点云特征。它报告的 LIBERO 平均成功率是 96.0%，在同一张表里比 SpatialVLA 高 17.9 个百分点。DISC 处理的是另一类对齐失败：指令生成任务特定策略，控制策略只看观测。这个设计在 LIBERO-90 上达到 94.3%，在一个真实的 9 任务共享上下文设置中达到 86.4%。

#### 资料来源
- [GaussianDream: A Feed-Forward 3D Gaussian World Model for Robotic Manipulation](../Inbox/2026-05-20--gaussiandream-a-feed-forward-3d-gaussian-world-model-for-robotic-manipulation.md): GaussianDream training design and reported LIBERO, RoboCasa, and real-robot results.
- [PointACT: Vision-Language-Action Models with Multi-Scale Point-Action Interaction](../Inbox/2026-05-20--pointact-vision-language-action-models-with-multi-scale-point-action-interaction.md): PointACT point-cloud action interaction and LIBERO comparison results.
- [DISC: Decoupling Instruction from State-Conditioned Control via Policy Generation](../Inbox/2026-05-20--disc-decoupling-instruction-from-state-conditioned-control-via-policy-generation.md): DISC policy-generation design and simulated plus real manipulation results.

### Reproducible evaluation for robot policies and world models
评测工作变得更具体，也更容易重复。VLA-REPLICA 定义了一个真实世界 VLA 测试平台，硬件大约花费 1050 美元，包含 10 个操作任务、500 个示范和 90 个测试场景。在其同分布结果中，π0.5 以 0.54 的平均成功率领先被测策略，这也说明低成本物理平台还有很多提升空间。

stable-worldmodel 处理的是 world model 侧的问题，包含统一的数据加载、基线训练、模型预测控制规划，以及跨机器人和控制任务的评测。它的 Lance 数据层在本地达到每秒 4,815 个 Push-T 样本，而 HDF5 是 1,416 个。Lost in Fog 加入了一个驾驶 VLA 压力测试：Alpamayo R1 的因果链解释变化，和在噪声、光照变化和雾天条件下更大的轨迹偏移相关。

#### 资料来源
- [VLA-REPLICA: A Low-Cost, Reproducible Benchmark for Real-World Evaluation of Vision-Language-Action Models](../Inbox/2026-05-20--vla-replica-a-low-cost-reproducible-benchmark-for-real-world-evaluation-of-vision-language-action-models.md): VLA-REPLICA hardware cost, task suite, demonstrations, scenes, and policy results.
- [stable-worldmodel: A Platform for Reproducible World Modeling Research and Evaluation](../Inbox/2026-05-20--stable-worldmodel-a-platform-for-reproducible-world-modeling-research-and-evaluation.md): stable-worldmodel data layer, included baselines, benchmark coverage, and loading results.
- [Lost in Fog: Sensor Perturbations Expose Reasoning Fragility in Driving VLAs](../Inbox/2026-05-20--lost-in-fog-sensor-perturbations-expose-reasoning-fragility-in-driving-vlas.md): Driving VLA perturbation study and link between explanation changes and trajectory deviation.

### Dexterous manipulation with local sensing and hard safety
灵巧手论文关注能在硬件限制下保住的控制信号。Proprioceptive Transformer 只使用 tendon-driven ORCA 手的关节位置和速度历史。在一个 55 mm 立方体上，它的直接关节感知策略在三次 60 秒试验中达到 11.83 RPM，旋转准确率 100%，没有掉落。

SafePBDS 给几何运动策略加入了明确的安全约束。它在关节空间中求解加速度，同时把任务流形的安全条件作为硬约束。在 Franka Panda 加 Allegro Hand 上，它在 120 次家用物体抓取试验中报告 92.5% 的成功率，并且能在两个方向都完成超过 360° 的偏航重定向。

#### 资料来源
- [Learning Robust Dexterous In-Hand Manipulation from Joint Sensors with Proprioceptive Transformer](../Inbox/2026-05-20--learning-robust-dexterous-in-hand-manipulation-from-joint-sensors-with-proprioceptive-transformer.md): Proprioceptive Transformer joint-only sensing setup and real ORCA hand rotation results.
- [Safe and Steerable Geometric Motion Policies for Robotic Dexterous Manipulation](../Inbox/2026-05-20--safe-and-steerable-geometric-motion-policies-for-robotic-dexterous-manipulation.md): SafePBDS constraint formulation and hardware dexterous manipulation results.

### Cross-embodiment imitation through latent goals
Demo-JEPA 把示范当作一个目标信号，目标机器人要用自己的动力学去实现它。一个 V-JEPA 风格编码器把观测映射到潜在状态，Dreamer Predictor 估计一个与目标兼容的未来潜在目标，机器人再用自己的 world model 朝这个目标规划动作。

结果在迁移设置里最好。在仿真中，Demo-JEPA 在跨具身桥接上的平均成功率是 0.45，在零样本泛化上是 0.36，在报告的对比里超过了 VPP 和 XSkill。域内行为对齐更弱，RLBench 仿真是 0.31，真实世界行为对齐是 0.43。

#### 资料来源
- [Demo-JEPA: Joint-Embedding Predictive Architecture for One-shot Cross-Embodiment Imitation](../Inbox/2026-05-20--demo-jepa-joint-embedding-predictive-architecture-for-one-shot-cross-embodiment-imitation.md): Demo-JEPA latent-goal method and mixed cross-embodiment, zero-shot, and behavior-grounding results.
