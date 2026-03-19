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
language_code: en
---

# A simplified PostgreSQL-backed ordered message queue with webhook delivery

## Summary
This is an ordered message queue implementation based on PostgreSQL, exposing a REST API via FastAPI and automatically delivering messages to subscribed webhooks. It emphasizes achieving strict in-partition ordering, failure retries, dead-letter handling, and near-real-time dispatch with as little infrastructure complexity as possible.

## Problem
- The problem it addresses is: how to build a message queue that **supports topics, in-partition ordering, and webhook delivery** without introducing standalone messaging systems such as Kafka or RabbitMQ.
- This matters because many applications already depend on PostgreSQL and want to reuse the existing database for event distribution, asynchronous decoupling, and external system notifications, reducing operational complexity.
- It also needs to solve reliability issues after failed deliveries, including retries, backoff, and dead-letter archiving, while supporting horizontal scaling across multiple workers without breaking ordering.

## Approach
- The core mechanism is very simple: messages are first written into PostgreSQL, database triggers generate delivery records for each subscribed webhook, and `LISTEN/NOTIFY` immediately wakes background workers.
- Workers pull pending delivery records from the database and execute HTTP POST requests one by one according to webhook and partition order; successes are acknowledged, while failures are retried with exponential backoff.
- To ensure concurrency safety and horizontal scaling, multiple workers use PostgreSQL's `FOR UPDATE SKIP LOCKED` to claim tasks, avoiding duplicate processing of the same delivery record.
- To ensure reliability, after reaching `MAX_RETRIES`, messages are moved into the dead-letter partition for manual inspection and follow-up handling.
- In addition to the REST API, the system also supports clients writing messages directly via SQL `INSERT`; triggers automatically fan out subscribed deliveries and send `NOTIFY`, enabling in-transaction integration.

## Results
- The text **does not provide standard paper-style quantitative experimental results**; it does not report throughput, latency, success rate, or numerical comparisons against baselines such as Kafka, RabbitMQ, or pgmq.
- The explicitly claimed capabilities include: **strict in-partition ordered delivery** (per webhook, per partition), **exponential-backoff retries**, and moving messages into a **dead-letter partition** after exceeding `MAX_RETRIES`.
- It explicitly claims to enable **near-real-time processing**, relying on PostgreSQL `LISTEN/NOTIFY` to trigger workers immediately after message insertion rather than using pure polling.
- It explicitly claims to support **horizontal scaling**, allowing multiple workers to run safely in parallel through `FOR UPDATE SKIP LOCKED`.
- From an engineering deployment perspective, the project can start PostgreSQL, migrations, the API, and workers with the single command `docker-compose up --build`, indicating that its focus is on simplifying deployment and usage rather than presenting novel algorithmic metrics.

## Link
- [https://github.com/alaminopu/pypgmq](https://github.com/alaminopu/pypgmq)
