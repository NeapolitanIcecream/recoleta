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
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# ReflexiCoder: Teaching Large Language Models to Self-Reflect on Generated Code and Self-Correct It via Reinforcement Learning

## Summary
本文提出 ReflexiCoder：一种用强化学习把“先写代码、再自我反思、再自我修正”内化到模型参数中的代码大模型训练框架，从而减少对测试器、执行环境或外部评论器的依赖。它面向复杂算法题上的单次生成瓶颈，主打在推理时自主调试且更省 token。

## Problem
- 现有代码 LLM 常用单次前向生成（"System 1"），在复杂、多步骤算法题上容易生成看起来合理但实际错误的代码。
- 现有迭代修复方法通常依赖外部 oracle、单元测试、执行反馈或多轮高成本 prompting，这在真实开发中常常不可得且延迟高。
- 关键问题是：如何让模型**在没有外部反馈的推理阶段**，也能自己发现 bug、反思并修正代码；这很重要，因为它关系到代码智能体的自治性、部署成本和实际可用性。

## Approach
- 核心方法是把代码生成过程建模成一个**结构化轨迹**：`reasoning -> answer -> reflection -> corrected answer`，并把整条“自我调试轨迹”而不只是第一次答案，用 RL 直接优化到模型权重里。
- 作者采用 **RL-zero** 范式，不先依赖传统 SFT 去教固定反思模板，而是让模型通过奖励自主学会适合自身参数空间的反思-修正模式。
- 奖励函数是组合式的：先要求**格式严格合规**；再奖励**每一轮质量提升**、**最终通过测试**，同时惩罚**过多反思轮数**并额外鼓励**用更少轮数获得更大提升**。
- 与以往 CodeRL/PPOCoder 这类“优化单次生成 + 执行奖励”的做法不同，ReflexiCoder 优化的是“发现问题并修复问题”的轨迹，因此目标是把 debugging 变成模型的内在能力。
- 训练上基于 Qwen3-8B 微调为 ReflexiCoder-8B，策略优化使用 reflection-aware GRPO；推理时可在单次模式下直接作答，也可在带系统提示的多步反思模式下运行。

## Results
- 作者声称 ReflexiCoder-8B 在 **1.5B-14B 开源模型区间**建立新 SOTA；单次设置下达到：**HumanEval 94.51%**、**HumanEval+ 87.20%**、**MBPP 81.80%**、**MBPP+ 78.57%**、**BigCodeBench 35.00%**、**LiveCodeBench 52.21%**、**CodeForces 37.34%**。
- 多轮反思设置下结果进一步提升到：**HumanEval 95.73%**、**BigCodeBench 36.84%**、**LiveCodeBench 54.12%**、**CodeForces 37.68%**；摘要中未给出 MBPP 多轮数值。
- 与专有模型对比，文中明确给出：在 **HumanEval+** 上 ReflexiCoder 为 **87.20%**，与 **GPT-5.1 的 87.20%** 持平；在 **LiveCodeBench** 上 ReflexiCoder **52.21%** 高于 **GPT-5.1 的 48.03%**；在 **CodeForces** 上 ReflexiCoder **37.34%** 高于 **GPT-5.1 的 34.70%**。
- 论文还声称其推理更高效：多轮模式下相较 base model，**推理 token 开销约降低 40%**，其中**reasoning token 近乎减少 50%**。
- 行为层面上，作者称模型表现出高度纪律化的反思模式：**几乎总是恰好执行 1 次 reflection cycle**，意味着其收益并非主要来自无节制的多轮采样，而是来自学到的高效自我修正能力。

## Link
- [http://arxiv.org/abs/2603.05863v1](http://arxiv.org/abs/2603.05863v1)
