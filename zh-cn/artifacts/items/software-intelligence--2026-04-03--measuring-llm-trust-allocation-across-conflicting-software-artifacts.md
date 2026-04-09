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
TRACE 衡量 LLM 软件助手在代码、文档、签名和测试上下文相互冲突时如何分配信任。论文表明，当前模型发现文档问题的可靠性高于发现实现漂移，而且它们的置信度通常与实际检测质量不一致。

## 问题
- 面向软件工程的 LLM 评测通常只看最终输出，例如生成的测试或补丁得分如何，但这无法说明模型在生成结果时是否信任了正确的工件。
- 在真实的软件任务中，Javadoc、方法签名、实现和测试前缀可能彼此不一致；模型可能给出看起来合理的答案，但依赖了错误的信息源。
- 这会影响对正确性要求高的工作流，因为隐藏的信任错误可能通过下游检查，却仍然编码了错误的行为。

## 方法
- 论文提出 **TRACE**（Trust Reasoning over Artifacts for Calibrated Evaluation），这是一个框架，要求模型针对四类工件输出结构化 JSON 信任轨迹：Javadoc、签名、方法实现和测试前缀。
- 每条轨迹都包含各工件的质量分数、两两冲突判断、带受影响工件归因的不一致报告、来源优先级排序，以及模型置信度。
- 作者构建了一个基准，包含来自 **25** 个真实系统的 **456** 组人工整理的 Java 方法包，然后为每组构造 **6** 个扰动变体，再加上干净版本，共 **3,192** 个评测实例。
- 扰动包括缺失文档字段、注入的 Javadoc 缺陷、注入的实现缺陷，以及明确的 Javadoc–实现矛盾，严重程度分为 **heavy / normal / subtle**。
- 他们在相同提示和盲扰动设置下运行了 **7** 个模型，在 **22,344** 次 API 调用中得到 **22,339** 条有效轨迹。

## 结果
- 在全部七个模型中，质量惩罚大多集中在被扰动的工件上，并且会随严重程度增加而增大。对于 Javadoc 缺陷，heavy 到 subtle 的分数差为 **0.152–0.253**；对于实现缺陷，这个差值只有 **0.049–0.123**。
- 同时移除 Javadoc 描述和 `@return` 会让 Javadoc 分数下降 **-0.300 to -0.463**，而 MUT 分数变化不到 **0.020**，总体分数下降 **-0.109 to -0.155**。
- 模型对显式文档缺陷的检测率约为 **67–95%**，对 Javadoc–MUT 矛盾的检测率约为 **50–91%**。
- 当只有实现发生漂移而文档仍然看起来合理时，不一致检测率在摘要中下降约 **7–42 个百分点**，在 RQ2 总结中下降约 **21–43 个百分点**。
- **7** 个模型中有 **6** 个的置信度校准较差。
- 干净输入基线校准在不同模型之间差异很大：在相同基础数据集上，GPT-4o 和 Grok 4 Fast Reasoning 的平均总体分数是 **0.713**，Claude Sonnet 4.6 是 **0.555**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.03447v1](http://arxiv.org/abs/2604.03447v1)
