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
language_code: en
---

# Real-Time Safe Multi-Threaded DAW Audio in Rust

## Summary
This article discusses how to implement as much "real-time-safe" multithreaded scheduling as possible in Rust for a directed acyclic audio graph in a digital audio workstation (DAW). The core contribution is a comparison of multiple parallelization approaches, leading to the design of a custom thread pool that significantly reduces callback load on consumer hardware and eliminates deadline misses in testing.

## Problem
- A DAW's audio callback must complete within a strict time budget, otherwise a buffer underrun (audio glitch/stutter) occurs; for example, at 44.1 kHz and 512 samples, the budget is about **11.6 ms**.
- The audio thread is typically a high-priority thread that must not block, and it should also avoid locks, heap allocation, I/O, system calls, and code with unpredictable worst-case latency, so common parallel runtimes are not suitable for direct use.
- Although single-threaded traversal of the DAG in topological order is simple and predictable, the total processing workload of large projects can easily exceed the callback budget, so multithreading is needed to reduce the execution upper bound from the "sum of all nodes" to something closer to the "critical path length."

## Approach
- The audio graph is modeled as a DAG: nodes represent processing units, and edges represent dependencies; the single-threaded baseline uses **DFS topological sorting**, with complexity **O(|V|+|E|)**.
- Multithreaded scheduling instead uses the **Kahn algorithm**: maintain the in-degree of each node, and any node whose in-degree drops to 0 can execute immediately; this naturally supports parallelism, with the same complexity **O(|V|+|E|)**.
- The author evaluates four implementations in sequence: Rayon spawning a task per node with `spawn`, Rayon `broadcast` + lock-free queue, a fork-union thread pool, and a custom thread pool; the earlier approaches respectively exposed problems such as races, heap allocation, audio-thread stalls, unacceptable CPU spinning, or engineering unsafety.
- The final custom thread pool uses shared atomic state (such as `epoch`, `active`, and `to_do`) + a work queue + a three-state worker model (idle/spinning/working); the audio thread also participates in execution and uses a "**reserved node**" strategy to reduce queue contention and scheduling overhead.
- The author explicitly notes that this approach is not strictly, formally real-time safe: waking worker threads from the audio thread still involves one system call (`futex_wake` on Linux), but its frequency and the number of threads involved are controlled, and the latency is acceptable in practice.

## Results
- The test project contains **84 processing nodes**, with a graph structure of **5 layers of fan-in: 71 → 7 → 3 → 2 → 1**, for a total of **38,000 measurements**; each node runs a Spectral Compressor, and the workload changes dynamically depending on whether the input is silent.
- Test environment: **Intel Core i7-13700H**, **18 worker threads**, **44.1 kHz** sample rate, **512** buffer size, running **Arch Linux 6.19.6**.
- Compared with the single-threaded version, **the load of both multithreaded implementations is clearly lower across the entire distribution**: the article states that the **P100 load of both multithreaded approaches is lower than the single-threaded P75 load**, and the **P75 load of both is lower than the single-threaded P25 load**.
- In terms of deadline misses: **the single-threaded version had 25 timeouts**, while **both multithreaded implementations had 0 timeouts**.
- Compared with the Rayon `spawn` approach, the custom thread pool shows **a slightly further reduction in load**; however, its variance is slightly larger: the custom thread pool has **σ≈0.0308**, while the Rayon `spawn` approach has **σ≈0.0283**.
- The article does not provide a more complete table of absolute load values, but the strongest quantitative conclusion is that in this test, the custom thread pool preserved low-latency characteristics while achieving more stable performance than the single-threaded version and no deadline misses.

## Link
- [https://edwloef.github.io/posts/real-time-safe-multi-threaded-daw-audio/](https://edwloef.github.io/posts/real-time-safe-multi-threaded-daw-audio/)
