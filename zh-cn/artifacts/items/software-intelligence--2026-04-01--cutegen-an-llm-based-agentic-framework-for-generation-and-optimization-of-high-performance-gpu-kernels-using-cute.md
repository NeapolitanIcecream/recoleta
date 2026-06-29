---
source: arxiv
url: http://arxiv.org/abs/2604.01489v1
published_at: '2026-04-01T23:55:23'
authors:
- Tara Saba
- Anne Ouyang
- Xujie Si
- Fan Long
topics:
- llm-agents
- gpu-kernel-generation
- cute
- code-optimization
- agentic-software-engineering
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# CuTeGen: An LLM-Based Agentic Framework for Generation and Optimization of High-Performance GPU Kernels using CuTe

## Summary
## 摘要
CuTeGen 是一个基于大语言模型的智能体系统，用于在 NVIDIA 的 CuTe 层中编写和调优 GPU kernel。它面向迭代式 kernel 改进，采用编译、测试、调试和优化循环，而不是一次性生成代码或大范围搜索候选实现。

## 问题
- 高性能 GPU kernel 很难编写，因为正确性、分块、内存移动、指令选择和硬件细节彼此紧密耦合。
- 现有的 LLM kernel 生成方法在迭代修改中常常在正确性或性能上出问题，尤其是在需要硬件特定优化的 kernel 上。
- 这很重要，因为矩阵乘法和激活函数 kernel 往往决定现代机器学习系统的端到端吞吐量。

## 方法
- CuTeGen 在 **CuTe** 中生成 kernel。CuTe 是一种底层但结构化的 CUDA/C++ 抽象，暴露了分块、布局、共享内存和指令级控制，比原始 CUDA 更容易迭代修改。
- 系统运行一个分阶段循环：生成 kernel、编译、在随机输入上执行、将输出与 PyTorch 参考结果比较，并把编译器、运行时和正确性错误反馈给模型。
- 调试分成两步：先定位失败原因，再做局部补丁式修改，而不是重写整个 kernel，这有助于保留已经可用且性能较好的代码。
- 在正确性满足后，CuTeGen 会针对 matmul 或 activation kernel 应用特定于工作负载的优化提示，通常一次只改一个点。
- 对于 matmul 这类复杂 kernel，系统会在后期加入 Nsight Compute 的性能分析反馈，让模型先做结构性修正，再调节 tile 大小等底层参数。

## 结果
- 在 **NVIDIA RTX 4090** 上，使用 **GPT-5**、**PyTorch 2.8.0** 和 **CUTLASS/CuTe v4.3.0**，对 **KernelBench Level-1** 中的 **12 个矩阵乘法 kernel** 和 **14 个激活函数 kernel** 进行评估。
- 在激活函数 kernel 上，CuTeGen 报告相对 PyTorch 参考实现的平均速度提升为 **1.70x**。
- 表中激活函数提升最高的是 **Softsign: 3.45x** 和 **Swish: 2.45x**；许多其他项接近持平，例如 **ReLU: 1.01x**、**Sigmoid: 1.00x** 和 **GELU: 1.01x**。
- 对于矩阵乘法，论文称 CuTeGen 在 **2 个基准案例** 上超过了调用 **cuBLAS** 的参考实现；表中显示 **Square MatMul: 1.16x** 和 **MatMul with Diagonal Matrices: 17.66x**。
- 还有几个 matmul 案例低于基线，包括 **Standard MatMul: 0.67x**、**Batched MatMul: 0.53x**、**3D Tensor MatMul: 0.43x** 和 **Upper-Triangular MatMul: 0.71x**。
- 这些结果支持这样一个判断：这个框架可以生成正确的 kernel，并在部分工作负载上达到有竞争力的速度，但在整个基准集上的表现不一致。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.01489v1](http://arxiv.org/abs/2604.01489v1)
