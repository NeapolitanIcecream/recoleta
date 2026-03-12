---
source: hf_daily
url: https://huggingface.co/papers/2603.07169
published_at: null
authors: []
topics:
- cuda-optimization
- multi-agent-systems
- llm-for-code
- gpu-kernels
- scientific-computing
relevance_score: 0.88
run_id: fa4f5d9d-bee2-47ee-b80f-c690622f57d0
---

# Making LLMs Optimize Multi-Scenario CUDA Kernels Like Experts

## Summary
**TL;DR:** 该论文提出了一个面向多场景 CUDA 内核自动优化的通用系统，通过多智能体协作、硬件感知和自动化编译执行链路，让 LLM 在科学计算与机器学习等不同任务上都能像专家一样优化 GPU kernel，并在多数算子上显著提速。

**Problem:**
- 手工优化 GPU kernel 难度高、耗时长，严重依赖专家经验，限制了高性能代码生产效率。
- 现有基于 LLM 的自动优化方法主要聚焦于机器学习场景（如 PyTorch 算子），对稀疏矩阵、科学计算等更广泛应用覆盖不足。
- 缺少面向“多场景 + 多精度”的系统化评测基准，导致方法难以验证其通用性与实际价值。

**Approach:**
- 提出 **MSKernelBench**，覆盖基础代数运算、常见 LLM kernels、稀疏矩阵算子和科学计算例程，并同时支持 **FP32** 与 **BF16**。
- 提出 **CUDAMaster**，一个用于 CUDA kernel 优化的**多智能体**、**硬件感知**系统。
- 系统利用**profiling 信息**指导优化决策，而不是仅靠静态代码改写。
- 自动构建完整的**编译与执行 toolchain**，把代码生成、编译、运行和性能反馈连成闭环。
- 目标是让 LLM 驱动的优化从单一 ML 场景扩展到更通用的高性能计算场景。

**Results:**
- 在**多数算子**上，CUDAMaster 实现了显著加速；摘要未给出所有任务的逐项指标。
- 相比基线方法 **Astra**，CUDAMaster **约提升 35%**。
- 在若干案例中，其性能可**达到或超过**高度优化的闭源库，如 **cuBLAS**。
- 论文同时发布了 **MSKernelBench** 作为多场景评测基准，覆盖基础代数、LLM kernels、稀疏算子和科学计算，并支持 **FP32/BF16**。
- 提供了在线 demo 展示原始代码与优化后代码，但当前摘录中**没有更细粒度的量化结果**（如具体数据集/每个算子的绝对速度）。

## Links
- Canonical: https://huggingface.co/papers/2603.07169
