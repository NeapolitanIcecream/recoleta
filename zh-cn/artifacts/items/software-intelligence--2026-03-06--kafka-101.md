---
source: hn
url: https://highscalability.com/untitled-2/
published_at: '2026-03-06T23:56:00'
authors:
- medbar
topics:
- apache-kafka
- distributed-systems
- stream-processing
- consensus
- tiered-storage
relevance_score: 0.36
run_id: materialize-outputs
language_code: zh-CN
---

# Kafka 101

## Summary
本文是一篇对 Apache Kafka 的系统性技术综述，解释它为何成为实时数据流的事实标准，以及它如何在高吞吐、持久化、复制、容错和云化演进之间做权衡。文章不是提出新算法的论文，而是总结 Kafka 的核心设计、KRaft 替代 ZooKeeper、以及 Tiered Storage 等关键进展。

## Problem
- 解决大规模分布式系统中的**服务协调与数据流转复杂性**：微服务和存储系统之间点对点连接会爆炸式增长，系统难以维护，需要一个统一的“事实来源”。
- 解决**高吞吐实时流处理与长期存储并存**的问题：系统既要支持每秒数百万消息，又要保存 TB 级数据，同时保证消费者解耦、顺序性、可用性与容错。
- 解决传统 Kafka 架构在云时代的**运维与扩展瓶颈**：本地磁盘存储导致历史读取、故障恢复、重平衡和大容量副本迁移带来 IOPS 与恢复时间问题。

## Approach
- 以**追加式不可变日志（log）**为核心存储抽象：topic 被切成 partition，partition 以顺序写/顺序读的方式落盘，利用 HDD/OS 对线性 I/O 的优化来兼顾成本与吞吐。
- 采用**leader-based replication**：每个 partition 只有一个 leader 负责写入，followers 异步复制；通过 `acks` 与 `min.insync.replicas` 在延迟和持久性之间做配置化权衡。
- 通过**消费者组 + offset 管理**实现可扩展消费：同组内一个 partition 只被一个 consumer 读取，从而保证分区内顺序，同时允许多个消费组独立订阅同一数据流。
- 在控制面上，从 **ZooKeeper** 迁移到 **KRaft**：把集群元数据建模成一个可复制日志 `__cluster_metadata`，由 Raft 管理控制器选举，从而减少外部依赖并统一一致性机制。
- 用**Tiered Storage**把冷热数据分层：热数据保留在本地，冷数据放到对象存储（如 S3），让历史读取与副本恢复更多依赖远端对象存储，缓解本地磁盘 IOPS 与大规模数据迁移压力。

## Results
- 文章给出的系统级性能声明是：优化良好的本地部署 Kafka 往往**瓶颈在网络而非磁盘/CPU**，可扩展到**每秒数 GB 级读写吞吐**；另处提到其目标可支持**每秒数百万消息**与**TB 级存储**。
- Kafka 自 2011 年起发展，文中称已有**24 个重要版本**，代码库在这些版本中的**平均增长率约为 24%**，用于说明其持续演进与社区活跃度。
- 关于控制面演进，文中指出 **Kafka 3.3（2022 年 10 月）** 首次提供**生产可用的 KRaft**；同时称 **ZooKeeper** 预计在 **Kafka 4.0（约 2024 年 Q3）** 被完全移除。
- 关于 Tiered Storage，文中给出最明确的量化结果：开发测试显示，在存在历史消费者时，**生产者性能提升 43%**，原因是历史读取不再显著耗尽本地磁盘 IOPS。
- 文中还给出若干运维规模示例来支撑问题严重性：单 broker 保存**3TB 历史数据**、在副本因子为 3 时对应**9TB 总数据**；若 broker 本地磁盘接近**10TB**，异常恢复中的 log recovery 可能需要**数小时到数天**，硬故障后全量复制也可能需要**长达一天**。
- 除上述数据外，文章没有提供标准化 benchmark、公开数据集或与其他系统的严格对照实验；其最强证据主要来自架构分析、经验性描述和少量开发测试数字。

## Link
- [https://highscalability.com/untitled-2/](https://highscalability.com/untitled-2/)
