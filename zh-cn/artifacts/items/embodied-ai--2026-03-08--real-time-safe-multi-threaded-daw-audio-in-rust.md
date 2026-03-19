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
- thread-pool
- dag-scheduling
relevance_score: 0.01
run_id: materialize-outputs
language_code: zh-CN
---

# Real-Time Safe Multi-Threaded DAW Audio in Rust

## Summary
本文讨论如何在 Rust 中为 DAW 音频图实现尽量接近实时安全的多线程调度，以避免音频回调超时导致爆音。核心贡献是从单线程、Rayon 方案一路演化到自定义线程池，并展示其在实际项目负载测试中的优势。

## Problem
- 目标问题是：在严格的音频回调时间预算内处理有依赖关系的音频图，同时避免阻塞、分配、锁竞争等会破坏实时性的操作。
- 这很重要，因为一旦回调没在下一个 buffer 播放前完成，就会发生 **buffer underrun**，产生可听见的音频故障。
- 单线程调度虽然简单且可预测，但大型工程容易超出预算；普通多线程库又常引入堆分配、停车/唤醒、锁或不可预测延迟，不适合高优先级音频线程。

## Approach
- 先把 DAW 处理流程建模成一个 **DAG 音频图**：节点代表处理单元，边代表依赖；单线程可用 DFS 拓扑排序，复杂度为 **O(|V|+|E|)**。
- 为支持并行，改用 **Kahn 算法**：维护每个节点的入度，任何入度为 0 的节点都可立即处理；处理完后递减其后继入度，因此天然适合并行执行，复杂度同样是 **O(|V|+|E|)**。
- 作者依次尝试了 3 类实现：Rayon 按节点 `spawn` 任务、Rayon `broadcast` + 无锁队列分发任务、以及 fork-union；前者存在竞态、堆分配、音频线程 park 等问题，后者又有不安全代码、C++ 依赖和空转高功耗等缺点。
- 最终实现了一个 **自定义线程池**：共享 `audio_graph`、`epoch`、`active`、`to_do` 等原子状态；工作线程在 idle/spinning/working 三态间切换，音频线程自己也参与处理，减少等待与调度开销。
- 采用 **reserved node/work-first** 优化：每个线程优先直接继续处理一个后继节点，只把其余任务放入队列，从而降低任务分发开销和队列竞争；还把调度器抽象为可复用的 `WorkList` trait。

## Results
- 实验图包含 **84 个处理节点**，结构为 **5 层 fan-in：71 → 7 → 3 → 2 → 1**；共进行了 **38,000 次测量**。
- 测试环境为 **Intel Core i7-13700H**，音频设置 **44.1 kHz**、**512 samples buffer**，对应回调预算约 **11.6 ms**；线程池使用 **18 个 worker threads**。
- 与单线程相比，两种多线程实现都显著降低回调负载：作者称两种多线程方案的 **P100 load 低于单线程的 P75 load**，且两种多线程方案的 **P75 load 低于单线程的 P25 load**。
- 截止期限表现上，**单线程方案有 25 次 missed deadline**，而 **两种多线程方案均为 0 次 missed deadline**。
- 在多线程内部对比中，自定义线程池相较 Rayon `spawn` 方案使负载 **整体略有下降**；但波动略大，自定义线程池的标准差约为 **σ≈0.0308**，Rayon `spawn` 方案约为 **σ≈0.0283**。
- 文中没有给出更完整的平均值/分位数表格，但最强的定量结论是：自定义线程池在实际 DAW 风格负载下消除了 deadline miss，并相对单线程显著降低了回调负载。

## Link
- [https://edwloef.github.io/posts/real-time-safe-multi-threaded-daw-audio/](https://edwloef.github.io/posts/real-time-safe-multi-threaded-daw-audio/)
