---
kind: trend
trend_doc_id: 388
granularity: week
period_start: '2026-05-11T00:00:00'
period_end: '2026-05-18T00:00:00'
topics:
- robotics
- vision-language-action
- world models
- robot manipulation
- embodied AI
- safety evaluation
run_id: materialize-outputs
aliases:
- recoleta-trend-388
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/world-models
- topic/robot-manipulation
- topic/embodied-ai
- topic/safety-evaluation
language_code: zh-CN
---

# 机器人 VLA 进展正在由真实控制压力下的执行表现来评判

## Overview
本周最强的信号是机器人视觉-语言-动作（VLA）模型的执行质量。HarmoWAM、RAW-Dream 和 Pelican-Unified 的工作将策略增益与想象 rollouts、阶段感知动作控制和共享的推理-动作状态联系起来。

## Clusters

### 世界模型训练与适配
世界模型现在被用作训练空间和控制先验，同时减少任务特定机器人数据的压力很明确。HarmoWAM 将视频世界模型与预测式、反应式动作专家结合起来，再在移动阶段和交互阶段之间路由控制。它报告的域外增益是在六个真实世界任务上比先前 VLA 模型高 33 个百分点，比先前世界动作模型（WAMs）高 29 个百分点。

RAW-Dream 给出了本周最明确的数据效率主张。它在一个任务无关的视频世界模型中用强化学习训练 OpenVLA-OFT，并使用 Qwen3-VL 做奖励判断。在 LIBERO 上，它用 10 个目标演示、且不使用目标 rollouts 训练世界模型，将 1-shot 监督微调基线从 43.4% 提高到 52.3%；加入域内世界模型调优后，达到 66.0%。

#### Evidence
- [HarmoWAM: Harmonizing Generalizable and Precise Manipulation via Adaptive World Action Models](../Inbox/2026-05-11--harmowam-harmonizing-generalizable-and-precise-manipulation-via-adaptive-world-action-models.md): HarmoWAM 摘要给出了双专家设计、阶段门控、真实世界评估设置和 OOD 增益。
- [Reinforcing VLAs in Task-Agnostic World Models](../Inbox/2026-05-12--reinforcing-vlas-in-task-agnostic-world-models.md): RAW-Dream 摘要提供了任务无关世界模型训练设置和 LIBERO 数据效率结果。

### 动作时机与空间定位
几篇论文都瞄准决定 VLA 策略是否成功的具体时刻和场景特征。GuidedVLA 将动作解码器注意力头分配给对象定位、技能阶段识别和基于深度的几何信息。在 LIBERO-Plus 上，完整模型达到 75.4% 的平均成功率，高于其 π0 基座的 68.2%；在真实世界试验中，它在域内、场景变化和光照变化设置下都优于基座策略。

FrameSkip 将密集演示视为不均衡的监督信号。它保留 20% 的唯一帧，保护夹爪转换帧和动作变化大的帧，并将 RoboCasa-GR1、SimplerEnv 和 LIBERO 上的宏平均从 66.50% 提高到 76.15%。Evo-Depth 和 AffordVLA 加入互补的空间信号：前者使用 RGB 推导的深度来改进放置和抓取，后者在训练时对齐接触区域的 affordance，无需增加推理模块。

#### Evidence
- [GuidedVLA: Specifying Task-Relevant Factors via Plug-and-Play Action Attention Specialization](../Inbox/2026-05-12--guidedvla-specifying-task-relevant-factors-via-plug-and-play-action-attention-specialization.md): GuidedVLA 摘要给出了动作头专门化，以及在 LIBERO-Plus、扰动、RoboTwin 2.0 和真实世界试验上的结果。
- [FrameSkip: Learning from Fewer but More Informative Frames in VLA Training](../Inbox/2026-05-13--frameskip-learning-from-fewer-but-more-informative-frames-in-vla-training.md): FrameSkip 摘要报告了 20% 帧保留设置和基准增益。
- [Evo-Depth: A Lightweight Depth-Enhanced Vision-Language-Action Model](../Inbox/2026-05-14--evo-depth-a-lightweight-depth-enhanced-vision-language-action-model.md): Evo-Depth 摘要给出了 RGB 推导深度设计、模型规模、基准结果、内存使用和推理速率。
- [AffordVLA: Injecting Affordance Representations into Vision-Language-Action Models via Implicit Feature Alignment](../Inbox/2026-05-17--affordvla-injecting-affordance-representations-into-vision-language-action-models-via-implicit-feature-alignment.md): AffordVLA 摘要解释了 affordance 特征对齐、接触区域聚焦，以及不增加推理成本的主张。

### 长程与多任务控制
长程执行被当作带共享状态和受保护任务知识的控制问题来处理。Pelican-Unified 训练一个具身模型，通过共同的潜在状态进行语言推理、预测未来视频并输出动作块。它报告在包含 50 个任务的 RoboTwin 双臂基准上达到 93.5% 的平均成功率，在 WorldArena 上 EWM Score 为 66.03。

DyGRO-VLA 关注模仿训练后的强化学习。它冻结一个基础 VLA，并学习带路由的残差专家来修正动作块，从而减少多任务调优对共享表征的损伤。它报告在 LIBERO 上达到 97.1% 的平均成功率，在 LIBERO-Long 上比其离线基座提高 9.8 个百分点。

#### Evidence
- [Pelican-Unified 1.0: A Unified Embodied Intelligence Model for Understanding, Reasoning, Imagination and Action](../Inbox/2026-05-14--pelican-unified-1-0-a-unified-embodied-intelligence-model-for-understanding-reasoning-imagination-and-action.md): Pelican-Unified 摘要提供了共享潜在状态设计，以及 RoboTwin、WorldArena 和 VLM 基准结果。
- [DyGRO-VLA: Cross-Task Scaling of Vision-Language-Action Models via Dynamic Grouped Residual Optimization](../Inbox/2026-05-17--dygro-vla-cross-task-scaling-of-vision-language-action-models-via-dynamic-grouped-residual-optimization.md): DyGRO-VLA 摘要提供了冻结基座的残差 RL 设计，以及 LIBERO、LIBERO-Long 和 RoboTwin2 结果。

### 安全性与行为级验证
评估开始检查 rollout 过程中发生了什么，而不只看最终任务状态。SafeManip 使用有限迹线性时序逻辑监控器，在碰撞、稳定抓取、包含、清洁和固定装置访问等谓词上定义时序安全属性。在 50 个 RoboCasa365 任务中，π0.5 相比 π0 将任务成功率从 8.1% 提高到 9.3%，但其安全违规率从 69.7% 上升到 82.8%。

本周的接触感知 VLA 工作也有同样的关注点。AffordVLA 训练策略关注功能性接触区域，5 月 17 日的趋势笔记将行为级检查列为 VLA 可解释性和安全性的一部分。这些证据指向更严格的部署门槛：成功率需要与接触、顺序、恢复和不安全状态暴露测量一起报告。

#### Evidence
- [SafeManip: A Property-Driven Benchmark for Temporal Safety Evaluation in Robotic Manipulation](../Inbox/2026-05-12--safemanip-a-property-driven-benchmark-for-temporal-safety-evaluation-in-robotic-manipulation.md): SafeManip 摘要给出了时序安全监控设计、任务集、策略集，以及安全性与成功率之间的结果。
- [AffordVLA: Injecting Affordance Representations into Vision-Language-Action Models via Implicit Feature Alignment](../Inbox/2026-05-17--affordvla-injecting-affordance-representations-into-vision-language-action-models-via-implicit-feature-alignment.md): AffordVLA 摘要说明了接触区域训练方法和推理路径细节。
