---
source: arxiv
url: https://arxiv.org/abs/2605.18073v1
published_at: '2026-05-18T08:55:30'
authors:
- Anika Tabassum
- Md Sifat Hossain
- Md. Fahim Arefin
- Tariqul Islam
- Tarannum Shaila Zaman
topics:
- code-generation
- autonomous-programming
- multi-model-feedback
- llm-debugging
- competitive-programming
- software-agents
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# A-ProS: Towards Reliable Autonomous Programming Through Multi-Model Feedback

## Summary
## 摘要
A-ProS 是一个自主编程系统，通过将 GPT-4 或 GPT-5 代码生成器与独立的 LLM 调试批评器和在线评测反馈配对，改进竞赛编程解法。在 367 道 ICPC 和 Codeforces 题目上，论文报告在三轮修复后有大幅提升，GPT-5 工作流尤其明显。

## 问题
- 单次生成的 LLM 代码在算法题上常常失败，因为模型不能使用编译器、运行时或评测反馈来修正错误解法。
- 竞赛编程适合作为测试场景，因为每道题都有严格的正确性、时间和内存检查，部分正确或看起来合理的代码也不会得分。
- 以往工作对迭代式代码修复中哪些部分真正有用，只有有限的控制性证据：持续上下文、重复采样，还是单独的批评器模型。

## 方法
- A-ProS 使用 GPT-4 和 GPT-5 作为解法生成器，并使用三个批评器模型提供调试反馈：Codestral-2508、Llama-3.3-70B 和 DeepSeek-R1。
- 该设计测试 6 种工作流，来自生成器和批评器的 2 × 3 组合。
- 每道题先生成一个 C++ 解法，然后在 Codeforces 返回 Accepted、Wrong Answer、Runtime Error 或 Time Limit Exceeded 等判定后，最多允许 3 轮修复。
- 系统在修复轮次之间保留对话历史，这样生成器和批评器可以利用早先的失败结果，而不是每次都从空提示开始。
- 评估覆盖 367 道题目：2011–2024 年 ICPC World Finals 的 167 道题，以及 1200–1800 分段的 200 道 Codeforces 题。

## 结果
- 在 367 题集合上，GPT-5 工作流的初始通过数从 39 提升到三轮修复后的 85–90。
- 在同一集合上，GPT-4 工作流的初始通过数从 15 提升到三轮修复后的 31–38。
- 在 47 道题的配对消融实验中，有状态修复在 Itr3 通过率上比无状态修复高 8.5–10.6 个百分点。
- 与无状态修复相比，有状态修复将重复失败减少了 2.9×–3.5×。
- A-ProS 报告的提升幅度比多轮无状态修复基线高 2.2×–2.3×。
- 消融实验给出的 bootstrap 95% 置信区间为 GPT-5 的 [0.00, +0.15] 和 GPT-4 的 [0.00, +0.11]，GPT-5 的精确 McNemar p 值约为 0.063。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.18073v1](https://arxiv.org/abs/2605.18073v1)
