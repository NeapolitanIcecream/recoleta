---
source: hn
url: https://www.osti.gov/biblio/3013883
published_at: '2026-03-12T23:55:07'
authors:
- matt_d
topics:
- mlir
- sparse-linear-algebra
- compiler-framework
- performance-portability
- distributed-memory
- graph-kernels
relevance_score: 0.31
run_id: materialize-outputs
language_code: en
---

# Enabling Efficient Sparse Computations Using Linear Algebra Aware Compilers

## Summary
This article introduces the MLIR-based LAPIS compiler framework for efficiently optimizing sparse linear algebra and graph computations, while achieving performance portability across different hardware and distributed-memory environments. Its core contributions are linear-algebra-oriented compiler abstractions, including the Kokkos dialect and partition dialect, to simultaneously improve productivity, performance, and cross-platform deployment.

## Problem
- Sparse linear algebra and graph computations are difficult to make simultaneously high-performance, portable, and easy to program across GPUs, CPUs, and distributed systems.
- Traditional programming languages and compilation workflows struggle to express linear-algebra-level optimizations, especially for sparse tensor distribution, communication patterns, and cross-architecture code generation.
- This matters because scientific computing, SciML, GraphBLAS/graph analytics, and database kernels all depend on efficient sparse computation, while manually tuning for each architecture is costly.

## Approach
- The LAPIS compiler framework was built on top of MLIR, using compiler intermediate representations to explicitly model sparse linear algebra operations.
- It introduces the **Kokkos dialect**, which can elegantly lower code from high-productivity languages to different hardware architectures, and can also convert lower-level MLIR into C++ Kokkos code.
- This mechanism also makes it easier to integrate scientific machine learning (SciML) models into existing applications.
- A new **partition dialect** was designed for distributed-memory settings to describe how sparse tensors are distributed, how communication is performed, and how operators are executed in distributed fashion.
- On top of this, the framework adds algorithm-level communication-reduction optimizations and uses MLIR to realize sparse/dense kernel optimizations at the linear algebra level.

## Results
- The project claims that LAPIS achieves **performance portability** for sparse linear algebra and graph kernels, covering “different GPUs” and distributed-memory architectures, but the abstract does not provide specific speedup, throughput, or energy-efficiency numbers.
- It explicitly demonstrates that MLIR can perform effective optimization at the **linear algebra level** and improve the performance of sparse and dense linear algebra kernels across different GPUs; however, no datasets, baselines, or percentage gains are provided.
- Representative supported applications include sparse linear algebra and graph kernels, the GraphBLAS-based relational database **TenSQL**, and subgraph isomorphism/monomorphism kernels.
- For distributed execution, the paper claims that the partition dialect can express communication and improve performance through communication-minimizing optimizations, but the provided text contains **no quantitative results**.

## Link
- [https://www.osti.gov/biblio/3013883](https://www.osti.gov/biblio/3013883)
