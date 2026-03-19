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
language_code: zh-CN
---

# The evolution of background job frameworks in Ruby

## Summary
这篇文章回顾了 Ruby 后台任务框架从 2008 年前后的早期实现到近年的演进脉络，解释了为什么不同阶段会从数据库队列转向 Redis，又回到更现代的数据库方案。核心价值不在提出新算法，而在总结这些框架如何围绕一致性、锁竞争、重试、并发模型和运维体验不断改进。

## Problem
- 文章要解决的是：**Ruby 后台任务框架是如何一步步演化的，各代方案分别修复了前代哪些缺陷**。
- 这件事重要，因为后台任务系统通常是生产系统关键基础设施，直接影响**事务一致性、失败重试、吞吐、内存占用、数据库压力和运维复杂度**。
- 文章还强调一个核心矛盾：**Redis 型队列更快、更独立，但缺少与主数据库事务的一致性；数据库型队列更一致，但会遇到锁竞争、膨胀和并发调度问题**。

## Approach
- 作者采用**历史回顾/系统比较**的方法，按时间线梳理多个 Ruby 队列框架：BackgrounDRb、Delayed::Job、Resque、Queue Classic、Que、Sidekiq、GoodJob、Solid Queue，并补充 River 作为后续对照。
- 对每个框架，文章都用最简单的机制层面解释其核心设计：例如**数据库持久化、Redis list/set、YAML/JSON 序列化、advisory locks、listen/notify、SKIP LOCKED、单 leader 分发、多线程 worker**。
- 文章重点比较它们如何处理几个共性问题：**任务锁定、失败重试、事务可见性、数据库膨胀、内存模型、内建 UI 与运维能力**。
- 作者给出的主线结论很简单：**框架的演进，本质上是在“速度、正确性、资源开销、功能完整性”之间不断重新取平衡**。

## Results
- **BackgrounDRb（约 2008）** 已经支持数据库持久化任务，但缺少内建重试，并依赖手动调用 `#finish!` / `#release_job`，容易因 API 误用导致任务状态错误；文中未给出量化指标。
- **Delayed::Job（2008）** 相比前代加入 `attempts` 和 `run_at` 字段，并用 `UPDATE ... WHERE locked_at IS NULL` 做原子 compare-and-swap 锁；但仍没有内建重试，且采用**每个 worker 一个进程**的 forking 模型，作者称其在大型 Ruby 代码库下会导致**“极高内存占用”**，未给出具体数字。
- **Resque** 使用 Redis 的 `SADD` 与 `RPUSH` 实现入队，这两个操作被明确描述为 **O(1)**；优势是把高吞吐队列压力从主数据库移走，但代价是**缺乏事务一致性**，可能出现“业务事务未提交、任务先执行失败”的经典问题。
- **Queue Classic / Que** 引入 Postgres 专属能力：`LISTEN/NOTIFY` 和 advisory locks 来加速任务发现与锁定；但文章指出在 MVCC 下，若出现长事务导致**数百万 dead rows**，队列扫描和锁定性能会严重退化，甚至“bring both these queues to their knees”。
- **Que** 后续通过**单 leader 锁定并向 worker 分发**来缓解数据库膨胀影响，因为膨胀带来的锁定成本从“每个 worker 都承担一次”降为“每批任务只承担一次”；这里是机制性改进，没有提供具体 benchmark 数字。
- **Solid Queue（2023）** 被描述为吸收前代经验后的成熟方案：使用 **`SKIP LOCKED` + 多 worker + 多线程**，兼顾数据库事务一致性与现代并发；与 Sidekiq 相比，文章声称它能做到**同样完整的功能集**、**无需额外 Redis 依赖**、并带有自带 UI。文中唯一明确量化数据来自相关背景论证：DHH 提到把缓存迁回磁盘型 MySQL 后，**P50 有所下降，但 P95 提升 50%**；这不是对 Solid Queue 本身的直接 benchmark。

## Link
- [https://riverqueue.com/blog/ruby-queue-history](https://riverqueue.com/blog/ruby-queue-history)
