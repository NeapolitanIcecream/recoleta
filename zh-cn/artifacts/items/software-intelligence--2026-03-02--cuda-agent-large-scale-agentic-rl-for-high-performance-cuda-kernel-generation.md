---
source: hn
url: https://arxiv.org/abs/2602.24286
published_at: '2026-03-02T23:55:53'
authors:
- petethomas
topics:
- cuda-kernel-generation
- agentic-rl
- code-optimization
- gpu-programming
- code-intelligence
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# CUDA Agent: Large-Scale Agentic RL for High-Performance CUDA Kernel Generation

## Summary
这篇论文提出 CUDA Agent，一个面向 CUDA 内核生成的大规模 agentic 强化学习系统，用于让模型真正学会 GPU 内核优化而不只是做浅层迭代修补。它面向高性能代码生成这一高门槛场景，并在 KernelBench 上报告了新的最优结果。

## Problem
- CUDA 内核优化对现代深度学习至关重要，但高度依赖硬件专家经验，难以自动化和规模化。
- 现有 LLM 方法虽然能写通用代码，但在 CUDA 内核生成上仍落后于编译器式系统，说明模型缺乏真正的底层优化能力。
- 现有方法主要依赖 training-free refinement 或固定多轮执行反馈微调，这些机制难以从根本上提升模型的 CUDA 优化能力，因此性能增益有限。

## Approach
- 核心方法是把 CUDA 内核开发变成一个可验证、可度量奖励的 agentic 强化学习任务，让模型在“写代码—验证—分析性能—再改进”的闭环中学习。
- 作者构建了可扩展的数据合成流水线，用来生成足够多的 CUDA 训练任务与轨迹，支撑大规模 RL 训练。
- 系统提供技能增强的 CUDA 开发环境，包含自动验证与性能分析，从而给出更可靠的 reward signal，而不是只依赖文本偏好或模糊反馈。
- 论文还引入了稳定训练所需的 RL 算法技术，以支持大规模 agentic 学习并逐步形成 CUDA kernel optimization 专长。

## Results
- 在 KernelBench 上，CUDA Agent 相比文中提到的基线系统实现了 **faster rate** 提升：Level-1 **+100%**、Level-2 **+100%**、Level-3 **+92%**。
- 在最难的 KernelBench Level-3 设置上，CUDA Agent 相比最强专有模型 **Claude Opus 4.5** 和 **Gemini 3 Pro** 约高 **40%**。
- 论文声称达到了 KernelBench 的 **state-of-the-art** 结果，表明 agentic RL 不只是改进格式或可执行性，而是显著提升了 CUDA 优化能力。
- 摘要未给出更多细粒度绝对分数、方差、训练规模或消融数字，因此当前可确认的定量结果主要是上述 faster-rate 相对提升。

## Link
- [https://arxiv.org/abs/2602.24286](https://arxiv.org/abs/2602.24286)
