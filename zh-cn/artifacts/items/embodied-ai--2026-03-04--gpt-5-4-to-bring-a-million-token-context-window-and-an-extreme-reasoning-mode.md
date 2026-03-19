---
source: hn
url: https://the-decoder.com/gpt-5-4-reportedly-brings-a-million-token-context-window-and-an-extreme-reasoning-mode/
published_at: '2026-03-04T22:52:08'
authors:
- jwilliams
topics:
- llm
- long-context
- reasoning
- ai-agents
- model-release
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# GPT-5.4 to bring a million-token context window and an extreme reasoning mode

## Summary
这是一则关于 OpenAI GPT-5.4 的媒体爆料，而非正式论文。其核心卖点据称是 **100 万 token 上下文窗口** 与一种面向高难任务的 **extreme reasoning mode**，目标是提升长程任务中的可靠性。

## Problem
- 要解决的问题是：现有模型在**超长上下文**与**持续数小时的复杂任务**中，容易出错、丢失关键信息或推理不稳定。
- 这很重要，因为编程代理等系统需要在长时间、多步骤流程里保持一致性与正确性；上下文和推理能力不足会直接限制实用性。
- 报道还隐含了一个产品问题：在竞争对手已提供超长上下文的情况下，OpenAI 需要缩小能力差距并改善用户预期管理。

## Approach
- 报道称 GPT-5.4 将把上下文窗口扩大到 **1,000,000 tokens**，使模型能一次处理更长的文档、对话或任务轨迹。
- 新增 **“extreme” thinking mode**：在难题上分配更多计算资源，以换取更强的推理稳定性，而不是优先追求响应速度。
- 该模式主要面向研究人员或高复杂度使用场景，而非只需要快速答案的日常用户。
- 整体机制可用最简单的话概括为：**让模型“看得更多”，并在必要时“想得更久”**，从而减少长任务中的错误。

## Results
- 报道声称上下文窗口将达到 **1,000,000 tokens**，相比当前 GPT-5.2 的 **400,000 tokens** 提升 **2.5 倍**。
- 文中称这将使 OpenAI 在上下文长度上与 **Google** 和 **Anthropic** 处于同一量级，但未给出正式基准测试或任务分数。
- 报道称 GPT-5.4 在**持续数小时的长任务**上会“更可靠、犯错更少”，并特别提到对 **Codex** 这类编程代理更重要；但没有提供具体误差率、成功率或对比实验数字。
- 没有论文式定量结果、数据集、评测协议或基线模型细节，因此所谓“突破性结果”目前主要是**能力声明与规格传闻**，而非可验证实验结论。

## Link
- [https://the-decoder.com/gpt-5-4-reportedly-brings-a-million-token-context-window-and-an-extreme-reasoning-mode/](https://the-decoder.com/gpt-5-4-reportedly-brings-a-million-token-context-window-and-an-extreme-reasoning-mode/)
