---
kind: trend
trend_doc_id: 160
granularity: day
period_start: '2026-04-20T00:00:00'
period_end: '2026-04-21T00:00:00'
topics:
- robotics
- vision-language-action
- long-horizon manipulation
- reasoning
- spatial modeling
run_id: materialize-outputs
aliases:
- recoleta-trend-160
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/long-horizon-manipulation
- topic/reasoning
- topic/spatial-modeling
language_code: zh-CN
---

# VLA 论文把执行结构显式化，而更严格的测试暴露出推理缺口

## Overview
这一天最突出的点是：VLA 工作正在把任务结构明确写进控制回路。HELM、ST-π 和 ReFineVLA 分别把记忆、子任务计划或推理监督做成具名组件，并带来了可测量的效果。与之配套的一篇基准论文 BeTTER 则指出，即使基准分数很高，模型在指代落地和重组上仍然存在明显缺口。

## Clusters

### 面向长时程操作的结构化执行
长时程机器人控制正在被构建为一个执行系统，而不只是更大的策略。HELM 是最清楚的例子。它加入了情节记忆、执行前的学习式失败检查，以及基于回滚的恢复机制。在 LIBERO-LONG 上，这让 OpenVLA 从 58.4% 提升到 81.5%。论文还显示，单纯延长上下文帮助小得多，在 H=32 时只达到 63.8%。ST-π 在规划层也走的是同一方向。它预测带有语义意图、目标位置和持续时间的 chunk 级提示，然后把每个 chunk 交给步级动作生成器。论文报告的 STAR 数据集也把这种结构直接写了出来：包含 30 个真实世界任务、每个任务 50 条演示，以及约 30 万个交互步骤。

#### Evidence
- [HELM: Harness-Enhanced Long-horizon Memory for Vision-Language-Action Manipulation](../Inbox/2026-04-20--helm-harness-enhanced-long-horizon-memory-for-vision-language-action-manipulation.md): HELM 关于记忆、验证、恢复以及上下文长度对比的总结和结果
- [ST-$π$: Structured SpatioTemporal VLA for Robotic Manipulation](../Inbox/2026-04-20--st-p-structured-spatiotemporal-vla-for-robotic-manipulation.md): ST-π 关于 chunk 级规划、动作生成和 STAR 数据集的总结

### 推理监督遇到更严格的压力测试
推理正更直接地被训练进 VLA 模型，但评估信号表明，目前的提升仍然比较脆弱。ReFineVLA 在微调中加入教师编写的解释，并报告了更好的 SimplerEnv 结果，包括 WidowX 上 47.7% 的平均成功率、variant aggregation 上 68.8%，以及 visual matching 上 76.6%。同一天发布的另一篇工作也更严格地检验了这些模型到底学到了什么。BeTTER 通过可控干预测试指代落地、重组和时间压力。在这些测试下，强模型在未见过的子目标组合上明显失效：pi_0.5 在 B->C 上降到 5.0%，GR00T-N1.6 降到 15.0%，Being-H0.5 降到 0.0%。目前的情况很明确：推理监督可以提升基准表现，但面对任务结构变化时的鲁棒性仍然是弱项。

#### Evidence
- [ReFineVLA: Multimodal Reasoning-Aware Generalist Robotic Policies via Teacher-Guided Fine-Tuning](../Inbox/2026-04-20--refinevla-multimodal-reasoning-aware-generalist-robotic-policies-via-teacher-guided-fine-tuning.md): ReFineVLA 关于解释引导微调和基准提升的结果
- [Unmasking the Illusion of Embodied Reasoning in Vision-Language-Action Models](../Inbox/2026-04-20--unmasking-the-illusion-of-embodied-reasoning-in-vision-language-action-models.md): BeTTER 基准结果，显示模型在指代落地和未见组合上的失败

### 3D 与时空结构进入策略核心
空间建模是另一条很强的主线，多篇论文都在尝试让 VLA 策略更好地控制几何结构和动作精度。OmniVLA-RL 将三专家 transformer、显式 3D 场景特征和在线强化学习结合起来。论文给出的核心结果是在 LIBERO 上达到 97.6% 的平均成功率，不过现有摘录没有包含完整的对比表。ST-π 也把空间和时间都当作核心输入，为每个子任务预测空间目标和时间长度。这两篇论文的重点都很具体：通过让空间结构在动作流水线内部可见，而不是埋在融合后的嵌入里，来提升抓取、放置和多阶段控制。

#### Evidence
- [OmniVLA-RL: A Vision-Language-Action Model with Spatial Understanding and Online RL](../Inbox/2026-04-20--omnivla-rl-a-vision-language-action-model-with-spatial-understanding-and-online-rl.md): OmniVLA-RL 关于 3D 空间建模、Flow-GSPO 和 LIBERO 结果的总结
- [ST-$π$: Structured SpatioTemporal VLA for Robotic Manipulation](../Inbox/2026-04-20--st-p-structured-spatiotemporal-vla-for-robotic-manipulation.md): ST-π 关于 chunk 级提示中的空间目标和时间长度的总结
