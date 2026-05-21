---
kind: trend
trend_doc_id: 343
granularity: day
period_start: '2026-05-11T00:00:00'
period_end: '2026-05-12T00:00:00'
topics:
- robotics
- vision-language-action models
- manipulation
- OOD generalization
- world models
- policy adaptation
- spatial grounding
run_id: materialize-outputs
aliases:
- recoleta-trend-343
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action-models
- topic/manipulation
- topic/ood-generalization
- topic/world-models
- topic/policy-adaptation
- topic/spatial-grounding
language_code: zh-CN
---

# 机器人 VLA 工作正集中于保留先验的 OOD 适配和更好的动作结构

## Overview
这一时期的机器人 Vision-Language-Action (VLA) 论文集中处理部署失败点：分布外场景、演示数量有限和动作监督薄弱。HarmoWAM、PriorVLA 和 UniSteer 在真实世界操作测试中给出了最清晰的测量信号。

## Clusters

### 用于分阶段操作的世界模型
HarmoWAM 将操作视为一个依赖阶段的控制问题。视频世界模型预测未来帧，两个动作专家处理任务的不同部分：反应式专家负责移动过程，预测式专家负责精细交互。推理时，学习得到的门控会选择使用哪个专家。

论文报告了在六个真实世界任务上的测试，包含背景、位置和物体变化。在分布外设置中，HarmoWAM 声称相比以往 VLA 模型平均提升 33 个百分点，相比以往 World Action Models 平均提升 29 个百分点。关键细节是将到达控制和接触控制分开，论文在动机研究中直接测量了这一点。

#### Evidence
- [HarmoWAM: Harmonizing Generalizable and Precise Manipulation via Adaptive World Action Models](../Inbox/2026-05-11--harmowam-harmonizing-generalizable-and-precise-manipulation-via-adaptive-world-action-models.md): 摘要涵盖 HarmoWAM 架构、分阶段专家、门控、真实世界任务和 OOD 提升。

### 适配时不覆盖预训练行为
PriorVLA 和 UniSteer 都在适配过程中保留预训练策略行为的可见性。PriorVLA 冻结一个先验专家，并训练一个单独的适配专家；其更新参数量约为完整微调的四分之一。它报告在 RoboTwin 2.0 上 Hard OOD 成功率为 53%，在涵盖八个任务和两种本体的真实世界测试中 OOD 成功率为 57%。

UniSteer 用另一种方式应对同样的部署压力。它冻结 flow-matching 解码器，并训练一个小型噪声 actor。人工纠正会被映射回噪声目标，因此纠正动作和强化学习会更新同一个 actor。在四个真实世界任务中，报告的平均成功率在适配 66 分钟后达到 90%，相比之下 DSRL 为 55%，DAgger 为 60%。

#### Evidence
- [PriorVLA: Prior-Preserving Adaptation for Vision-Language-Action Models](../Inbox/2026-05-11--priorvla-prior-preserving-adaptation-for-vision-language-action-models.md): 摘要描述了 PriorVLA 的冻结先验专家、参数更新占比和 OOD 结果。
- [Unified Noise Steering for Efficient Human-Guided VLA Adaptation](../Inbox/2026-05-11--unified-noise-steering-for-efficient-human-guided-vla-adaptation.md): 摘要描述了 UniSteer 的噪声目标训练、冻结解码器、真实世界适配时间和成功率。

### 从未标注视频中学习动作结构
ALAM 针对带动作标签的机器人数据成本。它从无动作视频中学习潜在转移，再用组合约束和反转约束对这些转移进行正则化。在 VLA 训练期间，这些潜在转移会成为辅助目标，而执行输出仍然是机器人动作流。

报告显示，它在标准操作套件上的提升很大。在 MetaWorld MT50 上，加入 ALAM 的 π0 平均成功率达到 85.0%，而 π0 为 47.9%。在 LIBERO 上，它报告的平均成功率为 98.1%，高于 π0 基线的 94.1%。这个结果支持一个实际判断：当潜在动作空间携带可复用的转移结构时，未标注视频是有用的。

#### Evidence
- [ALAM: Algebraically Consistent Latent Action Model for Vision-Language-Action Models](../Inbox/2026-05-11--alam-algebraically-consistent-latent-action-model-for-vision-language-action-models.md): 摘要涵盖 ALAM 的无动作视频预训练、代数损失、在 VLA 训练中的用法和基准结果。

### 在训练时加入空间落地
VEGA 关注一个更窄但重要的失败来源：主要在 2D 图像上训练的视觉编码器可能遗漏深度、高度和相对位置线索。该方法在训练期间将 OpenVLA-OFT 视觉特征对齐到一个冻结的、具备 3D 感知能力的 DINOv2-FiT3D 教师模型。推理时会移除教师模型和投影器，因此运行时开销与基础模型相同。

在 RoboTwin 2.0 上，VEGA 报告在六个双臂任务中 Easy 平均成功率为 67.5%，Hard 平均成功率为 30.7%。它相比 OpenVLA-OFT 在 Easy 上提升 11.5 个百分点，在 Hard 上提升 8.0 个百分点，并在 Move Card Away、Click Bell 和 Place Shoe 任务上取得任务级提升。

#### Evidence
- [VEGA: Visual Encoder Grounding Alignment for Spatially-Aware Vision-Language-Action Models](../Inbox/2026-05-11--vega-visual-encoder-grounding-alignment-for-spatially-aware-vision-language-action-models.md): 摘要涵盖 VEGA 的 3D 感知特征对齐方法、无推理开销和 RoboTwin 2.0 结果。
