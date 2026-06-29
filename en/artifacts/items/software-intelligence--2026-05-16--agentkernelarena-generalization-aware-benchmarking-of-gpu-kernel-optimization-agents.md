---
source: arxiv
url: https://arxiv.org/abs/2605.16819v1
published_at: '2026-05-16T05:25:11'
authors:
- Sharareh Younesian
- Wenwen Ouyang
- Sina Rafati
- Mehdi Rezagholizadeh
- Sharon Zhou
- Ji Liu
- Yue Liu
- Yuchen Yang
- Hao Li
- Ziqiong Liu
- Dong Li
- Vikram Appia
- Zhenyu Gu
- Emad Barsoum
topics:
- gpu-kernel-optimization
- coding-agents
- code-intelligence
- benchmarking
- generalization-testing
- software-engineering-agents
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# AgentKernelArena: Generalization-Aware Benchmarking of GPU Kernel Optimization Agents

## Summary
AgentKernelArena is an open-source benchmark for full AI coding agents that optimize GPU kernels, with 196 HIP, Triton, and PyTorch-to-HIP tasks. Its main claim is that agents can often compile correct faster kernels, but PyTorch-to-HIP kernels often fail on unseen shapes because agents hardcode shape assumptions.

## Problem
- GPU kernels affect deep-learning speed and cost, but fast HIP and Triton code requires hardware, compiler, memory, and scheduling knowledge.
- Existing kernel benchmarks mainly score single LLM calls or light prompting, so they miss agent workflows that compile, test, profile, and revise code.
- Prior benchmarks do not test whether kernel optimizations work on input shapes the agent never saw, which matters for real deployment.

## Approach
- The benchmark gives each agent an isolated workspace with source files, commands, optional hardware cheatsheets, and a timeout; the agent can edit code and run shell tools.
- It covers 196 tasks: 24 HIP-to-HIP optimization tasks, 148 Triton-to-Triton optimization tasks, and 24 PyTorch-to-HIP translation tasks.
- Evaluation uses a gated pipeline: compile first, then correctness checks, then performance timing with 10 warmup and 100 timed GPU iterations.
- Speedup is computed as baseline time divided by optimized time; the score gives 20 points for compilation, 100 for correctness, and 100 × speedup for correct kernels.
- The unseen-configuration protocol tests optimized kernels on hidden shapes such as non-power-of-two sizes, scale changes, edge cases, asymmetric shapes, and production-like transformer shapes.

## Results
- On HIP-to-HIP tasks, Claude Code with Opus 4.6 reached 100.0% compilation, 98.6% correctness, 6.69× mean speedup, 3.31× geometric mean speedup, and 50.0% fast₂.
- On Triton-to-Triton tasks, Cursor Agent with Opus 4.7 High led mean speedup at 2.13× with 100.0% compilation, 100.0% correctness, 1.31× geometric mean speedup, and 10.1% fast₂.
- On PyTorch-to-HIP tasks, Cursor Agent with Opus 4.6 High reached the highest mean speedup at 6.89× with 100.0% compilation, 98.6% correctness, 4.49× geometric mean speedup, and 75.0% fast₂.
- Claude Code with Opus 4.6 also performed strongly on PyTorch-to-HIP with 98.6% compilation, 97.2% correctness, 6.70× mean speedup, 4.53× geometric mean speedup, and 79.2% fast₂.
- Triton-to-Triton was the hardest category by speedup: all configurations stayed between 1.59× and 2.13× mean speedup, and fast₂ stayed below 11%.
- The unseen-shape evaluation found that HIP-to-HIP and Triton-to-Triton optimizations usually transfer, while PyTorch-to-HIP has large correctness drops on hidden configurations; the excerpt gives this as a qualitative result without a numeric gap.

## Link
- [https://arxiv.org/abs/2605.16819v1](https://arxiv.org/abs/2605.16819v1)
