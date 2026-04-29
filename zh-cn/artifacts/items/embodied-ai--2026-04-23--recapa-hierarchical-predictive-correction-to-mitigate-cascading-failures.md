---
source: arxiv
url: http://arxiv.org/abs/2604.21232v1
published_at: '2026-04-23T02:57:50'
authors:
- Xiyin Zeng
- Yuyu Sun
- Haoyang Li
- Shouqiang Liu
- Hao Wang
topics:
- vision-language-action
- embodied-agents
- hierarchical-planning
- error-correction
- long-horizon-control
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# ReCAPA: Hierarchical Predictive Correction to Mitigate Cascading Failures

## Summary
## 摘要
ReCAPA 是一个面向长时程具身任务的视觉-语言-动作框架，目的是防止早期错误扩散到计划的其余部分。它在动作、子目标和完整轨迹三个层级加入纠错机制，并在 VisualAgentBench、MineDojo 和 AI2-THOR 上报告了性能提升。

## 问题
- 长时程 VLA 智能体常常会在某个中间步骤出错后失败，因为局部错误会改变后续子目标和动作，并引发级联失败。
- 现有方法通常依赖固定的任务分解或事后修正，因此介入较晚，而且可能只让局部步骤保持一致，却逐渐偏离整体任务意图。
- 这很重要，因为导航、操作和合成等具身任务需要许多相互依赖的决策；论文引用的先前结果显示，在 VirtualHome 和 AI2-THOR 等基准上，一个子目标错误就可能让后续步骤的表现下降超过 60%。

## 方法
- ReCAPA 在行为上构建了一个三层层级：动作、子目标和完整轨迹。较低层会预测上一级的表示，因此模型可以更早发现不匹配。
- 核心模块是分层预测纠错（HPCC）。它使用 Transformer 预测器和 InfoNCE 损失，让动作片段预测子目标嵌入，让子目标片段预测轨迹嵌入。
- 它还用两种方式加入提示-轨迹对齐：一种是基于 Sinkhorn 最优传输损失的全局对齐，用于整个轨迹与指令之间的一致性；另一种是 score-field 模块，用于为逐步偏差提供局部纠正梯度。
- 在推理阶段，LLM（GPT-4o-mini）会提出子目标和完成条件。随后 ReCAPA 使用子目标相似度和轨迹层面的 Sinkhorn 一致性来过滤或重排候选动作，并在阈值不满足时使用回退规则。
- 论文还提出了两个用于分析失败动态的诊断指标：错误传播率（EPR），衡量一次错误会在多大程度上提高后续出错概率；传播衰减系数（PAC），衡量错误影响衰减的速度。

## 结果
- 在 **AI2-THOR** 上，ReCAPA 达到 **SR 0.75**，超过 **LLaMAR 0.68** 和 **GPT-4V 0.66**；同时还报告了 **TR 0.93** 和 **Balance 0.93**。
- 在 **VisualAgentBench** 上，ReCAPA 报告 **58.65 AVG**，高于 **GPT-4o mini 54.15**、**Gemini 2.5 Flash 53.00** 和 **Claude-4-Sonnet 50.25**。分领域来看，它在 OmniGibson 上得到 **50.6**，在 Minecraft 上得到 **66.7**。
- 论文称，相比强基线，ReCAPA 在 **VisualAgentBench** 上相对提升 **+5.65%**，在 **MineDojo** 上提升 **+9%**，在 **AI2-THOR** 上提升 **+7%**。
- 在错误传播方面，针对 **OmniGibson** 且 **k=10** 时，ReCAPA 报告 **EPR_10 = 0.082**，而 **GPT-4o-mini** 和 **Gemini-2.5** 约为 **0.3**，**Claude-4-sonnet** 高于 **0.45**。
- 在消融实验中，移除 HPCC 会使 **Behavior SR 从 72.2 降到 59.3**。在 AI2-THOR 上，**HPCC-AT** 达到 **0.73 SR**，**HPCC-ST 0.69**，两者都高于仅使用动作+子目标的变体。论文称，同时使用 Sinkhorn 和 Score-field 会得到最佳整体表现。
- 对于 **MineDojo**，摘录中给出了较强的定性结论，例如在 **10 个**长时程任务中的 **8 个**上领先，但提供的文本中没有完整的任务表。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.21232v1](http://arxiv.org/abs/2604.21232v1)
