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

# 部署偏移下的 Few-Shot VLA 适配

## Summary
适配预训练 VLA 策略的机器人团队有三个具体检查要做：在适配期间保留一条冻结策略路径，在评估中拆分长距离接近和重接触控制，并在动作标签稀缺时加入结构化辅助目标。共同压力来自有限演示条件下的新物体姿态、背景、embodiment 和接触动态部署。

## 面向少量演示 VLA 部署的冻结先验适配
将预训练 VLA 适配到新机器人工位的团队，应测试一条小型可训练适配路径，同时在训练或 rollout 期间保留预训练动作机制的可见性。PriorVLA 给出了一种实现：保留冻结的 Prior Expert，训练单独的 Adaptation Expert，并让学习到的查询从冻结路径读取场景和运动特征。UniSteer 为扩散或流匹配策略给出另一种做法：冻结解码器，训练轻量级噪声 actor，并把人类纠正动作映射回噪声目标。

实验室部署中的采用阻碍很常见：全量微调会拟合小规模演示集，并丢失来自大规模预训练的行为。PriorVLA 报告称，在标准数据下，跨八个真实世界任务和两种 embodiment 的 OOD 成功率为 57%，每个任务只有 10 条演示时 OOD 成功率为 32%。UniSteer 报告称，在四个任务上经过 66 分钟适配后，真实世界平均成功率从 20% 升至 90%，并且使用的纯人类轨迹少于 DAgger。一个低成本验证是，用同一套 OOD 物体摆放和背景测试集比较全量微调、冻结先验适配器和人类纠正噪声 actor，并按 ID 和 OOD 情况拆分成功率。

### Evidence
- [PriorVLA: Prior-Preserving Adaptation for Vision-Language-Action Models](../Inbox/2026-05-11--priorvla-prior-preserving-adaptation-for-vision-language-action-models.md): PriorVLA 保留冻结的先验专家，训练单独的适配专家，更新更少参数，并报告 OOD 和 few-shot 真实世界结果。
- [Unified Noise Steering for Efficient Human-Guided VLA Adaptation](../Inbox/2026-05-11--unified-noise-steering-for-efficient-human-guided-vla-adaptation.md): UniSteer 冻结流匹配 VLA 解码器，用 RL 和人类纠正训练小型噪声 actor，并报告 66 分钟后真实世界成功率达到 90%。

## 为长时程操作策略分开评估移动和接触
VLA 和 World Action Model 策略的操作基准应把移动到目标附近和交互作为两类独立失败模式来评分。HarmoWAM 的设计是一个实用模板：用世界模型预测未来帧，把移动和目标接近交给反应式专家，把精确接触交给预测式专家，并训练一个门控在执行期间选择控制路径。

这适用于堆叠、倾倒、书写、抓取和双臂协同等任务。在这些任务中，策略可能到达正确物体，却仍在接触阶段失败。HarmoWAM 的动机研究发现，Imagine-then-Execute 在所有 OOD transit 情况下都到达了目标，但 interaction 成功率低至 2/10；Joint Modeling 在物体附近保持了较高 interaction 成功率，却在 OOD transit 中更常失败。实际测试可以用物体距离、接触状态或人工分段边界按阶段标注 episode，然后报告 approach、first contact 和 completed manipulation 的成功率。如果某个阶段主导失败，带门控的双专家策略就可以作为定向改造，避免宽泛架构调整。

### Evidence
- [HarmoWAM: Harmonizing Generalizable and Precise Manipulation via Adaptive World Action Models](../Inbox/2026-05-11--harmowam-harmonizing-generalizable-and-precise-manipulation-via-adaptive-world-action-models.md): HarmoWAM 将反应式 transit 控制与预测式 interaction 控制分开，并报告按阶段划分的失败模式。
- [HarmoWAM: Harmonizing Generalizable and Precise Manipulation via Adaptive World Action Models](../Inbox/2026-05-11--harmowam-harmonizing-generalizable-and-precise-manipulation-via-adaptive-world-action-models.md): 论文描述了 Process-Adaptive Gating Mechanism，并报告了在未见背景、位置和物体变化上的 OOD 提升。
- [HarmoWAM: Harmonizing Generalizable and Precise Manipulation via Adaptive World Action Models](../Inbox/2026-05-11--harmowam-harmonizing-generalizable-and-precise-manipulation-via-adaptive-world-action-models.md): 动机研究在 ID 和 OOD 设置下比较了 Imagine-then-Execute 与 Joint Modeling 的 transit 和 manipulation 成功率。

## 来自无动作标签机器人视频的辅助潜在转移目标
拥有大量未标注视频的机器人数据流水线，应在收集更多带动作标签的演示前测试潜在转移预训练。ALAM 采样帧三元组，为每个帧对学习一个潜在转移，并加入组合和反转损失，使潜在空间携带可复用的时间结构。在 VLA 训练期间，冻结的编码器生成潜在转移序列作为辅助目标，执行输出仍是机器人动作流。

有用的检查很小且具体：在无动作标签的第三人称和腕部相机片段上预训练潜在编码器，测量可加性和可逆性误差，然后用相同 VLA backbone 在有无辅助潜在目标两种设置下微调。ALAM 报告的可加性和可逆性误差比非结构化潜在动作基线低 25-85 倍。在 MetaWorld MT50 上，π0 + ALAM 的平均成功率为 85.0%，π0 为 47.9%；在 LIBERO 上，它达到 98.1%，相比之下 π0 为 94.1%。对已经存储成功或接近成功操作视频、但没有同步动作标签的团队来说，这个方案证据最强。

### Evidence
- [ALAM: Algebraically Consistent Latent Action Model for Vision-Language-Action Models](../Inbox/2026-05-11--alam-algebraically-consistent-latent-action-model-for-vision-language-action-models.md): ALAM 从无动作标签视频中学习结构化潜在转移，并在 VLA 策略训练期间将其用作辅助目标。
- [ALAM: Algebraically Consistent Latent Action Model for Vision-Language-Action Models](../Inbox/2026-05-11--alam-algebraically-consistent-latent-action-model-for-vision-language-action-models.md): 论文报告了更低的潜在一致性误差，以及在 MetaWorld MT50 和 LIBERO 上的大幅成功率提升。
- [ALAM: Algebraically Consistent Latent Action Model for Vision-Language-Action Models](../Inbox/2026-05-11--alam-algebraically-consistent-latent-action-model-for-vision-language-action-models.md): 来源解释了在带动作标签机器人数据稀缺时，无动作标签视频为什么能提供与行为相关的先验。
