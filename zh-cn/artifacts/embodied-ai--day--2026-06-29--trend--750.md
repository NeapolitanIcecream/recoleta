---
kind: trend
trend_doc_id: 750
granularity: day
period_start: '2026-06-29T00:00:00'
period_end: '2026-06-30T00:00:00'
topics:
- robot learning
- vision-language-action models
- manipulation
- test-time RL
- tactile sensing
- navigation
- autonomous driving
run_id: materialize-outputs
aliases:
- recoleta-trend-750
tags:
- recoleta/trend
- topic/robot-learning
- topic/vision-language-action-models
- topic/manipulation
- topic/test-time-rl
- topic/tactile-sensing
- topic/navigation
- topic/autonomous-driving
language_code: zh-CN
---

# 机器人策略评估开始看执行机制，不能只看基准分数

## Overview
机器人学习工作集中在让策略能在真实控制约束下执行。ZR-0、T2VLA 和 Chronos 显示出主要重点：跨具身监督、无需奖励的测试时改进，以及基于完整轨迹的记忆。

## Clusters

### 视觉-语言-动作策略训练
视觉-语言-动作（VLA）论文关注策略学习中决定高层模型能否控制机器人的部分。ZR-0 训练了一个 2.6B 参数的 VLA 模型，使用密集的具身思维链标签；推理时跳过文本生成，由扩散动作专家输出连续动作块。它在 LIBERO 上报告 97.8% 的平均成功率，并使用 ProcCorpus-60M，其中约有 60M 帧，96.8% 的帧带有 ECoT 标签。

T2VLA 在测试时加入强化学习（RL），使用策略自身的置信度作为奖励信号。在 LIBERO 上，它将 OpenVLA-OFT 的平均成功率从 91.0% 提高到 97.2%，将 π0 从 57.7% 提高到 81.9%，将 π0.5 从 77.1% 提高到 85.1%。SA-VLA 处理一个更低层的失败点：固定动作 token 解码。它的状态感知 tokenizer 将 RoboTwin 平均成功率提高到 0.56，而列出的最强 tokenizer 基线为 0.29。

