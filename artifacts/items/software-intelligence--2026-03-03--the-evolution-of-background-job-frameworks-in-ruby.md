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
---

# The evolution of background job frameworks in Ruby

## Summary
本文回顾了 Ruby 后台任务框架从 2008 年前后的早期实现到现代方案的演进脉络，重点分析了数据库队列与 Redis 队列在一致性、并发、锁竞争、功能完备性和运维体验上的取舍。文章的核心价值在于总结各代框架如何逐步修补前代缺陷，并指出现代设计为何趋向于“事务一致 + 更强数据库原语 + 内置功能/UI”。

## Problem
- 文章要解决的问题是：Ruby 的后台任务框架为什么会一代代演进，以及不同架构分别解决了哪些真实生产问题。
- 这很重要，因为后台任务系统通常是业务关键基础设施，直接影响任务可靠性、事务一致性、吞吐、内存占用、数据库压力和运维复杂度。
- 具体痛点包括：手工任务生命周期容易出错、缺少内置重试、Redis 队列缺乏事务一致性、数据库队列会受锁竞争和表膨胀影响，以及早期 Ruby 多进程模型内存开销大。

## Approach
- 作者采用历史综述的方法，按时间顺序比较 BackgrounDRb、Delayed::Job、Resque、Queue Classic、Que、Sidekiq、GoodJob、Solid Queue 等代表性框架。
- 核心机制对比很简单：有些框架把任务存数据库里，依赖数据库锁、事务、listen/notify、advisory locks 或 `SKIP LOCKED` 来分发任务；另一些把任务放进 Redis，依赖列表/集合等高性能数据结构来快速入队出队。
- 文章重点解释每一代的“补丁式进步”：例如 Delayed::Job 增加 attempts/run_at，Resque 提升性能但牺牲事务一致性，Queue Classic/Que 利用 Postgres 特性，Sidekiq 强调“功能齐全 + 可运维化”，Solid Queue 则吸收前人经验并用较新的数据库能力改进数据库队列。
- 作者还抽象出较优现代模式：任务只有在事务真正提交后才可见，使用 `SKIP LOCKED` 降低竞争，最好配合单 leader 或更优调度模型，并内建重试、周期任务、唯一任务和 UI。

## Results
- 这不是一篇实验型论文，文中**没有提供系统性的基准测试、公开数据集或统一量化评测结果**。
- 最明确的量化结果来自 Solid Queue 背景叙述：DHH 提到将 Redis 缓存替换为磁盘型 MySQL 后，**P50 变差但 P95 提升 50%**；不过这组数字针对缓存系统，不是后台任务框架本身的正式对比实验。
- 文中给出若干时间与采用史实：BackgrounDRb/Delayed::Job 可追溯到 **2008**；Queue Classic 约 **2011**；Que 为 **2013**；GoodJob 发布于 **2020**；Solid Queue 在 **2023** Rails World 发布。
- 具体实现细节上的数字包括：Delayed::Job 工作者会一次尝试锁定最多 **5** 个任务（`worker.read_ahead`）；GoodJob 初始发布时宣称代码量约 **600 行**。
- 最强的非量化结论是：Solid Queue 被描述为兼具 Sidekiq 级别的功能、数据库事务一致性、内置 UI，以及基于 `SKIP LOCKED` 和多线程 worker 的现代并发模型；而 Redis 队列的核心缺陷是与主数据库事务脱耦，可能导致任务“先执行、后提交”的不一致问题。

## Link
- [https://riverqueue.com/blog/ruby-queue-history](https://riverqueue.com/blog/ruby-queue-history)
