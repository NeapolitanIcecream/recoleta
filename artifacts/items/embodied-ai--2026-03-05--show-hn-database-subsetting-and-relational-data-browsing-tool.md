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
- sql-tooling
relevance_score: 0.0
run_id: materialize-outputs
---

# Show HN: Database Subsetting and Relational Data Browsing Tool

## Summary
Jailer 是一个用于数据库子集提取与关系型数据浏览的工具，面向开发、测试和数据归档场景。它强调在缩小数据规模的同时保持引用完整性，并支持多种导出格式。

## Problem
- 生产数据库通常体量大、关系复杂，直接复制到开发或测试环境成本高且低效。
- 简单抽样或删除数据容易破坏外键依赖和引用完整性，导致测试数据不可用。
- 数据库中历史/过时数据的清理与归档如果处理不当，会影响性能或破坏一致性。

## Approach
- 提供 **Data Browser**，允许用户沿着表之间的关系导航数据，这些关系既可以基于外键，也可以由用户自定义。
- 提供 **Subsetter**，从生产数据库中抽取“小而完整”的数据切片，并导入开发/测试环境。
- 在抽取、导入和归档过程中保持数据 **consistent and referentially intact**，即一致且引用完整。
- 支持生成多种输出：拓扑排序的 SQL，以及层次化结构的 JSON、YAML、XML 和 DbUnit 数据集。
- 附带一个演示数据库，降低首次体验和配置门槛。

## Results
- 文本**没有提供定量实验结果**，未给出基准数据集、性能指标、准确率或与其他工具的数值对比。
- 最强的具体声明是：可从生产库创建“小切片”并导入开发/测试环境，同时保持**引用完整性**。
- 还声称可通过删除和归档过时数据来**改善数据库性能**，但未提供性能提升百分比或延迟/吞吐数字。
- 支持 **5 类输出形式**：SQL、JSON、YAML、XML、DbUnit；其中 SQL 为**拓扑排序**，其余为**层次化结构**。

## Link
- [https://wisser.github.io/Jailer/](https://wisser.github.io/Jailer/)
