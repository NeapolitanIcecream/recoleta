---
kind: trend
trend_doc_id: 928
granularity: day
period_start: '2026-07-20T00:00:00'
period_end: '2026-07-21T00:00:00'
topics:
- embodied AI
- vision-language-action models
- robot memory
- 3D grounding
- world-model planning
- robustness
run_id: materialize-outputs
aliases:
- recoleta-trend-928
tags:
- recoleta/trend
- topic/embodied-ai
- topic/vision-language-action-models
- topic/robot-memory
- topic/3d-grounding
- topic/world-model-planning
- topic/robustness
language_code: zh-CN
---

# 具身策略通过保留与行动相关的状态得到改进

## 概览
当天最有力的证据强化了最近一次有内容的日度信号：可靠的具身控制依赖于能够在执行过程中持续保留的状态。持久化的三维物体信息、力历史、密集视觉图像块和结构化的未来引导，都能改善操作或规划。结果很有前景，但大多局限于单个机器人和基准；一项鲁棒性研究还表明，加入推理并不能可靠地让策略更安全。

## 研究发现

### 闭环操作中的持久状态
当前图像通常缺少完成物理任务所需的信息。POT-VLA在行走、接触、遮挡和恢复过程中保留按角色索引的三维物体记录，在真实世界测试中达到71/80的成功率，而匹配基线为39/80。FM-VLA则将腕部力历史压缩为8个记忆标记；在三个接触密集型任务上，其平均成功率为83.3%，而无记忆策略为27.8%。这些研究共同表明，有用的记忆应保留物理事件和实体，而不只是增加更多过去的图像。

#### 资料来源
- [Closing the Loop in Humanoid VLA: Persistent 3D Object Tokens for Verifiable Loco-Manipulation](../Inbox/2026-07-20--closing-the-loop-in-humanoid-vla-persistent-3d-object-tokens-for-verifiable-loco-manipulation.md): 持久化三维物体标记将真实世界人形机器人任务的成功率从39/80提高到71/80，覆盖八类任务。
- [FM-VLA: Force-based Memory for Vision-Language-Action Models in Contact-Rich Manipulation](../Inbox/2026-07-20--fm-vla-force-based-memory-for-vision-language-action-models-in-contact-rich-manipulation.md): 8个力记忆标记在三个接触密集型任务上支持83.3%的平均成功率，并仅增加3.3毫秒延迟。

### 结构化表示高效引导行动
多篇论文通过显式保留通用表示会丢弃的结构来改善控制。Patch Policy保留密集的Vision Transformer图像块；在使用5155万参数而非76.1亿参数的情况下，其真实机器人结果优于OpenVLA-OFT。SAGE在提出动作前预测可到达的潜在子目标，使PushT在规划时域为150时的成功率从12.7%提升到64.7%。GeoWorldAD同样根据当前和预测的三维几何信息规划驾驶轨迹，在NAVSIM v1上达到91.0 PDMS。共同机制是缩小并面向行动的搜索空间，而不只是扩大规模。

#### 资料来源
- [Patch Policy: Efficient Embodied Control via Dense Visual Representations](../Inbox/2026-07-20--patch-policy-efficient-embodied-control-via-dense-visual-representations.md): 密集图像块特征改善了控制，而报告中的策略仅使用5155万参数，延迟为10.99毫秒。
- [SAGE: Subgoal-Conditioned Action Generation for Latent World Model Planning](../Inbox/2026-07-20--sage-subgoal-conditioned-action-generation-for-latent-world-model-planning.md): 在使用同一个冻结世界模型的情况下，子目标条件动作提议将规划时域为150时的PushT成功率从12.7%提高到64.7%。
- [GeoWorldAD: Geometry World Action Model for Autonomous Driving](../Inbox/2026-07-20--geoworldad-geometry-world-action-model-for-autonomous-driving.md): 当前和未来几何标记在NAVSIM v1上支持报告的91.0 PDMS，在NAVSIM v2上支持90.4 EPDMS。

### 推理仍取决于架构
显式的中间计算本身并不能证明控制具有鲁棒性，也不能证明模型具备因果理解。在一项VLA比较中，加入高斯视觉噪声后，潜在迭代推理的成功率降至14.8%，而文本思维链仍保持92.7%；一次自适应攻击还将基于推理的检测器AUC从0.996降至0.493。另一项视频研究发现，生成器即使缺乏较强的显式因果感知，也能生成看似合理的后续内容。这些结果收窄了可作出的结论：必须在推理影响行动或预测结果的环节检验其作用。

#### 资料来源
- [Reasoning as a Double-Edged Sword: Architecture and Cross-Stage Robustness in Vision-Language-Action Models](../Inbox/2026-07-20--reasoning-as-a-double-edged-sword-architecture-and-cross-stage-robustness-in-vision-language-action-models.md): 跨阶段测试显示，鲁棒性会因架构而发生崩溃；在自适应攻击下，监测性能降至接近随机水平。
- [Thinking in Video: Can Video Generators Really Reason About the Real World?](../Inbox/2026-07-20--thinking-in-video-can-video-generators-really-reason-about-the-real-world.md): 双评审基准识别出因果感知与合理视频预测之间的差距；现有摘录未提供模型的数值评分。
