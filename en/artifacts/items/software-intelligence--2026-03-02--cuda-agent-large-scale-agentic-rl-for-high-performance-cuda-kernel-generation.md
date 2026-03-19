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
language_code: en
---

# CUDA Agent: Large-Scale Agentic RL for High-Performance CUDA Kernel Generation

## Summary
This paper proposes CUDA Agent, a large-scale agentic reinforcement learning system for CUDA kernel generation, designed to help models genuinely learn GPU kernel optimization rather than merely perform shallow iterative patching. It targets the high-barrier scenario of high-performance code generation and reports new state-of-the-art results on KernelBench.

## Problem
- CUDA kernel optimization is crucial for modern deep learning, but it depends heavily on hardware expert experience and is difficult to automate and scale.
- Although existing LLM methods can write general-purpose code, they still lag behind compiler-style systems in CUDA kernel generation, indicating that the models lack true low-level optimization ability.
- Existing methods mainly rely on training-free refinement or fixed multi-turn execution-feedback fine-tuning. These mechanisms struggle to fundamentally improve the model's CUDA optimization ability, so the performance gains are limited.

## Approach
- The core idea is to turn CUDA kernel development into an agentic reinforcement learning task with verifiable, measurable rewards, allowing the model to learn in a closed loop of "write code - verify - analyze performance - improve again."
- The authors build a scalable data synthesis pipeline to generate enough CUDA training tasks and trajectories to support large-scale RL training.
- The system provides a skill-augmented CUDA development environment, including automated verification and profiling, thereby producing more reliable reward signals rather than relying only on textual preferences or vague feedback.
- The paper also introduces RL algorithmic techniques needed for stable training, supporting large-scale agentic learning and the gradual development of CUDA kernel optimization expertise.

## Results
- On KernelBench, CUDA Agent achieves **faster rate** improvements over the baseline system mentioned in the paper: Level-1 **+100%**, Level-2 **+100%**, and Level-3 **+92%**.
- On the hardest KernelBench Level-3 setting, CUDA Agent outperforms the strongest proprietary models, **Claude Opus 4.5** and **Gemini 3 Pro**, by about **40%**.
- The paper claims **state-of-the-art** results on KernelBench, suggesting that agentic RL does not merely improve formatting or executability, but significantly enhances CUDA optimization ability.
- The abstract does not provide more fine-grained absolute scores, variance, training scale, or ablation numbers, so the currently confirmable quantitative results are mainly the faster-rate relative improvements above.

## Link
- [https://arxiv.org/abs/2602.24286](https://arxiv.org/abs/2602.24286)
