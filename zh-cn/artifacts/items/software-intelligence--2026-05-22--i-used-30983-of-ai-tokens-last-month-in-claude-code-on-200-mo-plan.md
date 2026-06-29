---
source: hn
url: https://www.indiehackers.com/post/i-used-30-983-of-ai-tokens-last-month-in-claude-code-on-200-mo-plan-3337a369a6
published_at: '2026-05-22T23:11:54'
authors:
- khadinakbar
topics:
- ai-token-usage
- claude-code
- developer-tools
- code-intelligence
- ai-cost-monitoring
- human-ai-interaction
relevance_score: 0.62
run_id: materialize-outputs
language_code: zh-CN
---

# I used $30,983 of AI tokens last month in Claude Code on $200/mo plan

## Summary
## 摘要
这是一篇关于 tokenflex.ing 的产品发布帖。tokenflex.ing 是一个面向 AI token 使用情况的公开排行榜，覆盖 Claude Code、Codex、OpenCode、Cursor 等工具。帖子认为，随着 agentic 编码工作流普及，开发者需要能看见的 token 指标，因为原始用量会增长得很快。

## 问题
- 开发者通常不会知道编码工具到底消耗了多少 AI token，直到查看日志或计费数据。
- 原始模型套餐会掩盖真实使用成本；帖子称，在 $200/月 计划下，Claude Code 的 token 用量对应了 $30,983 的价值。
- 只看 token 总量会奖励浪费，所以一些评论者提出应改看结果指标，例如每个 shipped feature 的 token 数、合并的 PR 数、关闭的 issue 数或 commit 数。

## 方法
- tokenflex.ing 提供公开的个人资料页和排行榜来展示 AI token 消耗，帖子把它描述为类似 AI 使用版的 GitHub profile。
- 帖子建议用预先写好的项目说明文件来减少浪费，让 agent 不必每次都重复探索代码库。
- 它建议把涉及超过 3 个文件的任务拆成更小的子任务，并给出明确规格，以减少重试循环。
- 它建议在简单操作上直接用 grep、文件搜索和查找替换，而不是调用 AI agent。
- 评论者补充了路由思路：只在需要推理的工作上使用更强的模型，日常工作用更便宜的模型，对重复上下文使用 prompt caching，为每个 agent 设定预算，并基于工具调用加速设置熔断条件。

## 结果
- 主要用量说法是：一个月内在 $200/月 计划上使用了价值 $30,983 的 Claude Code token。
- 作者称，三项工作流改动让每月 Claude Code 支出大约下降了 65%。
- 帖子提到了一些很高的使用量示例，包括一个月 12B tokens、30 天 17B tokens、18B tokens，以及 51,414 次 Claude Code 事件，但没有提供可复现的测量方法。
- 一位评论者说，把解释类工作路由到 Sonnet、把 Opus 留给难修改任务后，每月支出下降了约 60%，且没有发现质量损失。
- 另一位评论者称，AI 计算通常只占企业 B2B 项目总成本的 10-15%，其余成本来自数据清理、集成工作和利益相关方审批。
- 帖子没有报告同行评审结果、基准分数、数据集或受控基线；它最明确的结论是使用可见性、降本经验，以及与已交付结果挂钩的效率指标需求。

## Problem

## Approach

## Results

## Link
- [https://www.indiehackers.com/post/i-used-30-983-of-ai-tokens-last-month-in-claude-code-on-200-mo-plan-3337a369a6](https://www.indiehackers.com/post/i-used-30-983-of-ai-tokens-last-month-in-claude-code-on-200-mo-plan-3337a369a6)
