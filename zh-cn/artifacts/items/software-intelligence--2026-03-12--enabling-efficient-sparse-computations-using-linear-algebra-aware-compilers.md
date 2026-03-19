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
language_code: zh-CN
---

# Enabling Efficient Sparse Computations Using Linear Algebra Aware Compilers

## Summary
本文介绍了基于 MLIR 的 LAPIS 编译器框架，用于高效优化稀疏线性代数与图计算，并在不同硬件与分布式内存环境中实现性能可移植性。其核心贡献是面向线性代数的编译抽象，包括 Kokkos dialect 和 partition dialect，以同时提升生产力、性能和跨平台部署能力。

## Problem
- 稀疏线性代数和图计算在 GPU、CPU 及分布式系统上很难同时做到高性能、可移植和易编程。
- 传统编程语言和编译流程难以表达线性代数层面的优化，尤其是稀疏张量分布、通信模式和跨架构代码生成。
- 这很重要，因为科学计算、SciML、GraphBLAS/图分析和数据库内核都依赖高效稀疏计算，而手工为每种架构调优成本很高。

## Approach
- 构建了 LAPIS 编译器框架，底层基于 MLIR，用编译器中间表示显式建模稀疏线性代数操作。
- 提出了 **Kokkos dialect**，可将高生产力语言代码优雅地降级到不同硬件架构，也可把较低层 MLIR 转成 C++ Kokkos 代码。
- 该机制还支持把科学机器学习（SciML）模型更容易集成进现有应用。
- 为分布式内存场景设计了新的 **partition dialect**，用于描述稀疏张量如何分布、如何通信以及如何分布式执行算子。
- 在此基础上加入减少通信的算法级优化，并利用 MLIR 实现线性代数层面的稀疏/稠密内核优化。

## Results
- 项目声称 LAPIS 实现了稀疏线性代数与图内核的**性能可移植性**，覆盖“不同 GPU”以及分布式内存架构，但摘要未给出具体速度提升、吞吐或能效数字。
- 明确展示了 MLIR 可在**线性代数层**进行有效优化，并改善稀疏与稠密线性代数内核在不同 GPU 上的性能；但未提供数据集、基线或百分比增益。
- 支持的代表性应用包括：稀疏线性代数与图内核、基于 GraphBLAS 的关系型数据库 **TenSQL**、以及子图同构/单态匹配内核。
- 对分布式执行，论文声称 partition dialect 能表达通信并通过通信最小化优化提升性能，但提供文本中**没有量化结果**。

## Link
- [https://www.osti.gov/biblio/3013883](https://www.osti.gov/biblio/3013883)
