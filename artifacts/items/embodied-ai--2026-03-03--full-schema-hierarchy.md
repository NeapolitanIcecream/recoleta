---
source: hn
url: https://schema.org/docs/full.html
published_at: '2026-03-03T23:43:32'
authors:
- vinhnx
topics:
- schema-org
- ontology
- knowledge-graph
- structured-data
- semantic-web
relevance_score: 0.03
run_id: materialize-outputs
---

# Full Schema Hierarchy

## Summary
该文本不是一篇机器人或机器学习研究论文，而是 Schema.org 的“完整模式层级”页面，描述类型与数据类型的层次结构。它的价值主要在于为网页结构化数据提供统一语义组织，而非提出可实验验证的新算法。

## Problem
- 解决的问题是：如何用统一、可扩展的类型层级来描述现实世界中的实体、属性及其文本/数据值。
- 这很重要，因为搜索、知识图谱、网页标注和跨系统数据交换需要共享语义，否则不同站点难以互操作。
- 给定摘录并未聚焦机器人、VLA、世界模型或通用机器人策略等用户主题。

## Approach
- 核心机制是定义**两套层级**：一套用于“被描述的事物（types/classes）”，一套用于“文本或数据类型的值（data types）”。
- 每个类型可以有一个或多个父类型，从而形成层次化本体；页面中为便于展示，只在树中显示其中一个分支。
- 通过列举大量具体类型（如 `Movie`、`Organization`、`LocalBusiness`、`Taxon` 等），把通用语义模式标准化，供网页和应用复用。
- 本质上，这不是“训练模型”，而是“建立一套共享词汇表和继承关系”，让机器更容易理解结构化元数据。

## Results
- 文本未提供任何实验设置、数据集、评测指标或与基线的定量比较，因此**没有可报告的论文式量化结果**。
- 最强的具体主张是：Schema.org 被定义为**两个层级结构**，分别覆盖事物类型与数据类型。
- 另一个具体主张是：主层级包含大量类型，且类型允许**多个父类型**，不过展示时每个类型只出现在树的一个分支中。
- 摘录中给出了大量实例化类型名称，但**没有数字化统计**（如总类型数、覆盖率、性能提升百分比等）。

## Link
- [https://schema.org/docs/full.html](https://schema.org/docs/full.html)
