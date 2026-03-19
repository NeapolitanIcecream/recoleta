---
source: arxiv
url: http://arxiv.org/abs/2603.09100v1
published_at: '2026-03-10T02:20:35'
authors:
- Jackson Nguyen
- Rui En Koe
- Fanyu Wang
- Chetan Arora
- Alessio Ferrari
topics:
- llm-for-software-engineering
- uml-class-diagram-generation
- requirements-engineering
- llm-as-a-judge
- plantuml
- human-in-the-loop
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Class Model Generation from Requirements using Large Language Models

## Summary
本文研究大语言模型能否把自然语言需求自动生成 UML 类图，并进一步检验 LLM 作为评审者是否能可靠评价这些图。核心贡献是一个“生成 + 双重验证”的流程：多模型生成 PlantUML，再用两个独立 LLM 裁判并结合人工评审进行验证。

## Problem
- 软件需求到 UML 类图的转换通常依赖人工建模，费时且需要较强领域知识，容易造成需求理解偏差。
- 现有自动化方法多依赖规则或传统 NLP，跨领域泛化能力有限，难以处理真实、异构需求文档。
- 若没有标准答案，如何既评估 LLM 生成的类图质量，又判断 LLM 评审是否可信，是落地自动化需求工程的关键问题。

## Approach
- 比较 4 个生成模型：GPT-5、Claude Sonnet 4.0、Gemini 2.5 Flash Thinking、Llama-3.1-8B-Instruct，从自然语言需求生成 PlantUML 类图。
- 在 8 个异构真实数据集上测试，覆盖数据管理、回收、露营、医疗、自动驾驶/嵌入式、库存、起搏器等领域；需求规模从 12 到 187 条不等。
- 使用链式提示，把任务拆成最简单的几个步骤：先抽取实体/属性/关系，再补充继承、多重性和类型，最后输出可编译的 PlantUML。
- 提出双重验证框架：由两个独立 LLM 裁判（Grok、Mistral Small 3.1 24B）做成对比较，并按 5 个维度打分：完整性、正确性、标准符合性、可理解性、术语一致性。
- 用 Spearman 相关、Cohen’s Kappa、显著性检验和 Cohen’s d 分析 LLM 评审之间及其与人工专家之间的一致性。

## Results
- 研究在 **8 个数据集**、**4 个生成模型**、**2 个 LLM 裁判** 上开展评估，需求文档规模范围为 **12–187 条需求**；这是文中给出的主要实验规模信息。
- 论文明确声称，LLM 生成的 UML 类图在结构和语义上“**structurally coherent and semantically meaningful**”，说明其已能从需求中提取实体、属性和关联并形成可用类图。
- 论文还声称，LLM 裁判与人工评审之间达到“**substantial alignment**”，并且 Grok 与 Mistral 的判断和人工意见具有较强一致性，支持 LLM 既可作建模助手，也可作评估者。
- 文本摘录**没有提供具体数值结果**，例如各模型在各数据集上的平均分、Spearman/Kappa/Cohen’s d 数值、最佳模型名称或相对基线提升幅度，因此无法报告精确的指标/数据集/基线对比数字。
- 最强的可验证结论是：相较于传统人工 UML 建模流程，作者认为该方法可为自动化需求工程工作流提供可行支持，尤其是在**无标准答案场景**下，通过“LLM-as-a-Judge + 人工复核”实现可扩展评估。

## Link
- [http://arxiv.org/abs/2603.09100v1](http://arxiv.org/abs/2603.09100v1)
