---
source: arxiv
url: http://arxiv.org/abs/2604.16756v2
published_at: '2026-04-18T00:11:35'
authors:
- Francesco Sovrano
- Gabriele Dominici
- Alberto Bacchelli
topics:
- prompt-bias
- software-engineering
- llm-evaluation
- prompt-engineering
- reasoning-cues
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# Mitigating Prompt-Induced Cognitive Biases in General-Purpose AI for Software Engineering

## Summary
## 概要
这篇论文研究仅靠措辞变化，是否会把通用 AI 系统推向更差的软件工程决策，以及简单的提示方式能否解决这个问题。主要结果是，常见的提示技巧作用很小，而在提示中加入明确的软件工程最佳实践规则后，偏差敏感性平均下降约 51%。

## 问题
- 论文关注软件工程决策支持中的**提示诱发认知偏差**：即使任务逻辑不变，模型也会因为带偏向的措辞而改变答案，例如框架效应、流行度暗示或事后偏见线索。
- 这很重要，因为许多软件工程任务都以自然语言形式出现，比如需求、权衡问题、设计选择和优先级排序提示，所以细微的措辞变化就可能把模型推向更差的决策。
- 文中引用的先前 PROBE-SWE 结果显示，在八类偏差中，偏差敏感性范围为 **5.9% 到 35.3%**，在更复杂任务上可达 **49%**。

## 方法
- 作者使用 **PROBE-SWE**，这是一个由成对的带偏差与无偏差软件工程两难问题组成的基准数据集，二者逻辑匹配，用来隔离仅由措辞导致的答案变化。
- 他们在来自 **GPT、LLaMA 和 DeepSeek** 系列的低成本模型上测试了几种现成的提示方法：思维链、命令式自去偏、角色化自去偏，以及 implication prompting。
- 他们的核心观点是，软件工程决策需要明确的背景规则，例如最佳实践，但带偏向的措辞会让模型跳过这些隐含规则，转而采用捷径。
- 为此，他们提出了 **axiomatic background self-elicitation** 和 **axiomatic reasoning cues**：在模型回答前，先向提示中加入简短的陈述式软件工程规则。
- 他们还对输出语言做了主题分析，以识别与更高偏差敏感性相关的语言模式，并提到使用开放式回答做了稳健性检查，以及对 DevGPT 语料进行了分析。

## 结果
- 在 RQ1 上，常见提示方法并不能稳定解决这个问题。**思维链表现最差，平均敏感性为 16.1%**，而**无策略基线为 12.9%**。
- **Implication prompting** 的平均敏感性为 **13.3%**，也高于基线。
- **命令式自去偏（10.3%）** 和 **角色化自去偏（10.2%）** 都优于基线，两者组合 **BW+IsD** 达到 **8.3%**，比 **12.9%** 的基线下降 **4.6 个百分点**。
- 即便有这个下降，论文仍指出，在经过 FDR 校正后，BW+IsD、BW 和 IsD 单独使用时，**各偏差类别上都没有统计显著的下降**（**all p >= 0.07**），各模型层面也没有显著改进。
- 论文声称的主要突破是公理化提示方法，它**将总体偏差敏感性平均降低了约 51%（p < .001）**。
- 对某些偏差类型，降幅**最高可达 73%**。这段摘录没有给出该公理化方法完整的分偏差表，但这些是文中给出的最强定量结论。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.16756v2](http://arxiv.org/abs/2604.16756v2)
