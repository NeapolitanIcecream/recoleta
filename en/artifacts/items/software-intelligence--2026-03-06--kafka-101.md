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
language_code: en
---

# Kafka 101

## Summary
This article is a systematic technical overview of Apache Kafka, explaining why it has become the de facto standard for real-time data streaming and how it makes trade-offs among high throughput, persistence, replication, fault tolerance, and cloud-era evolution. Rather than a paper proposing new algorithms, it summarizes Kafka’s core design, KRaft replacing ZooKeeper, and key advances such as Tiered Storage.

## Problem
- Solve the **complexity of service coordination and data flow** in large-scale distributed systems: point-to-point connections between microservices and storage systems grow explosively, making systems hard to maintain and creating the need for a unified “source of truth.”
- Solve the problem of **coexisting high-throughput real-time stream processing and long-term storage**: the system must support millions of messages per second while storing TB-scale data, while also ensuring consumer decoupling, ordering, availability, and fault tolerance.
- Solve the **operations and scalability bottlenecks** of traditional Kafka architecture in the cloud era: local-disk storage causes IOPS and recovery-time issues for historical reads, failure recovery, rebalancing, and large-scale replica migration.

## Approach
- Use the **append-only immutable log** as the core storage abstraction: a topic is split into partitions, and partitions are persisted with sequential writes/sequential reads, leveraging HDD/OS optimizations for linear I/O to balance cost and throughput.
- Adopt **leader-based replication**: each partition has only one leader responsible for writes, while followers replicate asynchronously; `acks` and `min.insync.replicas` provide configurable trade-offs between latency and durability.
- Achieve scalable consumption through **consumer groups + offset management**: within a group, one partition is read by only one consumer, preserving per-partition ordering while allowing multiple consumer groups to subscribe to the same data stream independently.
- In the control plane, migrate from **ZooKeeper** to **KRaft**: model cluster metadata as a replicated log `__cluster_metadata`, with controller election managed by Raft, thereby reducing external dependencies and unifying the consistency mechanism.
- Use **Tiered Storage** to separate hot and cold data: hot data remains local, while cold data is placed in object storage (such as S3), so historical reads and replica recovery rely more on remote object storage, easing local disk IOPS pressure and large-scale data migration burdens.

## Results
- The system-level performance claim given by the article is that well-optimized locally deployed Kafka is often **bottlenecked by the network rather than disk/CPU**, and can scale to **GB-per-second read/write throughput**; elsewhere it also states that its target is to support **millions of messages per second** and **TB-scale storage**.
- Kafka has evolved since 2011; the article states that it has had **24 notable releases**, and that its codebase has grown at an **average rate of about 24%** across those releases, illustrating its continued evolution and active community.
- Regarding control-plane evolution, the article notes that **Kafka 3.3 (October 2022)** was the first to provide **production-ready KRaft**; it also states that **ZooKeeper** is expected to be fully removed in **Kafka 4.0 (around Q3 2024)**.
- For Tiered Storage, the article gives its clearest quantitative result: development testing showed a **43% improvement in producer performance** when historical consumers were present, because historical reads no longer significantly exhausted local disk IOPS.
- The article also provides several operational scale examples to illustrate the severity of the problem: a single broker storing **3TB of historical data**, corresponding to **9TB of total data** with a replication factor of 3; if a broker’s local disks approach **10TB**, log recovery during abnormal recovery may take **hours to days**, and full replication after a hard failure may also take **up to a day**.
- Beyond the data above, the article does not provide standardized benchmarks, public datasets, or rigorous comparative experiments against other systems; its strongest evidence comes mainly from architectural analysis, experiential description, and a small number of development-test figures.

## Link
- [https://highscalability.com/untitled-2/](https://highscalability.com/untitled-2/)
