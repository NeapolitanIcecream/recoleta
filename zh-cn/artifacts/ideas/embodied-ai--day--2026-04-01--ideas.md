---
kind: ideas
granularity: day
period_start: '2026-04-01T00:00:00'
period_end: '2026-04-02T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robot-manipulation
- surgical-ai
- world-model-safety
tags:
- recoleta/ideas
- topic/robot-manipulation
- topic/surgical-ai
- topic/world-model-safety
language_code: zh-CN
---

# 接触前控制检查

## Summary
这一时期的控制工作指向三个具体的流程变化。在机器人操作中，扭矩应该在接触时进入策略，而不是贯穿整个动作。在手术自动化中，工具-动作特定的安全区域热图可以作为可见的接触前检查。在世界模型规划中，评估应跟踪小扰动是否会持续并跨滚动改变动作，因为普通的一步准确率无法捕捉这种暴露。

## 接触门控扭矩融合用于扩散策略操作
对已经在接触密集任务上运行基于视觉的扩散策略的机器人操作团队来说，接触门控的扭矩路径是一个实用升级。论文结果范围很窄，但很有用：只有在接触开始后才读取扭矩时，扭矩才会带来帮助，而且在视觉无法显示插入状态、摩擦或负载的任务上收益很大。在报告的设置中，视觉-扭矩自适应融合在瓶子放置、连接器拔出和煮蛋器盖打开三个任务上的平均成功率达到 82.0%，高于仅做扭矩门控的 68.0%，也远高于仅视觉的 30.0%。瓶子实验最能说明部署价值。仅视觉在空瓶上是 8/10，在满瓶上是 0/10；自适应模型在空瓶上保持 9/10，在满瓶上是 7/10。

实现方式很直接：在关节外部扭矩上加一个接触检测器，在自由运动时把扭矩分支置零，并记录融合权重何时启用。这样团队在重训更大的策略栈之前就能做一个具体测试。一个低成本验证办法是回放现有机器人日志，测量失败是否集中在首次接触窗口，然后在相同 SKU、相同重量或贴合变化条件下，对比仅视觉策略和接触门控变体。仓储、轻量装配和家电操作团队会先关心这个方案，因为他们本来就会遇到接触前看起来相近、夹爪加载后表现不同的对象。

### Evidence
- [Learning When to See and When to Feel: Adaptive Vision-Torque Fusion for Contact-Aware Manipulation](../Inbox/2026-04-01--learning-when-to-see-and-when-to-feel-adaptive-vision-torque-fusion-for-contact-aware-manipulation.md): Summary gives the contact-gated fusion design and the headline 82.0% vs 68.0% vs 30.0% benchmark results.
- [Learning When to See and When to Feel: Adaptive Vision-Torque Fusion for Contact-Aware Manipulation](../Inbox/2026-04-01--learning-when-to-see-and-when-to-feel-adaptive-vision-torque-fusion-for-contact-aware-manipulation.md): Paper text states why vision misses alignment, insertion depth, and contact state in contact-rich tasks.

## 手术工具动作的接触前安全区域叠加
密集安全区域热图可以直接作为胆囊切除手术自动化流程中的接触前检查。AffordTissue 从视频历史和文本提示中预测工具-动作特定的组织交互区域，它的价值在于提供可在工具碰到组织前检查的空间精度。在报告的基准上，ASSD 降到 20.557 px，而 Molmo-VLM 是 60.184 px，SAM3 是 81.138 px。PCK@0.05 达到 0.517，而基线分别停在 0.095 和 0.128。

这给正在构建半自主手术动作的团队指向了一个具体的支撑层：在控制台里显示预测热图，当计划接触点离开允许区域时阻止工具移动，并把热图和动作日志一起保存供回看。消融实验把产品要求说得很清楚。语言提示不是可有可无的，因为去掉语言编码器后 ASSD 升到 43.135 px。工具和动作条件也很重要，所以通用解剖掩码不足以直接部署。一个低成本验证办法是回顾性运行模型，拿预测区域和专家标注的接触点对比，统计热图会在多少次险些碰触或偏离目标的接近动作前触发提前停止。

### Evidence
- [AffordTissue: Dense Affordance Prediction for Tool-Action Specific Tissue Interaction](../Inbox/2026-04-01--affordtissue-dense-affordance-prediction-for-tool-action-specific-tissue-interaction.md): Summary reports the benchmark metrics and ablations showing the value of language, tool, and action conditioning.
- [AffordTissue: Dense Affordance Prediction for Tool-Action Specific Tissue Interaction](../Inbox/2026-04-01--affordtissue-dense-affordance-prediction-for-tool-action-specific-tissue-interaction.md): Paper text states that the heatmap can support explicit policy guidance and early safe stop when tools deviate outside predicted safe zones.

## 世界模型滚动评估的轨迹持续性测试
轨迹持续性测试是给使用想象滚动进行规划的团队添加到世界模型评估中的一项具体检查。论文没有证明已部署系统的下游失败率，但它给出了一个可测的审计目标：一个小扰动在模型向前滚动时会增长多少。在报告的基于 GRU 的 RSSM 实验中，第 1 步的放大比达到 2.26x，经过对抗微调后效果减少了 59.5%。一个随机 RSSM 代理模型降到 0.65x，这说明暴露程度取决于架构。

工作流上的变化是在机器人或驾驶的规划器里使用世界模型之前，把持续性检查和普通预测误差指标放在一起。团队可以把有界扰动注入输入或潜在状态，向前展开多个步骤，记录动作建议是漂移还是恢复。论文关于 DreamerV3 的证据只限于检查点探测中出现非零动作漂移，所以这里的直接用途是内部红队测试框架，而不是宣称生产系统不安全。一个低成本的第一步，是在同一组扰动测试上比较同一家族模型的确定性版本和随机版本，并记录规划器选定的动作在整个滚动跨度内有多少次变化。

### Evidence
- [Safety, Security, and Cognitive Risks in World Models](../Inbox/2026-04-01--safety-security-and-cognitive-risks-in-world-models.md): Summary defines trajectory persistence and reports the 2.26x amplification ratio, 59.5% reduction under adversarial fine-tuning, and 0.65x stochastic proxy result.
- [Safety, Security, and Cognitive Risks in World Models](../Inbox/2026-04-01--safety-security-and-cognitive-risks-in-world-models.md): Paper text describes proof-of-concept trajectory-persistent attacks and checkpoint-level probing of DreamerV3 with non-zero action drift.
