---
source: hn
url: https://www.together.ai/blog/using-llms-to-optimize-database-query-execution
published_at: '2026-04-11T22:27:08'
authors:
- matt_d
topics:
- database-query-optimization
- llm-for-systems
- query-planning
- code-intelligence
- datafusion
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# AI for Systems: Using LLMs to Optimize Database Query Execution

## Summary
## 摘要
这篇论文测试了大语言模型能否通过编辑现有物理执行计划来改进数据库查询执行。结果显示，在不修改数据库引擎的情况下，它在 Apache DataFusion 中带来了有意义的加速和内存下降。

## 问题
- 数据库优化器常常会选出较差的执行计划，因为基数估计会漏掉数据中的相关性，例如一些谓词之间存在很强的关联，而不是彼此独立。
- 这些行数估计错误会进一步传导到错误的连接顺序、访问路径和算子选择，从而拉高 OLAP 查询延迟和资源消耗。
- 靠人工修复这类问题需要投入工程成本，所以一种能自动修复执行计划的方法对真实查询负载有实际意义。

## 方法
- 作者构建了 **DBPlanBench**，这是一个测试框架，用紧凑的 JSON 形式把 Apache DataFusion 的物理执行计划暴露给 LLM。
- 他们把物理算子图序列化为一种节省 token 的结构，移除了与执行无关的字段，并对文件统计信息去重；与原生序列化相比，这使负载大小缩小了约 **10 倍**。
- LLM 不会从零生成完整执行计划。它提出局部的 **JSON Patch (RFC 6902)** 编辑，例如重排连接顺序或交换连接两侧，这样可以降低生成无效计划的概率。
- 系统采用迭代搜索：用 **GPT-5** 生成候选补丁，通过实际执行验证它们，保留能降低延迟的方案，然后基于改进后的计划继续重复这一过程。
- 为了把结果迁移到更大规模，它先在较小的基准实例上找到好的计划，例如 **SF3**，再用确定性脚本把它们改写为可在更大实例上运行的版本，例如 **SF10**，同时保留这些结构性修改。

## 结果
- 在一个源自 TPC-DS 的案例研究中，LLM 改变了连接顺序，使 `d_year=2001` 过滤条件更早应用，从而在后续连接之前，把销售事实表从 **1510 万** 行裁剪到 **290 万** 行。
- 该案例研究报告了 **4.78x** 的查询加速。
- 同一个案例还把聚合哈希表的构建时间从 **10.16 秒** 降到 **0.41 秒**，把构建内存从 **3.3 GB** 降到 **411 MB**。
- 在生成的 **TPC-H** 和 **TPC-DS** 工作负载上，中位加速大约在 **1.1x 到 1.2x** 之间。
- 一些复杂的多表连接查询提升更大，最高达到 **4.78x**，还有几个落在 **1.5x 到 1.7x** 区间。
- 在采样数据集中，**60.8%** 的查询提升超过 **5%**。在跨规模迁移方面，从 **SF3** 选出的每个优化后计划都成功迁移到了 **SF10**，论文称这些加速与原始结果保持接近。

## Problem

## Approach

## Results

## Link
- [https://www.together.ai/blog/using-llms-to-optimize-database-query-execution](https://www.together.ai/blog/using-llms-to-optimize-database-query-execution)
