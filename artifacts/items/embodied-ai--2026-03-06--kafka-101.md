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
relevance_score: 0.01
run_id: materialize-outputs
---

# Kafka 101

## Summary
这篇文章是对 Apache Kafka 的系统性入门综述，解释了它为何能成为实时数据流的事实标准。重点不在提出全新算法，而在梳理 Kafka 的核心设计、性能机制、容错共识演进与分层存储方向。

## Problem
- 解决大规模企业系统中**服务之间点对点集成过多、数据源分散、实时数据流难统一管理**的问题，这会导致系统复杂、脆弱且难扩展。
- 需要一个既能**高吞吐实时传输**，又能**长期持久化大量数据**的平台，避免传统消息总线中“消息一消费就删除”带来的生产者/消费者耦合。
- 还要应对分布式系统中的**副本一致性、故障切换、控制面共识、历史数据读取和扩容重平衡**等工程难题，因为这些直接影响可靠性、成本和运维效率。

## Approach
- Kafka 的核心机制很简单：把数据按 **topic/partition** 组织成**追加写日志（log）**，记录按 offset 顺序存储；这种顺序读写天然适合磁盘和并发读取。
- 它通过**分区 + 副本 + leader/follower**实现扩展与容错：写入只进 leader，再复制到 follower；生产者可用 `acks=0/1/all` 和 `min.insync.replicas` 在性能与持久性之间权衡。
- 它依赖一系列性能工程优化：**批量传输、顺序磁盘 I/O、OS page cache、异步刷盘、可选 zero-copy**，从而让“落盘存储”仍保持很高吞吐。
- 消费侧通过**consumer group** 协调分区读取，保证单分区内顺序，并允许多个独立消费组解耦地复用同一份数据流。
- 在控制面上，Kafka 正从 ZooKeeper 迁移到 **KRaft**：把集群元数据也表达为日志，由 Raft 风格控制器仲裁；在存储层则引入 **Tiered Storage**，把冷数据迁到对象存储以缓解本地磁盘容量和 IOPS 压力。

## Results
- 文中给出的系统级能力声明是：Kafka 可支持**每秒数百万条消息**，以及**TB 级数据存储**；优化良好的本地部署通常会被**网络而非磁盘/CPU**限制，吞吐可达到**每秒数 GB**。
- 文中指出 Kafka 自 2011 年起已发布**24 个 notable releases**，代码库在这些发布间平均增长**24%**，用来说明其长期演进和生态成熟度。
- 关于共识演进，文中给出明确时间点：**Kafka 3.3（2022 年 10 月）**首次提供生产可用的 **KRaft**；**ZooKeeper** 计划在 **Kafka 4.0（预计 2024 年 Q3）**中被彻底移除。
- 唯一明确量化的性能改进来自 **Tiered Storage**：开发测试显示，在存在历史消费者时，**producer performance 提升 43%**，原因是历史读取转移到对象存储后，不再严重争用本地磁盘 IOPS。
- 文章没有提供标准学术基准数据集、误差率或与论文基线模型的系统对比；最强的定量结论主要是上述**43% 性能提升**及若干吞吐/容量级别的工程声明。

## Link
- [https://highscalability.com/untitled-2/](https://highscalability.com/untitled-2/)
