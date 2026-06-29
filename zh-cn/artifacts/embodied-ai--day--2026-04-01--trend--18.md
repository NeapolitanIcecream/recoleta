---
kind: trend
trend_doc_id: 18
granularity: day
period_start: '2026-04-01T00:00:00'
period_end: '2026-04-02T00:00:00'
topics:
- robot-manipulation
- surgical-ai
- world-model-safety
run_id: materialize-outputs
aliases:
- recoleta-trend-18
tags:
- recoleta/trend
- topic/robot-manipulation
- topic/surgical-ai
- topic/world-model-safety
language_code: zh-CN
---

# 控制工作越来越明确地处理接触、安全区域和 rollout 风险

## Overview
这个时间段很小，但脉络一致：控制类论文把感知和动作连到错误会变成物理后果的那个点上。最强的证据来自机器人和手术场景，模型通过暴露接触状态或安全交互区域来增加价值。世界模型综述补了第二层意思：一旦预测进入规划，安全评估就必须跟踪错误在多次 rollout 中如何持续。

## Clusters

### 接触感知的操作中的传感器融合
如今的机器人操作工作很依赖任务条件。在这篇感知接触的操作论文里，最佳结果来自只在检测到接触时使用力矩，然后在扩散策略里把视觉和力矩结合起来。这个简单的时机规则很关键：这种方法在三个真实任务上的平均成功率达到 82.0%，高于单独的力矩门控 68.0%，而纯视觉和普通特征拼接都停在 30.0%。错误模式很具体。纯视觉在空瓶上能做到 8/10，但在满瓶上掉到 0/10；自适应融合模型在空瓶上保持 9/10，在满瓶上保持 7/10。这说明机器人控制里一个狭窄但重要的结论：当策略知道何时信任额外感知时，额外感知才有用。

#### Evidence
- [Learning When to See and When to Feel: Adaptive Vision-Torque Fusion for Contact-Aware Manipulation](../Inbox/2026-04-01--learning-when-to-see-and-when-to-feel-adaptive-vision-torque-fusion-for-contact-aware-manipulation.md): Summary gives the adaptive contact gate design and the main benchmark numbers.

### 手术动作的稠密安全区域预测
手术自动化工作越来越明确动作可以安全发生的位置。AffordTissue 在接触前预测与工具和动作相关的组织交互密集热图，使用文本、视频历史和专门的解码器。它的优势在空间精度，而不只是分类。ASSD 降到 20.557 px，而 Molmo-VLM 是 60.184 px，SAM3 是 81.138 px；PCK@0.05 达到 0.517，对比 0.095 和 0.128。消融也说明提示内容很重要。去掉语言编码器后，ASSD 升到 43.135 px；去掉工具或动作条件也会变差。这让这篇论文很适合作为安全层来理解：模型可以暴露一个预测的安全区域，供控制器或人类在工具接触前检查。

#### Evidence
- [AffordTissue: Dense Affordance Prediction for Tool-Action Specific Tissue Interaction](../Inbox/2026-04-01--affordtissue-dense-affordance-prediction-for-tool-action-specific-tissue-interaction.md): Summary contains the dataset scope, model inputs, main benchmark metrics, and ablations on language and conditioning.

### 世界模型正在接受持久失败模式审计
如今的世界模型研究更多在讨论风险，而不是新的能力提升。核心观点是，基于 rollout 的规划会把小错误或攻击保留并放大到想象的未来中。论文用轨迹持久性指标来定义这一点，并在基于 GRU 的循环状态空间模型上报告了 2.26x 的放大比，经过对抗微调后下降 59.5%。一个随机代理模型降到 0.65x，所以暴露程度取决于架构。证据仍然有限。DreamerV3 的结果显示，通过检查点探测会出现非零动作漂移，但论文没有给出完整的下游失败率基准。这让它更像一个有用的警告和评测议程，而不是当天另外两篇任务论文那样扎实的实证结果。

#### Evidence
- [Safety, Security, and Cognitive Risks in World Models](../Inbox/2026-04-01--safety-security-and-cognitive-risks-in-world-models.md): Summary gives the threat model, persistence metric, and proof-of-concept results including amplification and fine-tuning effects.
