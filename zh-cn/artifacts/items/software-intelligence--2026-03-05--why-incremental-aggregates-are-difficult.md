---
source: hn
url: https://www.feldera.com/blog/why-incremental-aggregates-are-difficult---part-1
published_at: '2026-03-05T23:56:24'
authors:
- gz09
topics:
- incremental-view-maintenance
- stream-processing
- sql-aggregates
- z-sets
- query-engines
relevance_score: 0.47
run_id: materialize-outputs
language_code: zh-CN
---

# Why incremental aggregates are difficult

## Summary
本文解释了为什么 SQL 中的增量聚合在真实查询计划里并不简单，尤其当聚合结果还会继续参与后续查询时。核心观点是：聚合会产生删除型更新，因此需要一种能统一表示插入和删除的执行模型。

## Problem
- 要解决的问题是：当底层表发生变化时，如何高效维护包含 `SUM`/`GROUP BY` 等聚合的视图，而不是每次都全量重算。
- 这很重要，因为复杂 SQL 查询通常是可组合的；一旦聚合结果被下游查询继续使用，更新就不再只是“加上新值”这么简单。
- 传统查询引擎往往只能对部分更新做增量维护，遇到删除或非单调算子时容易退回全量重算，影响流式与持续计算性能。

## Approach
- 文中用最简单的例子说明：普通 `SUM` 初次计算是扫描全部行，复杂度是 `O(n)`；但作为视图维护时，理论上可以利用旧结果只处理变更部分。
- Feldera/DBSP 的核心机制是 **Z-sets**：把表表示为“行 + 整数权重”，正权重表示插入，负权重表示删除，从而把数据和数据变化统一成同一种表示。
- 在这种模型里，聚合更新不是只输出新值，而是同时输出“删掉旧聚合结果”和“插入新聚合结果”。例如总和变化时，视图增量会包含一条 `-1` 的旧值和一条 `+1` 的新值。
- 所有查询算子都必须统一接受正负变化；这样下游算子才能继续传播由聚合产生的删除更新，支持组合查询的增量维护。
- 文中强调聚合和 `EXCEPT` 等算子是**非单调**的：即使输入只有插入，输出也可能出现删除，这正是标准引擎难以改造的根源。

## Results
- 文中没有给出基准测试、实验数据或精度指标等定量结果。
- 给出的明确复杂度结论是：常规聚合初次执行需要查看所有输入行，复杂度为 `O(n)`。
- 通过示例说明增量维护行为：表 `T` 初始两行工资 `100` 和 `115` 时，`SUM=215`；再插入 `120` 后，新总和变为 `345`。
- 关键机制性结果是：对于聚合视图更新，系统需要发出两条变化——删除旧结果、插入新结果，而不只是发送一个新值。
- 文章声称 DBSP/Feldera 的突破点在于用 Z-sets 统一处理插入与删除，使任意混合更新以及包含聚合的组合查询都能进行一致的增量维护；而许多传统引擎仅能支持部分更新类型。

## Link
- [https://www.feldera.com/blog/why-incremental-aggregates-are-difficult---part-1](https://www.feldera.com/blog/why-incremental-aggregates-are-difficult---part-1)
