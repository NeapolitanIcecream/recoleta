---
source: hn
url: https://onatm.dev/2026/03/14/what-can-change-the-nature-of-an-ai/
published_at: '2026-03-14T22:52:48'
authors:
- onatm
topics:
- llm-prompting
- ai-alignment
- model-behavior
- prompt-engineering
- ai-philosophy
relevance_score: 0.06
run_id: materialize-outputs
language_code: zh-CN
---

# What can change the nature of an AI?

## Summary
这篇文章是一篇观点性随笔，而不是技术研究论文。作者主张：LLM 通过提示词、角色设定或“PERSONALITY.md”改变的只是表面行为，真正的能力与“本性”只能在训练、后训练或微调阶段改变。

## Problem
- 文章试图纠正一种常见误解：把提示词中的人格、角色或语气变化，当成模型“本性”或能力的真实改变。
- 作者认为这种混淆很重要，因为它会夸大当前 AI 的自主性、道德性与职业替代风险。
- 文中还强调，把模仿当成良知，会导致人们错误理解模型在高风险决策中的责任与可靠性。

## Approach
- 核心机制非常简单：作者区分了**上下文驱动的表面行为**和**训练阶段形成的真实参数变化**。
- 文章认为，像 `AGENTS.md`、`PERSONALITY.md`、角色提示这类做法，只是在当前会话里改变输出风格、措辞和脚本。
- 按作者说法，模型的“nature”只能通过训练、后训练或微调改变；提示词不能让模型获得真正的 conscience、reasoning 或 stable personality。
- 作者以编码代理和聊天场景为例，说明所谓“人格”只是临时上下文在数据中心往返传递后的产物，而不是持久内在状态。

## Results
- **没有提供定量实验结果**：文中没有数据集、指标、baseline、ablation 或统计比较。
- 最强的具体主张是：`PERSONALITY.md`、角色设定和类似 prompt engineering **不能改变模型本性**，只能改变几秒钟内的会话表现。
- 作者明确声称：模型的真实变化只会发生在 **training / post-training / fine-tuning** 阶段，而不是普通上下文注入阶段。
- 文章还提出一个规范性结论：当前模型更像“Artificial Artificial Intelligence (AAI)”——即对智能、情感和道德的模仿，而非真正具备这些属性。

## Link
- [https://onatm.dev/2026/03/14/what-can-change-the-nature-of-an-ai/](https://onatm.dev/2026/03/14/what-can-change-the-nature-of-an-ai/)
