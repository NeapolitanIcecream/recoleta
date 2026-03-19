---
source: arxiv
url: http://arxiv.org/abs/2603.07906v1
published_at: '2026-03-09T02:59:22'
authors:
- Jia Wei
- Xin Su
- Chun Ouyang
topics:
- process-mining
- internet-of-things
- event-logs
- object-centric-process-mining
- data-integration
relevance_score: 0.18
run_id: materialize-outputs
language_code: zh-CN
---

# IOTEL: A Tool for Generating IoT-enriched Object-Centric Event Logs

## Summary
本文提出 IOTEL，一个用于把与流程相关的物联网数据系统化地并入对象中心事件日志（OCEL）的半自动工具。其目标是在不引入专有日志模式的前提下，让 IoT 增强流程分析能够直接复用现有 OCEL 与流程挖掘工具链。

## Problem
- 要分析 IoT 增强型业务流程，必须把低层传感器/执行器数据与高层业务事件日志结合起来，但两者抽象层级不同、数据源分离，直接整合很困难。
- 若把原始 IoT 数据直接塞进事件日志，会显著增加日志体积和语义复杂度，后续还需要大量预处理，影响流程分析可用性。
- 现有工具要么侧重从传感器流中抽取事件日志，要么依赖特定专有模式（如 CORE），缺少面向现有 OCEL 日志、集成“流程相关 IoT 数据”的通用工具。

## Approach
- IOTEL 以 **OCEL 2.0** 为目标日志模式，在不改变 OCEL 基本结构的情况下，把 IoT 数据作为对象属性或事件属性增补进去，从而兼容现有流程挖掘工具。
- 工具先做 **预集成筛选**：基于 SOSA/SSN 派生一个更小的子模式，只保留对流程分析有用的概念，避免把全部原始 IoT 语义和数据量一股脑导入日志。
- 它提供三类核心功能：IoT 数据处理、OCEL 日志探索、以及 IoT-OCEL 集成；用户可配置设备类型、交互模式、属性映射、关系限定词，以及聚合/过滤策略（如 min/max/avg/median）。
- 最核心的机制很简单：先判断 IoT 设备是在描述“某次活动”还是“某个业务对象”，再把相应数据写成 **事件属性** 或 **对象属性**；对连续或跨对象影响的数据则借助领域知识决定挂载位置。
- 系统实现上使用 DuckDB + Parquet 做中间分析处理，最终写入遵循 OCEL 2.0 的 SQLite 数据库，并采用非破坏式增量扩展保存新增 IoT 属性与关系。

## Results
- 论文的主要贡献是 **工具与原型实现**，并非算法精度提升论文；**没有报告标准基准上的性能、准确率、F1 或与基线方法的定量对比结果**。
- 为验证子模式适用性，作者分析并映射了 **69 个**公开 IoT 数据集，声称这些数据集的核心语义都可以被其派生模式一致表示。
- 工具实现了 **3 个**核心功能模块：IoT 数据处理、OCEL 日志探索、IoT 数据集成，并提供交互式 GUI 原型与 GitHub/演示视频。
- 在真实工业场景中，作者将 IOTEL 应用于港口货运提货流程，把 **GPS** 与 **称重传感器** 数据与港口管理系统中的 OCEL 日志整合，用于支持异常重量操纵/欺诈分析；但文中未给出如检测率提升、分析时间降低等量化收益。
- 相比依赖专有模式的方案，IOTEL 的最强具体主张是：直接基于 **OCEL** 进行结构化 IoT 富化，减少自定义数据管道需求，并提升与现有对象中心流程挖掘工具的兼容性。

## Link
- [http://arxiv.org/abs/2603.07906v1](http://arxiv.org/abs/2603.07906v1)
