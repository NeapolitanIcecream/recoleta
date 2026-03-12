---
source: arxiv
url: http://arxiv.org/abs/2603.02081v1
published_at: '2026-03-02T17:03:43'
authors:
- Jiale Lao
- Immanuel Trummer
topics:
- query-processing
- database-systems
- llm-code-generation
- agentic-systems
- olap
- system-optimization
relevance_score: 0.02
run_id: materialize-outputs
---

# GenDB: The Next Generation of Query Processing -- Synthesized, Not Engineered

## Summary
GenDB提出一种与传统数据库引擎不同的思路：不再长期手工工程化构建通用执行器，而是用LLM为每个查询直接合成定制执行代码。论文的核心主张是，这种按查询、按数据、按硬件生成的方式，在OLAP场景中已经能显著超过现有顶级查询引擎。

## Problem
- 传统DBMS高度复杂、扩展困难，面对新数据类型、新硬件和新优化需求时更新速度慢、工程成本高。
- 现有按模板/编译器生成查询代码的方法可定制空间有限，通常不了解具体数据分布、工作负载模式和硬件特征。
- 这很重要，因为分析型查询性能直接影响数据处理成本与时延，而现实中大量查询会重复执行，适合摊薄生成成本。

## Approach
- 用一个**多代理LLM系统**替代固定查询引擎流水线：依次做工作负载分析、存储/索引设计、查询规划、代码生成和迭代优化。
- 输入包括schema、SQL或自然语言问题、底层数据、用户目标/预算以及硬件资源；输出是**每个查询一个可执行文件**，外加定制存储结构和索引。
- 核心机制是：先提取结构化特征（如列统计、join模式、过滤选择率、SIMD/缓存层次），再据此生成**面向实例**的存储布局、算子算法和C++执行代码。
- 系统通过运行生成代码并读取反馈，迭代改进计划和实现；正确性目前主要通过与传统数据库结果对比验证，若无真值则建议人工审查代码。
- 一个典型例子是**缓存自适应聚合**：小基数group by直接用能放进L1缓存的数组，超大基数则改用适配L2/L3或共享哈希表的实现，以减少哈希、锁和合并开销。

## Results
- 在 **TPC-H SF=10** 的5个代表查询上，GenDB总执行时间为 **214 ms**；相比 **DuckDB 594 ms** 和 **Umbra 590 ms**，快 **2.8×**；相比 ClickHouse 快 **11.2×**。
- 在新构造的 **SEC-EDGAR** 基准上，GenDB总时间为 **328 ms**；比 **DuckDB** 快 **5.0×**，比 **Umbra** 快 **3.9×**。
- 在 **TPC-H Q9**（5表join + LIKE）上，GenDB耗时 **38 ms**，比 DuckDB 快 **6.1×**。
- 迭代优化带来大幅收益：**TPC-H Q18** 从 **12,147 ms** 降到 **74 ms**（第1轮），提升 **163×**；原因是把缓存抖动严重的哈希聚合替换为索引感知顺序扫描。
- 在 **SEC-EDGAR Q4** 上，从 **1,410 ms** 降到 **106 ms**（3轮），提升 **13.3×**；**Q6** 从 **1,121 ms** 降到 **88 ms**（4轮），提升 **12.7×**，且到第1轮已超过所有基线。
- 消融实验显示多代理设计优于单代理：TPC-H上 **236 ms vs. 281 ms**（guided），快 **1.2×**；SEC-EDGAR上 **752 ms**（guided）和 **1,325 ms**（high-level）相比，多代理分别快 **2.3×** 和 **4.1×**。同时成本更低：TPC-H **$14.15 vs. $17.54**，SEC-EDGAR **$23.49 vs. $27.46**。

## Link
- [http://arxiv.org/abs/2603.02081v1](http://arxiv.org/abs/2603.02081v1)
