---
source: arxiv
url: https://arxiv.org/abs/2605.30208v1
published_at: '2026-05-28T16:44:07'
authors:
- Chris Adams
- Arjun Singh Banga
- Parveen Bansal
- Souvik Bhattacharya
- Rujin Cao
- Pedro Canahuati
- Nate Cook
- Brian Ellis
- Prabhakar Goyal
- Gurinder Grewal
- Tianyu He
- Matt Labunka
- Alex Manners
- David Molnar
- Ging Cee Ng
- Vishal Parekh
- Jiefu Pei
- Frederic Sagnes
- James Saindon
- Will Shackleton
- Sid Sidhu
- Gursharan Singh
- Karthik Chengayan Sridhar
- Matt Steiner
- Pratibha Udmalpet
- Sean Xia
- Stacey Yan
- Audris Mockus
- Peter Rigby
- Nachiappan Nagappan
topics:
- code-review-automation
- software-foundation-models
- code-intelligence
- ai-generated-code
- developer-productivity
- risk-calibration
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Automating Low-Risk Code Review at Meta: RADAR, Risk Calibration, and Review Efficiency

## Summary
## 摘要
RADAR 通过把来源准入规则、Diff Risk Score 模型、基于 LLM 的代码审查和确定性检查结合起来，在落地变更前自动处理 Meta 的低风险代码审查。

## 问题
- Meta 的代码量增长速度超过了人工审查能力：每个由人落地的 diff 对应的代码行数同比增长 105.9%，每位开发者每月的 diff 数量增长 51%。
- 这部分增长中有 80% 以上来自 agentic AI，而在 24 小时内完成审查的 diff 占比在下降。
- 这篇论文把目标放在常规的低风险 diff 上，让人工审查者把时间留给生产风险或设计风险更高的变更。

## 方法
- RADAR 先按每个 diff 的作者来源分类：人工编写 diff、确定性 codemod、AI 生成的 codemod，以及 RACER runbook diff。
- Bot diff 经过 ACE，先应用静态安全门控、可配置的 Diff Risk Score 阈值、基于 LLM 的 Automated Code Review，然后在落地前做最终验证。
- 人工编写 diff 经过 RADAR Verification 和 RADAR Approval，使用作者准入、范围排除、内容黑名单、Diff Risk Score 和 LLM 审查。
- Diff Risk Score 阈值控制风险偏好：例如，默认人工编写 diff 使用 P5，更严格的 bot 来源使用 P20，白名单中的 RACER runbook 使用 P50。
- RACER runbook 还使用 60 天风险历史检查、每日落地上限，以及对有事故或敏感目标的来源设置黑名单。

## 结果
- RADAR 审查了超过 535K 个 diff，并在 Meta 的生产环境中落地了超过 331K 个 diff。
- 该系统每天处理超过 25K 个 diff。
- 将 Diff Risk Score 阈值从第 25 百分位放宽到第 50 百分位后，批准率升至 60.31%。
- RADAR 审查的 diff 的回滚率是非 RADAR diff 的三分之一。
- RADAR 审查的 diff 的 Production Incident 率是非 RADAR diff 的五十分之一。
- 与人工审查的 diff 相比，论文称 RADAR 将中位完成时间缩短了 330% 以上，并将中位 diff 审查墙钟时间缩短了 35%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.30208v1](https://arxiv.org/abs/2605.30208v1)
