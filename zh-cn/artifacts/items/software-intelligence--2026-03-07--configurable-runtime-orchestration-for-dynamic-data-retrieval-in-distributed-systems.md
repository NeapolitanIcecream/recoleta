---
source: arxiv
url: http://arxiv.org/abs/2603.06980v1
published_at: '2026-03-07T01:45:18'
authors:
- Abhiram Kandiraju
topics:
- runtime-orchestration
- distributed-systems
- microservices
- dynamic-workflows
- configuration-driven
relevance_score: 0.62
run_id: materialize-outputs
language_code: zh-CN
---

# Configurable Runtime Orchestration for Dynamic Data Retrieval in Distributed Systems

## Summary
本文提出一种**配置驱动、请求时动态生成执行图**的分布式数据检索编排框架，面向企业中频繁变化的微服务/API/分析平台聚合场景。核心价值是在**不重新部署编排代码**的情况下，通过配置更新实现低延迟、并行化的数据聚合。

## Problem
- 现有编排系统如 Airflow、Step Functions、Temporal 通常要求**预先定义工作流**（DAG、状态机或代码工作流），不适合请求级、拓扑频繁变化的数据聚合。
- 企业 Customer 360、风控、运营等场景常需在一次请求中访问多个异构系统；若编排逻辑写死在代码/工作流中，**新增数据源、修改依赖、调整可选规则**都会变成部署事件。
- 这很重要，因为企业既需要**灵活性**（快速接入变化的服务），也需要**性能**（低延迟响应），而串行调用会浪费延迟预算。

## Approach
- 方法核心是：**把配置而不是预定义工作流当成真实来源**。系统在收到请求后，读取配置，现算出一个依赖图，再执行它。
- 架构包含五层：Request Adapter、Configuration Resolver、Execution Planner、Execution Engine、Aggregation/Response；其中 Planner 负责把声明式配置解析成运行时依赖图。
- 执行机制很简单：把每个调用/转换看成图中的节点，把前置条件看成边；**没有未满足依赖的节点立即并行执行**，有依赖的节点等待前驱完成。
- 失败语义被显式建模为 required / optional / fallback 节点，从而支持在延迟受限场景下返回**部分但有效**的结果，而不是一味追求长时 durable completion。
- 在 Customer 360 案例中，account、transactions、fraud、risk 可作为四个初始独立节点并行执行；后来若增加 recent-case context，只需改配置并让规划器自动纳入图中。

## Results
- 论文**没有提供正式实验、基准测试或量化指标**；未报告延迟、吞吐、成功率等具体数字，也没有给出数据集和统计显著性结果。
- 最强的具体主张是：当 Customer 360 请求包含 **4 个可立即执行节点**（account、transactions、fraud、risk）时，系统可在运行时识别它们的独立性并**并行执行 4 路调用**。
- 论文声称相较 Airflow / Step Functions / Temporal，其优势在于：**请求级拓扑变化无需 redeploy**，而这些对比系统通常需要更新 DAG、状态机或工作流代码后再部署。
- 性能上的主张是定性的：运行时图生成会引入一定 planning overhead，但该开销通常**小于网络绑定的数据检索开销**；实际收益主要来自依赖感知并行和部署解耦。
- 适用边界也被明确指出：对于**长运行、强持久化、跨天重试、人工参与**的工作流，作者并不声称优于 Temporal 等 durable workflow 引擎。

## Link
- [http://arxiv.org/abs/2603.06980v1](http://arxiv.org/abs/2603.06980v1)
