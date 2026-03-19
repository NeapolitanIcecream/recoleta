---
source: hn
url: https://arxiv.org/abs/2602.24286
published_at: '2026-03-02T23:55:53'
authors:
- petethomas
topics:
- agentic-rl
- cuda-kernel-generation
- code-optimization
- llm-agents
- gpu-programming
relevance_score: 0.04
run_id: materialize-outputs
language_code: zh-CN
---

# CUDA Agent: Large-Scale Agentic RL for High-Performance CUDA Kernel Generation

## Summary
这篇论文提出 CUDA Agent，通过大规模 agentic 强化学习让模型学会更像 CUDA 专家一样编写和优化 GPU kernel。其目标是从根本上提升模型的 CUDA 优化能力，而不是只靠固定反馈回路做表面修补。

## Problem
- CUDA kernel 优化对现代深度学习至关重要，但通常需要很强的 GPU 硬件与性能调优专业知识。
- 现有 LLM 虽然擅长一般编程，但在 CUDA kernel 生成上仍落后于编译器式系统；已有方法多依赖 training-free refinement 或固定多轮执行反馈，难以真正提升内在优化能力。
- 这很重要，因为更高性能的 CUDA kernel 会直接影响深度学习训练与推理效率、成本和系统吞吐。

## Approach
- 提出 **CUDA Agent**：一个大规模 agentic RL 系统，用强化学习而不是仅靠提示修补，持续训练模型获得 CUDA kernel 开发技能。
- 构建可扩展的数据合成流水线，生成用于训练 CUDA 优化能力的大规模任务与样本。
- 设计带技能增强的 CUDA 开发环境，包含自动验证与性能 profiling，为 RL 提供可靠奖励信号；简单说，就是让模型“写代码—运行验证—测性能—按结果学”。
- 引入稳定训练所需的 RL 算法技术，使该 agent 能在真实代码执行反馈下持续改进。

## Results
- 在 **KernelBench** 上达到新的 SOTA。
- 相比文中提到的编译器式基线系统，在 **KernelBench Level-1 / Level-2 / Level-3** 上分别实现 **100% / 100% / 92% faster rate**。
- 在最难的 **Level-3** 设置上，超过最强专有模型 **Claude Opus 4.5** 和 **Gemini 3 Pro**，幅度约 **40%**。
- 论文摘要未给出更细的绝对分数、方差、样本规模或更多数据集结果，但核心定量主张是：其方法显著优于现有 CUDA 生成系统与强专有 LLM。

## Link
- [https://arxiv.org/abs/2602.24286](https://arxiv.org/abs/2602.24286)
