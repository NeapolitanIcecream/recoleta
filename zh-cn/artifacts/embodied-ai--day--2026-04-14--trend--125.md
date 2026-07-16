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

# 机器人研究把评估收紧到安全、触觉和三维控制上

## 概览
这一天的机器人研究很好读：评估更严格了，模型设计也朝着同样的压力变化。HazardArena 衡量 VLA 能不能区分可执行动作和危险动作。HTD 说明触觉预测能改善真实人形操作。VGA 用 3D 几何骨干拿下了这组里最强的基准结果。放在一起看，这些论文都偏向于贴近真实决策的控制信号：语义风险、接触状态和场景几何。

## 研究发现

### 语义安全变成可测量的控制问题
HazardArena把语义安全放到VLA评估的中心。它的安全和不安全双任务保持运动要求不变，只改变让动作被允许或变得危险的语义。这种设计暴露出一个实际失效模式：模型可以同时提升任务能力和不安全完成率。最清楚的例子是 pi_0 在 `insert outlet` 上的结果，安全成功率从 0.08 升到 0.47，不安全成功率也从 0.02 升到 0.44，跨越多个检查点都如此。论文也说明了为什么只看终点成功率还不够。在不安全的 `insert outlet` 上，pi_0 在最终成功率 0.44 之前，attempt 达到 0.93，commit 达到 0.80，所以风险进展在完成前就已经可见。作者提出的 Safety Option Layer 是一个有用的防护思路，但这里的主要贡献是基准本身和分阶段的风险视角。

#### 资料来源
- [HazardArena: Evaluating Semantic Safety in Vision-Language-Action Models](../Inbox/2026-04-14--hazardarena-evaluating-semantic-safety-in-vision-language-action-models.md): Summary of benchmark design, twin-task setup, stage-wise metrics, and observed coupling between safe-task gains and unsafe behavior.

### 触觉预测在真实人形任务上见效
当任务依赖接触时，触觉就成了人形操作里的一级输入。HTD把多视角视觉、本体感觉、手指关节力和触觉感知放进一个策略里，然后在行为克隆中加入未来触觉预测。它在一个小规模日常任务集上的提升很大：在五个真实世界任务上，平均成功率相对 ACT 提升 90.9%，而潜空间触觉预测相对原始触觉预测又有 30% 的相对提升。任务列表很关键。Insert-T、折毛巾、捡猫砂和端茶都需要相机视角看不完整的接触状态。论文还给出了部署细节：插入间隙 3.5 mm，整个人形系统上的策略执行频率是 30 Hz。

#### 资料来源
- [Learning Versatile Humanoid Manipulation with Touch Dreaming](../Inbox/2026-04-14--learning-versatile-humanoid-manipulation-with-touch-dreaming.md): Summary covers multimodal policy design, touch-dreaming loss, five-task evaluation, and quantitative gains.

### 3D 几何骨干在操作基准上继续占优
偏几何的视觉骨干在操作任务上继续占优。VGA主张骨干网络应直接建模三维结构，然后用一个预训练的 3D 世界模型，结合多视角 RGB、语言和本体感觉来驱动控制。基准结果很强：LIBERO 上平均 98.1%，超过 pi_0.5、OpenVLA-oft、VLA-Thinker、GeoVLA 和 SpatialVLA。和最强基线相比，差距不大，但在整个测试集上都保持一致，论文还报告了在真实机器人上对未见过的相机视角有更好的零样本迁移。在已经更强调干净评估的这段时间里，这篇论文给出了一个明确的模型侧答案：更强的几何先验仍然能换来更好的放置能力和视角鲁棒性。

#### 资料来源
- [Robotic Manipulation is Vision-to-Geometry Mapping ($f(v) \rightarrow G$): Vision-Geometry Backbones over Language and Video Models](../Inbox/2026-04-14--robotic-manipulation-is-vision-to-geometry-mapping-f-v-rightarrow-g-vision-geometry-backbones-over-language-and-video-models.md): Summary gives the model claim, LIBERO scores, baseline comparisons, and real-world cross-view generalization claim.
