---
source: arxiv
url: http://arxiv.org/abs/2603.11104v1
published_at: '2026-03-11T10:03:57'
authors:
- Jan Baumeister
- Bernd Finkbeiner
- Florian Kohn
topics:
- runtime-verification
- stream-monitoring
- refinement-types
- cyber-physical-systems
- parameterized-streams
relevance_score: 0.22
run_id: materialize-outputs
---

# Type-safe Monitoring of Parameterized Streams

## Summary
本文将参数化流安全地集成到实时流监控语言 RTLola 中，用于处理无限数量的动态对象，同时尽量保证监控器不会因非法内存访问而在运行时出错。核心贡献是一个面向时间点推理的细化类型系统，以及对“无运行时错误”可判定性边界的澄清。

## Problem
- 运行时监控需要处理**无界数据域**，例如无人机周围数量不受限的空域参与者，必须动态创建、访问和回收监控状态。
- 如果直接用动态数据结构或异步/实时流组合，监控规范可能在读取不存在的流值、历史值或已关闭实例时发生**运行时内存错误**。
- 对这类带参数化流和实时节拍的规范，想要在静态分析阶段完全保证“永不出错”并不容易；论文明确指出该问题**一般情况下是不可判定的**，这关系到安全关键 CPS 监控的可信部署。

## Approach
- 提出将**parameterized streams** 引入 RTLola：一个流不再只是单个序列，而是一组按参数区分、可在运行时 `spawn / eval / close` 的流实例，用于系统化管理无界对象集合。
- 给出这类参数化流在 RTLola 中的**形式语义**，精确定义实例何时存活、何时可访问、如何取前缀、窗口和历史值。
- 设计一个**refinement type system**，其核心思想是：不仅记录流“是什么类型”，还追踪它**在哪些时间点一定有值**；再用布尔流条件细化这些时间点，从而判断同步访问、hold、offset、聚合等是否安全。
- 类型系统保证：每一次内存/流值访问，要么静态证明一定成功，要么表达式中有**default value** 作为后备，因此不会在运行时因缺值而失败。
- 论文还扩展了**well-formedness** 定义以避免监控器的非确定性，并在 RTLola 框架中实现了该方法的一个**过近似**类型分析器。

## Results
- 理论结果：论文证明了对参数化流 RTLola 规范而言，想要一般性地保证**不存在运行时错误是不可判定的**；因此转而采用保守但可实施的细化类型检查。
- 安全性主张：作者声称**良类型（well-typed）规范可以在运行时无错误地被监控**，因为所有访问都被证明有效或由默认值兜底。
- 能力结果：该方法覆盖了以往参数化流方案难以表达的**异步与实时属性**场景，并能检测示例中由于 1Hz 触发器与 `avg_distance(id)` 不同步导致的非法访问问题。
- 工程结果：作者实现了 RTLola-framework 中的类型分析，并在**航空航天领域规范**与**合成规范**上评估其运行性能与可扩展性。
- 定量结果：在给定摘录中**未提供具体数值指标**（如类型检查耗时、基准规模、相对基线加速/开销、错误检出率等），因此无法报告精确的 metric/dataset/baseline 数字比较。

## Link
- [http://arxiv.org/abs/2603.11104v1](http://arxiv.org/abs/2603.11104v1)
