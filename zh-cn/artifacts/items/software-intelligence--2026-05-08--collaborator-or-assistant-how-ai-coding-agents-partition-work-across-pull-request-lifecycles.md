---
source: arxiv
url: https://arxiv.org/abs/2605.08017v2
published_at: '2026-05-08T17:06:54'
authors:
- Young Jo
- Chung
- Safwat Hassan
topics:
- ai-coding-agents
- pull-request-workflows
- code-review
- software-governance
- human-ai-interaction
- empirical-software-engineering
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Collaborator or Assistant? How AI Coding Agents Partition Work Across Pull Request Lifecycles

## Summary
## 总结
本文研究了 29,585 个 GitHub pull request，涉及 OpenAI、Copilot、Devin、Cursor 和 Claude Code，用来衡量是谁开始 AI 代理的 PR 工作，以及是谁完成合并。结果显示，在一些工具里，代理会先发起工作，但合并权限几乎总是由人保留。

## 问题
- 团队需要知道，当 AI 编码代理创建分支、编写代码并提交 PR 时，人类监督应该放在哪里。
- 以往研究报告的是合并率、评审次数或生产力，但没有还原每个 PR 中是谁发起、评审、修改和合并。
- 这很重要，因为由代理主导的编码看起来可能像是自主完成的，但合并决定仍由人控制，或者只被记录成一次自动化事件。

## 方法
- 作者分析了 AIDev 数据集：原始共有 33,600 个 PR；剔除 15 个没有提交记录的 PR 和 4,000 个没有终态结果的 PR 后，保留 29,585 个。
- 他们结合 GitHub 的 actor.type 和登录名模式，将每个参与者分类为 Agent 或 Human，这些模式包括 bot、copilot、devin、cursor、codex、openai 和 claude；验证结果显示残余错误率为 0.36%。
- 每个 PR 都被映射到这些阶段：created、review、revision、merged and closed，或 unmerged and closed。
- 核心机制很直接：先识别首个提交是谁做的，再识别如果发生合并时是谁执行了合并，然后把 PR 归入六种 Initiator × Approver 场景之一。
- 他们计算了每个工具的转移概率和中位时间，再用卡方检验和 Cramér's V 比较工具与场景的关联。

## 结果
- 工具身份可以预测交互模式：chi-square = 29,817，df = 20，p < 0.001；Cramér's V = 0.50。
- Cursor、Devin 和 Copilot 更接近 Collaborator 一侧，至少 96% 的 PR 由代理发起；OpenAI 和 Claude 更接近 Assistant 一侧，至少 95.6% 的 PR 由人发起。
- 合并权限仍由人掌握：Agent-Init + Agent-Approved 的 PR 总数为 14，且每个工具都低于 0.1%。
- 不同工具的评审路径不同：Copilot 有 90.3% 的 PR 进入评审，Cursor 为 51.3%，Devin 为 52.2%；OpenAI 有 76.5% 直接结束，Claude 有 37.6% 直接结束。
- 修改循环在 Collaborator 工具中更常见：Revision-to-Review 的返回率在 Copilot 中为 95.5%，在 Devin 中为 72.3%；评审中位时间在 Copilot 中为 3.0 小时，在 Devin 中为 2.0 小时，在 OpenAI 中为 0.7 小时。
- 关闭时间也不同：未合并关闭的中位时间在 Devin 中为 67.8 小时，在 Copilot 中为 0.2 小时，在 OpenAI 中为 1.4 小时。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08017v2](https://arxiv.org/abs/2605.08017v2)
