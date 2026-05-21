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
IssueSpecter 将未覆盖的 Python 代码片段转成带排名的缺陷报告，并包含复现步骤和候选修复。论文称，这有助于在人类提交 issue 之前发现潜在缺陷。

## 问题
- 自动化 issue 修复系统需要先有缺陷报告才能行动，因此未测试代码中的缺陷可能会一直隐藏，直到用户触发它们。
- 覆盖率驱动的测试生成可以到达有缺陷的路径，但生成的断言可能会固化当前的错误行为，从而掩盖缺陷。
- 原始 LLM 缺陷报告可能噪声较多；开发者需要排名、复现步骤和修复建议，才能决定先检查哪些内容。

## 方法
- SlipCover 识别现有单元测试未覆盖的代码片段。
- GPT-5-mini 审查每个未覆盖片段，并生成最多 3 份 issue 报告，包含严重程度、受影响的操作系统、复现步骤和建议代码修复。
- 基于规则的选择步骤按严重程度、操作系统影响和描述长度对报告排序，然后保留每个项目排名前 10 的 issue。
- GPT-5-mini 根据影响、范围和紧急程度对这 10 个 issue 重新排序。
- 系统在建议修复上运行现有测试套件，并降低那些补丁会引入新失败测试的 issue 的排名。

## 结果
- 在来自 CodaMosa 的 13 个活跃 Python 项目上，IssueSpecter 从未覆盖片段生成了 10,467 份 issue 报告。
- 对排名靠前的 130 个 issue 进行人工标注后发现，49 个是有效缺陷（37.7%），61 个需要进一步调查（46.9%），20 个是无效报告（15.4%）；有效或可信的报告合计为 84.6%。
- 标注者在这 130 个手动审查 issue 上的一致率为 80.3%。
- 基于 LLM 的排序在 P@3 上比基于规则的排序高 50%，在 MRR 上高 41%；在 HTTPie 示例中，MRR 从 0.14 提升到 1.00，并将一个 CWE-22 路径遍历 issue 排在首位。
- 与 CoverUp 在每个工具 168 个匹配产物上的对比中，IssueSpecter 报告了更高的缺陷有效率：81.0% 对 76.2%，使用的是相同模型和相同评估数量。
- 已标注的 issue 覆盖了 10 个缺陷分类类别中的 9 个，其中有 43 个逻辑或条件缺陷、39 个输入验证或边界缺陷，以及 4 个安全相关缺陷。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.26118v2](https://arxiv.org/abs/2604.26118v2)
