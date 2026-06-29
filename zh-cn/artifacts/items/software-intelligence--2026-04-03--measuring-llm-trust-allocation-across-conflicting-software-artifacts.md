---
source: arxiv
url: http://arxiv.org/abs/2604.03447v1
published_at: '2026-04-03T20:38:14'
authors:
- Noshin Ulfat
- Ahsanul Ameen Sabit
- Soneya Binta Hossain
topics:
- llm-evaluation
- code-intelligence
- software-artifacts
- trust-calibration
- consistency-detection
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Measuring LLM Trust Allocation Across Conflicting Software Artifacts

## Summary
## 摘要
TRACE 衡量 LLM 软件助手在代码、文档、签名和测试上下文发生冲突时如何分配信任。论文显示，当前模型更可靠地发现文档问题，而不是实现漂移，而且它们的置信度通常与实际检测质量不一致。

## 问题
- 面向软件工程的 LLM 评估通常只给生成的测试或补丁打分，但看不出模型在生成时信任了哪个工件。
- 在真实的软件任务中，Javadoc、方法签名、实现和测试前缀可能彼此不一致；模型可以给出看似合理的答案，却依赖了错误来源。
- 这会影响对正确性要求很高的工作流，因为隐藏的信任错误可能通过下游检查，但仍然保留错误行为。

## 方法
- 论文提出 **TRACE**（Trust Reasoning over Artifacts for Calibrated Evaluation），这是一个框架，要求模型对四类工件输出结构化 JSON 信任轨迹：Javadoc、签名、方法实现和测试前缀。
- 每条轨迹包含各工件质量分数、成对冲突判断、不一致报告及受影响工件归因、来源优先级排序，以及模型置信度。
- 作者构建了一个基准集，包含来自 **25** 个真实系统的 **456** 组精选 Java 方法包，然后为每组生成 **6** 个扰动变体和 1 个干净版本，共 **3,192** 个评测实例。
- 扰动包括缺失文档字段、注入的 Javadoc 错误、注入的实现错误，以及在 **heavy / normal / subtle** 三种严重级别下的显式 Javadoc–实现矛盾。
- 他们用相同的提示词和盲扰动设置运行 **7** 个模型，在 **22,344** 次 API 调用中得到 **22,339** 条有效轨迹。

## 结果
- 在全部七个模型中，质量惩罚主要局限在被扰动的工件上，并且会随着严重程度增加。对 Javadoc 错误而言，heavy 到 subtle 的分差是 **0.152–0.253**；对实现错误而言，只有 **0.049–0.123**。
- 同时删除 Javadoc 描述和 `@return` 会让 Javadoc 分数下降 **-0.300 到 -0.463**，而 MUT 分数变化小于 **0.020**，总体分数下降 **-0.109 到 -0.155**。
- 模型对显式文档错误的检测率约为 **67–95%**，对 Javadoc–MUT 矛盾的检测率约为 **50–91%**。
- 当只有实现漂移而文档仍然看起来合理时，不一致检测率在摘要中的下降约为 **7–42 个百分点**，在 RQ2 总结中的下降约为 **21–43 个百分点**。
- **7** 个模型中有 **6** 个的置信度校准较差。
- 干净输入上的基线校准因模型而异：GPT-4o 和 Grok 4 Fast Reasoning 的平均总体分数为 **0.713**，而 Claude Sonnet 4.6 在同一基础数据集上的平均总体分数为 **0.555**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.03447v1](http://arxiv.org/abs/2604.03447v1)
