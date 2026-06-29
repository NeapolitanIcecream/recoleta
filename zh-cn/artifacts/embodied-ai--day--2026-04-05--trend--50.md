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

# Embodied AI work is concentrating on the action loop

## Overview
4 月 5 日是一个以动作控制为中心的强 embodied-AI 日。最清楚的论文改进了感知和执行之间发生的事情：更安全的 VLA 策略、自适应 action chunking，以及用于驾驶的联合视频-动作规划。共同点是操作层面的细节。作者在模块级编辑机器人策略，在推理时调整重规划，并训练世界模型，让预测场景和计划动作保持一致。

## Clusters

### Selective unlearning reaches robot policy level
视觉-语言-动作模型里的安全工作变得更具体了。VLA-Forget 分阶段编辑视觉编码器、跨模态投影器和上层动作层，然后用 retain、forget、mismatch 和 feature-preservation 损失去除不想要的行为，同时不抹掉任务能力。报告的数值对这种干预来说很强：在 OpenVLA-7B 和 Open X-Embodiment 上，它给出 FC 93、RC 91 和 TSR 78；量化后安全违规恢复也低于 NPO，保留能力也明显好于 GA。原因很直接，因为失败目标是机器人的动作，不只是文本输出。

#### Evidence
- [VLA-Forget: Vision-Language-Action Unlearning for Embodied Foundation Models](../Inbox/2026-04-05--vla-forget-vision-language-action-unlearning-for-embodied-foundation-models.md): Summary with method and benchmark results for selective unlearning in VLA policies

### Action timing is becoming adaptive at inference
推理时控制已经成了实时优化目标。AAC 通过读取采样候选轨迹的熵，在线改变 action chunk 大小；当模型不确定时，它更早重规划；当预测稳定时，它执行更长的 chunk。收益不大，但覆盖面广：GR00T 在 RoboCasa 上从 59.7% 提升到 62.0%，在 LIBERO 上从 94.1% 提升到 95.0%，在 LIBERO-Long 上从 88.8% 提升到 92.8%。这个模式和这几天语料里的机器人工作一致：进展来自对动作接口和重规划循环更紧的控制。

#### Evidence
- [Adaptive Action Chunking at Inference-time for Vision-Language-Action Models](../Inbox/2026-04-05--adaptive-action-chunking-at-inference-time-for-vision-language-action-models.md): Summary with AAC mechanism and benchmark deltas across RoboCasa and LIBERO

### Driving world models keep gaining from joint video supervision
联合生成视频和动作仍然是更强驾驶规划器的清晰路径之一。DriveVA 在一个生成过程中同时预测未来视频潜变量和自车轨迹 token，论文把很大一部分收益归因于密集视频监督。在 NAVSIM v1 上，它达到 90.9 PDMS，高于 DiffusionDrive 的 88.1；它还报告了在 nuScenes 和 Bench2Drive/CARLA v2 上的零样本迁移增益，包括相对所述世界模型基线在 nuScenes 上碰撞率下降 83.3%。实用上的关键点是，这个模型只用两个采样步就声称接近最优的闭环表现。

#### Evidence
- [DriveVA: Video Action Models are Zero-Shot Drivers](../Inbox/2026-04-05--driveva-video-action-models-are-zero-shot-drivers.md): Summary with architecture, ablation claim on video supervision, and closed-loop plus transfer results

### Sparse task structure is improving dexterous grasping
灵巧操作也在借助人类可以检查的稀疏结构。GRIT 把 30 类抓取分类和手腕朝向作为高层指令，由视觉-语言模型根据场景和任务选择，再用 taxonomy-conditioned 控制策略执行。它报告总体成功率 87.9%，并在 30 个 YCB 物体上训练后，测试了 373 个新物体。论文也强调了用户控制：当抓取策略不对时，界面给出一个明确的修改入口。

#### Evidence
- [Learning Dexterous Grasping from Sparse Taxonomy Guidance](../Inbox/2026-04-05--learning-dexterous-grasping-from-sparse-taxonomy-guidance.md): Summary with two-stage taxonomy-guided method and reported success on novel objects
