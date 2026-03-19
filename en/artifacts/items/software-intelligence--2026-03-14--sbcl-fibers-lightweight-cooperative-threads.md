---
source: hn
url: https://atgreen.github.io/repl-yell/posts/sbcl-fibers/
published_at: '2026-03-14T23:22:39'
authors:
- anonzzzies
topics:
- lightweight-threads
- cooperative-scheduling
- common-lisp
- runtime-systems
- work-stealing
relevance_score: 0.56
run_id: materialize-outputs
language_code: en
---

# SBCL Fibers – Lightweight Cooperative Threads

## Summary
This article presents a draft design and implementation for lightweight cooperative user-space threads (fibers) for SBCL, aiming to preserve the experience of sequential programming while achieving concurrency efficiency close to event-driven systems. Its main focus is ensuring that Common Lisp's complex thread-local state, GC, and blocking primitives can all interoperate with fibers correctly and transparently.

## Problem
- OS threads in SBCL are expensive: each thread typically requires an **8 MB** control stack, plus a binding stack, TLS, and kernel scheduling overhead. With **10,000** concurrent connections, stack space alone would consume about **80 GB** of virtual address space.
- Event-driven I/O is scalable, but it breaks sequential logic into callbacks or state machines, increasing the complexity of error handling, resource cleanup, and debugging.
- Common Lisp/SBCL also introduces extra challenges: it is not enough to switch only the control stack; dynamic variable bindings, `catch`/`unwind-protect` chains, and GC visibility must also be saved and restored correctly, or state corruption or heap corruption can result.

## Approach
- Use **fiber = user-space cooperative thread** in place of large numbers of OS threads: each fiber has its own control stack and binding stack, and a small number of carrier OS threads schedule and run them in user space.
- Perform ultra-lightweight context switching with hand-written assembly `fiber_switch`: save only the callee-saved registers required by the ABI; for example, x86-64 SysV saves only **6 registers (48 bytes)**, and the switching path is designed for **zero heap allocation and zero mutexes**.
- Deep runtime integration for SBCL: save and restore the binding stack, TLS overlay, and `catch`/`unwind-protect` chains, and design a GC visibility scheme based on a "two-table" approach so that stack objects in suspended fibers can still be scanned correctly under stop-the-world and compacting GC.
- The scheduler uses one scheduler per carrier, combined with a **Chase-Lev lock-free work-stealing deque**, a deadline min-heap, and `epoll`/`kqueue`/`poll` I/O multiplexing to support multicore utilization and highly concurrent waiting.
- By adding fiber-aware dispatch to blocking primitives such as `grab-mutex`, `condition-wait`, `sleep`, and `wait-until-fd-usable`, existing SBCL code can usually suspend cooperatively inside a fiber without modification.

## Results
- The article gives explicit resource targets: the default fiber control stack is only **256 KB**, and the binding stack is **16 KB**. Compared with the common **8 MB** control stack of SBCL OS threads, per-task stack usage is greatly reduced.
- The article states that it is designed for **tens of thousands** of fibers, with the **10,000**-connection scenario as a core motivation; compared with one OS thread per connection, this can significantly reduce virtual address space usage and kernel scheduling pressure.
- For context switching, the author's target is **sub-microsecond** switching overhead, but the excerpt **does not provide actual microbenchmark numbers, datasets, or quantitative comparisons with existing SBCL threads or other fiber runtimes**.
- For scalability mechanisms, the article provides complexity claims: run-queue operations are **O(1)**, deadline scheduling insertion/removal is **O(log N)**, and I/O waiter dispatch is implemented as **O(1) dispatch** via fd indexing.
- In terms of platform support, the draft claims coverage of **x86-64 (Linux/macOS/Windows)**, **ARM64**, **ARM32**, **PPC64/PPC32**, and **RISC-V**, but the excerpt **does not provide cross-platform performance or stability experiment data**.
- Overall, this is a **work-in-progress design/implementation document** rather than a finished paper; its strongest concrete claim is transparent fiber integration in SBCL for GC, safe dynamic bindings, exception cleanup, blocking primitives, and multicore work-stealing.

## Link
- [https://atgreen.github.io/repl-yell/posts/sbcl-fibers/](https://atgreen.github.io/repl-yell/posts/sbcl-fibers/)
