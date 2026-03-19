---
source: hn
url: https://www.rogerbinns.com/blog/async-apsw.html
published_at: '2026-03-14T23:51:04'
authors:
- fowl2
topics:
- python
- sqlite
- async-programming
- event-loop
- database-wrapper
- code-maintainability
relevance_score: 0.52
run_id: materialize-outputs
language_code: zh-CN
---

# APSW in Colour (Async) – Another Python SQLite Wrapper

## Summary
这篇文章介绍了 APSW（Another Python SQLite Wrapper）如何在不拆分库、不复制 API 的前提下，为整个 SQLite/Python 绑定实现完整异步支持。其核心贡献是用同一套底层实现同时服务同步与异步调用，并把回调、虚表、超时/取消和多事件循环支持一起做全。

## Problem
- 现有 Python 异步 SQLite 封装通常只是把同步调用丢到后台线程执行，**API 不完整**，常常缺少游标、blob、backup、session 等高级能力。
- 这些封装通常**无法在 SQLite 回调中使用 async 函数**，因此像 SQL 中调用用户注册的异步函数、异步虚拟表这类重要场景难以支持。
- 维护同步版和异步版两套接口会造成**重复实现、文档/类型滞后、事件循环兼容性差**，随着 SQLite/Python API 演进很难长期维护。

## Approach
- 采用**单 worker thread + 同一套 C 实现**：SQLite C API 本质是同步的，所以把真正的 SQLite 调用放到后台工作线程；连接对象自己知道是 sync 还是 async，从而复用同一条实现路径，而不是维护独立 AsyncConnection 代码库。
- 通过 **Controller 抽象**把事件循环差异隔离出来，统一负责启动/停止 worker、在线程间转发调用、把协程/任务送回事件循环执行；可支持 asyncio、Trio、AnyIO，并允许用户自定义控制器。
- 对 APSW 中所有回调调用点做统一拦截：若回调结果是协程，就借助 **context/thread local + run_coroutine_threadsafe** 把它送回事件循环执行，从而让大量 SQLite 回调位点自动支持 async 回调。
- 处理异步语义中的难点：把**超时、取消、deadline**从事件循环传递到 worker 线程及其异步回调；并为查询迭代实现**批量取行**，避免每一行都跨线程往返带来的高开销。
- 借助已有 APSW 工具链进行**自动化维护**：参数解析、错误处理、类型桩、文档标注、行为测试都尽量数据化/自动化，避免手写“异步包装层”导致长期失配。

## Results
- 作者声称实现了 **完整 async support across the entire APSW API**，覆盖普通数据库操作、**callbacks、virtual tables、advanced SQLite features**，而不仅是常见子集。
- 实现同时支持 **3 个主要异步生态**：**asyncio、Trio、AnyIO**，且**不需要单独发布 async-apsw 包**，也不要求复制一套异步 API。
- 通过一次统一改造，APSW 里**大约 120 个回调点**都获得了对 async 函数的支持，这是对现有 async SQLite wrapper 的关键扩展。
- 自定义 Controller 的实现规模被压到**50 行以内**，表明跨事件循环适配层被设计得足够轻量、可替换。
- 在性能方面，作者发现逐行异步迭代会非常慢，因此引入类似 aiosqlite 的**批量取行（默认 64 行）**策略；文中没有给出最终吞吐/延迟的具体数值对比，但明确说明已把 benchmark 纳入工具和文档。
- 文中**没有提供标准化基准分数、数据集或百分比提升**；最强的实证性主张是：该方案已能稳健运行，并在功能完整性、回调异步化、多事件循环兼容和可维护性上明显超出已有同类封装。

## Link
- [https://www.rogerbinns.com/blog/async-apsw.html](https://www.rogerbinns.com/blog/async-apsw.html)
