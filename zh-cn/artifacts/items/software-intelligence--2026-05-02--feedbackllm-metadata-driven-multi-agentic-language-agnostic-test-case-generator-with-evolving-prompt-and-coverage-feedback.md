---
source: arxiv
url: https://arxiv.org/abs/2605.01264v1
published_at: '2026-05-02T05:43:29'
authors:
- Kushal Jasti
- Tejamani Prashanth Sahu
- Rishitha Pentyala
- Muvvala Mohit
- Vivek Yelleti
topics:
- llm-test-generation
- code-coverage
- multi-agent-systems
- software-testing
- code-intelligence
- automated-software-engineering
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# FeedbackLLM: Metadata driven Multi-Agentic Language Agnostic Test Case Generator with Evolving prompt and Coverage Feedback

## Summary
## 摘要
FeedbackLLM 通过把未覆盖的行和分支数据反馈到后续 LLM 提示中，为 C 和 Python 自动生成测试输入。论文称，在许多 PALS/RERS C 程序上，它的分支覆盖率高于 KS-LLM，并且在若干具体基准上提升较大。

## 问题
- 手动生成测试用例会占用开发者时间，随机工具或符号工具在处理分支约束和大型状态空间时可能表现不佳。
- 单次提示的 LLM 测试生成可能重复输入、漏掉分支，并生成幻觉测试用例。
- 这个问题重要，因为行覆盖率和分支覆盖率会影响边界情况和逻辑缺陷能否在发布前被执行到。

## 方法
- FeedbackLLM 使用 Gemini-2.5-Flash 代理构成迭代循环，目标综合覆盖率阈值为 90%，最多迭代 10 次。
- Test Case Generator 读取源代码和基线提示，然后输出 JSON 测试输入。
- Line Feedback Agent 读取未命中的行号，并推断可能执行这些行的输入模式。
- Branch Feedback Agent 读取部分覆盖的条件，并建议能翻转 true/false 结果的输入。
- 冗余缓存保存已生成的输入元组，通过集合查找过滤重复项，并把先前输入加入后续提示，使模型避免重复测试用例。

## 结果
- 评估使用了来自 PALS/RERS 的 20 个 C 程序，以及 20 个包含嵌套条件、循环和数学约束的 Python 程序。
- 在 bound 1 的 PS-P1-L-R18-B4 上，FeedbackLLM 报告 100% 分支覆盖率和 100% 行覆盖率；KS-LLM 的分支覆盖率为 46.10%，行覆盖率为 62.97%。
- 在 bound 1 的 PS-P1-L-T-R16-B2 上，FeedbackLLM 报告 93.09% 分支覆盖率和 92.17% 行覆盖率；KS-LLM 的分支覆盖率为 1.79%，行覆盖率为 10.57%。
- 在 bound 1 的 PS-P2-L-R16-B3 上，FeedbackLLM 报告 98.5% 分支覆盖率和 98.17% 行覆盖率；KS-LLM 的分支覆盖率为 13.44%，行覆盖率为 20.44%。
- 在 bound 10 下，PS-P1-L-T-R16-B2 对 FeedbackLLM 报告 94.88% 分支覆盖率和 100% 行覆盖率；KS-LLM 的分支覆盖率为 2.17%，行覆盖率为 10.57%。
- 表中也显示了较弱的案例：在 bound 1 的 Mpals2-B10-cil 上，FeedbackLLM 的分支覆盖率高于 KS-LLM，为 30.00% 对 21.25%，但行覆盖率较低，为 48.57% 对 52.14%。摘录中没有提供总体平均覆盖率。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.01264v1](https://arxiv.org/abs/2605.01264v1)
