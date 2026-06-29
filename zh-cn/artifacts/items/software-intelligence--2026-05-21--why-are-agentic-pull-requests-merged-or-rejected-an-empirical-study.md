---
source: arxiv
url: https://arxiv.org/abs/2605.22534v1
published_at: '2026-05-21T14:24:20'
authors:
- Sien Reeve O. Peralta
- Fumika Hoshi
- Hironori Washizaki
- Naoyasu Ubayashi
- Inase Kondo
- Yoshiki Higo
- Hiroki Mukai
- Norihiro Yoshida
- Kazuki Kusama
- Hidetake Tanaka
- Youmei Fan
topics:
- agentic-pull-requests
- code-review
- ai-coding-agents
- human-ai-collaboration
- software-engineering-metrics
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Why Are Agentic Pull Requests Merged or Rejected? An Empirical Study

## Summary
## 摘要
本文发现，合并和拒绝标签会误判 AI 编码代理，因为 PR 决策往往取决于审查评论、CI 结果、提交记录和仓库流程。作者分析了 11,048 个已关闭的 agentic pull request，并手工编码了 717 个案例，把代理失败和流程影响、人为帮助分开。

## 问题
- Agentic PR 常按合并或拒绝状态来评估，但这个结果会把有缺陷的代码、重复工作、被后续改动取代的变更、无声关闭和项目规则混在一起。
- 这很重要，因为只看合并率会夸大被拒 PR 中的代理错误，也会夸大已合并 PR 中的自治程度。
- 更好的评估需要查看审查记录：评论、CI 状态、提交历史、关闭上下文和审查者修改。

## 方法
- 研究从 AIDev 数据集出发，保留至少有 500 个 stars 的仓库中的已关闭 Agentic-PR，得到 11,048 个 PR。
- 去掉只有机器人参与审查的案例后，精炼数据集包含 9,799 个有人类审查的 PR：6,179 个已合并，3,620 个被拒绝。
- 作者手工检查了一个分层样本，共 717 个 PR：353 个被拒绝，364 个已合并，并在不同代理和仓库之间保持平衡。
- 被拒绝的 PR 编码为代理失败、非代理失败或未知。已合并的 PR 编码为反馈循环、人类介入、无反馈循环或未知。
- 每个 PR 由两名标注者编码。报告的一致性为：拒绝原因的 Cohen’s κ≈0.90，已合并 PR 交互模式的 κ=1.0。

## 结果
- 在 353 个被拒绝的 PR 中，只有 126 个是明确的代理失败，占 35.7%。非代理原因有 110 个，占 31.2%；未知原因有 117 个，占 33.1%。
- Devin 的被拒 PR 中，37/153 属于代理失败，占 24.2%；OpenAI Codex 为 54/113，占 47.8%。论文把这解释为：如果没有审查上下文，就不能直接比较不同代理的拒绝标签。
- 在 364 个已合并 PR 中，288 个，占 79.1%，没有观察到反馈循环或审查者应用的提交。
- 56/364 个已合并 PR 出现了人类介入，占 15.4%，其中 28 个是反馈循环，占 7.7%；28 个是审查者应用的提交，占 7.7%。
- 在带有反馈循环或人类介入的 56 个已合并 PR 中，Copilot 和 Devin 占了 54 个。Copilot 有 29/49 个这类已合并 PR，占 59.2%；Devin 有 25/107，占 23.4%。
- OpenAI Codex 在样本中只有 1/167 个已合并 PR 出现人类介入，占 0.6%，没有反馈循环案例；Cursor 有 1/33 个反馈循环案例，占 3.0%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.22534v1](https://arxiv.org/abs/2605.22534v1)
