---
kind: trend
trend_doc_id: 50
granularity: day
period_start: '2026-04-05T00:00:00'
period_end: '2026-04-06T00:00:00'
topics:
- embodied-ai
- vla-safety
- adaptive-control
- driving-world-models
- dexterous-grasping
run_id: materialize-outputs
aliases:
- recoleta-trend-50
tags:
- recoleta/trend
- topic/embodied-ai
- topic/vla-safety
- topic/adaptive-control
- topic/driving-world-models
- topic/dexterous-grasping
language_code: zh-CN
---

# Embodied AI 工作正聚焦于动作回路

## Overview
4 月 5 日的 embodied-AI 进展很强，重点在动作控制。最清楚的几篇论文都在改进感知和执行之间的环节：更安全的 VLA 策略、自适应动作分块，以及面向驾驶的联合视频-动作规划。共同点是操作层面的细节。作者们在模块层面编辑机器人策略，在推理时调整重规划，并训练世界模型，让预测场景与计划运动保持一致。

## Clusters

### 选择性遗忘进入机器人策略层面
视觉-语言-动作模型中的安全工作正变得更具体。VLA-Forget 分阶段编辑视觉编码器、跨模态投影器和高层动作层，再结合 retain、forget、mismatch 和 feature-preservation losses，在不抹掉任务能力的情况下移除不想要的行为。对这类干预来说，报告结果很强：在 OpenVLA-7B 配合 Open X-Embodiment 上，它达到 FC 93、RC 91 和 TSR 78；量化后的安全违规恢复低于 NPO，保留能力则明显好于 GA。这一点很重要，因为这里要处理的失败目标是机器人动作，不只是文本输出。

#### Evidence
- [VLA-Forget: Vision-Language-Action Unlearning for Embodied Foundation Models](../Inbox/2026-04-05--vla-forget-vision-language-action-unlearning-for-embodied-foundation-models.md): VLA 策略选择性遗忘的方法与基准结果摘要

### 动作时序在推理时变得自适应
推理时控制正成为一个活跃的优化目标。AAC 读取采样候选轨迹上的熵，动态调整动作块大小；当模型不确定时更早重规划，当预测保持稳定时执行更长的动作块。收益不大，但覆盖面广：GR00T 在 RoboCasa 上从 59.7% 提高到 62.0%，在 LIBERO 上从 94.1% 提高到 95.0%，在 LIBERO-Long 上从 88.8% 提高到 92.8%。这个模式和该语料中最近几天的机器人工作一致：进展来自对动作接口和重规划回路更紧的控制。

#### Evidence
- [Adaptive Action Chunking at Inference-time for Vision-Language-Action Models](../Inbox/2026-04-05--adaptive-action-chunking-at-inference-time-for-vision-language-action-models.md): 包含 AAC 机制以及 RoboCasa 和 LIBERO 基准变化的摘要

### 驾驶世界模型继续从联合视频监督中获益
联合生成视频和动作，仍然是增强驾驶规划器最清晰的路径之一。DriveVA 在一个生成过程中同时预测未来视频潜变量和自车轨迹 token，论文将很大一部分提升归因于稠密视频监督。在 NAVSIM v1 上，它达到 90.9 PDMS，高于 DiffusionDrive 的 88.1；同时还报告了在 nuScenes 和 Bench2Drive/CARLA v2 上显著的零样本迁移收益，其中包括相对文中所述世界模型基线在 nuScenes 上 83.3% 的碰撞率下降。还有一个实际上的点：模型声称只需两步采样就能达到接近最优的闭环性能。

#### Evidence
- [DriveVA: Video Action Models are Zero-Shot Drivers](../Inbox/2026-04-05--driveva-video-action-models-are-zero-shot-drivers.md): 包含架构、视频监督消融结论以及闭环和迁移结果的摘要

### 稀疏任务结构正在提升灵巧抓取
灵巧操作工作也在依赖人可以检查的稀疏结构。GRIT 使用一个 30 类抓取分类体系加上手腕朝向作为高层命令，由视觉语言模型根据场景和任务选择，再由分类体系条件控制策略执行。它报告总体成功率为 87.9%，并在用 30 个 YCB 物体训练后，测试了 373 个新物体。论文也强调用户控制：当抓取策略不对时，界面会给出一个可以直接修改的具体入口。

#### Evidence
- [Learning Dexterous Grasping from Sparse Taxonomy Guidance](../Inbox/2026-04-05--learning-dexterous-grasping-from-sparse-taxonomy-guidance.md): 包含两阶段分类体系引导方法和新物体成功率结果的摘要
