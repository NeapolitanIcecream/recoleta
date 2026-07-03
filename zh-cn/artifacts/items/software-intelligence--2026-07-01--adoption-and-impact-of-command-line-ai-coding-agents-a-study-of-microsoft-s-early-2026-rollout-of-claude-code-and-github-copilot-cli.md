---
source: arxiv
url: https://arxiv.org/abs/2607.01418v1
published_at: '2026-07-01T19:24:27'
authors:
- Emerson Murphy-Hill
- Jenna Butler
- Alexandra Savelieva
topics:
- command-line-agents
- code-intelligence
- developer-productivity
- ai-tool-adoption
- software-engineering-telemetry
- human-ai-interaction
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Adoption and Impact of Command-Line AI Coding Agents: A Study of Microsoft's Early 2026 Rollout of Claude Code and GitHub Copilot CLI

## Summary
## 摘要
本文使用开发者遥测数据，研究微软在 2026 年初推出 Claude Code 和 GitHub Copilot CLI 的情况。研究发现，同事接触度可以预测试用，编码活动可以预测留存，采用者合并的拉取请求数量比估计的反事实情况多约 24%。

## 问题
- 组织需要知道哪些工程师会试用命令行 AI 编码代理，哪些工程师会持续使用它们，以及这些工具是否会改变交付产出。
- 这一点很重要，因为大型公司的 token 成本每年可能达到数百万美元，而已合并的拉取请求只能作为交付价值的代理指标。
- 以往研究常使用调查、实验室任务、公共仓库信号或 IDE 工具数据；本研究使用微软遥测数据，研究对象是可以采用获准 CLI 代理的工程师。

## 方法
- 采用研究跟踪 2026 年 1 月 5 日至 4 月 29 日期间，符合条件的微软软件工程师首次使用 Copilot CLI 和留存的情况，预测变量来自 HR 数据、此前的拉取请求活动、此前的 IDE Copilot 使用情况和社交接触度。
- 初次使用采用基于工程师-周行的离散时间逻辑回归建模；留存定义为首次使用后的前 14 天内至少使用 5 天。
- 社交接触度通过此前 14 天内使用过 Copilot CLI 的评审同事、隔级同事和直接经理来衡量。
- 结果研究覆盖 Claude Code 和 Copilot CLI，并使用创建后 28 天内合并的拉取请求作为产出指标。
- 影响估计使用 CausalImpact 合成控制反事实方法，以及同一工程师在不同工具使用强度周之间进行比较的个体内剂量-反应设计。

## 结果
- 采用者合并的拉取请求数量比原本估计情况多约 24%，这一提升在四个月观察窗口内持续存在。
- 社交接触度与采用的关联最大：超过 25% 的隔级同事使用 Copilot CLI 的工程师，试用几率高 +216%，留存几率高 +66%；直接经理使用该工具与试用几率高 +82%、留存几率高 +22% 相关。
- 评审同事接触度也有影响：当至少 25% 的评审同事使用 Copilot CLI 时，试用几率比没有接触过评审同事使用的工程师高 +54%。
- 此前使用 IDE Copilot 可以预测试用，但对留存的预测较弱：此前使用与试用 Copilot CLI 的几率高 +49% 到 +83% 相关，而留存几率低约 12% 到 15%。
- 基线编码活动可以预测留存：此前每周创建 2 个或更多 PR 的工程师，试用 Copilot CLI 的几率比前期没有 PR 的工程师高 +34%，留存几率高 +31%。
- 职级和任职年限的影响较小：IC2 和 IC3 工程师的试用几率比 IC4 工程师低约 13% 到 14%，IC5 工程师的试用几率高约 +22%，入职微软第一年的工程师的试用几率比任职 5 到 15 年的群体高 +11%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.01418v1](https://arxiv.org/abs/2607.01418v1)
