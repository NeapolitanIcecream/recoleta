---
source: hn
url: https://atgreen.github.io/repl-yell/posts/sbcl-fibers/
published_at: '2026-03-14T23:22:39'
authors:
- anonzzzies
topics:
- lightweight-threads
- cooperative-scheduling
- common-lisp-runtime
- io-multiplexing
- work-stealing
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# SBCL Fibers – Lightweight Cooperative Threads

## Summary
This draft work proposes lightweight cooperative user-space threads (fibers) for SBCL, aiming to retain the sequential programming model while achieving scalability close to event-driven I/O and lower thread overhead. Its focus is deep integration with the Common Lisp/SBCL runtime, especially correct handling of GC, dynamic bindings, exception cleanup, and multicore scheduling.

## Problem
- Server-style workloads are often “high concurrency but low parallelism”: many connections are primarily waiting on I/O, but SBCL OS threads are expensive, with a default control stack of about **8 MB**, so **10,000** connections would consume about **80 GB** of virtual address space in stack space alone.
- Although the event-driven model scales well, it fragments sequential logic into callbacks/state machines, increasing the difficulty of error handling, resource cleanup, and debugging; backtraces also struggle to reflect the true request call stack.
- In Common Lisp, switching only the control stack is not enough; if dynamic variable bindings, the `catch`/`unwind-protect` chains, and GC visibility are not correctly saved/restored, it can lead to runtime state corruption or even heap corruption.

## Approach
- Introduce user-space cooperative fibers: each fiber has its own control stack and binding stack, scheduled in user space by a small number of OS carrier threads rather than one kernel thread per connection.
- Use handwritten assembly `fiber_switch` for context switching, saving only the ABI-required callee-saved registers; the hot path emphasizes **zero heap allocation and zero mutex locks** to reduce switching overhead.
- Deeply integrate with the SBCL runtime: save/restore TLS overlays, binding stacks, `catch` blocks, and `unwind-protect` chains, and design GC visibility structures so that suspended fibers’ stacks and binding stacks can still be correctly scanned under stop-the-world GC.
- The scheduling layer uses multiple carriers plus a Chase-Lev lock-free work-stealing deque, supporting a deadline heap, condition-based wakeups, I/O multiplexing (`epoll`/`kqueue`/`poll`), and fiber-aware mutex/condition variable/semaphore/sleep/I/O wait primitives.
- Provide a pinning mechanism: for code sections that cannot migrate across carriers or cannot be suspended midway, yielding is prohibited, and OS blocking primitives are used as a fallback when necessary.

## Results
- The article gives a clear resource comparison: the default SBCL OS thread control stack is about **8 MB**, while a fiber’s default control stack is only **256 KB** and its binding stack **16 KB**; compared with thread stacks, a single fiber control stack is reduced to about **1/32**.
- For **10,000** concurrent connections, using OS threads would require about **80 GB** of virtual address space for thread stacks alone according to the article’s estimate; the design goal of fibers is to let “tens of thousands” of connections share a small number of carrier threads.
- On x86-64 SysV, the context-switch hot path needs to save only **6 registers (48 bytes)**; the author explicitly sets a **sub-microsecond** switching target, but the excerpt **does not provide measured microbenchmark numbers**.
- The complexity claims for scheduling and waiting operations are relatively specific: the work-stealing deque targets **O(1)** for common operations, deadline scheduling uses **O(log N)** insertion/deletion, and I/O waiter dispatch is **O(1)** via an fd-to-fiber table.
- The article claims existing SBCL blocking primitives can be transparently reused and automatically turned into cooperative waits inside fibers; it also claims support for multiple platforms (x86-64, ARM64, RISC-V, etc.) and multicore scalability, but the excerpt **does not include formal benchmarks, datasets, or relative throughput/latency baseline numbers**.
- Overall, this reads more like a **system design/implementation description plus performance-goal statement** than a completed paper with extensive experimental results; its strongest claim is achieving a lightweight fiber runtime that is GC-safe, debuggable, and multicore-scalable **without changing the Lisp sequential programming model**.

## Link
- [https://atgreen.github.io/repl-yell/posts/sbcl-fibers/](https://atgreen.github.io/repl-yell/posts/sbcl-fibers/)
