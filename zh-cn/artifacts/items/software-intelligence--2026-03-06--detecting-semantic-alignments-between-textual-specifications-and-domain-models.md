---
source: arxiv
url: http://arxiv.org/abs/2603.06037v1
published_at: '2026-03-06T08:46:57'
authors:
- Shwetali Shimangaud
- "Lola Burgue\xF1o"
- Rijul Saini
- "J\xF6rg Kienzle"
topics:
- requirements-engineering
- domain-modeling
- semantic-alignment
- llm-for-se
- traceability
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Detecting Semantic Alignments between Textual Specifications and Domain Models

## Summary
本文提出一种用于检测**文本需求规格**与**领域模型元素**之间语义对齐/错配的方法，目标是帮助建模者验证模型是否正确并给出证据句。其核心是把模型元素先转成自然语言，再用LLM判断它与需求句子是否等价、矛盾或被包含。

## Problem
- 领域模型在软件工程早期很重要，但从自然语言需求中构建正确模型并建立清晰追踪链接，对新手尤其困难。
- 现有自动/半自动建模方法生成的模型仍需要人工验证；而同一需求往往不存在唯一正确模型，导致验证更难。
- 需要一种方法能指出**哪些模型元素是正确的、哪些是错误的、依据是哪几句需求文本**，以支持教学、建模辅助和离线质量检查。

## Approach
- 先用**规则式NLP**预处理文本需求，抽取文本概念、关系及其对应句子；再对领域模型做**切片**，为每个属性、关联、继承、枚举等提取最小上下文。
- 对每个模型元素，系统用规则把模型切片生成一句简单自然语言描述，例如把属性/关联转成“a car has a plate”这类句子。
- 再通过**语义匹配器**，把模型元素与需求中可能相关的句子对齐，得到每个元素的候选证据句集合。
- 最后用**GPT-4零样本**执行三类判断：语义等价、语义矛盾、语义包含；每类判断都使用多种语义等价提示词，并通过**相对多数投票**减少提示敏感性。
- 分类规则很直接：若任一句与模型描述等价则判为aligned；若无等价但有矛盾则判为misaligned；若无矛盾但需求句包含模型句含义则也判为aligned；否则为unclassified。

## Results
- 论文声称在来自文献的多个不同领域示例，以及由正确模型经**mutation**系统生成错误模型的评测上，能够识别对齐与错配，**precision接近1.0**。
- 召回率约为**78%**，意味着系统能对**超过3/4**的模型元素给出判断，但仍有一部分会保留为unclassified。
- 运行时间约为**每个模型元素18秒到1分钟**，说明方法更适合建模辅助或离线验证，而非极低延迟场景。
- 文中还说明其优势在于**几乎不会把元素错误分类**，并且会返回支持判定的原始需求句，便于在建模工具中提供正向反馈或警告。
- 摘要未给出更细粒度的基准对比数字（如与其他方法在同一数据集上的直接比较），因此最强定量结论主要是**precision≈1、recall≈78%、18s–1min/element**。

## Link
- [http://arxiv.org/abs/2603.06037v1](http://arxiv.org/abs/2603.06037v1)
