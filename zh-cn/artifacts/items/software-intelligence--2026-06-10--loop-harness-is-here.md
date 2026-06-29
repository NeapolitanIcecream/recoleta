---
source: hn
url: https://github.com/lSAAGl/loop-harness
published_at: '2026-06-10T23:02:01'
authors:
- LordIsBack
topics:
- coding-agents
- software-engineering-automation
- agent-orchestration
- code-review
- ci-triage
- human-ai-interaction
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# Loop Harness Is Here

## Summary
## 摘要
Loop-Harness 是一个基于 shell 的协调器，按计划在仓库任务上运行 Claude Code 代理，用第二个 Claude 会话检查输出，只发布通过审核的变更。它面向无人值守的代码维护任务，例如 CI 分流、PR 审查、issue 整理、依赖更新和文档同步。

## 问题
- 带有 shell 访问权限的编码代理在无人值守运行时会损坏仓库；团队需要隔离、最小化工具权限和审核关口。
- 常规维护工作需要轮询、状态跟踪、去重、重试、日志和输出处理；一次性提示不提供这些控制。
- 这个问题很重要，因为可写循环可以提交代码、打开 PR、发布评论，并把分支推送到实际开发流程中。

## 方法
- 调度器会根据 `every` 频率或 5 字段 cron 表达式，为每个仓库选出到期的循环。
- 每次写入运行都会在 `loop/<name>/<ts>` 分支上的新 git worktree 中进行，因此代理不会修改用户当前的检出。
- 主 `claude -p` 会话会接收一个任务技能文件和一个范围受限的 `allowed_tools` 列表。它可以暂存提交、`PR_BODY.md` 或 outbox 文件，但不能直接发布或推送。
- 验证器 `claude -p` 会话会检查 diff 和已暂存输出，运行低成本检查，并且必须打印 `VERDICT: PASS`，协调器才会发布任何内容。
- 每个循环的 JSON 状态会记录 `last_run`、已处理条目 ID、失败、重试和指标，这样重复轮询和重复触发也可以安全处理。

## 结果
- 摘要没有给出受控基准测试、消融实验，也没有与另一种代理协调器做比较。
- 示例仪表盘显示 `pr-reviewer` 有 112 次运行、98% 成功率、31 个已处理条目、64 秒平均时长和 2 次失败，周期为 3 分钟。
- 示例仪表盘显示 `triage-ci` 有 38 次运行、95% 成功率、9 个已处理条目、241 秒平均时长和 2 次失败，周期为 10 分钟。
- 示例仪表盘显示 `dependency-updater`、`doc-sync` 和 `issue-groomer` 的成功率都是 100%，运行次数分别为 4、4 和 9；处理条目分别为 6、2 和 14；平均时长分别为 312 秒、198 秒和 87 秒。
- 具体的运行声明包括：每次写入运行使用一个 worktree，带有精确通过判定的验证关口，受限的 Claude 工具，默认 `max_retries: 2`，默认 `timeout_minutes: 15`，以及在有活动循环时最多等待 5 分钟的关闭流程。

## Problem

## Approach

## Results

## Link
- [https://github.com/lSAAGl/loop-harness](https://github.com/lSAAGl/loop-harness)
