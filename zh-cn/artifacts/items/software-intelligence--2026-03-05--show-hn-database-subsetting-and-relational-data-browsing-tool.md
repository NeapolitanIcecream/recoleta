---
source: hn
url: https://wisser.github.io/Jailer/
published_at: '2026-03-05T23:42:53'
authors:
- mrporter
topics:
- database-subsetting
- relational-data-browsing
- test-data-management
- data-archiving
- developer-tooling
relevance_score: 0.33
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Database Subsetting and Relational Data Browsing Tool

## Summary
Jailer 是一个面向关系数据库的子集抽取与数据浏览工具，用于安全地从生产库生成小而一致的数据切片，并支持基于表关系的交互式浏览。它主要解决开发、测试与归档场景下的数据搬运与完整性维护问题。

## Problem
- 生产数据库通常体量大、关系复杂，直接复制到开发或测试环境成本高且不便使用。
- 手工抽取部分数据时，容易破坏外键依赖与引用完整性，导致测试数据不可用或不一致。
- 数据归档或清理过期数据时，如果不理解表间依赖关系，容易影响数据库完整性与性能。

## Approach
- 提供 **Data Browser**，让用户沿着表之间的关系（外键或用户自定义关系）逐步浏览关系型数据。
- 提供 **Subsetter**，从生产数据库抽取“小切片”数据，并导入到开发/测试环境，同时保持数据一致且引用完整。
- 在导出时生成按依赖拓扑排序的 SQL，降低导入或重建数据时的约束冲突风险。
- 支持将结果输出为 SQL、JSON、YAML、XML 和 DbUnit 数据集，适配不同测试和工程流程。
- 支持通过删除/归档过期数据来改善数据库性能，同时尽量不破坏完整性约束。

## Results
- 文本未提供基准实验、公开数据集或定量指标，因此**没有可报告的数值结果**。
- 明确声称可生成**小型、一致、引用完整**的数据库子集，用于开发与测试环境。
- 明确声称支持 **5 类输出格式**：SQL、JSON、YAML、XML、DbUnit datasets。
- 明确声称 SQL 导出为**拓扑排序**结果，便于按依赖顺序导入。
- 明确声称可基于**外键或用户自定义关系**进行关系导航与浏览。
- 提供一个**内置 demo 数据库**，可在几乎无需配置的情况下快速体验工具。

## Link
- [https://wisser.github.io/Jailer/](https://wisser.github.io/Jailer/)
