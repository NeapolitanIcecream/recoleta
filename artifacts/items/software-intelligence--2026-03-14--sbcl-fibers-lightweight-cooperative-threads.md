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
---

# SBCL Fibers – Lightweight Cooperative Threads

## Summary
这篇文章提出了面向 SBCL 的轻量级协作式用户态线程（fibers）设计与实现草案，目标是在保持顺序式编程体验的同时，获得接近事件驱动系统的并发效率。其重点在于让 Common Lisp 复杂的线程本地状态、GC 和阻塞原语都能与 fibers 正确且透明地协同工作。

## Problem
- SBCL 的 OS 线程开销很高：每线程通常需要 **8 MB** 控制栈，加上绑定栈、TLS 和内核调度成本，面对 **10,000** 并发连接时仅栈空间就约 **80 GB** 虚拟地址空间。
- 事件驱动 I/O 虽然可扩展，但会把顺序逻辑拆成回调或状态机，增加错误处理、资源清理和调试复杂度。
- Common Lisp/SBCL 还有额外难点：不仅要切换控制栈，还要正确保存/恢复动态变量绑定、`catch`/`unwind-protect` 链和 GC 可见性，否则会导致状态损坏或堆损坏。

## Approach
- 用 **fiber = 用户态协作线程** 替代大量 OS 线程：每个 fiber 拥有独立控制栈和绑定栈，由少量 carrier OS 线程在用户态调度运行。
- 通过手写汇编 `fiber_switch` 做超轻量上下文切换：只保存 ABI 要求的 callee-saved 寄存器；例如 x86-64 SysV 仅保存 **6 个寄存器（48 字节）**，并强调切换路径 **零堆分配、零互斥锁**。
- 为 SBCL 做深度运行时集成：保存/恢复 binding stack、TLS overlay、`catch`/`unwind-protect` 链，并设计“两张表”式 GC 可见性管理，让暂停 fiber 的栈对象在 stop-the-world、compacting GC 下仍可被正确扫描。
- 调度器采用每 carrier 一个 scheduler 的结构，结合 **Chase-Lev 无锁 work-stealing deque**、deadline 小顶堆和 `epoll`/`kqueue`/`poll` I/O 多路复用，以支持多核利用和高并发等待。
- 通过对 `grab-mutex`、`condition-wait`、`sleep`、`wait-until-fd-usable` 等阻塞原语做 fiber-aware 分发，让现有 SBCL 代码在 fiber 中通常无需修改即可协作式挂起。

## Results
- 文中给出了明确的资源目标：fiber 默认控制栈仅 **256 KB**、绑定栈 **16 KB**，相比 SBCL OS 线程常见 **8 MB** 控制栈，单任务栈占用大幅下降。
- 文章宣称面向 **tens of thousands** 级别 fibers 设计，且以 **10,000** 连接场景为核心动机；相比每连接一个 OS 线程，可显著减少虚拟地址空间与内核调度压力。
- 在上下文切换方面，作者的目标是 **sub-microsecond** 级切换开销，但摘录内容**未提供实际微基准数值、数据集或与现有 SBCL 线程/其他 fiber 运行时的定量对比结果**。
- 在可扩展性机制上，文中给出复杂度声明：运行队列操作为 **O(1)**，deadline 调度插入/删除为 **O(log N)**，I/O waiter 通过 fd 索引实现 **O(1) dispatch**。
- 平台支持方面，草案声称覆盖 **x86-64（Linux/macOS/Windows）**、**ARM64**、**ARM32**、**PPC64/PPC32**、**RISC-V**，但摘录中**没有给出跨平台性能或稳定性实验数据**。
- 整体上，这是一篇**进行中的设计/实现文档**而非完成版论文；最强的具体主张是：在 SBCL 中实现对 GC、安全动态绑定、异常清理、阻塞原语和多核 work-stealing 的透明 fiber 集成。

## Link
- [https://atgreen.github.io/repl-yell/posts/sbcl-fibers/](https://atgreen.github.io/repl-yell/posts/sbcl-fibers/)
