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

# VLA 论文把执行结构说清楚了，更严格的测试则暴露出推理缺口

## Overview
这一天最强的一点是：VLA 工作正在把任务结构明确地放进控制循环里。HELM、ST-π 和 ReFineVLA 分别加入了记忆、子任务计划或理由监督，而且都是带有可测效果的明确组件。配套的基准论文 BeTTER 也让这个领域保持克制，它显示高分基准成绩仍然留下了 grounding 和 recomposition 上的大缺口。

## Clusters

### 长时程操控的结构化执行
长时程机器人控制正在被构建成一个执行系统，而不只是更大的策略。HELM 是最清楚的例子。它加入了情景记忆、执行前的失败检查，以及基于回滚的恢复。在 LIBERO-LONG 上，这把 OpenVLA 从 58.4% 提升到 81.5%。论文还表明，单纯扩大上下文帮助小得多，在 H=32 时只到 63.8%。ST-π 在规划层面推进同样的思路。它预测带有语义意图、目标位置和持续时间的 chunk 级提示，然后把每个 chunk 交给 step 级动作生成器。论文报告的 STAR 数据集也把这种结构写得很清楚，包含 30 个真实世界任务、每个任务 50 个示范，以及约 300k 次交互步骤。

#### Evidence
- [HELM: Harness-Enhanced Long-horizon Memory for Vision-Language-Action Manipulation](../Inbox/2026-04-20--helm-harness-enhanced-long-horizon-memory-for-vision-language-action-manipulation.md): HELM summary and results on memory, verification, recovery, and context-length comparison
- [ST-$π$: Structured SpatioTemporal VLA for Robotic Manipulation](../Inbox/2026-04-20--st-p-structured-spatiotemporal-vla-for-robotic-manipulation.md): ST-π summary on chunk-level planning, action generation, and STAR dataset

### 推理监督遇上更 কঠ سخت的压力测试
推理正在更直接地被训练进 VLA 模型，但评测信号说明，当前提升仍然脆弱。ReFineVLA 在微调中加入教师撰写的理由说明，并报告了更好的 SimplerEnv 结果，包括 WidowX 上 47.7% 的平均成功率、variant aggregation 上 68.8%、visual matching 上 76.6%。同一天还有一个更严格的检验，用来看看这些模型到底学到了什么。BeTTER 对 grounding、重组和时间压力做了受控干预。在这些测试下，强模型在未见过的子目标组合上直接崩溃：pi_0.5 在 B->C 上降到 5.0%，GR00T-N1.6 降到 15.0%，Being-H0.5 降到 0.0%。这说明当前情况很清楚：推理监督可以提高基准成绩，但对任务结构变化的鲁棒性仍然很弱。

#### Evidence
- [ReFineVLA: Multimodal Reasoning-Aware Generalist Robotic Policies via Teacher-Guided Fine-Tuning](../Inbox/2026-04-20--refinevla-multimodal-reasoning-aware-generalist-robotic-policies-via-teacher-guided-fine-tuning.md): ReFineVLA results on rationale-guided fine-tuning and benchmark gains
- [Unmasking the Illusion of Embodied Reasoning in Vision-Language-Action Models](../Inbox/2026-04-20--unmasking-the-illusion-of-embodied-reasoning-in-vision-language-action-models.md): BeTTER benchmark results showing failures on grounding and unseen composition

### 3D 与时空结构进入策略核心
空间建模也是一个强线索，论文在尝试让 VLA 策略更好地控制几何和动作精度。OmniVLA-RL 把三专家 Transformer、显式 3D 场景特征和在线强化学习结合起来。报告中的亮点是 LIBERO 上 97.6% 的平均成功率，不过可见摘要没有给出完整对比表。ST-π 也把空间和时间当作一等输入，为每个子任务预测空间目标和时间持续时间。两篇论文的重点都很具体：通过让空间结构在动作管线内部可见，而不是把它埋在融合 embedding 里，来提升抓取、放置和多阶段控制。

#### Evidence
- [OmniVLA-RL: A Vision-Language-Action Model with Spatial Understanding and Online RL](../Inbox/2026-04-20--omnivla-rl-a-vision-language-action-model-with-spatial-understanding-and-online-rl.md): OmniVLA-RL summary on 3D spatial modeling, Flow-GSPO, and LIBERO result
- [ST-$π$: Structured SpatioTemporal VLA for Robotic Manipulation](../Inbox/2026-04-20--st-p-structured-spatiotemporal-vla-for-robotic-manipulation.md): ST-π summary on spatial targets and temporal durations in chunk-level prompts
