---
kind: trend
trend_doc_id: 330
granularity: week
period_start: '2026-05-04T00:00:00'
period_end: '2026-05-11T00:00:00'
topics:
- robotics
- vision-language-action
- world models
- failure recovery
- long-horizon manipulation
- model release safety
run_id: materialize-outputs
aliases:
- recoleta-trend-330
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/world-models
- topic/failure-recovery
- topic/long-horizon-manipulation
- topic/model-release-safety
language_code: zh-CN
---

# 机器人 VLA 可靠性取决于可恢复控制和紧凑前瞻

## Overview
本周机器人语料把 Vision-Language-Action (VLA) 策略视为可部署的控制系统。最有力的工作衡量漂移后的恢复、长任务中的记忆，以及低成本世界状态预测。RePO-VLA、ECHO 和 OneWM-VLA 支撑了这一信号。前几周已经强调在线执行；本周加入了更具体的测试，覆盖恢复数据、紧凑内部状态和已发布模型检查。

## Clusters

### 失败恢复和长时程记忆
可靠性取决于任务开始出错后策略会怎么做。RePO-VLA 使用成功、失败和恢复 rollout 训练，并为它们设置不同标签；论文报告平均对抗成功率从 20% 升至 75%，在规模化真实世界试验中最高达到 80%。关键细节是对不利状态、接触漂移和有用的失败前缀进行监督，而不只使用干净示范。

ECHO 用记忆处理同一个长时程问题。它把成功的子目标片段存入分层记忆，并在推理时检索这些片段。在 LIBERO-Long 上，它报告 93.5% 的成功率，高于原始 π0 基线的 80.7%。这些论文把恢复和记忆变成了 VLA 执行质量中可度量的部分。

#### Evidence
- [RePO-VLA: Recovery-Driven Policy Optimization for Vision-Language-Action Models](../Inbox/2026-05-10--repo-vla-recovery-driven-policy-optimization-for-vision-language-action-models.md): RePO-VLA 摘要、方法细节和报告的恢复收益。
- [ECHO: Continuous Hierarchical Memory for Vision-Language-Action Models](../Inbox/2026-05-09--echo-continuous-hierarchical-memory-for-vision-language-action-models.md): ECHO 摘要、记忆设计和 LIBERO-Long 结果。

### 用于可部署前瞻的紧凑世界状态
世界模型研究偏向使用小型内部状态，同时仍能在长时程中指导动作。OneWM-VLA 将每个视角的每一帧压缩成一个语义 token，并联合生成未来潜在 token 和动作块。它报告在 LIBERO 各套件上的平均成功率为 98.1%，在 LIBERO-Long 上为 95.6%，同时只在冻结骨干上训练一个小型 LoRA 适配。

ConsisVLA-4D 加入紧凑的多视角 3D 感知和未来场景推理。其结果称，相比 OpenVLA，它在 LIBERO 上性能提升 21.6%、推理加速 2.3×；在真实机器人平台上性能提升 41.5%、加速 2.4×。共同的设计目标是让策略能够前瞻，同时不让推理成本高到影响控制。

#### Evidence
- [One Token Per Frame: Reconsidering Visual Bandwidth in World Models for VLA Policy](../Inbox/2026-05-08--one-token-per-frame-reconsidering-visual-bandwidth-in-world-models-for-vla-policy.md): OneWM-VLA 摘要、单 token 设计和 LIBERO/真实机器人结果。
- [ConsisVLA-4D: Advancing Spatiotemporal Consistency in Efficient 3D-Perception and 4D-Reasoning for Robotic Manipulation](../Inbox/2026-05-06--consisvla-4d-advancing-spatiotemporal-consistency-in-efficient-3d-perception-and-4d-reasoning-for-robotic-manipulation.md): ConsisVLA-4D 摘要、紧凑空间推理设计和报告的速度/性能收益。

### 场景变化下的对象身份
几篇论文把目标绑定作为核心控制问题。OA-WAM 将每个对象槽拆成固定身份地址和会变化的内容状态，然后通过地址切片路由注意力，使动作解码器能跟踪指令指定的对象。它报告在 LIBERO 上平均成功率为 97.8%，并且在报告的几何平均指标上，LIBERO-Plus 的几何泛化强于 π0.5。

这一点有实际影响，因为场景变化可能保留可见对象，却改变布局、相机视角、机器人初始位姿或附近干扰物。ConsisVLA-4D 用与指令相关的对象选择和紧凑跨视角几何处理相关问题。本周证据表明，对象级状态是让操作策略承受场景变化的一条实用途径。

#### Evidence
- [OA-WAM: Object-Addressable World Action Model for Robust Robot Manipulation](../Inbox/2026-05-07--oa-wam-object-addressable-world-action-model-for-robust-robot-manipulation.md): OA-WAM 摘要、对象地址设计和 LIBERO/LIBERO-Plus 结果。
- [ConsisVLA-4D: Advancing Spatiotemporal Consistency in Efficient 3D-Perception and 4D-Reasoning for Robotic Manipulation](../Inbox/2026-05-06--consisvla-4d-advancing-spatiotemporal-consistency-in-efficient-3d-perception-and-4d-reasoning-for-robotic-manipulation.md): ConsisVLA-4D 关于跨视角对象一致性和紧凑几何的摘要。

### 发布的 VLA 模型需要验证检查
开放机器人策略带来第二个可靠性问题：发布后的模型能否在不改变正常机器人行为的情况下被复制、修改或审计。GuardVLA 在训练期间嵌入秘密视觉水印，并在之后用替换的验证头检查所有权。在 LIBERO 实验中，带水印模型的水印识别置信度接近 100%，干净模型接近零，良性任务成功率仍接近干净基线。

每日趋势还提到调优后的 ATAAT 式后门风险。这使发布安全与控制可靠性进入同一个评估范围。可部署的 VLA 现在需要任务成功率、恢复行为，以及发布后的策略在下游适配后仍可检查的证据。

#### Evidence
- [Towards Backdoor-Based Ownership Verification for Vision-Language-Action Models](../Inbox/2026-05-09--towards-backdoor-based-ownership-verification-for-vision-language-action-models.md): GuardVLA 摘要、水印方法和所有权验证结果。
