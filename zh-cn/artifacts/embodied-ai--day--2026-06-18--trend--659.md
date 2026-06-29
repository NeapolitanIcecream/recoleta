---
kind: trend
trend_doc_id: 659
granularity: day
period_start: '2026-06-18T00:00:00'
period_end: '2026-06-19T00:00:00'
topics:
- robotics
- vision-language-action
- world models
- robot policy safety
- data efficiency
run_id: materialize-outputs
aliases:
- recoleta-trend-659
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/world-models
- topic/robot-policy-safety
- topic/data-efficiency
language_code: zh-CN
---

# 机器人 VLA 工作正集中于可部署的控制机制

## Overview
当天的研究主要集中在机器人。视觉-语言-动作（VLA）论文关注如何让策略成本更低、更理解几何，并能更安全地在硬件上运行。EquiVLA、CLP 和 Qwen-RobotWorld 给出主要方向：实际控制增益需要动作头、训练循环和预测模型中的结构。

## Clusters

### 结构化动作生成
几篇论文把控制结构加入策略输出内部，没有把机器人动作当作扁平向量处理。EquiVLA 在冻结的视觉-语言骨干和流匹配动作头中加入旋转等变性，在 LIBERO 相对控制上达到 92.6% 平均成功率，在五个 Mobile ALOHA 真实机器人任务上达到 72% 平均成功率。Co-VLA 将双臂动作分成共享协调潜变量和每条手臂的残差潜变量；它报告的最大增益来自 Handover Block Easy：成功率 91%，π0 基线为 64%。FAFM 预测连续轨迹的频率系数，用于处理混合控制频率，并在不增加网络参数的情况下让运动更平滑。

#### Evidence
- [EquiVLA: A General Framework for Rotationally Equivariant Vision-Language-Action Models](../Inbox/2026-06-18--equivla-a-general-framework-for-rotationally-equivariant-vision-language-action-models.md): EquiVLA 方法，以及在 LIBERO、CALVIN 和 Mobile ALOHA 上报告的增益。
- [Co-VLA: Coordination-Aware Structured Action Modeling for Dual-Arm Vision-Language-Action Systems](../Inbox/2026-06-18--co-vla-coordination-aware-structured-action-modeling-for-dual-arm-vision-language-action-systems.md): Co-VLA 的结构化双臂动作头和双手任务结果。
- [Frequency-Aware Flow Matching for Continuous and Consistent Robotic Action Generation](../Inbox/2026-06-18--frequency-aware-flow-matching-for-continuous-and-consistent-robotic-action-generation.md): FAFM 的频域动作预测和平滑性结果。

### 更低成本的适配和有针对性的数据修复
效率收益有具体数字。CLP 在微调前剪除冗余层，并保留原始训练目标。在 LIBERO 上的 π0、GR00T-N1.5 和 SmolVLA 三个模型中，它将模型大小减少 21.3% 到 25.9%，将可训练参数减少 25.8% 到 37.0%，并降低三种模型在 RTX 4070 上的推理延迟。Pose6DAug 处理另一个瓶颈：失败对象。它把新的 3D 对象换入成功的多视角机器人 episode，同时保留 6D 位姿和接触几何。在 RoboCasa365 Counter-to-Cabinet 失败 episode 上，它报告的平均成功率为 22.8%，VACE 为 16.4%，MimicGen 为 15.8%。

#### Evidence
- [Finetuning Vision-Language-Action Models Requires Fewer Layers Than You Think](../Inbox/2026-06-18--finetuning-vision-language-action-models-requires-fewer-layers-than-you-think.md): CLP 的剪枝方法，以及计算、延迟和成功率结果。
- [Pose6DAug: Physically Plausible Multi-view Object Swapping for Robot Data Augmentation](../Inbox/2026-06-18--pose6daug-physically-plausible-multi-view-object-swapping-for-robot-data-augmentation.md): Pose6DAug 数据增强方法和 RoboCasa365 失败案例结果。

### 具身世界模型需要基于动作的检查
世界模型论文把预测质量当作控制问题处理。Qwen-RobotWorld 使用语言作为共享动作接口，在操作、驾驶、导航和人到机器人场景中预测未来视频；它用 8.6M 个视频-文本样本和超过 200M 帧训练。Reward as An Agent 增加一个基于 VLM 的评估器，评估视觉质量、指令遵循、物理合规性和任务完成情况，然后在 RL 后训练期间使用动态区域探索。Sensorimotor World Models 采用较小规模的路线：用逆动力学正则化潜变量预测，使学到的状态保留与动作相关的变量，并丢弃干扰项。

#### Evidence
- [Unifying Embodied World Modeling Through Language-Conditioned Video Gen](../Inbox/2026-06-18--unifying-embodied-world-modeling-through-language-conditioned-video-gen.md): Qwen-RobotWorld 的语言条件视频世界模型和训练规模。
- [Reward as An Agent for Embodied World Models](../Inbox/2026-06-18--reward-as-an-agent-for-embodied-world-models.md): 面向具身世界模型的奖励评估器设计和动态感知 GRPO。
- [Sensorimotor World Models: Perception for Action via Inverse Dynamics](../Inbox/2026-06-18--sensorimotor-world-models-perception-for-action-via-inverse-dynamics.md): 用于保留动作相关潜变量世界模型的逆动力学正则化。

### 运行时验证正在成为机器人学习的一部分
安全和自动化论文把检查放进循环中。Tri-Info 根据近期状态和动作嵌入上的熵与互信息预测 VLA rollout 失败。它报告在 sim-to-real 迁移下的真实世界任务准确率为 83%，并给出与动作多样性、时间一致性或弱状态-动作耦合相关的警报。ENPIRE 为真实机器人上的编码 agent 提供重置、rollout、验证和代码编辑 API。论文报告在灵巧任务上的成功率最高为 99%，并显示 8 个机器人-agent worker 并行运行时改进更快。Slow Brain, Fast Planner 将同样的实用逻辑用于导航：一个慢速视觉-语言模型在快速规划器轨迹中做选择，延迟到达的选择会融合进实时规划器分数。

#### Evidence
- [Tri-Info: Generalizable, Interpretable Failure Prediction for VLA Models via Information Theory](../Inbox/2026-06-18--tri-info-generalizable-interpretable-failure-prediction-for-vla-models-via-information-theory.md): Tri-Info 的失败预测信号和迁移结果。
- [ENPIRE: Agentic Robot Policy Self-Improvement in the Real World](../Inbox/2026-06-18--enpire-agentic-robot-policy-self-improvement-in-the-real-world.md): ENPIRE 的 agentic 真实机器人改进循环和集群扩展结果。
- [Slow Brain, Fast Planner: Latency-Resilient VLM-Augmented Urban Navigation](../Inbox/2026-06-18--slow-brain-fast-planner-latency-resilient-vlm-augmented-urban-navigation.md): 抗延迟的 VLM 增强导航方法和 ADE/仿真结果。
