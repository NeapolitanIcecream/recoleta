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
---

# SBCL Fibers – Lightweight Cooperative Threads

## Summary
这篇工作草案提出了 SBCL 的轻量级协作式用户态线程（fibers），目标是在保留顺序式编程模型的同时，获得接近事件驱动 I/O 的扩展性与更低的线程开销。其重点在于与 Common Lisp/SBCL 运行时深度集成，尤其正确处理 GC、动态绑定、异常清理与多核调度。

## Problem
- 服务器类负载常常“高并发但低并行”：大量连接主要在等待 I/O，但 SBCL 的 OS 线程代价很高，默认约 **8 MB** 控制栈，**10,000** 连接仅栈空间就约 **80 GB** 虚拟地址空间。
- 事件驱动模型虽可扩展，但会把顺序逻辑打碎成回调/状态机，增加错误处理、资源清理与调试难度，回溯也难以反映真实请求调用栈。
- 在 Common Lisp 中，仅切换控制栈是不够的；若不正确保存/恢复动态变量绑定、`catch`/`unwind-protect` 链与 GC 可见性，会导致运行时状态损坏甚至堆破坏。

## Approach
- 引入用户态 cooperative fibers：每个 fiber 拥有自己的控制栈和 binding stack，由少量 OS carrier threads 在用户态调度，而不是一连接一内核线程。
- 通过手写汇编 `fiber_switch` 做上下文切换，仅保存 ABI 要求的 callee-saved 寄存器；热路径强调**零堆分配、零互斥锁**，以降低切换开销。
- 深度集成 SBCL 运行时：保存/恢复 TLS overlay、binding stack、`catch` 块、`unwind-protect` 链，并设计 GC 可见性结构，让暂停 fiber 的栈与绑定栈在 stop-the-world GC 下仍可被正确扫描。
- 调度层采用多 carrier + Chase-Lev 无锁 work-stealing deque，支持 deadline heap、条件唤醒、I/O multiplexing（`epoll`/`kqueue`/`poll`）以及 fiber-aware 的 mutex/condition variable/semaphore/sleep/I/O wait。
- 提供 pinning 机制：对不能跨 carrier 迁移或不能在中途挂起的代码段，禁止 yield，并在必要时退回到 OS 阻塞原语。

## Results
- 文中给出明确的资源对比：SBCL OS 线程默认控制栈约 **8 MB**，fiber 默认控制栈仅 **256 KB**，binding stack **16 KB**；相较线程栈，单 fiber 控制栈约缩小到 **1/32**。
- 对 **10,000** 并发连接，若使用 OS 线程，文中估算仅线程栈就需约 **80 GB** 虚拟地址空间；fibers 的设计目标是让“成千上万”连接共享少量 carrier threads。
- 上下文切换热路径在 x86-64 SysV 上仅需保存 **6 个寄存器（48 bytes）**；作者明确将目标设为 **sub-microsecond** 级切换，但摘录中**未提供实测微基准数值**。
- 调度与等待操作的复杂度声明较具体：work-stealing deque 目标为常见操作 **O(1)**，deadline 调度为 **O(log N)** 插入/删除，I/O waiter 通过 fd-to-fiber 表实现 **O(1)** 分发。
- 文中声称可透明复用现有 SBCL 阻塞原语，并在 fiber 中自动转为协作式等待；还声称支持多平台（x86-64、ARM64、RISC-V 等）与多核扩展，但摘录里**没有正式 benchmark、数据集或相对基线吞吐/延迟数字**。
- 结论上，这更像一份**系统设计/实现说明与性能目标陈述**，而非已完成并附充分实验结果的论文；其最强主张是“在不改变 Lisp 顺序编程模型的前提下，实现可 GC 安全、可调试、可多核扩展的轻量级纤程运行时”。

## Link
- [https://atgreen.github.io/repl-yell/posts/sbcl-fibers/](https://atgreen.github.io/repl-yell/posts/sbcl-fibers/)
