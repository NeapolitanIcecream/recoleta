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
language_code: zh-CN
---

# AgentKernelArena: Generalization-Aware Benchmarking of GPU Kernel Optimization Agents

## Summary
## 摘要
AgentKernelArena 是一个开源基准，用于评估优化 GPU kernel 的完整 AI 编程智能体，包含 196 个 HIP、Triton 和 PyTorch-to-HIP 任务。它的主要结论是，智能体经常能编译出正确且更快的 kernel，但 PyTorch-to-HIP kernel 常在未见过的 shape 上失败，因为智能体会硬编码 shape 假设。

## 问题
- GPU kernel 会影响深度学习的速度和成本，但编写快速的 HIP 和 Triton 代码需要硬件、编译器、内存和调度知识。
- 现有 kernel 基准主要评估单次 LLM 调用或简单提示，因此无法覆盖会编译、测试、分析性能并修改代码的智能体工作流。
- 以往基准不测试 kernel 优化是否适用于智能体从未见过的输入 shape，而这对实际部署很重要。

## 方法
- 该基准为每个智能体提供隔离的工作区，包括源文件、命令、可选硬件速查表和超时限制；智能体可以编辑代码并运行 shell 工具。
- 它覆盖 196 个任务：24 个 HIP-to-HIP 优化任务、148 个 Triton-to-Triton 优化任务和 24 个 PyTorch-to-HIP 翻译任务。
- 评估使用分阶段流水线：先编译，再做正确性检查，然后用 10 次预热和 100 次计时 GPU 迭代测量性能。
- 加速比按基线时间除以优化后时间计算；评分给编译 20 分、正确性 100 分，并给正确 kernel 100 × 加速比的分数。
- 未见配置协议会在隐藏 shape 上测试优化后的 kernel，包括非 2 的幂大小、尺度变化、边界案例、非对称 shape 和类似生产环境的 transformer shape。

## 结果
- 在 HIP-to-HIP 任务上，使用 Opus 4.6 的 Claude Code 达到 100.0% 编译率、98.6% 正确率、6.69× 平均加速比、3.31× 几何平均加速比和 50.0% fast₂。
- 在 Triton-to-Triton 任务上，使用 Opus 4.7 High 的 Cursor Agent 平均加速比最高，为 2.13×，同时有 100.0% 编译率、100.0% 正确率、1.31× 几何平均加速比和 10.1% fast₂。
- 在 PyTorch-to-HIP 任务上，使用 Opus 4.6 High 的 Cursor Agent 达到最高平均加速比 6.89×，同时有 100.0% 编译率、98.6% 正确率、4.49× 几何平均加速比和 75.0% fast₂。
- 使用 Opus 4.6 的 Claude Code 在 PyTorch-to-HIP 上也表现较强，达到 98.6% 编译率、97.2% 正确率、6.70× 平均加速比、4.53× 几何平均加速比和 79.2% fast₂。
- 按加速比看，Triton-to-Triton 是最难的类别：所有配置的平均加速比都在 1.59× 到 2.13× 之间，fast₂ 低于 11%。
- 未见 shape 评估发现，HIP-to-HIP 和 Triton-to-Triton 优化通常可以迁移，而 PyTorch-to-HIP 在隐藏配置上的正确率大幅下降；摘录将此作为定性结果给出，没有提供数值差距。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.16819v1](https://arxiv.org/abs/2605.16819v1)
