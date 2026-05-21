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
论文认为，AI 辅助编码会增加审查负载，因此代码审查需要一种由人类控制的代理式 PR 工作流，而不是孤立的自动化工具。它提出了一个五阶段流程，用于在 PR 创建、增强、审查者选择、审查和回顾之间传递上下文。

## 问题
- AI 编码助手可以将代码产出速度提高 50% 以上，这会增加必须经过 PR 审查的代码量。
- 当前的 AI 审查支持分散在审查者推荐、PR 描述生成和评论建议等狭窄任务中，因此上下文会在阶段之间丢失。
- 审查者仍然面临缺少理由说明、审查者分配不佳、反馈质量不均、隐私风险、偏见、自动化偏差和评估方法薄弱等问题。

## 方法
- 核心机制是一个协调式 PR 工作流，将专门代理分配给不同的审查任务，同时由人类在关键质量关口保留最终控制权。
- 提出的工作流包含五个阶段：PR 创建、PR 增强、审查者选择、AI 辅助代码审查和 PR 回顾。
- 代理会用理由说明、问题链接、摘要、风险信号、审查者建议和审查支持来丰富 PR，使后续阶段能够复用前面阶段的上下文。
- 人类审查者仍然负责判断、问责、团队知识和合并决策。
- 论文还给出了关于可靠性、透明度、隐私、偏见、评估指标以及人类与 AI 权限边界的研究议程。

## 结果
- 论文没有报告针对所提代理式审查工作流的新基准、原型评估、用户研究或受控实验。
- 它的主要具体主张是一个五阶段代理式 PR 流程，目标是连接当前工具分别处理的任务。
- 其动机引用了既有证据：AI 编码助手可将个人编码任务加速 50% 以上，而 AI 生成的贡献比人类编写的贡献需要更多轮审查。
- 背景部分引用了 Fagan 检查法在某些情况下可在测试前发现最多 80% 错误的结果。
- 背景部分引用了 Google 在审查中解决 FindBugs 标记的 1,000 多个问题、75% 的 GitHub 项目要求贡献经过同行审查，以及超过 90% 的被分析 GitHub 项目使用 CI 服务。
- 背景部分引用了 Microsoft 分支研究，其中长期存在的分支平均使集成延迟增加近 9 天。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.17548v1](https://arxiv.org/abs/2605.17548v1)
