---
source: arxiv
url: http://arxiv.org/abs/2604.18616v1
published_at: '2026-04-16T15:49:31'
authors:
- Haohui Mai
- Xiaoyan Guo
- Xiangyun Ding
- Daifeng Li
- Qiuchu Yu
- Chenzhun Guo
- Cong Wang
- Jiacheng Zhao
- Christos Kozyrakis
- Binhang Yuan
topics:
- gpu-kernel-optimization
- agentic-code-generation
- data-flow-invariants
- llm-coding-agents
- static-analysis
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# ARGUS: Agentic GPU Optimization Guided by Data-Flow Invariants

## Summary
Argus is an agentic system for generating high-performance GPU kernels by giving the coding agent compile-time data-flow invariants instead of relying only on pass/fail tests. On AMD MI300X, it reports kernels for GEMM, flash attention, and MoE that match hand-optimized assembly throughput and beat prior agentic systems by large margins.

## Problem
- Existing LLM coding agents can write functionally correct GPU kernels, but their performance is often far below hand-optimized libraries on workloads such as GEMM, attention, and MoE.
- Peak GPU performance depends on many coupled choices at once: tiling, shared-memory staging, software pipelining, instruction scheduling, register use, and data layout transformations. Unit tests do not show which global constraint a kernel violated.
- This matters because these kernels account for most LLM inference time, and even small efficiency gains can cut large GPU costs at deployment scale.

## Approach
- Argus adds **data-flow invariants** to GPU kernel generation. These are compile-time rules that specify how data elements should stay aligned as the kernel tiles, reorders, stages, and computes on them.
- It uses a tile-based Python DSL with **tag functions** and **tag assertions**. Tag functions attach symbolic labels such as logical coordinates to tensor elements. Tag assertions check that the right elements meet at use sites, for example in matrix-core instructions.
- The compiler verifies these invariants at compile time with abstract interpretation over layout algebra plus SMT solving. If a check fails, it returns a concrete counterexample with the thread, data element, and program point. The paper says this adds **zero runtime overhead** because tags exist only in compilation.
- An agentic optimization harness uses an LLM planner plus in-context reinforcement learning to choose optimizations, write invariants, compile, test, profile, and revise the kernel using invariant violations and runtime performance as feedback.

## Results
- On **AMD MI300X**, Argus reports **99–104%** of the effective throughput of state-of-the-art **hand-optimized assembly** for **GEMM, flash attention, and MoE** kernels.
- Against existing **agentic baselines**, it reports **2–1543×** higher geometric-mean throughput across the evaluated workload families.
- For **flash attention**, it reports a **2.4×** speedup over **KernelFalcon**, named as the strongest baseline.
- The evaluated kernel families account for **over 90%** of GPU execution time in LLM inference on the target platform, so the reported gains target major serving bottlenecks.
- On **KernelBench**, Argus reports correct kernels for **100% of Level 1** tasks and **90% of Level 2** tasks.
- The excerpt does not provide deeper per-dataset breakdowns, ablations, or exact baseline numbers for every workload family beyond the headline comparisons above.

## Link
- [http://arxiv.org/abs/2604.18616v1](http://arxiv.org/abs/2604.18616v1)
