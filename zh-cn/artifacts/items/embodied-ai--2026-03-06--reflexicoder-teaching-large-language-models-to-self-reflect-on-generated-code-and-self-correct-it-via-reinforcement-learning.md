---
source: arxiv
url: http://arxiv.org/abs/2603.05863v1
published_at: '2026-03-06T03:38:17'
authors:
- Juyong Jiang
- Jiasi Shen
- Sunghun Kim
- Kang Min Yoo
- Jeonghoon Kim
- Sungju Kim
topics:
- code-generation
- reinforcement-learning
- self-reflection
- self-correction
- llm-reasoning
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# ReflexiCoder: Teaching Large Language Models to Self-Reflect on Generated Code and Self-Correct It via Reinforcement Learning

## Summary
本文提出 ReflexiCoder，用强化学习把“先写代码、再自我反思、再自我修正”的调试过程直接学进模型参数中，从而在推理时不依赖外部测试器或执行反馈。它面向复杂代码生成任务，主打更强的单次成功率与更低的迭代 token 开销。

## Problem
- 现有代码 LLM 常用单次生成（“System 1”），在复杂算法题上容易第一次写出看似合理但实际错误的代码。
- 现有迭代改进方法通常依赖外部 oracle、执行环境、单元测试或多轮提示交互，导致部署成本高、延迟高、token 消耗大。
- 这很重要，因为真实开发场景里往往没有完善测试集；如果模型不能**内化调试能力**，就难以稳定解决复杂编程任务。

## Approach
- 核心方法是把代码生成建模为一个**结构化轨迹**：`reasoning -> answer -> reflection -> corrected answer`，让模型自己先解题、再检查 bug/优化点、再改正。
- 作者用 **RL-zero** 范式而不是先做传统 SFT，直接用强化学习优化整条“反思-修正”轨迹，目标不是只奖励最终代码对不对，而是奖励“是否会自我发现问题并有效修复”。
- 奖励函数由几部分组成：格式合规奖励、反思轮数惩罚、逐步质量提升奖励、效率奖励；简单说，就是鼓励**少而有效的反思**，惩罚无效循环和冗长推理。
- 训练时使用 reflection-aware GRPO，使模型学会在自己的“内心独白”里完成调试；推理时不需要外部执行器或额外 critic 来驱动修复。

## Results
- 作者声称在 **7 个代码基准**上验证有效，且 **ReflexiCoder-8B** 在 **1.5B-14B 开源模型范围内达到 SOTA**。
- **单次尝试（Single）**成绩：HumanEval **94.51%**，HumanEval+ **87.20%**，MBPP **81.80%**，MBPP+ **78.57%**，BigCodeBench **35.00%**，LiveCodeBench **52.21%**，CodeForces **37.34%**。
- **多轮反思（Multiple）**成绩进一步提升到：HumanEval **95.73%**，BigCodeBench **36.84%**，LiveCodeBench **54.12%**，CodeForces **37.68%**；文中称其可**媲美或超过 GPT-5.1** 的部分指标。
- 与专有模型对比的具体数字中，GPT-5.1 在表中为：HumanEval **95.12%**、HumanEval+ **87.20%**、MBPP **84.00%**、MBPP+ **79.10%**、BigCodeBench **39.56%**、LiveCodeBench **48.03%**、CodeForces **34.70%**；据此 ReflexiCoder 在 **LCB（52.21 vs 48.03）**、**CF（37.34 vs 34.70）** 上单次设置已超过 GPT-5.1，但在 **BCB/MBPP** 等上并非全面领先。
- 效率方面，作者称其比基座模型在迭代模式下**推理 token 开销降低约 40%**，其中**reasoning tokens 减少近 50%**，并且“几乎总是只执行 1 次反思循环”。
- 论文还强调：即使在**与基线相同 token 预算**的单次设置下，性能依然优于基线，说明收益不只是来自“多试几次”，而是来自把调试能力学进模型内部。

## Link
- [http://arxiv.org/abs/2603.05863v1](http://arxiv.org/abs/2603.05863v1)
