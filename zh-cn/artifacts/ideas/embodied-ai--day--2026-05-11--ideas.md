---
kind: ideas
granularity: day
period_start: '2026-05-11T00:00:00'
period_end: '2026-05-12T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- vision-language-action models
- manipulation
- OOD generalization
- world models
- policy adaptation
- spatial grounding
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action-models
- topic/manipulation
- topic/ood-generalization
- topic/world-models
- topic/policy-adaptation
- topic/spatial-grounding
language_code: zh-CN
---

# Few-Shot VLA Adaptation Under Deployment Shift

## 摘要
适配预训练 VLA 策略的机器人团队有三个具体检查项：在适配时保留冻结的策略路径；在评估中把长距离接近和接触密集控制分开；当动作标签稀缺时加入结构化辅助目标。共同压力来自在新物体姿态、背景、embodiment 和接触动力学下，用有限演示完成部署。

## Frozen-prior adaptation for few-demonstration VLA deployment
将预训练 VLA 适配到新的机器人工位时，团队应该测试一条可训练的轻量适配路径，同时在训练或 rollout 里保留预训练动作模块可见。PriorVLA 给出了一种实现：保留冻结的 Prior Expert，训练单独的 Adaptation Expert，让学习到的 queries 从冻结路径里读取场景和运动特征。UniSteer 也给出了一种做法，适用于 diffusion 或 flow-matching 策略：冻结 decoder，训练一个轻量 noise actor，再把人类纠正动作映射回 noise target。

实验室部署里的阻碍很常见：全量微调会贴合少量演示数据，同时丢掉大规模预训练得到的行为。PriorVLA 报告在 8 个真实世界任务和 2 种 embodiment 上，使用标准数据时 OOD 成功率为 57%，只有每个任务 10 条演示时 OOD 成功率为 32%。UniSteer 报告在 4 个任务上适应 66 分钟后，真实世界平均成功率从 20% 升到 90%，而且用到的纯人类轨迹少于 DAgger。一个低成本验证方法是，把同样的 OOD 放置和背景测试套件分别跑在全量微调、冻结先验适配器和人类纠正 noise actor 上，并按 ID 和 OOD 情况拆分成功率。

### 资料来源
- [PriorVLA: Prior-Preserving Adaptation for Vision-Language-Action Models](../Inbox/2026-05-11--priorvla-prior-preserving-adaptation-for-vision-language-action-models.md): PriorVLA keeps a frozen prior expert, trains a separate adaptation expert, updates fewer parameters, and reports OOD and few-shot real-world results.
- [Unified Noise Steering for Efficient Human-Guided VLA Adaptation](../Inbox/2026-05-11--unified-noise-steering-for-efficient-human-guided-vla-adaptation.md): UniSteer freezes the flow-matching VLA decoder, trains a small noise actor from RL and human corrections, and reports 90% real-world success after 66 minutes.

## Separate transit and contact evaluation for long-horizon manipulation policies
VLA 和 World Action Model 策略的操作基准应该把 transit 和 interaction 作为两个独立的失败模式来评分。HarmoWAM 的设计可以直接参考：用世界模型预测未来帧，把 transit 和目标接近交给 reactive expert，把精确接触交给 predictive expert，再训练一个 gate 在执行时选择控制路径。

这对堆叠、倾倒、书写、抓取和双臂协作这类任务很重要，因为策略可能已经到达正确物体，却在接触时失败。HarmoWAM 的动机研究发现，Imagine-then-Execute 在所有 OOD transit 情况下都能到达目标，但 interaction 成功率最低只有 2/10；Joint Modeling 在靠近物体时保持较高的 interaction 成功率，但在 OOD transit 中更容易失败。实际测试可以按阶段给 episode 标注，方法是用物体距离、接触状态或手工分段边界，然后分别报告接近、首次接触和完成操作的成功率。如果某一个阶段主导了失败，那么带 gate 的双专家策略就是针对性改造，而不是整体架构替换。

### 资料来源
- [HarmoWAM: Harmonizing Generalizable and Precise Manipulation via Adaptive World Action Models](../Inbox/2026-05-11--harmowam-harmonizing-generalizable-and-precise-manipulation-via-adaptive-world-action-models.md): HarmoWAM separates reactive transit control from predictive interaction control and reports phase-specific failure patterns.
- [HarmoWAM: Harmonizing Generalizable and Precise Manipulation via Adaptive World Action Models](../Inbox/2026-05-11--harmowam-harmonizing-generalizable-and-precise-manipulation-via-adaptive-world-action-models.md): The paper describes a Process-Adaptive Gating Mechanism and reports OOD gains across unseen background, position, and object variations.
- [HarmoWAM: Harmonizing Generalizable and Precise Manipulation via Adaptive World Action Models](../Inbox/2026-05-11--harmowam-harmonizing-generalizable-and-precise-manipulation-via-adaptive-world-action-models.md): The motivation study compares Imagine-then-Execute and Joint Modeling on transit and manipulation success under ID and OOD settings.

## Auxiliary latent-transition targets from action-free robot video
有大量未标注视频的机器人数据管线，应该先测试 latent-transition 预训练，再去收集更多带动作标签的演示。ALAM 会采样 frame triplet，为每个帧对学习一个 latent transition，再加入 composition 和 reversal 损失，让 latent space 带上可复用的时间结构。在 VLA 训练中，冻结的 encoder 会生成 latent-transition 序列作为辅助目标，而实际执行的输出仍然是机器人动作流。

一个实用检查很小，也很机械：先在无动作标签的第三人称和 wrist-camera 片段上预训练 latent encoder，测 additivity 和 reversibility error，再用有和没有辅助 latent target 的方式微调同一个 VLA backbone。ALAM 报告它的 additivity 和 reversibility error 比未结构化 latent-action 基线低 25-85 倍。在 MetaWorld MT50 上，π0 + ALAM 的平均成功率达到 85.0%，而 π0 是 47.9%；在 LIBERO 上，它达到 98.1%，而 π0 是 94.1%。对于已经在保存成功或接近成功的操作视频、但没有同步动作标签的团队，这个方法最有价值。

### 资料来源
- [ALAM: Algebraically Consistent Latent Action Model for Vision-Language-Action Models](../Inbox/2026-05-11--alam-algebraically-consistent-latent-action-model-for-vision-language-action-models.md): ALAM learns structured latent transitions from action-free videos and uses them as auxiliary targets during VLA policy training.
- [ALAM: Algebraically Consistent Latent Action Model for Vision-Language-Action Models](../Inbox/2026-05-11--alam-algebraically-consistent-latent-action-model-for-vision-language-action-models.md): The paper reports lower latent consistency errors and large success gains on MetaWorld MT50 and LIBERO.
- [ALAM: Algebraically Consistent Latent Action Model for Vision-Language-Action Models](../Inbox/2026-05-11--alam-algebraically-consistent-latent-action-model-for-vision-language-action-models.md): The source explains why action-free videos can supply behavior-relevant priors when action-labeled robot data is scarce.
