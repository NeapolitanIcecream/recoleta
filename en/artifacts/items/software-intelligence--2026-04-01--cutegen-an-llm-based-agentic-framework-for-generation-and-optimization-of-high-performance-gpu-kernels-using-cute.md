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
language_code: en
---

# CuTeGen: An LLM-Based Agentic Framework for Generation and Optimization of High-Performance GPU Kernels using CuTe

## Summary
CuTeGen is an LLM-based agentic system for writing and tuning GPU kernels in NVIDIA's CuTe layer. It targets iterative kernel improvement with compile, test, debug, and optimize loops instead of one-shot code generation or broad candidate search.

## Problem
- High-performance GPU kernels are hard to write because correctness, tiling, memory movement, instruction choice, and hardware details interact tightly.
- Prior LLM kernel generation often fails on either correctness or performance during iterative edits, especially for kernels that need hardware-specific optimization.
- This matters because matrix multiplication and activation kernels often set end-to-end throughput for modern ML systems.

## Approach
- CuTeGen generates kernels in **CuTe**, a low-level but structured CUDA/C++ abstraction that exposes tiling, layouts, shared memory, and instruction-level control in a form that is easier to refine than raw CUDA.
- The system runs a staged loop: generate a kernel, compile it, execute it on randomized inputs, compare outputs to a PyTorch reference, and feed compiler/runtime/correctness errors back to the model.
- Debugging is split into two steps: diagnosis of the failure, then localized patch edits instead of full kernel rewrites, which helps preserve working and performant code.
- After correctness is reached, CuTeGen applies workload-specific optimization prompts for matmul or activation kernels, usually making one change at a time.
- It adds Nsight Compute profiling feedback later for complex kernels such as matmul, so the model does structural fixes before tuning low-level parameters like tile sizes.

## Results
- Evaluated on **12 matrix multiplication kernels** and **14 activation kernels** from **KernelBench Level-1** on an **NVIDIA RTX 4090** using **GPT-5**, **PyTorch 2.8.0**, and **CUTLASS/CuTe v4.3.0**.
- On activation kernels, CuTeGen reports an average **1.70x speedup** over the PyTorch reference implementations.
- The strongest activation gains in the provided table are **Softsign: 3.45x** and **Swish: 2.45x**; many others are near parity, such as **ReLU: 1.01x**, **Sigmoid: 1.00x**, and **GELU: 1.01x**.
- For matrix multiplication, the paper claims CuTeGen beats the reference implementation that calls **cuBLAS** on **2 benchmark cases**; the provided table shows **Square MatMul: 1.16x** and **MatMul with Diagonal Matrices: 17.66x**.
- Several matmul cases remain below the baseline, including **Standard MatMul: 0.67x**, **Batched MatMul: 0.53x**, **3D Tensor MatMul: 0.43x**, and **Upper-Triangular MatMul: 0.71x**.
- The results support the claim that the framework can produce correct kernels and reach competitive speed on a subset of workloads, with mixed performance across the full benchmark set.

## Link
- [http://arxiv.org/abs/2604.01489v1](http://arxiv.org/abs/2604.01489v1)
