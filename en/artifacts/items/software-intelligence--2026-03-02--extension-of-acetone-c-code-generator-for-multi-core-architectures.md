---
source: arxiv
url: http://arxiv.org/abs/2603.08744v1
published_at: '2026-03-02T13:53:59'
authors:
- "Yanis A\xEFt-A\xEFssa"
- Thomas Carle
- Sergei Chichin
- Benjamin Lesage
- Claire Pagetti
topics:
- code-generation
- multi-core-scheduling
- real-time-systems
- dnn-inference
- constraint-programming
relevance_score: 0.71
run_id: materialize-outputs
language_code: en
---

# Extension of ACETONE C code generator for multi-core architectures

## Summary
This paper extends ACETONE, advancing its original certifiable DNN inference C code generation for single-core systems to predictable parallel execution on multi-core CPUs. The core idea is to model network inference as a DAG scheduling problem in an offline phase, then use constraint programming or heuristic methods to generate parallel code with synchronization.

## Problem
- Target problem: In safety-critical systems such as aviation, how can a trained DNN run faster on **multi-core CPUs** while still preserving code properties such as **predictability, analyzable WCET, and ease of certification**.
- Importance: Single-core execution causes inference time to grow rapidly and may violate real-time constraints; meanwhile, in the short term, aviation scenarios are not well suited to rely on dedicated accelerators, so multi-core CPUs are a practical and deployable path.
- Difficulties: Multi-core parallelism must not only determine how tasks are partitioned and mapped to cores, but also handle synchronization, communication delays, static scheduling, non-preemptive execution, and certification-friendly code generation constraints.

## Approach
- Each DNN layer is treated as a task, and the whole network is represented as a **DAG**: nodes carry the WCET of each layer, and edges carry inter-core communication delays; the goal is to minimize the total completion time (**makespan**) on a fixed number of cores.
- A **static offline schedule** is used: tasks are non-preemptive and can start only after all predecessors have finished and data is available; task replication across multiple cores is allowed to reduce communication overhead, but redundant replication is limited.
- The paper proposes a more efficient **constraint programming / ILP-style encoding revision** than Tang et al.: it removes the original complex 4D communication-variable tensor and instead uses fewer decision variables and improved constraints to represent communication and replication, thereby improving scalability.
- Two heuristics are also implemented: **ISH** uses critical-path-priority list scheduling and inserts tasks into idle gaps; **DSH** further attempts to replicate parent tasks to reduce inter-core waiting, and is usually closer to optimal but slower and more memory-intensive.
- At the code-generation level, the authors extend ACETONE so it can generate **multi-core parallel C code** from offline scheduling results, adding core mapping and synchronization mechanisms in a bare-metal environment.

## Results
- Evaluation on randomly generated **20 / 50 / 100-node DAG** datasets with **10% density** shows that as the number of cores increases from **2 to 20**, the **speedup** of both ISH and DSH first rises and then reaches a plateau; the plateau is determined by the graph's maximum parallelism.
- Heuristic comparison: **DSH speedup is always higher than or equal to ISH**, indicating it is closer to optimal; however, **DSH computation time increases by 1–2 orders of magnitude as the number of cores grows**, reaching **nearly 2 minutes per graph** in the reported experiments, while ISH is faster and more stable.
- Exact-solver comparison: under the same conditions, **Tang et al.'s formulation cannot find a solution within the 1-hour timeout**; the authors' optimized encoding, by contrast, returns at least one solution under **all tested configurations**, and the returned solutions are **no worse than** Tang's method.
- The runtime cost of the optimized ILP/CP encoding remains very high: on **50-node** graphs, the average solving time is **never below 54 minutes**, and a **1-hour timeout** is often triggered; therefore it is better suited to smaller graphs or use as a high-quality optimizer.
- In terms of solution quality, the speedup plateau obtained by the optimized encoding is close to DSH, but it usually **reaches the plateau at around 5 cores**, whereas DSH needs about **7 cores**, supporting the conclusion that **DSH is near-optimal, while the solver is closer to optimal**.
- Regarding real deployment results, the abstract explicitly states that the multi-core extension has been validated through **OTAWA WCET analysis** and **experimentally measured WCET**, but the provided excerpt **does not include specific real-machine WCET values**.

## Link
- [http://arxiv.org/abs/2603.08744v1](http://arxiv.org/abs/2603.08744v1)
