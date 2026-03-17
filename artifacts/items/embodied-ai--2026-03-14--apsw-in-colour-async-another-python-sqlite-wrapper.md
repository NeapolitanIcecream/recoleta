---
source: hn
url: https://www.rogerbinns.com/blog/async-apsw.html
published_at: '2026-03-14T23:51:04'
authors:
- fowl2
topics:
- python
- sqlite
- async-io
- api-design
- worker-thread
relevance_score: 0.01
run_id: materialize-outputs
---

# APSW in Colour (Async) – Another Python SQLite Wrapper

## Summary
这篇文章介绍了 APSW 如何在**不分叉 API、不断裂功能、不过度复制代码**的前提下，为 Python 的 SQLite 封装实现完整异步支持。其核心价值在于：把 SQLite 的同步 C API 安全地接入 asyncio/Trio/AnyIO，并且连回调、虚拟表和高级特性都能异步工作。

## Problem
- 现有 Python 异步 SQLite 封装通常只是把同步调用丢到后台线程，**API 不完整**，常缺少游标、blob、backup、session 等高级能力。
- 这些封装通常**无法在 SQLite 回调中使用 async 函数**，例如无法把异步函数注册给 SQL 或虚拟表回调，这限制了网络访问等典型异步场景。
- 维护异步版往往需要**重复一整套接口、文档和类型信息**，容易落后于主库更新，也增加了跨事件循环和版本兼容的负担。

## Approach
- 用**单个后台工作线程**执行 SQLite 的同步 C API，因为 SQLite 本身没有非阻塞接口；这样避免线程池带来的调试困难、重入死锁和执行顺序不确定性。
- 不创建独立 async 包，也不手写一套平行 API；而是在 **同一套 APSW C 实现** 中检测连接是否为异步连接，若是则把同样的函数调用转发到 worker thread，返回可 await 的结果。
- 通过统一的 **Controller 抽象** 管理：启动/停止 worker、把调用送到线程、把协程/任务送回事件循环执行，从而支持 asyncio、Trio、AnyIO，并允许自动检测事件循环。
- 对 SQLite 的约 **120 个回调点**，在底层调用时检查返回值是否为 coroutine；若是，则把它提交回事件循环执行，因此**同步/异步回调都能工作**。
- 为了降低线程往返开销，查询迭代采用**批量取行**而不是每行一次线程切换，并把批大小做成可配置；同时实现了超时、取消、deadline 传播，以及文档/类型桩的自动维护。

## Results
- 作者声称实现了 **APSW 全 API 的完整异步支持**，覆盖 callbacks、virtual tables 以及 backup、session 等高级 SQLite 能力，而不是常见 async wrapper 的子集。
- 异步回调支持扩展到 APSW 中大约 **120 个 callbacks**，这是文章里最明确的覆盖规模数字。
- Controller 的标准实现被描述为**不到 50 行代码**，表明跨事件循环适配层相对轻量。
- 文章明确对比指出：常见方案对查询结果逐行跨线程迭代性能很差，因此 APSW 改为类似 aiosqlite 的**批量拉取（示例默认批大小 64）**策略以改善性能。
- 作者表示已把**benchmarking 纳入工具和文档**，并且额外做了独立仓库测量线程通信开销；但摘录中**没有给出具体吞吐、延迟、速度提升或基准分数**，因此缺少可复现的定量 SOTA 指标。
- 最强的具体主张是：无需独立包或重复 API，即可同时支持 **asyncio、Trio、AnyIO**，并保持未来 SQLite/Python API 更新时的自动化维护能力。

## Link
- [https://www.rogerbinns.com/blog/async-apsw.html](https://www.rogerbinns.com/blog/async-apsw.html)
