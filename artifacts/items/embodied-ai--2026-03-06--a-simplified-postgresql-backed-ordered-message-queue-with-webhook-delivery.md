---
source: hn
url: https://github.com/alaminopu/pypgmq
published_at: '2026-03-06T23:36:10'
authors:
- alaminopu
topics:
- postgresql-queue
- webhook-delivery
- ordered-messaging
- fastapi
- retry-dead-letter
relevance_score: 0.0
run_id: materialize-outputs
---

# A simplified PostgreSQL-backed ordered message queue with webhook delivery

## Summary
这是一个基于 PostgreSQL 的有序消息队列系统，通过 FastAPI 暴露接口，并把消息自动投递到已注册的 webhook。其核心价值是用常见数据库能力实现近实时、可重试、分区内严格有序的消息分发。

## Problem
- 解决的是：如何在较低系统复杂度下，构建一个支持**主题/分区消息、webhook 自动投递、失败重试、死信处理、严格顺序保证**的消息队列。
- 这很重要，因为很多应用只需要可靠事件分发与 HTTP 回调，不一定想引入 Kafka / RabbitMQ 等更重的基础设施。
- 还要兼顾直接 SQL 写入业务事务、近实时触发处理，以及多 worker 横向扩展时的并发安全。

## Approach
- 以 **PostgreSQL 作为消息存储与协调层**：消息写入数据库，topic 和 partition 组织消息流。
- 通过 **FastAPI REST API** 暴露消息写入与 webhook 注册能力，同时也支持客户端**直接 SQL INSERT** 写消息。
- 使用 **PostgreSQL trigger + LISTEN/NOTIFY**：当消息写入后，触发器为每个订阅 webhook 创建投递记录，并发送 NOTIFY，让 worker 立即处理。
- 使用后台 **delivery worker** 执行 HTTP POST 投递；若返回非 2xx，则按**指数退避**重试，超过 `MAX_RETRIES` 后进入**dead-letter partition**。
- 为了支持多 worker 安全并行处理，依赖 **`FOR UPDATE SKIP LOCKED`** 实现并发抢占，且在每个 partition 内对每个 webhook 保持严格顺序。

## Results
- 文本**没有提供标准数据集或基准实验的定量结果**，因此没有吞吐、延迟、成功率等具体数字可报告。
- 明确宣称的能力包括：**分区内严格有序投递**（per webhook, per partition）、**失败后指数退避重试**、以及在超过 **`MAX_RETRIES`** 后转入**死信分区**。
- 系统声称支持**横向扩展**：可运行多个 worker，并通过 **`FOR UPDATE SKIP LOCKED`** 安全处理并发。
- 系统声称具备**近实时处理**：借助 PostgreSQL **LISTEN/NOTIFY**，消息写入后可立即唤醒 worker。
- 工程可用性方面，项目宣称可通过 **`docker-compose up --build` 一条命令**启动 PostgreSQL、迁移、API 与 worker。

## Link
- [https://github.com/alaminopu/pypgmq](https://github.com/alaminopu/pypgmq)
