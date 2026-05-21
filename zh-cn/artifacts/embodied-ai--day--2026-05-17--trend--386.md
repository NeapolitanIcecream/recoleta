---
kind: trend
trend_doc_id: 386
granularity: day
period_start: '2026-05-17T00:00:00'
period_end: '2026-05-18T00:00:00'
topics:
- vision-language-action
- robot manipulation
- reinforcement learning
- affordance learning
- 3D planning
- interpretability
- autonomous driving safety
run_id: materialize-outputs
aliases:
- recoleta-trend-386
tags:
- recoleta/trend
- topic/vision-language-action
- topic/robot-manipulation
- topic/reinforcement-learning
- topic/affordance-learning
- topic/3d-planning
- topic/interpretability
- topic/autonomous-driving-safety
language_code: zh-CN
---

# 机器人 VLA 论文要求具备接触感知控制和行为层验证

## Overview
这一时期的视觉-语言-动作（VLA）机器人研究以执行为中心。DyGRO-VLA 在强化学习期间保护多任务策略。AffordVLA 在不增加运行时模块的情况下教授接触区域。RoboFlow4D 为闭环控制加入快速 3D 运动计划。

## Clusters

### 多任务 VLA 控制和接触定位
DyGRO-VLA 将强化学习视为对基础机器人策略的受控修改。它冻结基础 VLA，并训练路由残差专家来添加增量动作片段。在 LIBERO 上，它报告的平均成功率为 97.1%，比离线基础模型高 +4.4 个百分点；在 LIBERO-Long 上高 +9.8 个百分点。

AffordVLA 处理另一类失效模式：策略可能选对物体，但仍接触到错误部位。它在训练期间将中间 VLA 视觉 token 与冻结的可供性教师模型对齐，然后在推理时移除教师模型。论文报告称，相比此前最佳基线，RoboTwin 在 Easy 设置下提升 20.5%，在 Hard 设置下提升 12.8%。

#### Evidence
- [DyGRO-VLA: Cross-Task Scaling of Vision-Language-Action Models via Dynamic Grouped Residual Optimization](../Inbox/2026-05-17--dygro-vla-cross-task-scaling-of-vision-language-action-models-via-dynamic-grouped-residual-optimization.md): DyGRO-VLA 方法，以及报告的 LIBERO、LIBERO-Long 和 RoboTwin2 结果。
- [AffordVLA: Injecting Affordance Representations into Vision-Language-Action Models via Implicit Feature Alignment](../Inbox/2026-05-17--affordvla-injecting-affordance-representations-into-vision-language-action-models-via-implicit-feature-alignment.md): AffordVLA 训练设置、推理时移除可供性教师模型，以及 RoboTwin 提升。

### 用于闭环操作的 3D 规划信号
RoboFlow4D 使用预测的 3D 夹爪流作为策略可跟踪的显式计划。它的慢-快循环规划较低频率的轨迹，并让动作策略执行较高频率的动作片段。论文报告称，在 LIBERO 上，使用 Diffusion Policy 提升 +6.2 个百分点，使用 DiT 策略提升 +4.0 个百分点，并且规划延迟低于 1 秒。

Visual Sculpting 在可变形物体操作中也重视这类信号。它基于密集的 512×512 深度图和空间深度梯度进行规划，然后在执行小批量动作后用模型预测控制重新规划。该系统生成了超过 100 个动作的长时程黏土序列；在报告的留出测试中，其视觉损失改进了泡沫和面团变形指标。

#### Evidence
- [RoboFlow4D: A Lightweight Flow World Model Toward Real-Time Flow-Guided Robotic Manipulation](../Inbox/2026-05-17--roboflow4d-a-lightweight-flow-world-model-toward-real-time-flow-guided-robotic-manipulation.md): RoboFlow4D 的 3D 流规划方法、慢-快控制、基准提升和延迟声明。
- [Visual Sculpting: Visually-Aligned Planning Representations for Long-Horizon Robot Clay Sculpting](../Inbox/2026-05-17--visual-sculpting-visually-aligned-planning-representations-for-long-horizon-robot-clay-sculpting.md): Visual Sculpting 的密集深度表示、MPC 循环、变形结果和长时程运行。

### 面向 VLA 可解释性和安全性的行为层检查
Event-Grounded Sparse Autoencoders 通过将特征锚定到反复出现的 rollout 事件，把稀疏自编码器（SAE）用于机器人策略。该流程提取末端执行器关键帧，按视觉和机器人状态线索聚类，然后通过闭环干预测试特征。在 OpenVLA 第 31 层，将 event-aligned 特征置零使成功率从 70.0% 降到 48.8%，影响大于 window-mean、task-mean 或 random-alive 排名。

自动驾驶安全论文测试 Alpamayo-R1-10B 中的 Chain-of-Causation（CoC）解释是否与场景和轨迹一致。在带障碍物上下文的推理中，整体推理忠实度为 42.5%。研究还报告了 94 次漏检行人、53.3% 的低推理-动作一致性，以及 37.9% 声称停车的案例实际继续行驶。

#### Evidence
- [Event-Grounded Sparse Autoencoders for Vision-Language-Action Policies](../Inbox/2026-05-17--event-grounded-sparse-autoencoders-for-vision-language-action-policies.md): 事件锚定 SAE 流程和闭环干预结果。
- [Is VLA Reasoning Faithful? Probing Safety of Chain-of-Causation](../Inbox/2026-05-17--is-vla-reasoning-faithful-probing-safety-of-chain-of-causation.md): VLA 驾驶推理忠实度评估、行人漏检和推理-动作不匹配结果。
