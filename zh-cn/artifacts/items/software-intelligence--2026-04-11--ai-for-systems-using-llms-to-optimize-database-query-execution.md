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
本文测试大型语言模型是否可以通过编辑现有物理计划来改进数据库查询执行。结果显示，在不修改数据库引擎的情况下，Apache DataFusion 的速度和内存占用都得到改善。

## Problem
- 数据库优化器常常会选出较差的执行计划，因为基数估计无法捕捉数据中的相关性，比如彼此强相关而不是独立的谓词。
- 这些行数估计错误会传导到错误的连接顺序、访问路径和算子选择，进而拖慢 OLAP 查询并增加资源消耗。
- 逐个手工修复这些情况需要工程投入，因此一种能自动修复计划的方法对真实查询负载有价值。

## Approach
- 作者构建了 **DBPlanBench**，这是一个把 Apache DataFusion 物理计划以紧凑 JSON 形式暴露给 LLM 的工具。
- 他们把物理算子图序列化为节省 token 的 schema，去掉与执行无关的字段，并对文件统计信息去重；与原生序列化相比，这把载荷大小压缩了约 **10x**。
- LLM 不会从头生成完整计划。它只提出局部的 **JSON Patch (RFC 6902)** 编辑，比如调整连接顺序或交换连接输入侧，这降低了生成无效计划的概率。
- 系统使用迭代搜索：用 **GPT-5** 生成候选补丁，执行验证，保留能降低延迟的补丁，然后从改进后的计划继续迭代。
- 为了跨规模迁移，它先在较小的基准实例上找到较优计划，例如 **SF3**，再用确定性脚本重写这些计划，使其能在较大的实例上运行，例如 **SF10**，同时保留结构性修改。

## Results
- 在一个基于 TPC-DS 的案例研究中，LLM 调整了连接顺序，使 `d_year=2001` 过滤更早执行，把销售事实表在后续连接前从 **15.1 million** 行缩减到 **2.9 million** 行。
- 该案例研究报告了 **4.78x** 的查询加速。
- 同一案例中，聚合哈希表构建时间从 **10.16 s** 降到 **0.41 s**，构建内存从 **3.3 GB** 降到 **411 MB**。
- 在生成的 **TPC-H** 和 **TPC-DS** 工作负载上，中位数加速约为 **1.1x to 1.2x**。
- 一些复杂的多连接查询提升更大，最高达到 **4.78x**，另有几项在 **1.5x to 1.7x** 范围内。
- 在抽样数据集中，**60.8%** 的查询提升超过 **5%**。在跨规模迁移中，所有从 **SF3** 选出的优化计划都成功迁移到 **SF10**，论文称其加速效果与原计划接近。

## Link
- [https://www.together.ai/blog/using-llms-to-optimize-database-query-execution](https://www.together.ai/blog/using-llms-to-optimize-database-query-execution)
