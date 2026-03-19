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
language_code: en
---

# Real-Time Safe Multi-Threaded DAW Audio in Rust

## Summary
This article discusses how to implement multi-threaded scheduling for a DAW audio graph in Rust in a way that gets as close as possible to real-time safety, so as to avoid audio glitches caused by audio callback overruns. The core contribution is an evolution from a single-threaded approach and Rayon-based solutions to a custom thread pool, along with a demonstration of its advantages under real project workload tests.

## Problem
- The target problem is how to process an audio graph with dependencies within a strict audio callback time budget, while avoiding operations such as blocking, allocation, and lock contention that would break real-time guarantees.
- This matters because once a callback does not finish before the next buffer must be played, a **buffer underrun** occurs, producing audible audio artifacts.
- Single-threaded scheduling is simple and predictable, but large projects can easily exceed the budget; meanwhile, ordinary multithreading libraries often introduce heap allocation, park/wake behavior, locks, or unpredictable latency, making them unsuitable for high-priority audio threads.

## Approach
- The DAW processing flow is first modeled as a **DAG audio graph**: nodes represent processing units, and edges represent dependencies; in the single-threaded case, DFS topological sorting can be used, with complexity **O(|V|+|E|)**.
- To support parallelism, it switches to **Kahn's algorithm**: maintain the in-degree of each node, and any node with in-degree 0 can be processed immediately; after processing, decrement the in-degree of its successors, which makes it naturally suitable for parallel execution, with the same complexity **O(|V|+|E|)**.
- The author successively tried 3 kinds of implementations: using Rayon to `spawn` a task per node, using Rayon `broadcast` plus a lock-free queue to distribute tasks, and fork-union; the former had problems such as races, heap allocation, and parking the audio thread, while the latter had drawbacks such as unsafe code, C++ dependencies, and high power consumption from busy-spinning.
- A **custom thread pool** was ultimately implemented: it shares atomic state such as `audio_graph`, `epoch`, `active`, and `to_do`; worker threads switch among three states—idle, spinning, and working—and the audio thread itself also participates in processing, reducing waiting and scheduling overhead.
- A **reserved node/work-first** optimization is used: each thread preferentially continues directly with one successor node and only places the remaining tasks into the queue, thereby reducing task distribution overhead and queue contention; the scheduler is also abstracted as a reusable `WorkList` trait.

## Results
- The experimental graph contains **84 processing nodes**, structured as **5 layers of fan-in: 71 → 7 → 3 → 2 → 1**; a total of **38,000 measurements** were conducted.
- The test environment was an **Intel Core i7-13700H**, with audio settings of **44.1 kHz** and a **512 samples buffer**, corresponding to a callback budget of about **11.6 ms**; the thread pool used **18 worker threads**.
- Compared with the single-threaded approach, both multithreaded implementations significantly reduced callback load: the author states that the **P100 load of both multithreaded schemes is lower than the P75 load of the single-threaded scheme**, and the **P75 load of both multithreaded schemes is lower than the P25 load of the single-threaded scheme**.
- In terms of deadline behavior, the **single-threaded scheme had 25 missed deadlines**, while **both multithreaded schemes had 0 missed deadlines**.
- In the internal multithreaded comparison, the custom thread pool showed a **slight overall reduction in load** relative to the Rayon `spawn` scheme; however, its variability was slightly larger, with the custom thread pool having a standard deviation of about **σ≈0.0308**, versus about **σ≈0.0283** for the Rayon `spawn` scheme.
- The article does not provide a more complete table of means or quantiles, but the strongest quantitative conclusion is that the custom thread pool eliminated deadline misses under realistic DAW-style workloads and significantly reduced callback load relative to the single-threaded approach.

## Link
- [https://edwloef.github.io/posts/real-time-safe-multi-threaded-daw-audio/](https://edwloef.github.io/posts/real-time-safe-multi-threaded-daw-audio/)
