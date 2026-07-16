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

# 机器人 VLA 工作正在聚焦于保留先验并改进动作结构的 OOD 适应

## 概览
这一时期的机器人 Vision-Language-Action（VLA）论文集中在部署失效点：分布外场景、有限演示和薄弱的动作监督。HarmoWAM、PriorVLA 和 UniSteer 在真实世界操作测试中给出了最清楚的量化信号。

## 研究发现

### World models for staged manipulation
HarmoWAM 将操作视为一个依赖阶段的控制问题。一个视频世界模型预测未来帧，两个动作专家分别处理任务的不同部分：一个反应式专家负责移动，一个预测式专家负责精细交互。一个学习到的门控在推理时选择专家。

论文报告了在六个真实世界任务上的测试，任务包含背景、位置和物体变化。在分布外设置下，HarmoWAM 声称相较于先前的 VLA 模型平均提升 33 个百分点，相较于先前的 World Action Models 提升 29 个百分点。关键细节是把到达控制和接触控制分开，论文在动机研究中直接测量了这一点。

#### 资料来源
- [HarmoWAM: Harmonizing Generalizable and Precise Manipulation via Adaptive World Action Models](../Inbox/2026-05-11--harmowam-harmonizing-generalizable-and-precise-manipulation-via-adaptive-world-action-models.md): Summary covers HarmoWAM architecture, staged experts, gating, real-world tasks, and OOD gains.

### Adaptation without overwriting pretrained behavior
PriorVLA 和 UniSteer 都在适应过程中保留了预训练策略的行为可见性。PriorVLA 冻结一个先验专家，并训练一个单独的适配专家，更新的参数量大约只有完整微调的四分之一。它在 RoboTwin 2.0 上报告了 53% 的 Hard OOD 成功率，并在八个任务、两种本体的真实世界测试中报告了 57% 的 OOD 成功率。

UniSteer 采用了另一条路径来应对同样的部署压力。它冻结 flow-matching 解码器，只训练一个小型噪声 actor。人类纠正会映射回噪声目标，因此纠正动作和强化学习更新的是同一个 actor。跨四个真实世界任务，报告的平均成功率在适应 66 分钟后达到 90%，高于 DSRL 的 55% 和 DAgger 的 60%。

#### 资料来源
- [PriorVLA: Prior-Preserving Adaptation for Vision-Language-Action Models](../Inbox/2026-05-11--priorvla-prior-preserving-adaptation-for-vision-language-action-models.md): Summary describes PriorVLA's frozen prior expert, parameter update share, and OOD results.
- [Unified Noise Steering for Efficient Human-Guided VLA Adaptation](../Inbox/2026-05-11--unified-noise-steering-for-efficient-human-guided-vla-adaptation.md): Summary describes UniSteer's noise-target training, frozen decoder, real-world adaptation time, and success rates.

### Action structure learned from unlabeled video
ALAM 针对带动作标注的机器人数据成本。它从无动作视频中学习潜在转移，再用组合和反转约束对其进行正则化。在 VLA 训练期间，这些潜在转移变成辅助目标，而执行输出仍然是机器人动作流。

报告的提升在标准操作基准上很大。在 MetaWorld MT50 上，加入 ALAM 的 π0 达到 85.0% 的平均成功率，而 π0 为 47.9%。在 LIBERO 上，它报告 98.1% 的平均成功率，高于 π0 基线的 94.1%。这个结果支持一个实际判断：当潜在动作空间包含可复用的转移结构时，无标注视频就有用。

#### 资料来源
- [ALAM: Algebraically Consistent Latent Action Model for Vision-Language-Action Models](../Inbox/2026-05-11--alam-algebraically-consistent-latent-action-model-for-vision-language-action-models.md): Summary covers ALAM's action-free video pretraining, algebraic losses, VLA training use, and benchmark results.

### Spatial grounding added at training time
VEGA 关注一个范围更窄但重要的失效来源：主要在 2D 图像上训练的视觉编码器可能会错过深度、高度和相对位置线索。该方法在训练期间把 OpenVLA-OFT 的视觉特征对齐到一个冻结的、具备 3D 感知能力的 DINOv2-FiT3D 教师。教师和投影器在推理时被移除，所以运行时与基模型相同。

在 RoboTwin 2.0 上，VEGA 在六个双臂任务中报告 Easy 平均成功率 67.5%，Hard 为 30.7%。它把 OpenVLA-OFT 在 Easy 上提高 11.5 个百分点，在 Hard 上提高 8.0 个百分点，任务级提升出现在 Move Card Away、Click Bell 和 Place Shoe 上。

#### 资料来源
- [VEGA: Visual Encoder Grounding Alignment for Spatially-Aware Vision-Language-Action Models](../Inbox/2026-05-11--vega-visual-encoder-grounding-alignment-for-spatially-aware-vision-language-action-models.md): Summary covers VEGA's 3D-aware feature alignment method, no inference overhead, and RoboTwin 2.0 results.
