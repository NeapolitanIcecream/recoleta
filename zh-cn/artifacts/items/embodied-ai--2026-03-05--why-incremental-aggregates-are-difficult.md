---
source: hn
url: https://www.feldera.com/blog/why-incremental-aggregates-are-difficult---part-1
published_at: '2026-03-05T23:56:24'
authors:
- gz09
topics:
- incremental-view-maintenance
- sql-aggregation
- stream-processing
- z-sets
- dbsp
relevance_score: 0.02
run_id: materialize-outputs
language_code: zh-CN
---

# Why incremental aggregates are difficult

## Summary
这篇文章解释了为什么 SQL 中的增量聚合并不像“维护一个运行中的总和”那么简单，尤其当聚合出现在可组合查询计划中时。核心观点是：聚合会产生删除型更新，而这要求整个查询引擎统一处理插入和删除，而不是只处理新增数据。

## Problem
- 它解决的问题是：**当底层表发生变化时，如何高效维护包含聚合的 SQL 视图，而不对整张表或整条查询链路做全量重算**。
- 这很重要，因为 SQL 查询是可组合的；即使单个聚合视图 `V` 能增量维护，依赖它的下游视图 `L` 也可能因为聚合产生的“旧值删除”而无法继续增量更新。
- 传统查询引擎通常更容易处理单调算子，但聚合和 `EXCEPT` 这类**非单调**操作会在输入只插入时也产生输出删除，使增量维护变得困难。

## Approach
- 文章用一个最简单的例子说明：`SUM(salary)` 的初次计算是遍历所有行的 `O(n)` 聚合，但在视图已经存在后，新插入一行时，理想上只更新差量，而不是重扫全表。
- Feldera/DBSP 的核心机制是把**数据和数据变化统一表示为 Z-sets**：每一行都带一个整数权重，`+1` 表示插入，`-1` 表示删除。
- 在这种模型里，视图更新不是“只发新结果”，而是同时**撤销旧聚合结果**并**插入新聚合结果**；例如总和变化时，输出会包含旧总和的 `-1` 和新总和的 `+1`。
- 所有查询算子都统一在 Z-sets 上计算，因此上游聚合产生的删除可以继续传播到下游查询；这使复杂组合查询也能做增量维护。
- 文章进一步指出，难点不在某个局部优化，而在于**整个执行引擎的所有算子都必须支持负更新**，这也是标准引擎难以事后补上的原因。

## Results
- 文中**没有提供基准实验、数据集或系统性量化指标**，因此没有可报告的准确率、吞吐、延迟或相对提升数字。
- 给出的复杂度结论是：普通全量 `SUM` 需要扫描所有输入行，复杂度为 **`O(n)`**；增量维护的目标是只处理变化部分，而非重扫全部数据。
- 示例中，表 `T` 初始两行工资 `100` 和 `115`，聚合结果为 **`215`**；插入 `120` 后，新总和变为 **`345`**。
- 在 Feldera 的 Z-set 语义下，视图更新不是单条新值，而是两条变化：**删除旧结果（权重 `-1`）并插入新结果（权重 `+1`）**，这是聚合增量传播到下游查询的关键具体主张。
- 文章声称其底层理论 **DBSP** 的一个主要贡献是：通过 Z-sets **统一处理插入和删除**，从而支持包含聚合等非单调算子的复杂查询做增量视图维护；而许多传统引擎只支持部分更新类型，遇到删除时会退回全量重算。

## Link
- [https://www.feldera.com/blog/why-incremental-aggregates-are-difficult---part-1](https://www.feldera.com/blog/why-incremental-aggregates-are-difficult---part-1)
