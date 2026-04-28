---
kind: trend
trend_doc_id: 125
granularity: day
period_start: '2026-04-14T00:00:00'
period_end: '2026-04-15T00:00:00'
topics:
- robotics
- vla-safety
- humanoid-manipulation
- tactile-sensing
- 3d-geometry
run_id: materialize-outputs
aliases:
- recoleta-trend-125
tags:
- recoleta/trend
- topic/robotics
- topic/vla-safety
- topic/humanoid-manipulation
- topic/tactile-sensing
- topic/3d-geometry
language_code: zh-CN
---

# 机器人研究将评测收紧到安全、触觉和 3D 控制上

## Overview
这一天的机器人论文脉络很清楚：评测变得更严格，模型设计也在跟着这个压力调整。HazardArena 衡量的是 VLA 能不能区分一个动作是可执行还是危险。HTD 说明触觉预测能提升真实人形机器人操作。VGA 用 3D 几何骨干拿到了这组工作里最强的基准结果。合在一起看，这些论文更偏向与真实决策直接对应的控制信号：语义风险、接触状态和场景几何。

## Clusters

### 语义安全成为可度量的控制问题
HazardArena 把语义安全放到 VLA 评测的核心位置。它的安全/不安全孪生任务保持运动要求不变，只改变让某个动作变成允许或危险的语义条件。这个设计暴露出一个实际失效模式：模型的任务能力和不安全完成率会一起上升。最清楚的例子是 pi_0 在 `insert outlet` 上，安全成功率从 0.08 升到 0.47，同时不安全成功率也从 0.02 升到 0.44，且这一变化贯穿多个 checkpoint。论文也说明了为什么只看终点成功率范围太窄。在不安全的 `insert outlet` 上，pi_0 在最终成功率到 0.44 之前，attempt 已达到 0.93，commit 已达到 0.80，所以在真正完成之前就能看到危险进展。论文提出的 Safety Option Layer 是一个有用的防护思路，但这里更主要的贡献是这个基准，以及按阶段观察风险的视角。

#### Evidence
- [HazardArena: Evaluating Semantic Safety in Vision-Language-Action Models](../Inbox/2026-04-14--hazardarena-evaluating-semantic-safety-in-vision-language-action-models.md): 对基准设计、孪生任务设置、分阶段指标，以及安全任务提升与不安全行为耦合现象的总结。

### 触觉预测在人形机器人真实任务上带来明显收益
当任务依赖接触时，触觉就成了人形机器人操作中的一等输入。HTD 在单一策略中结合了多视角视觉、本体感觉、手部关节力和触觉传感，并在行为克隆中加入未来触觉预测。对于一个规模不大的当日任务集，论文报告的提升幅度很大：在五个真实世界任务上，平均成功率相比 ACT 相对提升 90.9%；潜在空间触觉预测相比原始触觉预测还有 30% 的相对增益。这里的任务列表很关键。Insert-T、毛巾折叠、猫砂铲取和端茶都需要接触状态信息，而相机视角无法把这些信息完全揭示出来。论文还用部署细节支撑了这一结论，包括 3.5 mm 的插入间隙，以及在完整人形机器人系统上以 30 Hz 执行策略。

#### Evidence
- [Learning Versatile Humanoid Manipulation with Touch Dreaming](../Inbox/2026-04-14--learning-versatile-humanoid-manipulation-with-touch-dreaming.md): 总结涵盖了多模态策略设计、touch-dreaming 损失、五任务评测和定量提升。

### 3D 几何骨干在操作基准上继续保持领先
强调几何结构的视觉骨干在操作任务中继续扩大优势。VGA 认为骨干网络应直接建模 3D 结构，然后用一个预训练 3D 世界模型，结合多视角 RGB、语言和本体感觉来驱动控制。基准结果很强：在 LIBERO 上平均 98.1%，并且超过了 pi_0.5、OpenVLA-oft、VLA-Thinker、GeoVLA 和 SpatialVLA。与最强基线相比，领先幅度不大，但在整个基准套件上表现稳定；论文还报告了在真实机器人上，对未见过的相机视角有更好的零样本迁移。在一个已经更强调评测干净性的阶段，这篇论文给出了一个具体的模型侧答案：更强的几何先验仍然会转化成更好的放置能力和视角鲁棒性。

#### Evidence
- [Robotic Manipulation is Vision-to-Geometry Mapping ($f(v) \rightarrow G$): Vision-Geometry Backbones over Language and Video Models](../Inbox/2026-04-14--robotic-manipulation-is-vision-to-geometry-mapping-f-v-rightarrow-g-vision-geometry-backbones-over-language-and-video-models.md): 总结给出了模型主张、LIBERO 分数、基线对比，以及真实世界跨视角泛化的结论。
