---
source: hn
url: https://htmx.org/essays/code-is-cheap/
published_at: '2026-06-06T23:58:45'
authors:
- chr15m
topics:
- ai-code-generation
- code-review
- software-complexity
- llm-tools
- human-ai-interaction
relevance_score: 0.72
run_id: materialize-outputs
language_code: zh-CN
---

# Code Is Cheap(er)

## Summary
## 摘要
这篇文章认为，AI 让代码更便宜地写出来，也把更多成本转移到了阅读、判断和简化代码上。作者的主要建议是，让 LLM 生成的改动保持小规模，并让工程师对阻止不必要的复杂性负责。

## 问题
- AI 编码工具能比开发者理解代码更快地产生大规模改动，所以团队可能合并自己无法解释或维护的行为。
- 这在关键任务软件里最重要，因为生成的代码仍然需要人工审查和负责。
- 便宜的代码会增加系统复杂度；作者认为复杂度增长比系统规模更快，并且会让代码库更难修改。

## 方法
- 把 LLM 输出当作必须在生成后阅读和理解的代码，因为传统的“写代码”过程不再自动带来理解。
- 增量使用 LLM，尤其是在代码库引入新的语义时；大规模生成的变更集主要留给机械性重构。
- 从 3 个方面拒绝把它和编译器输出类比：编译器是确定性的，编译器工作流保留源代码，而编译器输出面向的是机器码这种受限领域，不是通用软件。
- 接受“做减法、加约束的工程师”这个角色：说不、检查输出、简化设计、移除层次，并阻止不必要的代码和系统边界。

## 结果
- 没有提供定量基准、数据集、基线或测量结果。
- 文章声称，由于 AI 工具能快速生成大量质量尚可的代码，过去一年里代码生成成本已经下降。
- 它列出了编译器类比的 3 个具体限制：确定性、源代码保留，以及输出领域受限。
- 它给出 1 条主要操作建议：小步使用 LLM，让审查者能理解每次改动。
- 最明确的具体主张是，失控的 LLM 输出会提高复杂度，让系统更难修改，但文章没有为这一点提供实证测量。

## Problem

## Approach

## Results

## Link
- [https://htmx.org/essays/code-is-cheap/](https://htmx.org/essays/code-is-cheap/)
