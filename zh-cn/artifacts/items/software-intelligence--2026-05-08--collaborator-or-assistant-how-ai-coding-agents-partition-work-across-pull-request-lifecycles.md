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
## 摘要
本文研究了 29,585 个涉及 OpenAI、Copilot、Devin、Cursor 和 Claude Code 的 GitHub 拉取请求，用来衡量谁启动 AI 代理的 PR 工作，以及谁合并这些 PR。论文发现，在一些工具中，代理经常发起工作，但合并权限几乎总是由人类保留。

## 问题
- 当 AI 编码代理创建分支、编写代码并提交 PR 时，团队需要知道人类监督应放在哪些环节。
- 以往研究报告合并率、审查次数或生产率，但没有重建每个 PR 中谁发起、谁审查、谁修改、谁合并。
- 这一点很重要，因为代理主导的编码看起来可能具有自主性，但合并决定仍由人类控制，或只被记录为一次自动化事件。

## 方法
- 作者分析了 AIDev 数据集：原始 PR 为 33,600 个；排除 15 个没有提交的 PR 和 4,000 个没有终态结果的 PR 后，剩余 29,585 个 PR。
- 他们使用 GitHub actor.type 以及 bot、copilot、devin、cursor、codex、openai 和 claude 等登录名模式，将每个参与者分类为 Agent 或 Human；验证结果显示残余错误率为 0.36%。
- 每个 PR 都被映射到若干阶段：创建、审查、修改、合并并关闭，或未合并并关闭。
- 核心机制很简单：识别谁做了第一次提交，识别在发生合并时谁执行了合并，然后把 PR 分配到六种 Initiator × Approver 场景之一。
- 他们计算每个工具的转移概率和中位耗时，然后用卡方检验和 Cramér's V 比较工具与场景之间的关联。

## 结果
- 工具身份可以预测交互模式：chi-square = 29,817，df = 20，p < 0.001；Cramér's V = 0.50。
- Cursor、Devin 和 Copilot 落在 Collaborator 一侧，至少 96% 的 PR 由代理发起；OpenAI 和 Claude 落在 Assistant 一侧，至少 95.6% 的 PR 由人类发起。
- 合并权限仍由人类掌握：Agent-Init + Agent-Approved PR 总数为 14，并且每个工具中都低于 0.1%。
- 审查路由因工具而异：Copilot 将 90.3% 的 PR 送入审查，Cursor 为 51.3%，Devin 为 52.2%；OpenAI 有 76.5% 直接解决，Claude 有 37.6% 直接解决。
- 修改循环在 Collaborator 工具中更常见：Revision-to-Review 返回率为 Copilot 95.5%、Devin 72.3%；审查时间中位数为 Copilot 3.0 小时、Devin 2.0 小时、OpenAI 0.7 小时。
- 关闭时间存在差异：未合并关闭的中位耗时为 Devin 67.8 小时、Copilot 0.2 小时、OpenAI 1.4 小时。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08017v2](https://arxiv.org/abs/2605.08017v2)
