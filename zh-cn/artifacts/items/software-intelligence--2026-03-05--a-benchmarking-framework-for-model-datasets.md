---
source: arxiv
url: http://arxiv.org/abs/2603.05250v1
published_at: '2026-03-05T15:04:35'
authors:
- Philipp-Lorenz Glaser
- "Lola Burgue\xF1o"
- Dominik Bork
topics:
- benchmarking
- model-driven-engineering
- dataset-quality
- software-models
- llm-evaluation
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# A Benchmarking Framework for Model Datasets

## Summary
本文提出一个面向模型驱动工程（MDE）中“模型数据集”的基准测试框架与平台，用来评估数据集本身而不是只评估下游模型。其目标是让软件模型数据集的质量、代表性和任务适配性变得可测量、可比较、可复现。

## Problem
- 现有MDE与LLM研究越来越依赖UML、Ecore、ArchiMate等软件模型数据集，但这些数据集通常是**临时收集**的，缺少针对具体任务的系统质量评估。
- 这会导致**研究结果不可比、可复现性弱、偏差难以发现**；例如重复样本、虚假/占位模型、格式异构、命名质量差、结构分布失衡等都会影响训练和评测。
- 该问题之所以重要，是因为AI/LLM方法对数据质量高度敏感；若数据集本身不透明或不具代表性，下游结论和自动化能力都可能被误导。

## Approach
- 提出一个**benchmarking the dataset itself** 的框架：不是只测算法，而是系统衡量模型数据集的**质量、代表性、适用性**。
- 设计了一个统一的 **Benchmark Platform for MDE**，可接收 UML、ArchiMate、Ecore 等语言及其不同格式的模型。
- 平台先把输入模型解析到一个**标准化中间表示**（将模型视为受元模型约束的类型图），再通过专门的指标引擎提取**描述性统计和结构统计**。
- 输出**benchmark reports**，支持跨数据集比较，并帮助研究者判断某个数据集是否适合分类、补全、修复、重构等不同任务。
- 论文还梳理了模型数据集的特征、生命周期和代表性数据源，为后续形成核心指标集合与原型评测流程提供基础。

## Results
- 论文的核心贡献是**框架与平台提案**，并声明将在**3个代表性数据集**上展示平台用法；但给定摘录中**没有提供具体实验指标或性能数值**。
- 文中列举了多种现有数据集规模，说明问题具有现实基础：如 **ModelSet 10,586** 个模型、**EA ModelSet 977**、**Golden UML 45**、**SAP-SAM Signavio 1,021,471**、**Lindholmen 约93,000**、**AtlanMod Zoo 约300**、**OntoUML/UFO 127**、**Labeled Ecore 555**。
- 相比已有工作，作者声称其新意在于：现有基准多用于**工具、任务或模型变换**，而**没有工作专门对MDE中的数据集本身做基准测试**。
- 平台声称可跨**多建模语言与多序列化格式**进行统一分析，并提升**可比性、透明度与复现性**；但摘录未给出与现有方法相比的定量提升百分比或基线对照结果。

## Link
- [http://arxiv.org/abs/2603.05250v1](http://arxiv.org/abs/2603.05250v1)
