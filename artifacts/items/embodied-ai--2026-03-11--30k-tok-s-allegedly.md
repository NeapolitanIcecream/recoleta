---
source: hn
url: https://www.percepta.ai/blog/can-llms-be-computers
published_at: '2026-03-11T23:28:16'
authors:
- E-Reverance
topics:
- llm-computation
- transformer-execution
- program-execution
- inference-speed
relevance_score: 0.08
run_id: materialize-outputs
---

# 30k Tok/S (Allegedly)

## Summary
这篇文章探讨是否可以让大语言模型像计算机一样在 Transformer 内部直接执行程序，从而实现更快的推理。核心主张是通过在模型中“执行程序”而不是逐步生成所有中间步骤，可以把某些计算过程的推理速度提升到指数级更快。

## Problem
- 传统 LLM 在执行需要多步计算、算法推理或程序式操作时，通常依赖逐 token 生成中间过程，导致推理慢且成本高。
- 如果模型只能用自然语言链式推理来模拟计算机执行，那么复杂任务的延迟会随步骤数快速增长，限制实际可用性。
- 让 Transformer 直接充当“计算机”很重要，因为这可能显著提升算法型任务的效率，并扩展模型可处理的程序执行能力。

## Approach
- 文章提出的核心方向是：让程序在 Transformer 内部被执行，而不是把每个中间计算步骤都显式输出成 token。
- 用最简单的话说，就是把“逐字写出解题过程”变成“在网络内部完成运算，只输出结果”。
- 作者声称这样可带来指数级更快的推理，意味着对于某些程序/算法类任务，执行时间不再严格受显式中间 token 长度限制。
- 从标题“30k Tok/S (Allegedly)”和副标题可见，工作重点是高吞吐推理与 Transformer 内部程序执行机制，而不是传统文本生成优化。

## Results
- 提供的摘录没有给出可核验的实验表格、数据集、基线模型或详细指标。
- 标题声称可达到 **30k Tok/S**，但同时带有 **“Allegedly”**，说明这是吸引注意的性能说法而非在摘录中完整证明的结果。
- 副标题明确宣称：在 Transformer 内部执行程序可实现 **“exponentially faster inference”**，但摘录中没有给出具体倍率、任务设置或对比基线。
- 基于当前文本，最强的具体主张是：**程序内执行 + 推理速度指数级提升 + 约 30k tok/s 级别吞吐**；但没有足够证据评估其普适性或严谨性。

## Link
- [https://www.percepta.ai/blog/can-llms-be-computers](https://www.percepta.ai/blog/can-llms-be-computers)
