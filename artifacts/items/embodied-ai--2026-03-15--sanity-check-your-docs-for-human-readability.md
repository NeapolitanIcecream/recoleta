---
source: hn
url: https://docsalot.dev/tools/docs-human-readability
published_at: '2026-03-15T22:55:03'
authors:
- fazkan
topics:
- documentation-quality
- readability-audit
- developer-documentation
- plain-language
relevance_score: 0.03
run_id: materialize-outputs
---

# Sanity Check Your Docs for Human Readability

## Summary
这是一种针对文档首页的人类可读性审计工具，用七个维度评估文档是否易懂、易扫读且有说服力。它关注开发者文档沟通质量，而非机器人、世界模型或通用策略等研究问题。

## Problem
- 解决的问题是：产品或开发者文档即使信息完整，也可能因为语言晦涩、结构混乱或认知负担过高而让读者难以理解。
- 这很重要，因为文档首页通常决定用户是否能快速明白“这是什么、适合谁、解决什么问题、为什么值得继续读”。
- 提供文本未讨论机器人/具身智能任务，因此与用户给定研究主题关联较弱。

## Approach
- 核心机制很简单：输入文档介绍页 URL，系统对页面做“7 维可读性审计”，并给出详细评分与可执行改进建议。
- 七个维度包括 plain language、clarity of purpose、scannability、information architecture、persuasion & conviction、developer experience、cognitive load。
- 其中部分维度基于可读性规则与标准，例如 Flesch-Kincaid、Hemingway、plain language best practices，用来检查年级阅读水平、句长、术语/jargon、简单词选择等。
- 其余维度更偏内容与结构诊断，如是否说明产品是什么、面向谁、解决什么问题，是否有清晰标题、短段落、导航、示例、快速开始路径等。

## Results
- 文本没有提供实验数据、基准数据集或与其他方法的定量对比结果。
- 给出的最具体结果声明是：工具会在 **7 个维度** 上打分并输出 actionable recommendations。
- 评分权重被明确列出：Plain Language **20 pts**；Clarity of Purpose **15 pts**；Scannability **15 pts**；Information Architecture **15 pts**；Persuasion & Conviction **15 pts**；Developer Experience **10 pts**；Cognitive Load **10 pts**。
- 量化检查项包括阅读年级水平、句长、术语检测，以及基于 **Flesch-Kincaid** 和 **Hemingway** 标准的评估，但没有给出实际性能数值或改进幅度。

## Link
- [https://docsalot.dev/tools/docs-human-readability](https://docsalot.dev/tools/docs-human-readability)
