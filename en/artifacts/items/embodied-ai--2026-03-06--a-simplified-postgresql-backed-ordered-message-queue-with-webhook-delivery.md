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
language_code: en
---

# A simplified PostgreSQL-backed ordered message queue with webhook delivery

## Summary
This is a PostgreSQL-based ordered message queue system that exposes interfaces through FastAPI and automatically delivers messages to registered webhooks. Its core value is using common database capabilities to achieve near-real-time, retryable, strictly ordered message distribution within partitions.

## Problem
- It addresses the question of how to build a message queue with **topic/partition messaging, automatic webhook delivery, failure retries, dead-letter handling, and strict ordering guarantees** while keeping overall system complexity low.
- This matters because many applications only need reliable event distribution and HTTP callbacks, and may not want to introduce heavier infrastructure such as Kafka or RabbitMQ.
- It also needs to support direct SQL writes within business transactions, near-real-time trigger-based processing, and concurrency safety when scaling horizontally with multiple workers.

## Approach
- It uses **PostgreSQL as the message storage and coordination layer**: messages are written to the database, with topic and partition organizing message streams.
- It exposes message publishing and webhook registration through a **FastAPI REST API**, while also supporting clients writing messages through **direct SQL INSERT**.
- It uses **PostgreSQL trigger + LISTEN/NOTIFY**: after a message is written, a trigger creates delivery records for each subscribed webhook and sends a NOTIFY so workers can process immediately.
- A background **delivery worker** performs HTTP POST delivery; if the response is non-2xx, it retries with **exponential backoff**, and after exceeding `MAX_RETRIES` the message goes to the **dead-letter partition**.
- To support safe parallel processing across multiple workers, it relies on **`FOR UPDATE SKIP LOCKED`** for concurrent claiming, while maintaining strict ordering for each webhook within each partition.

## Results
- The text **does not provide quantitative results from standard datasets or benchmark experiments**, so there are no specific numbers for throughput, latency, or success rate to report.
- Explicitly claimed capabilities include **strictly ordered delivery within a partition** (per webhook, per partition), **exponential backoff retries after failures**, and moving messages to the **dead-letter partition** after exceeding **`MAX_RETRIES`**.
- The system claims to support **horizontal scaling**: multiple workers can run, with concurrent processing handled safely through **`FOR UPDATE SKIP LOCKED`**.
- The system claims to provide **near-real-time processing**: with PostgreSQL **LISTEN/NOTIFY**, writing a message can immediately wake a worker.
- In terms of engineering usability, the project claims that PostgreSQL, migrations, the API, and the worker can all be started with a single **`docker-compose up --build` command**.

## Link
- [https://github.com/alaminopu/pypgmq](https://github.com/alaminopu/pypgmq)
