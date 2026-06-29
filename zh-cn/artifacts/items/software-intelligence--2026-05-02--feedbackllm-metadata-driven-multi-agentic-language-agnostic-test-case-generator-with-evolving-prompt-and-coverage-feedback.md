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
FeedbackLLM 通过把未覆盖的行和分支信息反馈到后续的 LLM 提示中，自动生成 C 和 Python 的测试输入。论文声称它在许多 PALS/RERS C 程序上的分支覆盖率高于 KS-LLM，并且在一些基准上有明显提升。

## 问题
- 手动生成测试用例会消耗开发者时间，而随机工具和符号执行工具在分支约束和大状态空间下可能表现不佳。
- 一次性 LLM 测试生成容易重复输入、漏掉分支，还会编造测试用例。
- 这个问题很重要，因为行覆盖和分支覆盖决定了发布前是否能运行到边界情况和逻辑缺陷。

## 方法
- FeedbackLLM 使用 Gemini-2.5-Flash 代理，在迭代循环中运行，目标是组合覆盖率达到 90%，最多迭代 10 次。
- Test Case Generator 读取源代码和基础提示，然后输出 JSON 测试输入。
- Line Feedback Agent 读取遗漏的行号，并推断可以执行这些行的输入模式。
- Branch Feedback Agent 读取部分覆盖的条件，并建议能切换 true/false 结果的输入。
- 去重缓存保存生成的输入元组，用集合查找过滤重复项，并把先前输入加入后续提示，避免模型重复生成测试用例。

## 结果
- 评估使用了 20 个来自 PALS/RERS 的 C 程序和 20 个包含嵌套条件、循环和数学约束的 Python 程序。
- 在 PS-P1-L-R18-B4、bound 1 下，FeedbackLLM 的分支覆盖率为 100%，行覆盖率为 100%；KS-LLM 的分支覆盖率为 46.10%，行覆盖率为 62.97%。
- 在 PS-P1-L-T-R16-B2、bound 1 下，FeedbackLLM 的分支覆盖率为 93.09%，行覆盖率为 92.17%；KS-LLM 的分支覆盖率为 1.79%，行覆盖率为 10.57%。
- 在 PS-P2-L-R16-B3、bound 1 下，FeedbackLLM 的分支覆盖率为 98.5%，行覆盖率为 98.17%；KS-LLM 的分支覆盖率为 13.44%，行覆盖率为 20.44%。
- 在 bound 10 下，PS-P1-L-T-R16-B2 的 FeedbackLLM 分支覆盖率为 94.88%，行覆盖率为 100%；KS-LLM 的分支覆盖率为 2.17%，行覆盖率为 10.57%。
- 表中也有较弱的案例：在 Mpals2-B10-cil、bound 1 下，FeedbackLLM 的分支覆盖率高于 KS-LLM，分别为 30.00% 和 21.25%，但行覆盖率更低，分别为 48.57% 和 52.14%。摘录中没有提供汇总平均覆盖率。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.01264v1](https://arxiv.org/abs/2605.01264v1)
