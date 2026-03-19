---
source: hn
url: https://riverqueue.com/blog/ruby-queue-history
published_at: '2026-03-03T23:50:34'
authors:
- thunderbong
topics:
- ruby-background-jobs
- job-queue-frameworks
- postgres-queues
- redis-queues
- transactional-consistency
relevance_score: 0.35
run_id: materialize-outputs
language_code: en
---

# The evolution of background job frameworks in Ruby

## Summary
This article reviews the evolution of Ruby background job frameworks from early implementations around 2008 to modern solutions, focusing on the trade-offs between database-backed queues and Redis-backed queues in consistency, concurrency, lock contention, feature completeness, and operational experience. The core value of the article is in summarizing how each generation of frameworks gradually patched the shortcomings of its predecessors, and in explaining why modern designs tend toward "transactional consistency + stronger database primitives + built-in features/UI."

## Problem
- The article addresses the question of why Ruby background job frameworks evolved generation by generation, and which real production problems different architectures solved.
- This matters because background job systems are usually business-critical infrastructure, directly affecting job reliability, transactional consistency, throughput, memory usage, database pressure, and operational complexity.
- Specific pain points include: manually managed job lifecycles being error-prone, lack of built-in retries, Redis queues lacking transactional consistency, database queues being affected by lock contention and table bloat, and the high memory overhead of Ruby's early multi-process model.

## Approach
- The author uses a historical survey approach, comparing representative frameworks in chronological order, including BackgrounDRb, Delayed::Job, Resque, Queue Classic, Que, Sidekiq, GoodJob, and Solid Queue.
- The core mechanism comparison is straightforward: some frameworks store jobs in the database, relying on database locks, transactions, listen/notify, advisory locks, or `SKIP LOCKED` to distribute jobs; others put jobs in Redis, relying on high-performance data structures like lists/sets for fast enqueue and dequeue.
- The article emphasizes each generation's "patch-style progress": for example, Delayed::Job added attempts/run_at, Resque improved performance but sacrificed transactional consistency, Queue Classic/Que leveraged Postgres features, Sidekiq emphasized being "feature-complete + operable," and Solid Queue absorbed lessons from its predecessors while improving database queues with newer database capabilities.
- The author also abstracts a stronger modern pattern: jobs should only become visible after a transaction truly commits, `SKIP LOCKED` should be used to reduce contention, ideally paired with a single leader or a better scheduling model, along with built-in retries, periodic jobs, unique jobs, and a UI.

## Results
- This is not an experimental paper, and the article **does not provide systematic benchmark tests, public datasets, or unified quantitative evaluation results**.
- The clearest quantitative result comes from the Solid Queue background discussion: DHH mentioned that after replacing a Redis cache with disk-backed MySQL, **P50 worsened but P95 improved by 50%**; however, these numbers refer to a caching system, not a formal comparative experiment on background job frameworks themselves.
- The article provides several dates and adoption-history facts: BackgrounDRb/Delayed::Job trace back to **2008**; Queue Classic to around **2011**; Que to **2013**; GoodJob was released in **2020**; and Solid Queue was announced at Rails World in **2023**.
- Numerical details in specific implementations include: Delayed::Job workers will try to lock up to **5** jobs at a time (`worker.read_ahead`); GoodJob claimed to be about **600 lines** of code when first released.
- The strongest non-quantitative conclusion is that Solid Queue is described as combining Sidekiq-level features, database transactional consistency, a built-in UI, and a modern concurrency model based on `SKIP LOCKED` and multithreaded workers; meanwhile, the core flaw of Redis queues is their decoupling from the primary database transaction, which can lead to the inconsistency of jobs being "executed before commit."

## Link
- [https://riverqueue.com/blog/ruby-queue-history](https://riverqueue.com/blog/ruby-queue-history)
