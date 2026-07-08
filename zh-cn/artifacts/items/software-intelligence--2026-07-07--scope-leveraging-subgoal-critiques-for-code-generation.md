---
source: arxiv
url: https://arxiv.org/abs/2607.05810v1
published_at: '2026-07-07T04:09:41'
authors:
- Yueke Zhang
- Yifan Zhang
- Zihan Fang
- Kevin Leach
- Wei Zhang
- Yu Huang
topics:
- code-generation
- code-intelligence
- llm-feedback
- program-repair
- formal-methods
- software-agents
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# SCOPE: Leveraging Subgoal Critiques for Code Generation

## Summary
## 摘要
SCOPE 通过使用一个经过证明器训练的评论器，在编码器修改程序之前明确缺失的语义要求，从而改进代码生成。在 LiveCodeBench V6 和 BigCodeBench Hard 上，它的 pass@1 高于仅编码器、Self-Refine 和 Reflexion 基线。

## 问题
- LLM 生成的代码可能看起来正确，但遗漏提示词中的约束，例如边界情况、不变量、API 限制或输入规则。
- 测试反馈通常只说明程序失败，但可能不会指出代码违反了哪项语义义务。
- 这会影响开发者，因为开发者无法为开放式编码任务编写穷尽测试，而薄弱的反馈可能导致模型进行大范围修改，却没有修复真正的 bug。

## 方法
- SCOPE 使用两个模型：冻结的 Qwen3-Coder-30B 编码器，以及一个从 DeepSeek-Prover-V2-7B 初始化的评论器。
- 评论器读取问题和代码草稿，然后输出三个可解析字段：子目标、差距分析和稳健性检查清单。
- 监督微调使用 528 个由评论引导的元组来训练评论器，这些元组来自 LiveCodeBench V1-V3，并使用 DeepSeek-V3 生成教师评论。
- 强化学习使用 GRPO，并包含两种奖励：一种针对评论质量和语义对齐的密集奖励，一种基于评论是否在编码器修改草稿后提高执行分数的稀疏奖励。
- 推理时，编码器先写出初始解法，评论器识别缺失的义务，然后编码器根据该评论修改解法。

## 结果
- 在 LiveCodeBench V6 上，SCOPE 达到 39.4% pass@1，相比之下 Reflexion 为 36.6%，Self-Refine 为 33.1%，仅编码器生成为 20.6%。
- 在 BigCodeBench Hard 上，SCOPE 达到 42.6% pass@1，相比之下 Reflexion 为 36.5%，仅编码器生成为 34.5%。
- 论文报告称，SCOPE 挽救了 19 个失败解法，Reflexion 为 16 个。
- 在由 bug 触发的定位上，SCOPE 在 20 行以内的局部胜出率为 42.1%，Reflexion 为 31.3%。
- SCOPE 的修复规模更小，修改行数中位数为 28.0，Reflexion 为 35.0。
- 报告中的收益在具有具体语义约束的任务上最强；在这些任务中，显式子目标可以把编码器指向某个具体的缺失条件。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.05810v1](https://arxiv.org/abs/2607.05810v1)
