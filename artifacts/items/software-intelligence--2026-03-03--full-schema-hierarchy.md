---
source: hn
url: https://schema.org/docs/full.html
published_at: '2026-03-03T23:43:32'
authors:
- vinhnx
topics:
- schema-org
- knowledge-graph
- ontology
- structured-data
- metadata
relevance_score: 0.33
run_id: materialize-outputs
---

# Full Schema Hierarchy

## Summary
这不是一篇研究论文，而是 Schema.org 的完整模式层级页面，列出“事物类型”和“数据类型”的分类体系。它的价值在于为网页、知识图谱和结构化元数据提供统一词汇表，但文中没有提出新的算法或实验结果。

## Problem
- 解决的问题是：如何用统一、可扩展的模式来描述现实世界中的实体、属性和它们的层级关系，以支持结构化数据标注。
- 这很重要，因为缺少统一语义会导致网页数据、知识库和应用之间难以互操作、搜索理解差、自动处理成本高。
- 对软件与智能系统而言，它提供了一个可复用的语义骨架，但本页本身更像参考文档而非研究工作。

## Approach
- 核心机制很简单：把 Schema.org 定义成两套层级结构，一套描述“事物/类型（classes）”，另一套描述“文本属性值/数据类型（data types）”。
- 每个类型可以有一个或多个父类型；页面为了可读性，只在树中展示其中一个分支位置。
- 页面通过枚举大量具体类型与枚举值来构建完整层级，例如 `SoftwareSourceCode`、`WebSite`、`MedicalResearcher`、`OrderStatus` 等。
- 本质上，它不是训练模型或推理算法，而是提供一个人工设计的通用本体/词汇层次，用于标注和语义对齐。

## Results
- 提供了一个**完整层级视图**的具体产物：覆盖大量 Schema.org 类型与枚举项，但摘录中**没有给出总节点数、覆盖率或版本对比数字**。
- 文中明确声称 Schema.org 被定义为**两套层级**：一套用于 textual property values，一套用于 things they describe。
- 文中还明确说明：**类型可有多个父类型**，但在该页面中**每个类型只显示在树的一个分支**。
- 未提供任何实验、基准、准确率、召回率、消融研究或与其他本体/模式语言的定量比较。

## Link
- [https://schema.org/docs/full.html](https://schema.org/docs/full.html)
