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
- ai-ops
relevance_score: 0.02
run_id: materialize-outputs
---

# Show HN: Natural language queries for Prometheus Kafka metrics (StreamLens)

## Summary
StreamLens 是一个面向 Apache Kafka 的可视化与 AI 助手工具，支持用自然语言查询实时 Prometheus/JMX 指标，并交互式探索集群拓扑。它更像一个工程系统/开源产品发布，而不是传统研究论文。

## Problem
- Kafka 集群中的主题、消费者组、生产者、连接器、Schema 与 ACL 分散在多个系统中，排障和理解拓扑成本高。
- 运维人员通常需要手写 PromQL/JMX 查询或在多个控制台间切换，难以及时回答吞吐、积压、分区、副本异常等问题。
- 大规模集群下，节点多、关系复杂，缺少统一的可视化与自然语言入口会降低排查效率。

## Approach
- 构建一个前后端系统：前端用交互式图展示 Kafka 拓扑，后端从 live cluster 自动发现 topics、consumer groups、producers、connectors、schemas 和 ACLs。
- 引入 AI 助手 StreamPilot，把用户自然语言问题映射到一组**预先整理的** Prometheus broker metrics / PromQL 查询，并在界面中高亮、缩放相关节点。
- 生产者检测采用自动回退链：优先使用 Prometheus 的客户端级指标；若没有，则退化到 broker-side topic 指标；再不行可使用 Broker JMX。
- 支持 Schema Registry、Kafka Connect、Consumer lag、topic details、sample client code 生成、消息生产、搜索导航、分页加载等运维功能。
- 兼容 OpenAI、Gemini、Anthropic、Ollama，并支持多种 Kafka 认证/连接方式（如 SASL_SSL、SSL、PLAINTEXT）。

## Results
- 文本中**没有提供正式实验、基准测试或论文式定量结果**，因此无法给出准确的 SOTA/提升百分比。
- 给出的最明确数字性声明是：AI 助手可查询 **17 个**经过整理的 broker metrics，覆盖 **5 类**指标。
- 系统支持回答的示例问题包括当前 message throughput、under-replicated partitions、produce request 平均处理时间、partition 数量等，但未报告回答准确率或延迟。
- 功能层面的具体声明包括：支持自动发现 topology 元素、按 partition 查看 consumer lag、根据 Schema Registry ID 合并 schema 节点、以及在大集群中进行 topic 分页加载。
- 与传统“手动写 PromQL/JMX + 多工具切换”相比，其主要改进是把可视化、实时指标和自然语言问答整合到单一 UI 中，但文本未给出用户研究或效率提升数据。

## Link
- [https://github.com/muralibasani/streamlens](https://github.com/muralibasani/streamlens)
