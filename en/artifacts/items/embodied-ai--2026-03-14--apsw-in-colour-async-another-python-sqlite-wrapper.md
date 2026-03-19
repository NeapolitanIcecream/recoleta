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
language_code: en
---

# APSW in Colour (Async) – Another Python SQLite Wrapper

## Summary
This article explains how APSW implements full async support for Python's SQLite wrapper **without forking the API, breaking functionality, or excessively duplicating code**. Its core value is safely connecting SQLite's synchronous C API to asyncio/Trio/AnyIO, while also allowing callbacks, virtual tables, and advanced features to work asynchronously.

## Problem
- Existing Python async SQLite wrappers usually just offload synchronous calls to background threads, resulting in an **incomplete API** that often lacks advanced capabilities such as cursors, blob, backup, and session.
- These wrappers typically **cannot use async functions in SQLite callbacks**, for example they cannot register async functions for SQL or virtual table callbacks, which limits typical async scenarios such as network access.
- Maintaining an async version often requires **duplicating an entire set of interfaces, documentation, and type information**, making it easy to fall behind updates to the main library and increasing the burden of cross-event-loop and version compatibility.

## Approach
- Use a **single background worker thread** to execute SQLite's synchronous C API, since SQLite itself has no non-blocking interface; this avoids the debugging difficulties, reentrant deadlocks, and nondeterministic execution order caused by thread pools.
- Do not create a separate async package or hand-write a parallel API; instead, in the **same APSW C implementation**, detect whether a connection is an async connection, and if so forward the same function calls to the worker thread and return awaitable results.
- Manage everything through a unified **Controller abstraction**: starting/stopping the worker, sending calls to the thread, and sending coroutines/tasks back to the event loop for execution, thereby supporting asyncio, Trio, and AnyIO, while also allowing automatic event loop detection.
- For SQLite's roughly **120 callback points**, check at the low-level call site whether the return value is a coroutine; if so, submit it back to the event loop for execution, so **both synchronous and asynchronous callbacks work**.
- To reduce thread round-trip overhead, query iteration uses **batched row fetching** rather than one thread switch per row, and makes the batch size configurable; it also implements timeouts, cancellation, deadline propagation, and automatic maintenance of documentation/type stubs.

## Results
- The author claims to have achieved **complete async support for the full APSW API**, covering callbacks, virtual tables, and advanced SQLite capabilities such as backup and session, rather than the subset typical of common async wrappers.
- Async callback support extends to about **120 callbacks** in APSW, which is the clearest coverage-scale number given in the article.
- The standard implementation of Controller is described as **under 50 lines of code**, suggesting that the cross-event-loop adaptation layer is relatively lightweight.
- The article explicitly compares common approaches and notes that iterating query results across threads one row at a time performs poorly, so APSW instead adopts a strategy similar to aiosqlite with **batched fetching (example default batch size 64)** to improve performance.
- The author says **benchmarking has been incorporated into the tools and documentation**, and that a separate repository was also created to measure thread communication overhead; however, the excerpt **does not provide specific throughput, latency, speedup, or benchmark scores**, so reproducible quantitative SOTA metrics are lacking.
- The strongest concrete claim is that, without requiring a separate package or duplicated API, it can simultaneously support **asyncio, Trio, and AnyIO**, while preserving automated maintainability for future SQLite/Python API updates.

## Link
- [https://www.rogerbinns.com/blog/async-apsw.html](https://www.rogerbinns.com/blog/async-apsw.html)
