---
source: arxiv
url: http://arxiv.org/abs/2603.02081v1
published_at: '2026-03-02T17:03:43'
authors:
- Jiale Lao
- Immanuel Trummer
topics:
- llm-agents
- query-processing
- database-systems
- code-generation
- performance-optimization
relevance_score: 0.79
run_id: materialize-outputs
---

# GenDB: The Next Generation of Query Processing -- Synthesized, Not Engineered

## Summary
GenDB提出一种不同于传统数据库引擎的思路：不再长期工程化维护通用查询执行器，而是用LLM按查询直接合成执行代码。论文用一个多代理原型展示，这种“为每个查询生成定制程序”的方法在OLAP基准上可显著超过现有引擎。

## Problem
- 传统DBMS高度复杂、扩展困难，面对新数据类型、新硬件和新优化技术时迭代慢、成本高。
- 通用查询引擎必须用固定算子抽象处理任意工作负载，难以针对具体数据分布、查询模式和缓存/硬件特征做激进优化。
- 这很重要，因为分析型查询常重复出现，若能为高频查询生成专用代码，可摊薄生成成本并显著提升性能。

## Approach
- 核心方法是：对每个输入查询，不依赖预先手写的大型执行引擎，而是由LLM驱动的多代理系统分析数据、工作负载和硬件后，直接生成可执行的查询代码。
- 系统分成多个专职代理：Workload Analyzer提取结构化特征，Storage/Index Designer生成定制存储与索引，Query Planner生成资源感知计划，Code Generator产出C++/Python代码，Query Optimizer根据运行反馈迭代改进。
- 简单说，它像“自动数据库编译器+自动调优器”：先看这个查询和这台机器的具体情况，再写一份最合适的专用程序，而不是调用一套固定的通用算子。
- 优化机制强调数据感知与硬件感知，例如按基数和缓存层级选择聚合策略：小group直接用L1内数组，大group改为适配L2/L3的哈希结构；还会生成查询特定的数据结构与算子重构代码。
- 正确性目前主要通过与传统数据库的查询结果对比验证；若无真值结果，则建议人工检查生成代码。

## Results
- 在TPC-H（SF=10）5个代表性查询上，GenDB总执行时间为**214 ms**，相比两大最快基线**DuckDB 594 ms**和**Umbra 590 ms**快**2.8×**，相比**ClickHouse**快**11.2×**。
- 在新构造的**SEC-EDGAR**基准上，GenDB总执行时间为**328 ms**，比**DuckDB**快**5.0×**，比**Umbra**快**3.9×**。
- 在复杂查询**TPC-H Q9**（五表连接+LIKE过滤）上，GenDB用时**38 ms**，比DuckDB快**6.1×**。
- 迭代优化效果显著：**TPC-H Q18**从**12,147 ms**降到第1轮的**74 ms**，提升**163×**；**TPC-H Q6**在第0轮就达到近最优**17 ms**。
- 在SEC-EDGAR上，**Q4**从**1,410 ms**降到**106 ms**（**13.3×**），**Q6**从**1,121 ms**降到**88 ms**（**12.7×**）；且Q6到第1轮时已超过全部基线。
- 消融实验显示多代理优于单代理：TPC-H上多代理**236 ms**，比最佳单代理guided **281 ms**快**1.2×**；SEC-EDGAR上比guided **752 ms**快**2.3×**，比high-level **1,325 ms**快**4.1×**，且成本更低（TPC-H **$14.15 vs. $17.54**；SEC-EDGAR **$23.49 vs. $27.46**）。

## Link
- [http://arxiv.org/abs/2603.02081v1](http://arxiv.org/abs/2603.02081v1)
