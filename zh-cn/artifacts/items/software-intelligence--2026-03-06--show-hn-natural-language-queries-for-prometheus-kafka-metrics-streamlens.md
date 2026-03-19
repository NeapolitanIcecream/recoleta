---
source: hn
url: https://github.com/muralibasani/streamlens
published_at: '2026-03-06T23:05:37'
authors:
- muralibasani
topics:
- kafka-observability
- natural-language-query
- prometheus-metrics
- topology-visualization
- ai-assistant
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Natural language queries for Prometheus Kafka metrics (StreamLens)

## Summary
StreamLens 是一个面向 Apache Kafka 的可视化与问答工具，把集群拓扑浏览、实时指标查询和自然语言交互结合起来。它的核心价值是让运维与开发者更快理解 Kafka 系统状态，并直接从 Prometheus/JMX 中获取可操作信息。

## Problem
- Kafka 集群包含 topics、producers、consumers、connectors、schemas、ACLs 等多类对象，结构复杂，人工排查拓扑和依赖关系成本高。
- 监控指标通常分散在 Prometheus/JMX 中，用户需要手写查询语句，难以快速回答“当前吞吐量如何”“是否有 under-replicated partitions”之类的问题。
- 大型集群中的节点发现、生产者识别、consumer lag 排查和 topic 配置检查往往依赖多个工具切换，影响运维效率。

## Approach
- 构建一个前后端系统：前端用 React Flow 展示 Kafka 集群拓扑，后端用 FastAPI 连接 Kafka、Schema Registry、Kafka Connect、Prometheus 和 JMX 数据源。
- 自动发现 Kafka 资源，包括 topics、consumer groups、producers、connectors、schemas 和 ACLs，并把共享同一 Schema Registry ID 的 schema 合并显示。
- 提供生产者检测的自动回退链：优先读取 Prometheus 中按 client_id 和 topic 聚合的生产者指标；若无则退回 broker-side topic 指标；再不行可用 JMX/offset-change 检测。
- 引入 AI 助手 StreamPilot，把自然语言问题映射为对一组预定义 Kafka broker 指标的查询，并在图中高亮相关节点、缩放定位结果。
- 支持 topic 详情、最近消息查看、consumer per-partition lag、connector 配置检查，以及样例客户端代码生成等交互能力。

## Results
- 文中没有提供标准基准测试、离线评测或与现有系统的定量对比结果，因此**没有可报告的量化性能提升数字**。
- 提出可查询 **17 个 broker metrics**，覆盖 **5 个类别**，并支持用自然语言提问实时 Kafka broker 指标。
- 支持多种 AI 提供方：**OpenAI、Gemini、Anthropic、Ollama**。
- 支持多种 Kafka 连接/认证方式：**SASL_SSL、SSL、PLAINTEXT**，以及 **OAUTHBEARER、SCRAM-SHA-512、SCRAM-SHA-256、PLAIN**。
- 可直接回答的示例问题包括当前消息吞吐量、under-replicated partitions、produce request 平均处理时间、partition 数量等，但原文未给出这些问答的准确率或延迟数据。

## Link
- [https://github.com/muralibasani/streamlens](https://github.com/muralibasani/streamlens)
