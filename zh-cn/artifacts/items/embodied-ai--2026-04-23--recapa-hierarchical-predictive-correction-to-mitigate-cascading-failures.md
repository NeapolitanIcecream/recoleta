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
## 总结
ReCAPA 是一个面向长视野具身任务的视觉-语言-动作框架，目标是阻止早期错误沿着后续计划扩散。它在动作、子目标和完整轨迹三个层面加入纠错，并在 VisualAgentBench、MineDojo 和 AI2-THOR 上报告了性能提升。

## 问题
- 长视野 VLA 代理在一个中间步骤出错后，常常会失败，因为局部错误会改变后续子目标和动作，进而造成连锁失败。
- 现有方法往往依赖固定的任务拆分或事后修正，所以反应偏晚，可能让局部步骤保持对齐，却偏离整体任务意图。
- 这对具身任务很重要，因为导航、操作和制作都需要很多相互依赖的决策；论文引用了先前结果，指出在 VirtualHome 和 AI2-THOR 等基准上，一个子目标错误会让后续步骤表现下降超过 60%。

## 方法
- ReCAPA 在行为上建立了三层结构：动作、子目标和完整轨迹。低层预测更高一层的表示，这样模型可以更早发现不匹配。
- 主要模块 Hierarchical Predictive Correction (HPCC) 使用 Transformer 预测器和 InfoNCE 损失，让动作片段预测子目标嵌入，让子目标片段预测轨迹嵌入。
- 它通过两种方式加入提示-轨迹对齐：一是用 Sinkhorn 最优传输损失做整条轨迹与指令之间的全局对齐，二是用 score-field 模块为逐步偏差提供局部纠正梯度。
- 在推理阶段，LLM（GPT-4o-mini）提出子目标和完成标准。ReCAPA 再根据子目标相似度和轨迹级 Sinkhorn 一致性对候选动作进行过滤或重排序，如果阈值不满足，则使用回退规则。
- 论文还提出了两个用于分析失败动态的诊断指标：Error Propagation Rate (EPR)，衡量一个错误会把后续错误概率抬高多少；Propagation Attenuation Coefficient (PAC)，衡量错误影响衰减得有多快。

## 结果
- 在 **AI2-THOR** 上，ReCAPA 达到 **SR 0.75**，超过 **LLaMAR 0.68** 和 **GPT-4V 0.66**；同时报告了 **TR 0.93** 和 **Balance 0.93**。
- 在 **VisualAgentBench** 上，ReCAPA 报告 **58.65 AVG**，高于 **GPT-4o mini 54.15**、**Gemini 2.5 Flash 53.00** 和 **Claude-4-Sonnet 50.25**。按领域看，它在 OmniGibson 上得分 **50.6**，在 Minecraft 上得分 **66.7**。
- 论文称，相比强基线，ReCAPA 在 **VisualAgentBench** 上提升 **+5.65%**，在 **MineDojo** 上提升 **+9%**，在 **AI2-THOR** 上提升 **+7%**。
- 在错误传播分析中，**OmniGibson** 上 **k=10** 时，ReCAPA 报告 **EPR_10 = 0.082**，而 **GPT-4o-mini** 和 **Gemini-2.5** 大约是 **0.3**，**Claude-4-sonnet** 则高于 **0.45**。
- 消融实验中，去掉 HPCC 会让 **Behavior SR** 从 **72.2** 降到 **59.3**。在 AI2-THOR 上，**HPCC-AT** 达到 **0.73 SR**，**HPCC-ST** 达到 **0.69**，两者都高于只用动作+子目标的变体。论文称 Sinkhorn 和 Score-field 一起使用时整体表现最好。
- 这段摘要对 **MineDojo** 给出了较强的定性结论，例如在 **10** 个长视野任务中有 **8** 个领先，但提供的文本里没有完整任务表。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.21232v1](http://arxiv.org/abs/2604.21232v1)
