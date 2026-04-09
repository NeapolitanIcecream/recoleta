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

# 控制研究正更明确地处理接触、安全区域和 rollout 风险

## Overview
这个时间段内的论文数量不多，但主题一致：控制类论文正在把感知和动作连接到错误会变成物理后果的那个节点上。最强的证据来自机器人和手术场景，在这些场景中，模型通过显式暴露接触状态或安全交互区域来体现价值。另一篇世界模型综述补充了第二条信息：一旦预测进入规划流程，安全评估就必须跟踪错误如何在多步 rollout 中持续存在。

## Clusters

### 操作中的接触感知传感融合
当前的机器人操作研究很依赖具体任务条件。在这篇接触感知操作论文中，最佳结果来自这样一条规则：只在检测到接触时使用力矩，再在扩散策略内部融合视觉和力矩。这个简单的时机控制很关键：该方法在三个真实任务上的平均成功率达到 82.0%，高于仅做力矩门控的 68.0%，而纯视觉和直接特征拼接都停留在 30.0%。错误模式也很具体。纯视觉在空瓶任务上能做到 8/10，但面对满瓶会降到 0/10；自适应融合模型则在空瓶上保持 9/10，在满瓶上达到 7/10。这说明了机器人控制中的一个具体结论：额外传感只有在策略知道何时该相信它时才有帮助。

#### Evidence
- [Learning When to See and When to Feel: Adaptive Vision-Torque Fusion for Contact-Aware Manipulation](../Inbox/2026-04-01--learning-when-to-see-and-when-to-feel-adaptive-vision-torque-fusion-for-contact-aware-manipulation.md): 摘要给出了自适应接触门的设计和主要基准结果。

### 手术动作的稠密安全区域预测
手术自动化研究越来越明确地指出动作可以安全发生在什么位置。AffordTissue 在接触发生前预测面向特定工具-动作组织交互的稠密热图，输入包括文本、视频历史和专门的解码器。它的优势主要体现在空间精度，而不只是分类。ASSD 降到 20.557 px，相比之下 Molmo-VLM 为 60.184 px，SAM3 为 81.138 px；同时 PCK@0.05 达到 0.517，而后两者分别是 0.095 和 0.128。消融实验也表明提示内容很重要。去掉语言编码器会把 ASSD 提高到 43.135 px，去掉工具或动作条件也会带来性能下降。这让这篇论文适合作为一层安全机制来理解：模型可以给出一个预测的安全区域，让控制器或人类在工具接触前进行检查。

#### Evidence
- [AffordTissue: Dense Affordance Prediction for Tool-Action Specific Tissue Interaction](../Inbox/2026-04-01--affordtissue-dense-affordance-prediction-for-tool-action-specific-tissue-interaction.md): 摘要包含了数据集范围、模型输入、主要基准指标，以及语言和条件输入的消融结果。

### 世界模型开始因持续性失效模式而接受审查
当前的世界模型研究主要在讨论风险，而不是新的能力提升。核心观点是，基于 rollout 的规划会在想象出的未来轨迹中保留并放大小误差或攻击。论文用轨迹持续性指标来定义这一点，并在基于 GRU 的循环状态空间模型上报告了 2.26x 的放大比；经过对抗微调后，这个效应降低了 59.5%。一个随机代理模型把这个值降到 0.65x，因此暴露程度取决于架构。现有证据仍然有限。DreamerV3 的结果显示，基于 checkpoint 探测会产生非零动作漂移，但论文没有给出完整的下游失败率基准。这使它更像是一条有用的警示和评估议程，而在经验支撑上弱于当天另外两篇任务论文。

#### Evidence
- [Safety, Security, and Cognitive Risks in World Models](../Inbox/2026-04-01--safety-security-and-cognitive-risks-in-world-models.md): 摘要给出了威胁模型、持续性指标，以及包含放大效应和微调影响的概念验证结果。
