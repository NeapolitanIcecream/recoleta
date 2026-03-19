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
- llm-based-validation
- traceability
relevance_score: 0.01
run_id: materialize-outputs
language_code: zh-CN
---

# Detecting Semantic Alignments between Textual Specifications and Domain Models

## Summary
本文提出一种用于检测**文本需求规格**与**领域模型**之间语义对齐/失配的方法，目标是帮助建模者验证模型元素是否被需求正确支持。方法把规则式NLP、模型切片、模板化句子生成与LLM判别结合起来，并给出可追溯的证据句子。

## Problem
- 解决的问题：判断一个完整或部分完成的领域模型中的元素，是否与原始自然语言需求**语义一致**、**语义冲突**，或**证据不足**。
- 这很重要，因为从文本创建正确的领域模型本就困难，尤其对新手建模者；错误模型会影响需求分析、追踪与后续模型驱动开发。
- 现有自动生成/链接方法仍需人工验证，而“同一需求可对应多种正确模型”使验证本身很难自动化。

## Approach
- 先用**规则式NLP预处理**需求文本，抽取文本概念、关系及它们对应的原句集合。
- 对领域模型中的每个元素（属性、关联、组合、继承、枚举等）提取一个**最小模型切片**，保留理解该元素所需的最小上下文。
- 用启发式**语义匹配器**把模型元素与需求中的相关句子对应起来，确定“哪些句子在谈这个元素”。
- 再用规则把每个模型切片转成一条**人工自然语言句子**，例如把属性/关联改写成简单英文句。
- 最后用LLM对“生成句”与“匹配到的原句”做三类判断：**等价**、**矛盾**、**包含**；对每类问题使用多种等义提示词并做**相对多数投票**，将元素分类为 aligned / misaligned / unclassified，并输出证据句。

## Results
- 在文献中的多个示例领域上进行了评估，数据由**文本规格 + 参考领域模型**组成，并另外通过**mutation**从正确模型系统性构造带错模型。
- 论文声称可识别对齐与失配，**precision 接近 1.0**，说明几乎不会把模型元素错误分类。
- **recall 约为 78%**，意味着可对超过 **3/4** 的模型元素给出分类，其余为证据不足的未分类。
- 推理耗时为**每个模型元素 18 秒到 1 分钟**。
- 文中最明确的对比式结论不是与具体SOTA数值基线的全面表格比较，而是强调：该算法“几乎从不错误分类”，且能覆盖大部分元素，因此适合集成到建模工具中做即时反馈、警告或离线质量评估。

## Link
- [http://arxiv.org/abs/2603.06037v1](http://arxiv.org/abs/2603.06037v1)
