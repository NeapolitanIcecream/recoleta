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
- requirements-engineering
- uml-generation
- large-language-models
- software-modeling
- llm-as-a-judge
relevance_score: 0.02
run_id: materialize-outputs
---

# Class Model Generation from Requirements using Large Language Models

## Summary
本文研究大语言模型能否把自然语言需求自动转换为 UML 类图，并进一步评估 LLM 是否也能充当可靠的图质量评审者。作者提出了一个“LLM 生成 + LLM 判审 + 人类复核”的双重验证框架，用于需求工程中的自动建模。

## Problem
- 软件需求到 UML 类图的转换通常依赖人工完成，耗时、需要专业知识，且容易在需求工程师与利益相关者之间产生误解。
- 现有自动化方法多为规则式 NLP，泛化到复杂或异构领域需求时能力有限；而 LLM 在这项任务上的真实效果与可靠性仍缺乏系统验证。
- 在很多真实场景中没有标准答案类图，因此不仅要问“LLM 能否生成好图”，还要问“LLM 能否可靠地评价这些图”。

## Approach
- 比较 4 个生成模型：GPT-5、Claude Sonnet 4.0、Gemini 2.5 Flash Thinking、Llama-3.1-8B-Instruct，从自然语言需求生成 PlantUML 类图。
- 使用链式思维提示，把任务拆成：抽取实体/属性/关联、决定继承与接口、补全多重性、最后检查 PlantUML 语法。
- 在 8 个异构数据集上测试，覆盖数据管理、回收系统、露营、医疗、嵌入式、库存、起搏器、网络物理系统等领域；需求规模从 12 到 187 条不等。
- 用两个独立 LLM 评审器（Grok、Mistral Small 3.1 24B）做成对比较，按 5 个维度打分：完整性、正确性、标准符合性、可理解性、术语一致性。
- 再用人类专家做 human-in-the-loop 验证，并结合 Spearman 相关、Cohen’s kappa、显著性检验和 Cohen’s d 分析 LLM 评审与人类评审的一致性。

## Results
- 论文声明 LLM 能生成“结构连贯且语义有意义”的 UML 类图，并且 LLM 评审与人类评审之间存在“显著一致性”，支持其在自动化需求工程流程中同时作为建模助手和评估器使用。
- 实验覆盖 **8 个数据集**、**4 个生成模型**、**2 个 LLM judges**，评价维度为 **5 项质量标准**。
- 数据集需求数量分别为：g14-datahub **67**、g04-recycling **51**、g12-camperplus **13**、UHOPE **12**、Autopilot **14**、Finite State Machine **13**、Inventory **22**、Pacemaker **187**。
- 文本节选未给出具体的最终性能数值，如各模型胜率、Spearman \(\rho\)、Cohen’s kappa、Cohen’s d、p 值或人类对比打分，因此无法报告精确的量化领先幅度。
- 目前可确认的最强具体结论是：作者声称双重验证框架表明 LLM 生成的 UML 图在结构和语义上可用，且基于 LLM 的自动评价与专家判断“高度对齐/一致”。

## Link
- [http://arxiv.org/abs/2603.09100v1](http://arxiv.org/abs/2603.09100v1)
