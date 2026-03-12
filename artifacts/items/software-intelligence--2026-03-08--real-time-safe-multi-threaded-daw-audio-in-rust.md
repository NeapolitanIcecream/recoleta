---
source: hn
url: https://edwloef.github.io/posts/real-time-safe-multi-threaded-daw-audio/
published_at: '2026-03-08T23:08:18'
authors:
- airstrike
topics:
- real-time-audio
- rust
- multithreading
- dag-scheduling
- thread-pool
relevance_score: 0.42
run_id: materialize-outputs
---

# Real-Time Safe Multi-Threaded DAW Audio in Rust

## Summary
本文讨论如何用 Rust 为数字音频工作站（DAW）的有向无环音频图实现尽量“实时安全”的多线程调度。核心贡献是从多种并行方案对比出发，设计了一个自定义线程池，在消费级硬件上显著降低回调负载并消除测试中的 deadline miss。

## Problem
- DAW 的音频回调必须在严格时间预算内完成，否则会发生 buffer underrun（爆音/卡顿）；例如 44.1 kHz、512 samples 时预算约为 **11.6 ms**。
- 音频线程通常是高优先级线程，不能阻塞，也应避免锁、堆分配、I/O、系统调用和最坏时延不可预测的代码，因此常见并行运行时不适合直接使用。
- 单线程按拓扑序遍历 DAG 虽然简单且可预测，但大型工程的总处理量很容易超出回调预算，因此需要多线程把执行上界从“所有节点总和”降到更接近“关键路径长度”。

## Approach
- 将音频图建模为 DAG：节点代表处理单元，边代表依赖；单线程基线使用 **DFS 拓扑排序**，复杂度为 **O(|V|+|E|)**。
- 多线程调度改用 **Kahn 算法**：维护每个节点的入度，谁的入度降到 0 就可立即执行；这样天然支持并行，复杂度同样是 **O(|V|+|E|)**。
- 作者依次评估了 4 种实现：Rayon 按节点 `spawn` 任务、Rayon `broadcast` + 无锁队列、fork-union 线程池、自研线程池；前几者分别暴露出竞态、堆分配、音频线程停等、不可接受 CPU 空转或工程不安全等问题。
- 最终自研线程池使用共享原子状态（如 `epoch`、`active`、`to_do`）+ 工作队列 + 工作者三态（idle/spinning/working）驱动；音频线程也参与执行，并使用“**reserved node**”策略减少队列竞争和调度开销。
- 作者明确指出该方案并非严格形式化的实时安全：音频线程唤醒工作线程仍涉及一次系统调用（Linux 上是 `futex_wake`），但其触发频率和线程数是受控的，实践中延迟可接受。

## Results
- 测试工程包含 **84 个处理节点**，图结构为 **5 层 fan-in：71 → 7 → 3 → 2 → 1**，总计 **38000 次测量**；每个节点运行一个 Spectral Compressor，负载随输入静音情况动态变化。
- 测试环境：**Intel Core i7-13700H**，**18 个 worker 线程**，**44.1 kHz** 采样率，**512** buffer size，系统为 **Arch Linux 6.19.6**。
- 相比单线程，**两种多线程实现的负载在整个分布上都明显下降**：文中称两种多线程方案的 **P100 load 都低于单线程的 P75 load**，且两者的 **P75 load 低于单线程的 P25 load**。
- deadline miss 方面：**单线程出现 25 次超时**，而 **两种多线程实现均为 0 次超时**。
- 自研线程池与 Rayon `spawn` 方案相比，**负载“略有进一步下降”**；但波动稍大：自研线程池 **σ≈0.0308**，Rayon `spawn` 方案 **σ≈0.0283**。
- 文中未给出更完整的绝对 load 数值表，但最强的定量结论是：在该测试中，自研线程池保留低延迟特性的同时，达到了比单线程更稳定且无 deadline miss 的表现。

## Link
- [https://edwloef.github.io/posts/real-time-safe-multi-threaded-daw-audio/](https://edwloef.github.io/posts/real-time-safe-multi-threaded-daw-audio/)
