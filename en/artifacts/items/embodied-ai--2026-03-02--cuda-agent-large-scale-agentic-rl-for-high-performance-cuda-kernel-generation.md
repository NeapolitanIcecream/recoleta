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
language_code: en
---

# CUDA Agent: Large-Scale Agentic RL for High-Performance CUDA Kernel Generation

## Summary
This paper proposes CUDA Agent, which uses large-scale agentic reinforcement learning to teach models to write and optimize GPU kernels more like CUDA experts. Its goal is to fundamentally improve the model's CUDA optimization ability, rather than merely patching surface issues through fixed feedback loops.

## Problem
- CUDA kernel optimization is crucial for modern deep learning, but it usually requires strong expertise in GPU hardware and performance tuning.
- Although existing LLMs are good at general programming, they still lag behind compiler-style systems in CUDA kernel generation; existing methods mostly rely on training-free refinement or fixed multi-turn execution feedback, making it difficult to truly improve intrinsic optimization ability.
- This matters because higher-performance CUDA kernels directly affect deep learning training and inference efficiency, cost, and system throughput.

## Approach
- Proposes **CUDA Agent**: a large-scale agentic RL system that uses reinforcement learning, rather than only prompt-based patching, to continuously train the model to acquire CUDA kernel development skills.
- Builds a scalable data synthesis pipeline to generate large-scale tasks and samples for training CUDA optimization ability.
- Designs a skill-augmented CUDA development environment that includes automated verification and performance profiling to provide reliable reward signals for RL; simply put, it lets the model “write code → run verification → measure performance → learn from the results.”
- Introduces RL algorithmic techniques needed for stable training, enabling the agent to keep improving under real code execution feedback.

## Results
- Achieves new SOTA on **KernelBench**.
- Compared with the compiler-style baseline system mentioned in the paper, it achieves **100% / 100% / 92% faster rate** on **KernelBench Level-1 / Level-2 / Level-3**, respectively.
- On the hardest **Level-3** setting, it surpasses the strongest proprietary models, **Claude Opus 4.5** and **Gemini 3 Pro**, by about **40%**.
- The abstract does not provide more detailed absolute scores, variance, sample scale, or results on additional datasets, but the core quantitative claim is that the method significantly outperforms existing CUDA generation systems and strong proprietary LLMs.

## Link
- [https://arxiv.org/abs/2602.24286](https://arxiv.org/abs/2602.24286)
