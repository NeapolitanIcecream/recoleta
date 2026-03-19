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
- real-time-systems
- multi-core-scheduling
- dnn-inference
- code-generation
- wcet-analysis
relevance_score: 0.04
run_id: materialize-outputs
language_code: en
---

# Extension of ACETONE C code generator for multi-core architectures

## Summary
This paper extends ACETONE, advancing it from certifiable DNN C code generation originally targeting single-core systems to predictable parallel code generation for multi-core CPUs. The core contribution is to formulate neural network inference orchestration as a DAG static scheduling problem, and to use an optimized constraint programming/heuristic approach to reduce inference latency while preserving the analyzability required by safety-critical systems.

## Problem
- Deploying deep neural networks in safety-critical systems such as aviation requires not only high performance, but also **predictability, analyzability, and ease of certification**; single-core execution often leads to inference times that are too long to satisfy real-time constraints.
- Aeronautical embedded platforms are transitioning from single-core to multi-core, but may not use dedicated accelerators in the short term, so a parallel inference code generation solution suitable for **multi-core CPUs** is needed.
- Multi-core parallelization is not straightforward: it must handle task partitioning, core mapping, synchronization, and inter-core communication delays, while preserving WCET (Worst-Case Execution Time) analysis capability. This is a capability directly missing from the original ACETONE, which only generated sequential code.

## Approach
- Represent fixed-structure feedforward networks (such as CNNs/MLPs) as a **DAG**: nodes are layers, edges are data dependencies; nodes carry WCET values, edges carry inter-core communication delays, and the goal is to find a shortest-makespan schedule on multi-core platforms that is **static, non-preemptive, and allows node duplication**.
- Propose a more efficient **constraint programming / ILP-style encoding** than the method of Tang et al.: remove complex 4D communication variables, and instead use fewer decision variables and improved constraints to express dependencies, communication, and replication, thereby improving solver scalability.
- Introduce two heuristic schedulers: **ISH** quickly obtains near-optimal solutions through critical-path-first ordering plus idle-slot insertion; **DSH** further attempts to duplicate parent nodes to reduce waiting caused by inter-core communication, usually getting closer to optimal but being slower and requiring more memory.
- At the ACETONE implementation level, extend the code generator to output **bare-metal multi-core parallel C code**, while automatically adding program-to-core mapping and necessary synchronization mechanisms, and use OTAWA for WCET analysis together with measurements to validate predictability.

## Results
- On random DAGs (**20/50/100 nodes, 10% density**), the speedup of both **ISH and DSH increases with the number of cores and then reaches a plateau**; the plateau is determined by the graph’s intrinsic maximum parallelism. The examples and experimental observations reported in the paper indicate that more nodes usually bring greater parallel gains.
- **DSH speedup is always greater than or equal to that of ISH**, consistent with its design goal of being “closer to optimal”; however, its scheduling computation time increases by **1–2 orders of magnitude** as the number of cores grows, reaching **nearly 2 minutes per graph** in the slowest cases, while ISH is clearly faster and more stable.
- For exact solving, the authors’ **improved encoding** **returns at least one solution for all tested configurations** under conditions similar to those used for Tang et al.’s method; by contrast, Tang’s representation failed to return a solution in time under the same conditions with a **1-hour timeout**. When the authors’ method returns a solution, its quality is **at least no worse than** Tang’s result.
- In the ILP/CP solving experiments, speedup on the platform also reaches a plateau after a small number of cores; for the **20- and 50-node** datasets, the plateau value is close to that of DSH, but the **optimized encoding reaches the plateau at about 5 cores**, whereas **DSH reaches it at about 7 cores**, supporting the conclusion that “DSH is near-optimal rather than optimal.”
- The trade-off is that exact solving is very slow: for **50-node graphs**, the average solving time is **no less than 54 minutes**, and the **1-hour** timeout is often triggered; with more cores, **DSH and ILP show similar speedup performance, but the heuristic can be up to 10× faster**.
- The paper abstract also claims that the extended solution is validated through **OTAWA WCET analysis** and **experimentally measured WCET**, but the provided excerpt **does not include specific OTAWA figures or end-to-end parallel code performance numbers on real networks**.

## Link
- [http://arxiv.org/abs/2603.08744v1](http://arxiv.org/abs/2603.08744v1)