#### Evidence
- [Training Vision-Language-Action Models with Dense Embodied Chain-of-Thought Supervision](../Inbox/2026-06-29--training-vision-language-action-models-with-dense-embodied-chain-of-thought-supervision.md): ZR-0 架构、ProcCorpus-60M 规模和 LIBERO 结果。
- [Trust Your Instincts: Confidence-Driven Test-Time RL for Vision-Language-Action Models](../Inbox/2026-06-29--trust-your-instincts-confidence-driven-test-time-rl-for-vision-language-action-models.md): T2VLA 由置信度驱动的测试时 RL 方法和 LIBERO 增益。
- [SA-VLA: State-aware tokenizer for improving Vision-Language-Action Models' performance](../Inbox/2026-06-29--sa-vla-state-aware-tokenizer-for-improving-vision-language-action-models-performance.md): SA-VLA 状态感知 tokenizer 设计和 RoboTwin 结果。

### 长程操作和几何执行
多个系统把任务阶段、物体几何和恢复流程显式纳入控制。Chronos 将完整观察历史作为策略状态，用于同一相机视图可能需要不同动作的长程操作。它在 RMBench 上报告 73.6% 的平均成功率，在四个真实世界双臂任务上的平均成功率为 78%。

OpenSPM 从演示中存储相对于物体的关键姿态，并用 6D 物体姿态估计来迁移这些姿态。它的 0.24M 参数动作模型在 10 个 LIBERO-GOAL 任务上报告 85.6% 的成功率，动作块生成延迟为 4.8 ms。Spark 使用一个由 LLM 生成的行为树，然后在测试时把计算用于物体定位和重试逻辑。它在六个 Libero-Pro 扰动单元上的平均成功率为 43.7%，在 11 个实体机器人任务单元上的平均成功率为 68%。

#### Evidence
- [Chronos: A Physics-Informed Full-History Framework for Non-Markovian Long-Horizon Manipulation](../Inbox/2026-06-29--chronos-a-physics-informed-full-history-framework-for-non-markovian-long-horizon-manipulation.md): Chronos 完整历史策略状态以及 RMBench/真实世界成功率。
- [OpenSPM: An Environment-Transferable Robotic Key Spatial Pose Memory and Closed-Loop High-Frequency Flow-Matching Action Generation Model](../Inbox/2026-06-29--openspm-an-environment-transferable-robotic-key-spatial-pose-memory-and-closed-loop-high-frequency-flow-matching-action-generation-model.md): OpenSPM 关键姿态记忆、模型大小、延迟和 LIBERO-GOAL 结果。
- [Sequential Planning via Anchored Robotic Keypoints](../Inbox/2026-06-29--sequential-planning-via-anchored-robotic-keypoints.md): Spark 行为树规划、感知重试以及仿真/真实机器人结果。

### 验证、部署和触觉传感
这一时期也显示出策略迭代对测量和传感的依赖。Critical Interval MSE 只给任务关键轨迹片段打分，并在比较预测动作和专家动作之前对齐动作序列。在 LBM-Eval 上，它与 rollout 成功率的 Spearman ρ = -0.87，而原始 MSE 为 -0.61。

UR5e 案例研究展示了另一个部署问题。OpenVLA 在 A100 上的推理速度约为 3 Hz；作者报告称，当动作语义、坐标系、时序、预处理和数据覆盖不匹配时，闭环行为不稳定。Heterogeneous Tactile Transformer 将这一工程重点扩展到接触传感，在光学传感器和阵列传感器上训练一个触觉骨干模型。在未见过的 Sharpa 指尖、无相机真实世界测试中，它在 toy screw 上达到 95% 成功率，在 grasp tofu 上达到 55%。

#### Evidence
- [Critical Interval MSE: Toward Reliable Offline Validation for Robot Manipulation Policies](../Inbox/2026-06-29--critical-interval-mse-toward-reliable-offline-validation-for-robot-manipulation-policies.md): CI-MSE 定义以及它与 rollout 成功率的相关性结果。
- [Vision-Language-Action Models: Experimental Insights from a Real-World UR5 Platform](../Inbox/2026-06-29--vision-language-action-models-experimental-insights-from-a-real-world-ur5-platform.md): UR5e VLA 部署流程、推理速度和闭环不稳定发现。
- [Heterogeneous Tactile Transformer](../Inbox/2026-06-29--heterogeneous-tactile-transformer.md): HTT 配对触觉预训练和真实世界触觉操作结果。

### 用于导航和驾驶的世界模型
世界模型工作出现在导航和自动驾驶中，规划与预测的未来观察绑定。SWAM 在一次扩散过程中为视觉导航生成中间 RGB-D 序列和 2D 动作。它将 RECON 绝对轨迹误差降至 0.93，NWM+NoMaD x16 为 1.53；每个 episode 运行 16.91 秒，而该采样规划器为 245.98 秒。

LWDrive 使用视觉-语言模型（VLM）生成粗略驾驶轨迹，然后用世界模型监督特征和鸟瞰图几何来细化候选轨迹。它在 NAVSIM 上报告 92.0 PDMS，在 NAVSIM-v2 上报告 89.6 EPDMS。X-Morph 覆盖了另一种控制设置：它将人体运动映射为四足、六足和四足-机械臂行为。在 Go2 clips 上，它的物理校正器将足端滑移减少 27.2%，将 penetration p95 减少 46.9%。

#### Evidence
- [Pondering the Way: Spatial-perceiving World Action Model for Embodied Navigation](../Inbox/2026-06-29--pondering-the-way-spatial-perceiving-world-action-model-for-embodied-navigation.md): SWAM 联合观察-动作生成和导航指标。
- [LWDrive: Layer-Wise World-Model-Guided Vision-Language Model Planning for Autonomous Driving](../Inbox/2026-06-29--lwdrive-layer-wise-world-model-guided-vision-language-model-planning-for-autonomous-driving.md): LWDrive VLM 规划方法以及 NAVSIM/NAVSIM-v2 分数。
- [X-Morph: Human Motion Priors for Scalable Robot Learning Across Morphologies](../Inbox/2026-06-29--x-morph-human-motion-priors-for-scalable-robot-learning-across-morphologies.md): X-Morph 跨形态运动迁移和物理校正指标。
