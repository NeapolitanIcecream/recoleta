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
language_code: en
---

# Kafka 101

## Summary
This article is a systematic introductory overview of Apache Kafka, explaining why it has become the de facto standard for real-time data streaming. The focus is not on proposing entirely new algorithms, but on clarifying Kafka’s core design, performance mechanisms, evolution of fault-tolerance consensus, and direction toward tiered storage.

## Problem
- Solve the problem in large-scale enterprise systems of **too many point-to-point integrations between services, fragmented data sources, and difficulty in unified management of real-time data streams**, which makes systems complex, fragile, and hard to scale.
- A platform is needed that can provide both **high-throughput real-time transmission** and **long-term durable storage of large amounts of data**, avoiding the producer/consumer coupling caused by the traditional message bus model where “messages are deleted once consumed.”
- It must also address engineering challenges in distributed systems such as **replica consistency, failover, control-plane consensus, historical data reads, and scaling rebalancing**, because these directly affect reliability, cost, and operational efficiency.

## Approach
- Kafka’s core mechanism is simple: organize data by **topic/partition** into an **append-only log**, where records are stored in offset order; this sequential read/write pattern is naturally well suited to disks and concurrent reads.
- It achieves scalability and fault tolerance through **partitions + replicas + leader/follower**: writes go only to the leader and are then replicated to followers; producers can use `acks=0/1/all` and `min.insync.replicas` to balance performance and durability.
- It relies on a series of performance engineering optimizations: **batch transfer, sequential disk I/O, OS page cache, asynchronous flush, optional zero-copy**, allowing “persisting to disk” to still maintain very high throughput.
- On the consumption side, **consumer group** coordinates partition reads, ensuring order within a single partition while allowing multiple independent consumer groups to reuse the same data stream in a decoupled way.
- In the control plane, Kafka is migrating from ZooKeeper to **KRaft**: cluster metadata is also expressed as a log and arbitrated by a Raft-style controller; in the storage layer, **Tiered Storage** is introduced to move cold data to object storage and relieve pressure on local disk capacity and IOPS.

## Results
- The system-level capability claims given in the article are that Kafka can support **millions of messages per second** and **terabyte-scale data storage**; well-optimized local deployments are typically limited by the **network rather than disk/CPU**, with throughput reaching **multiple GB per second**.
- The article notes that since 2011 Kafka has had **24 notable releases**, and its codebase grew by an average of **24%** between those releases, illustrating its long-term evolution and ecosystem maturity.
- Regarding the consensus evolution, the article gives clear milestones: **Kafka 3.3 (October 2022)** first provided production-ready **KRaft**; **ZooKeeper** is planned to be fully removed in **Kafka 4.0 (expected Q3 2024)**.
- The only explicitly quantified performance improvement comes from **Tiered Storage**: development testing showed that, when historical consumers are present, **producer performance improved by 43%**, because historical reads are shifted to object storage and no longer heavily contend for local disk IOPS.
- The article does not provide a standard academic benchmark dataset, error rate, or a systematic comparison against baseline models from papers; the strongest quantitative conclusions are mainly the above **43% performance improvement** and several engineering claims about throughput/capacity levels.

## Link
- [https://highscalability.com/untitled-2/](https://highscalability.com/untitled-2/)
