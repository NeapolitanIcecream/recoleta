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
这一时期的控制方向研究指向三个具体的流程变化。在机器人操作中，力矩应该在接触时进入策略，而不是贯穿整个运动过程。在手术自动化中，特定工具-动作的安全区域热力图可以作为可见的接触前检查。在世界模型规划中，评估应跟踪小扰动是否会在多步 rollout 中持续并改变动作，因为普通的单步精度无法覆盖这种暴露。

## 用于扩散策略操作的接触门控力矩融合
对已经在接触密集型任务中使用视觉扩散策略的机器人操作团队来说，带接触门控的力矩通路是一个实用升级。论文的结果范围不大，但很有用：只有在接触开始后再读取力矩，力矩才会带来帮助；在视觉无法揭示插入状态、摩擦或载荷的任务上，收益很明显。在论文报告的设置中，自适应视觉-力矩融合在瓶子放置、连接器拔出和煮蛋器盖开启三项任务上的平均成功率达到 82.0%，高于仅使用力矩门控的 68.0%，也远高于纯视觉的 30.0%。瓶子实验最能说明部署价值。纯视觉对空瓶的成绩是 8/10，对满瓶是 0/10；自适应模型对空瓶保持 9/10，对满瓶达到 7/10。

实现方式很直接：在关节外力矩上加一个接触检测器，在自由运动阶段将力矩分支置零，并记录融合权重何时开启。这样，团队在重训更大的策略栈之前就有了一个明确的测试方案。一个低成本的验证方法是回放现有机器人日志，检查失败是否集中在首次接触窗口；然后在同一批存在重量或配合差异的 SKU 上，对比纯视觉策略和接触门控变体。仓储、轻型装配和家电搬运团队会最先关心这件事，因为他们已经遇到过这类情况：物体在接触前看起来相似，但夹爪加载后行为不同。

### Evidence
- [Learning When to See and When to Feel: Adaptive Vision-Torque Fusion for Contact-Aware Manipulation](../Inbox/2026-04-01--learning-when-to-see-and-when-to-feel-adaptive-vision-torque-fusion-for-contact-aware-manipulation.md): 摘要给出了接触门控融合设计，以及 82.0% 对 68.0% 对 30.0% 的主要基准结果。
- [Learning When to See and When to Feel: Adaptive Vision-Torque Fusion for Contact-Aware Manipulation](../Inbox/2026-04-01--learning-when-to-see-and-when-to-feel-adaptive-vision-torque-fusion-for-contact-aware-manipulation.md): 论文正文说明了在接触密集型任务中，视觉为什么会漏掉对齐情况、插入深度和接触状态。

## 用于手术工具动作的接触前安全区域叠加层
在胆囊切除术的手术自动化流程中，稠密安全区域热力图已经可以作为接触前检查来使用。AffordTissue 根据视频历史和文本提示预测特定工具-动作的组织交互区域，它的价值在于提供可供控制器或监督者在工具接触组织前检查的空间精度。在论文报告的基准上，ASSD 降到 20.557 px，而 Molmo-VLM 为 60.184 px，SAM3 为 81.138 px。PCK@0.05 达到 0.517，基线分别只有 0.095 和 0.128。

这为构建半自主手术动作的团队提供了一层明确的支持能力：在控制台中渲染预测热力图，当计划接触点离开允许区域时阻止工具运动，并将热力图与动作日志一同保存以供复查。消融实验也帮助界定了产品需求。语言提示不是可有可无的，因为去掉语言编码器后，ASSD 上升到 43.135 px。工具和动作条件同样重要，所以通用的解剖掩码不足以支持部署。一个低成本的验证方法是做回顾性分析：在已记录的手术过程上运行模型，将预测区域与专家标注的接触点对比，并统计热力图在险些出错或偏离目标接近之前本可以提前触发停止的次数。

### Evidence
- [AffordTissue: Dense Affordance Prediction for Tool-Action Specific Tissue Interaction](../Inbox/2026-04-01--affordtissue-dense-affordance-prediction-for-tool-action-specific-tissue-interaction.md): 摘要报告了基准指标和消融结果，说明语言、工具和动作条件输入都有价值。
- [AffordTissue: Dense Affordance Prediction for Tool-Action Specific Tissue Interaction](../Inbox/2026-04-01--affordtissue-dense-affordance-prediction-for-tool-action-specific-tissue-interaction.md): 论文正文指出，当工具偏离预测安全区域时，热力图可以支持显式策略引导和提前安全停止。

## 用于世界模型 rollout 评估的轨迹持续性测试
对在规划中使用想象式 rollout 的团队来说，轨迹持续性测试是世界模型评估中的一个具体补充。论文没有证明已部署系统中的下游失效率，但它给出了一个可测量的审计目标：小扰动在模型向前 rollout 时会放大多少。在论文报告的基于 GRU 的 RSSM 实验中，第 1 步的放大比达到 2.26x，对抗微调将这一效应降低了 59.5%。一个随机 RSSM 代理模型把该比值降到 0.65x，这说明暴露程度与架构有关。

流程上的变化是，在世界模型被用于机器人或驾驶规划器之前，除了常规预测误差指标外，还要加入持续性检查。团队可以向输入或潜在状态注入有界扰动，roll out 多个步骤，并跟踪动作建议是漂移还是恢复。论文中关于 DreamerV3 的证据仅限于检查点探测得到的非零动作漂移，因此眼下更直接的用途是做内部红队测试工具，而不是据此断言生产系统不安全。一个低成本的第一步是，在同一组扰动测试上比较同一模型家族的确定性版本和随机版本，并记录在 rollout 时间范围内规划器所选动作发生变化的频率。

### Evidence
- [Safety, Security, and Cognitive Risks in World Models](../Inbox/2026-04-01--safety-security-and-cognitive-risks-in-world-models.md): 摘要定义了轨迹持续性，并报告了 2.26x 的放大比、对抗微调下 59.5% 的下降，以及 0.65x 的随机代理结果。
- [Safety, Security, and Cognitive Risks in World Models](../Inbox/2026-04-01--safety-security-and-cognitive-risks-in-world-models.md): 论文正文描述了概念验证性质的轨迹持续型攻击，以及对 DreamerV3 的检查点级探测中观察到的非零动作漂移。
