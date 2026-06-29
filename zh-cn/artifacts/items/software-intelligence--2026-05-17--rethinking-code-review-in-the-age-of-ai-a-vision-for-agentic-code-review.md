---
source: arxiv
url: https://arxiv.org/abs/2605.17548v1
published_at: '2026-05-17T17:04:21'
authors:
- "H\xFCseyin \xD6zg\xFCr Kamal\u0131"
- Erdem Tuna
- Vahid Haratian
- "Eray T\xFCz\xFCn"
topics:
- code-review
- ai-agents
- software-engineering
- human-ai-collaboration
- pull-requests
- llm-code-tools
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Rethinking Code Review in the Age of AI: A Vision for Agentic Code Review

## Summary
## 摘要
论文认为，AI 辅助编码会增加审查负担，因此代码审查需要一种由智能体驱动、由人控制的 PR 工作流，而不是零散的自动化工具。它提出了一个五阶段流程，用来在 PR 创建、增强、审查者选择、审查和复盘之间传递上下文。

## 问题
- AI 编码助手可以把代码产出速度提高 50% 以上，这会增加必须经过 PR 审查的代码量。
- 现有的 AI 审查支持分散在审查者推荐、PR 描述生成和评论建议等窄任务上，导致上下文在各阶段之间丢失。
- 审查者仍然面临缺少设计理由、审查者分配不当、反馈质量不一致、隐私风险、偏见、自动化偏见，以及评估方法薄弱等问题。

## 方法
- 核心机制是一个协调一致的 PR 工作流，不同智能体负责不同的审查任务，而人类在关键质量关口保留最终控制权。
- 提出的工作流包含五个阶段：PR Creation、PR Augmentation、Reviewer Selection、AI-Assisted Code Review 和 PR Retrospective。
- 智能体会为 PR 补充理由、问题链接、摘要、风险信号、审查者建议和审查支持，让后续阶段复用前面的上下文。
- 人类审查者仍然负责判断、问责、团队知识和合并决策。
- 论文还给出了一个研究议程，覆盖可靠性、透明度、隐私、偏见、评估指标，以及人机权限边界。

## 结果
- 论文没有为提出的智能体式审查工作流报告新的基准、原型评估、用户研究或对照实验。
- 它的主要具体主张是一个五阶段的智能体式 PR 流程，用来连接当前工具分别处理的任务。
- 这一动机引用了既有证据：AI 编码助手把单个编码任务的速度提高了 50% 以上，而 AI 生成的贡献比人工编写的贡献需要更多轮审查。
- 背景部分引用了 Fagan 检查在某些情况下能在测试前发现高达 80% 的错误。
- 背景部分还引用了 Google 在审查中解决了 FindBugs 标出的 1,000 多个问题，75% 的 GitHub 项目要求对贡献进行同行评审，以及超过 90% 的被分析 GitHub 项目使用 CI 服务。
- 背景部分引用了 Microsoft 的分支研究，其中长生命周期分支平均让集成延迟了将近 9 天。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.17548v1](https://arxiv.org/abs/2605.17548v1)
