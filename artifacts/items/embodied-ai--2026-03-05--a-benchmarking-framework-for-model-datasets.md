---
source: arxiv
url: http://arxiv.org/abs/2603.05250v1
published_at: '2026-03-05T15:04:35'
authors:
- Philipp-Lorenz Glaser
- "Lola Burgue\xF1o"
- Dominik Bork
topics:
- benchmarking-framework
- model-datasets
- model-driven-engineering
- dataset-quality
- research-infrastructure
relevance_score: 0.06
run_id: materialize-outputs
---

# A Benchmarking Framework for Model Datasets

## Summary
本文提出一个用于**软件模型数据集本身**的基准测试框架与平台，目标是让MDE/AI研究中常被临时拼凑的数据集变得可测量、可比较、可复现。核心贡献不是新的学习模型，而是把模型数据集当作一等研究对象，系统评估其质量、代表性与任务适配性。

## Problem
- 现有MDE研究中的模型数据集通常是**临时收集或构建**的，缺少针对具体任务的质量保证。
- 数据集的**克隆、虚假/玩具模型、格式异构、标注与元数据缺失**会影响AI/LLM方法的训练与评测，导致结果不可比、难复现、且可能带偏差。
- 社区缺少一个**统一框架**来跨建模语言和格式地分析数据集本身，而不仅仅是基准测试算法或任务。

## Approach
- 提出一个**benchmarking framework for model datasets**：不是评估模型算法，而是系统测量数据集的质量、代表性和对特定任务的适用性。
- 设计一个**Benchmark Platform for MDE**，接收 UML、ArchiMate、Ecore 等模型，将其解析为统一的**中间表示**，再通过指标引擎提取描述性与结构性统计。
- 方法上把模型视为受元模型约束的**类型化图**，而非纯文本序列，因此同时关注词汇特征、结构复杂度、构造覆盖、重复/近重复、可解析性等特性。
- 框架强调**显式报告数据集属性**，支持跨数据集比较、生成benchmark报告，并帮助研究者判断某数据集是否适合分类、补全、修复、重构等不同任务。
- 论文还给出研究议程：调研相关领域基准方法、形式化核心指标、实现多语言原型，并在现有MDE数据集与已发表研究上评估实用性。

## Results
- 论文声称平台可处理**多种建模语言**，文中明确提到支持 **UML、ArchiMate、Ecore** 等，并可跨语言/格式生成统一报告。
- 文中综述并对比了多个现有数据集，规模跨度很大，例如 **ModelSet 10,586** 个模型、**EA ModelSet 977**、**Golden UML 45**、**Lindholmen 约93,000**、**SAP-SAM Signavio 1,021,471** 个模型、**AtlanMod Zoo 约300**、**OntoUML/UFO 127**、**Labeled Ecore 555**。
- 论文明确指出其平台将在**3个代表性数据集**上演示使用方式，但给定摘录中**没有提供具体实验指标、性能数值或与现有方法的定量对比**。
- 最强的具体主张是：该框架能够提升**数据集质量透明度、跨研究可比性与可复现性**，并补上现有MDE基准主要关注算法/任务、而非“数据集本身”的空缺。

## Link
- [http://arxiv.org/abs/2603.05250v1](http://arxiv.org/abs/2603.05250v1)
