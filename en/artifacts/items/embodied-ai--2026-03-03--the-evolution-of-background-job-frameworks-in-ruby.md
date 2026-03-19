---
source: hn
url: https://riverqueue.com/blog/ruby-queue-history
published_at: '2026-03-03T23:50:34'
authors:
- thunderbong
topics:
- ruby-background-jobs
- job-queue-history
- postgres-queues
- redis-queues
- transactional-consistency
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# The evolution of background job frameworks in Ruby

## Summary
This article reviews the evolution of Ruby background job frameworks from their early implementations around 2008 to more recent developments, explaining why different stages shifted from database-backed queues to Redis and then back to more modern database-based approaches. Its core value is not in proposing a new algorithm, but in summarizing how these frameworks continually improved around consistency, lock contention, retries, concurrency models, and operational experience.

## Problem
- The article aims to answer: **How did Ruby background job frameworks evolve step by step, and which shortcomings of previous generations did each new approach fix**.
- This matters because background job systems are usually critical infrastructure in production systems, directly affecting **transactional consistency, failure retries, throughput, memory usage, database pressure, and operational complexity**.
- The article also emphasizes a central tension: **Redis-style queues are faster and more independent, but lack consistency with the primary database transaction; database-style queues are more consistent, but run into lock contention, bloat, and concurrency scheduling problems**.

## Approach
- The author uses a **historical review / systems comparison** approach, tracing multiple Ruby queue frameworks along a timeline: BackgrounDRb, Delayed::Job, Resque, Queue Classic, Que, Sidekiq, GoodJob, Solid Queue, and adds River as a later point of comparison.
- For each framework, the article explains its core design at the simplest mechanism level, such as **database persistence, Redis list/set, YAML/JSON serialization, advisory locks, listen/notify, SKIP LOCKED, single-leader dispatch, and multithreaded workers**.
- The article focuses on how they handle several common problems: **job locking, failure retries, transactional visibility, database bloat, memory model, and built-in UI and operational capabilities**.
- The author’s main conclusion is simple: **the evolution of these frameworks is essentially a continual rebalancing among “speed, correctness, resource cost, and feature completeness”**.

## Results
- **BackgrounDRb (around 2008)** already supported database-persisted jobs, but lacked built-in retries and relied on manually calling `#finish!` / `#release_job`, making it easy for API misuse to produce incorrect job states; the article provides no quantitative metrics.
- **Delayed::Job (2008)** added `attempts` and `run_at` fields compared with its predecessor, and used `UPDATE ... WHERE locked_at IS NULL` as an atomic compare-and-swap lock; but it still had no built-in retries, and used a **one-process-per-worker** forking model that the author says led to **“extremely high memory usage”** in large Ruby codebases, without giving specific numbers.
- **Resque** uses Redis `SADD` and `RPUSH` for enqueueing, and these two operations are explicitly described as **O(1)**; its advantage is moving high-throughput queue pressure off the primary database, but the cost is **lack of transactional consistency**, which can produce the classic problem where “the business transaction has not committed, but the job runs early and fails.”
- **Queue Classic / Que** introduced Postgres-specific capabilities: `LISTEN/NOTIFY` and advisory locks to speed up job discovery and locking; but the article notes that under MVCC, if long-running transactions produce **millions of dead rows**, queue scanning and locking performance can degrade severely, even “bring both these queues to their knees”.
- **Que** later mitigated the effects of database bloat through **a single leader that acquires locks and dispatches to workers**, because the locking cost caused by bloat dropped from “paid once by every worker” to “paid once per batch of jobs”; this is a mechanistic improvement, and no specific benchmark numbers are provided.
- **Solid Queue (2023)** is described as a mature solution that absorbs the lessons of earlier generations: using **`SKIP LOCKED` + multiple workers + multithreading**, it combines database transactional consistency with modern concurrency; compared with Sidekiq, the article claims it can provide **an equally complete feature set**, **without an extra Redis dependency**, and with a built-in UI. The only clearly quantified figure in the article comes from related background argumentation: DHH mentioned that after moving cache back to disk-backed MySQL, **P50 decreased somewhat, but P95 improved by 50%**; this is not a direct benchmark of Solid Queue itself.

## Link
- [https://riverqueue.com/blog/ruby-queue-history](https://riverqueue.com/blog/ruby-queue-history)
