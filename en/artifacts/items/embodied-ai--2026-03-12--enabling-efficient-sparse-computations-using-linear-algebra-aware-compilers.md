---
source: hn
url: https://www.osti.gov/biblio/3013883
published_at: '2026-03-12T23:55:07'
authors:
- matt_d
topics:
- sparse-linear-algebra
- mlir
- compiler-framework
- performance-portability
- distributed-memory
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Enabling Efficient Sparse Computations Using Linear Algebra Aware Compilers

## Summary
This work introduces the MLIR-based LAPIS compiler framework for efficiently optimizing sparse linear algebra and enabling performance portability across hardware. Its core contribution is a set of compiler abstractions for linear algebra and distributed sparse tensors, allowing high-productivity code to be mapped more easily to GPUs, distributed-memory systems, and the Kokkos ecosystem.

## Problem
- Sparse linear algebra and graph computation struggle to achieve **high performance, portability, and ease of development** at the same time, because different hardware platforms and storage/communication patterns vary greatly.
- Traditional programming languages and compilation pipelines have difficulty expressing and optimizing sparse operators at the **linear algebra level**, especially for distributed sparse tensors and their communication.
- This matters because applications in scientific computing, SciML, and GraphBLAS/graph analytics all depend on these operators; if they cannot be efficiently ported across architectures, development and deployment costs become high.

## Approach
- Build the **LAPIS** compiler framework on top of **MLIR** so that sparse and dense linear algebra can be optimized at a higher level within a multilevel intermediate representation.
- Introduce the **Kokkos dialect**: it elegantly lowers code from high-productivity languages to different hardware backends, and can also convert lower-level MLIR into **C++ Kokkos** code for easier integration with SciML applications.
- Add a new **partition dialect** for distributed-memory architectures: it is used to represent how sparse tensors are distributed, how communication is performed, and how distributed sparse linear algebra operators are executed.
- Incorporate communication-minimizing algorithmic optimizations into this distributed dialect to reduce distributed execution overhead.
- Use MLIR for **linear algebra-level optimizations** across sparse and dense kernels on different GPUs, as well as applications such as GraphBLAS, TenSQL, and subgraph isomorphism/monomorphism kernels.

## Results
- The text **does not provide specific quantitative metrics**; it does not report explicit speedup percentages, throughput, latency, energy consumption, or numerical comparisons against specific baselines.
- The paper claims that LAPIS achieves four key goals: **productivity, performance, portability, distributed-memory execution**.
- The paper claims that on **different GPUs**, MLIR supports effective optimization of **sparse and dense linear algebra kernels** and delivers performance improvements, but it does not provide specific numbers or baseline names.
- The paper demonstrates successful application of LAPIS in **sparse linear algebra, graph kernels, TenSQL (a database solution based on GraphBLAS), and subgraph isomorphism and monomorphism kernels**, emphasizing **performance portability**.
- Compared with traditional languages/pipelines, the authors' strongest claim is that LAPIS can perform **linear algebra-level optimizations that are difficult to achieve in traditional programming languages**, while also supporting a unified representation of **distributed sparse tensors and communication patterns**.

## Link
- [https://www.osti.gov/biblio/3013883](https://www.osti.gov/biblio/3013883)
