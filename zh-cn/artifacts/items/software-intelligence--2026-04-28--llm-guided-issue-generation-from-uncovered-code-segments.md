---
source: arxiv
url: https://arxiv.org/abs/2604.26118v2
published_at: '2026-04-28T21:10:53'
authors:
- Diany Pressato
- Honghao Tan
- Mariam Elmoazen
- Shin Hwei Tan
topics:
- code-intelligence
- automated-bug-detection
- llm-agents
- software-testing
- issue-generation
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# LLM-Guided Issue Generation from Uncovered Code Segments

## Summary
## 摘要
IssueSpecter 将未覆盖的 Python 代码段转成带优先级的 bug 报告，包含复现步骤和候选修复。论文认为，这有助于在人工提交 issue 之前发现潜在缺陷。

## 问题
- 自动化 issue 修复系统需要先有 bug 报告才能行动，所以未测试代码里的缺陷可能会一直隐藏，直到用户撞上它们。
- 覆盖率驱动的测试生成可以跑到有 bug 的路径，但生成的断言可能把当前错误行为写进去，反而掩盖缺陷。
- 原始的 LLM bug 报告噪声很大；开发者需要排序、复现步骤和修复建议，才能决定先看什么。

## 方法
- SlipCover 找出现有单元测试没有覆盖的代码段。
- GPT-5-mini 逐个查看这些未覆盖代码段，最多生成 3 条 issue 报告，包含严重性、受影响的操作系统、复现步骤和建议的代码修复。
- 基于规则的选择步骤按严重性、操作系统影响和描述长度给报告排序，然后每个项目保留前 10 个 issue。
- GPT-5-mini 再按影响、范围和紧急程度对这 10 个 issue 重排。
- 系统会对候选修复运行现有测试套件，并把那些补丁引入新失败测试的 issue 排名降低。

## 结果
- 在 CodaMosa 的 13 个活跃 Python 项目上，IssueSpecter 从未覆盖代码段生成了 10,467 条 issue 报告。
- 对人工标注的 130 条高排名 issue 的结果显示，49 条是真实 bug（37.7%），61 条需要进一步调查（46.9%），20 条无效报告（15.4%）；真实或可信的报告合计 84.6%。
- 这 130 条人工复核 issue 的标注者一致率为 80.3%。
- 基于 LLM 的排序在 P@3 上比基于规则的排序高 50%，在 MRR 上高 41%；在 HTTPie 示例中，MRR 从 0.14 提升到 1.00，并把一个 CWE-22 路径穿越问题排到了第一位。
- 在每个工具 168 个匹配工件的 CoverUp 对比中，IssueSpecter 报告的 bug 有效率更高：81.0% 对 76.2%，而且使用了相同的模型和评估次数。
- 被标注的 issue 覆盖了 10 个 bug 分类中的 9 类，其中有 43 个逻辑或条件 bug、39 个输入验证或边界 bug，以及 4 个安全相关 bug。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.26118v2](https://arxiv.org/abs/2604.26118v2)
