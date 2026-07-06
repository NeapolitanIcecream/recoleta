---
source: hn
url: https://mattmccormick.ca/we-re-all-managers-now-my-journey-into-ai-assisted-development/
published_at: '2026-07-05T23:57:12'
authors:
- mattm
topics:
- ai-assisted-development
- code-generation
- human-ai-interaction
- software-engineering-workflow
- requirements-engineering
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# We're All Managers Now: My Journey into AI-Assisted Development

## Summary
## 摘要
本文认为，AI 辅助开发把软件工程师的工作推向类似管理者的方向：定义需求，把实现委派给 Claude Code 等工具，审查输出，并协调并行任务。

## 问题
- AI 编码工具生成代码的速度可能超过人类审查代码的速度，这会改变工程时间的分配。
- 宽松的需求会让失败更快发生：作者的大功能实验在 20-30 分钟内生成了几个 PR，但实现偏离了预期设计。
- 工程师需要养成新的上下文切换、审查和规格说明习惯，因为作者发现，随着对 Claude 的信任增加，直接跟着代码逐行看变得不那么有用。

## 方法
- 作者在全职构建一个创业项目时，把 Claude Code 作为主要编码助手。
- 工作流从反复的提示-处理-响应循环，转向委派模式：写下上下文和需求，让 Claude 实现，然后审查生成的输出。
- 实现前，需求和设计文档获得更多关注，因为小缺口会在生成的代码中快速造成可见的不匹配。
- 在 Claude 处理期间，作者会开始其他任务并在任务之间切换，类似于管理多个工作流。
- 作者认为，过去担任工程经理时积累的技能，例如上下文切换和通过反馈循环审查工作，对 AI 辅助编码有用。

## 结果
- 文中没有报告经过基准测试的定量结果；这是一篇从业者文章，不是实证研究论文。
- 在一次实验中，Claude 在大约 20-30 分钟内生成了几个串联的 PR，但由于需求不清晰，工作没有达到目标。
- 作者表示，实际并发上限是 3 个由 Claude 辅助的任务，因为恢复上下文变得困难。
- 有些任务审查每个可能需要 20 或 30 分钟，这使得离开 1 个多小时后再回到第三个任务变得困难。
- 工具使用量随时间增加：作者在 2024 年圣诞节期间开始实验，2025 年 6 月付费购买了基础 Claude Code 计划，并在 2026 年 3 月转到 Claude 5x Max 计划。

## Problem

## Approach

## Results

## Link
- [https://mattmccormick.ca/we-re-all-managers-now-my-journey-into-ai-assisted-development/](https://mattmccormick.ca/we-re-all-managers-now-my-journey-into-ai-assisted-development/)
