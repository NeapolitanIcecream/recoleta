---
source: arxiv
url: https://arxiv.org/abs/2605.21537v1
published_at: '2026-05-20T05:00:31'
authors:
- Gokul Chandra Purnachandra Reddy
- Aditya Lolla
- Harsha Sanku
topics:
- llm-code-modernization
- self-review
- behavioral-equivalence
- code-intelligence
- software-testing
relevance_score: 0.87
run_id: materialize-outputs
language_code: zh-CN
---

# Articulate but Wrong: Self-Review Failures in LLM-Based Code Modernization

## Summary
## 摘要
论文发现，LLM 在将 Python 2 代码现代化为 Python 3 时，经常改变原有行为，而同一个模型的自我审查会漏掉很多这类失败。它的主要实践结论是，生产级现代化流程需要外部行为检查，不能只靠模型自我确认。

## 问题
- LLM 代理可以生成能运行、看起来也合理的代码，但会改变遗留程序的可观察行为。
- 这很重要，因为迁移后即使编译检查和基础测试通过，下游调用方拿到的值或类型也可能不同。
- 论文检验的是，写出迁移后代码的模型能否发现自己输出中的行为变化。

## 方法
- 作者构建了一个 60 个片段的 Python 2 语料库：20 个语义陷阱、20 个语法陷阱、20 个不需要真正现代化的良性对照。
- 他们在 11 个生产级 LLM、7 个模型家族和 3 种提示表述上，以 temperature 0 运行了 1,980 次现代化调用。
- 一个类型严格的行为 oracle 将每个候选结果与 Python 2 合约进行比较，包括值和返回类型，因此 int 到 float 的漂移也会被计入。
- 生成后，同一个模型会审查遗留片段和它生成的候选输出，并回答行为是否保持不变。

## 结果
- 在每个类别 660 次调用中，语义陷阱的漂移率为 39.7%，良性对照为 7.0%，语法陷阱为 12.7%。
- 数值语义陷阱是主要失败类型，漂移率为 57%；惰性求值陷阱的漂移率为 21%；类型模型和字面量语法陷阱接近基线。
- 模型对哪些片段难达成一致：55 对模型组合的平均两两 Pearson r=0.52，而且有一组核心数值片段在每种提示下都让至少 11 个模型中的 8 个失败。
- 同一个模型的自我审查会认可 262 个语义漂移案例中的 83 个，即 31.7%；在数值漂移上，它漏掉了 207 个案例中的 75 个，即 36%。
- 各模型的自我漏检率从 5 个模型上的 0% 到 1 个模型上的 100% 不等；语义漂移率在摘要中为 5.6% 到 46.7%，在按模型的表格中最高到 65.0%。
- 方法选择会改变测得的比率：宽松相等判断会把语义漂移从 39.7% 降到约 26.7%，而只用 fence 的解析器会把良性对照漂移从 7.0% 提高到约 23%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.21537v1](https://arxiv.org/abs/2605.21537v1)
