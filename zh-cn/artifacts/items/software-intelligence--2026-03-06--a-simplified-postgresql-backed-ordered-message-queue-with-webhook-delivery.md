---
source: hn
url: https://github.com/alaminopu/pypgmq
published_at: '2026-03-06T23:36:10'
authors:
- alaminopu
topics:
- message-queue
- postgresql
- webhook-delivery
- fastapi
- event-driven
relevance_score: 0.42
run_id: materialize-outputs
language_code: zh-CN
---

# A simplified PostgreSQL-backed ordered message queue with webhook delivery

## Summary
这是一个基于 PostgreSQL 的有序消息队列实现，通过 FastAPI 暴露 REST API，并将消息自动投递到已订阅的 webhook。它强调用尽量简单的基础设施实现分区内严格有序、失败重试、死信处理和近实时分发。

## Problem
- 解决的问题是：如何在不引入 Kafka/RabbitMQ 等独立消息系统的情况下，构建一个**支持主题、分区内顺序、Webhook 投递**的消息队列。
- 这很重要，因为很多应用已经依赖 PostgreSQL，希望直接复用现有数据库来完成事件分发、异步解耦和外部系统通知，降低运维复杂度。
- 还要解决失败投递后的可靠性问题，包括重试、退避和死信归档，同时支持多 worker 横向扩展而不破坏顺序。

## Approach
- 核心机制非常简单：消息先写入 PostgreSQL，数据库触发器为每个订阅的 webhook 生成投递记录，并通过 `LISTEN/NOTIFY` 立即唤醒后台 worker。
- worker 从数据库中拉取待发送记录，并按 webhook 与分区顺序逐条执行 HTTP POST；成功则确认，失败则按指数退避重试。
- 为保证并发安全和横向扩展，多个 worker 使用 PostgreSQL 的 `FOR UPDATE SKIP LOCKED` 抢占任务，避免重复处理同一投递记录。
- 为保证可靠性，达到 `MAX_RETRIES` 后消息会转入 dead-letter partition，便于人工检查和后续处理。
- 除了 REST API，系统还支持客户端直接通过 SQL `INSERT` 写消息；触发器会自动 fan-out 订阅投递并发送 `NOTIFY`，实现事务内集成。

## Results
- 文本**没有提供标准论文式定量实验结果**，没有给出吞吐、延迟、成功率或与 Kafka/RabbitMQ/pgmq 等基线的数值对比。
- 明确声称支持的能力包括：**分区内严格有序投递**（per webhook, per partition）、**指数退避重试**、以及在超过 `MAX_RETRIES` 后进入**死信分区**。
- 明确声称可实现**近实时处理**，依赖 PostgreSQL `LISTEN/NOTIFY` 在消息写入后立即触发 worker，而不是纯轮询。
- 明确声称支持**横向扩展**，通过 `FOR UPDATE SKIP LOCKED` 让多个 worker 安全并发运行。
- 工程落地方面，项目可通过 `docker-compose up --build` 单命令启动 PostgreSQL、迁移、API 和 worker，表明其重点是简化部署与使用，而非展示新的算法指标。

## Link
- [https://github.com/alaminopu/pypgmq](https://github.com/alaminopu/pypgmq)
