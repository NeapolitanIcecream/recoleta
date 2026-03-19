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
language_code: en
---

# APSW in Colour (Async) – Another Python SQLite Wrapper

## Summary
This article explains how APSW (Another Python SQLite Wrapper) implemented full async support for the entire SQLite/Python binding without splitting the library or duplicating the API. Its core contribution is using the same underlying implementation to serve both synchronous and asynchronous calls, while also fully supporting callbacks, virtual tables, timeouts/cancellation, and multiple event loops.

## Problem
- Existing Python async SQLite wrappers usually just offload synchronous calls to background threads, resulting in an **incomplete API** that often lacks advanced capabilities such as cursors, blobs, backup, and sessions.
- These wrappers typically **cannot use async functions inside SQLite callbacks**, making important scenarios like calling user-registered async functions from SQL or implementing async virtual tables difficult to support.
- Maintaining separate synchronous and asynchronous interfaces causes **duplicated implementations, lagging documentation/types, and poor event loop compatibility**, making long-term maintenance difficult as the SQLite/Python API evolves.

## Approach
- Use **a single worker thread + the same C implementation**: because the SQLite C API is inherently synchronous, the actual SQLite calls run in a background worker thread; the connection object knows whether it is sync or async, allowing reuse of the same implementation path instead of maintaining a separate AsyncConnection codebase.
- Isolate event loop differences through a **Controller abstraction**, which uniformly handles starting/stopping the worker, forwarding calls across threads, and sending coroutines/tasks back to the event loop for execution; this supports asyncio, Trio, and AnyIO, and also allows users to define custom controllers.
- Uniformly intercept all callback invocation points in APSW: if a callback result is a coroutine, it is sent back to the event loop for execution using **context/thread local + run_coroutine_threadsafe**, allowing many SQLite callback sites to automatically support async callbacks.
- Handle the hard parts of async semantics: propagate **timeouts, cancellation, and deadlines** from the event loop to the worker thread and its async callbacks; also implement **batched row fetching** for query iteration to avoid the high overhead of crossing threads for every single row.
- Rely on the existing APSW toolchain for **automated maintenance**: parameter parsing, error handling, type stubs, documentation annotations, and behavior tests are made as data-driven/automated as possible, avoiding long-term drift caused by hand-written “async wrapper layers.”

## Results
- The author claims **complete async support across the entire APSW API**, covering ordinary database operations, **callbacks, virtual tables, advanced SQLite features**, rather than just the usual subset.
- The implementation supports **3 major async ecosystems** simultaneously: **asyncio, Trio, AnyIO**, and **does not require publishing a separate async-apsw package**, nor duplicating a separate async API.
- Through one unified refactor, about **120 callback sites** in APSW gained support for async functions, which is a key extension beyond existing async SQLite wrappers.
- The implementation size of a custom Controller is kept to **under 50 lines**, suggesting the cross-event-loop adaptation layer is designed to be lightweight and replaceable.
- On performance, the author found that per-row async iteration is very slow, so they introduced a **batched row fetch (default 64 rows)** strategy similar to aiosqlite; the article does not provide final throughput/latency comparisons in concrete numbers, but clearly states that benchmarks have been included in the tooling and documentation.
- The article **does not provide standardized benchmark scores, datasets, or percentage improvements**; the strongest empirical claim is that the approach now runs robustly and clearly exceeds existing similar wrappers in feature completeness, callback async support, multi-event-loop compatibility, and maintainability.

## Link
- [https://www.rogerbinns.com/blog/async-apsw.html](https://www.rogerbinns.com/blog/async-apsw.html)
