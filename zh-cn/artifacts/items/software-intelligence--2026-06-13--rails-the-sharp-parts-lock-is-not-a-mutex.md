---
source: hn
url: https://baweaver.com/writing/2026/06/05/rails-sharp-parts-lock-is-not-a-mutex/
published_at: '2026-06-13T22:31:22'
authors:
- mooreds
topics:
- rails
- database-locking
- transactions
- concurrency-control
- data-integrity
relevance_score: 0.71
run_id: materialize-outputs
language_code: zh-CN
---

# Rails: The Sharp Parts. Lock Is Not a Mutex

## Summary
## 摘要
这篇文章解释了 Rails 锁为什么容易被误用，以及这种误用如何导致丢失更新、死锁、过期读取和其他生产环境竞态。它的核心观点是：设计应先由不变量驱动，并且数据库在可能时应该负责强制约束。

## 问题
- Rails 的 `lock`、`lock!` 和 `with_lock` 看起来很简单，但它们依赖事务范围、适配器行为、隔离级别和查询形状。
- 许多应用不变量覆盖的范围比一行数据更大，所以单行锁无法保护它们。
- 隐式写入、后台任务、管理员脚本和控制台修改都可能绕开应用层的锁定规则。

## 方法
- 先从不变量出发，再选择能强制它的最小机制：行锁、唯一索引、`CHECK`、`SERIALIZABLE`、advisory lock，或按顺序加锁。
- 需要悲观行锁时，使用 `with_lock` 或显式事务，并把锁定区间保持得尽量短。
- 对单一事实来源的规则，优先用数据库约束，比如用唯一的预订记录代替可变标志位。
- 对集合和计数器，锁定父行、切换到 `SERIALIZABLE`，或把规则编码成约束。
- 让写入路径经过一个受控入口，这样调用方就不能绕开规则。

## 结果
- 摘要里没有给出新的基准数据。
- 它说明，`Seat.lock.find(id)` 如果没有外层事务，会立刻释放锁，等于没有保护。
- 它说明，锁住所有匹配行会形成意外的排队，而 `FOR UPDATE SKIP LOCKED` 允许工作线程从池中领取可用行。
- 它说明，长事务会在外部调用期间持有锁并增加争用；修复方法是把非数据库工作移到事务外。
- 它说明，不同的加锁顺序会引发死锁，先对 ID 排序再加锁可以降低这种风险。
- 它说明，写偏斜和幻读会破坏诸如“始终至少有一名值班管理员”或“每个活动的预订不超过 100 个”这样的不变量，而 `SERIALIZABLE`、受锁保护的父行，或约束都可以修复这些问题。

## Problem

## Approach

## Results

## Link
- [https://baweaver.com/writing/2026/06/05/rails-sharp-parts-lock-is-not-a-mutex/](https://baweaver.com/writing/2026/06/05/rails-sharp-parts-lock-is-not-a-mutex/)
