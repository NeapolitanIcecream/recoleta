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
language_code: zh-CN
---

# Enabling Efficient Sparse Computations Using Linear Algebra Aware Compilers

## Summary
这篇工作介绍了基于 MLIR 的 LAPIS 编译器框架，用于高效优化稀疏线性代数并实现跨硬件的性能可移植性。其核心贡献是面向线性代数与分布式稀疏张量的编译抽象，使高生产力代码能更容易映射到 GPU、分布式内存系统和 Kokkos 生态。

## Problem
- 稀疏线性代数和图计算很难同时做到**高性能、可移植、易开发**，因为不同硬件和存储/通信模式差异很大。
- 传统编程语言和编译流程难以在**线性代数层面**表达和优化稀疏算子，尤其难处理分布式稀疏张量及其通信。
- 这很重要，因为科学计算、SciML、GraphBLAS/图分析等应用都依赖这些算子；若不能高效移植到不同架构，开发和部署成本会很高。

## Approach
- 构建 **LAPIS** 编译器框架，并建立在 **MLIR** 之上，以便在多级中间表示里对稀疏与稠密线性代数做更高层优化。
- 提出 **Kokkos dialect**：把高生产力语言代码优雅地下沉到不同硬件后端，并能把较低层 MLIR 转成 **C++ Kokkos** 代码，方便与 SciML 应用集成。
- 为分布式内存架构新增 **partition dialect**：用于表示稀疏张量如何分布、如何通信，以及如何执行分布式稀疏线性代数算子。
- 在该分布式方言中加入**最小化通信**的算法优化，以降低分布式执行开销。
- 通过 MLIR 进行**线性代数级优化**，覆盖不同 GPU 上的稀疏与稠密内核，以及 GraphBLAS、TenSQL、子图同构/单态核等应用。

## Results
- 文本**没有提供具体量化指标**，未报告明确的速度提升百分比、吞吐、延迟、能耗或与特定基线的数值对比。
- 论文声称 LAPIS 实现了四个关键目标：**productivity、performance、portability、distributed-memory execution**。
- 论文声称在**不同 GPU**上，MLIR 支持对**稀疏和稠密线性代数内核**进行有效优化，并带来性能提升，但未给出具体数字或基线名称。
- 论文展示了 LAPIS 在**稀疏线性代数、图内核、TenSQL（基于 GraphBLAS 的数据库方案）、子图同构与单态核**中的成功应用，强调了**性能可移植性**。
- 相比传统语言/流程，作者的 strongest claim 是：LAPIS 能进行**传统编程语言中难以实现的线性代数层优化**，并支持**分布式稀疏张量与通信模式**的统一表达。

## Link
- [https://www.osti.gov/biblio/3013883](https://www.osti.gov/biblio/3013883)
