---
source: hn
url: https://tessl.io/eval-runs/019cc02f-bb26-76e0-a7c9-598a7337edb7
published_at: '2026-03-05T23:34:24'
authors:
- sjmaplesec
topics:
- cli-evaluation
- tool-use
- prompt-context
- safety
- google-workspace
relevance_score: 0.05
run_id: materialize-outputs
language_code: zh-CN
---

# Googleworkspace/CLI isn't optimized – Test your skills

## Summary
这不是一篇传统学术论文，而是一份针对 Google Workspace CLI 使用能力的评测结果摘要，展示了通过提供特定“tile/context”后，智能体在一组 CLI 技能任务上的成功率与效率变化。核心结论是：结构化上下文能显著提升任务成功率，并在若干关键操作上把正确率从接近 0% 提升到 100%。

## Problem
- 该工作要解决的问题是：智能体在使用 Google Workspace/CLI 时，经常因为**资源语法、参数构造、安全流程、输出格式**等细节出错，导致任务成功率低。
- 这很重要，因为企业自动化场景中，CLI 误用不仅会降低效率，还可能引发**错误写入、泄露凭证、PII 暴露**等安全与合规风险。
- 文中还隐含关注一个实际问题：给智能体提供合适的结构化操作上下文，是否能显著提升其真实工具使用能力与成本效率。

## Approach
- 核心方法很简单：在一组 Google Workspace CLI 技能评测任务上，对比**无上下文**与**有特定 tile/context**两种设置下的智能体表现。
- 这些 context/tile 似乎提供了任务相关的操作规范，例如**schema-first API inspection、flag 构造规则、dry-run 安全流程、格式化与分页参数、认证与脱敏要求**。
- 评测按技能维度细分，检查智能体是否做到诸如：正确 CLI 资源语法、正确 flags、先 dry-run 再 live run、使用 `--format`/`--page-all`、不输出 secrets 等。
- 除了成功率，还报告了执行成本、耗时、对话轮次和 token 用量，以衡量上下文是否同时改善效率。

## Results
- 总体上，使用该 tile 后智能体成功率达到 **81%**，相比基线 **45%** 提升了 **1.8x**。
- 在 **Schema-first API inspection** 中，多项能力从低水平跃升到满分：`Correct CLI resource syntax` **0% → 100%**，`Params flag used` **0% → 100%**，`Schema-driven flag construction` **13% → 100%**；同时该组成本/时延从 **$1.1610 / 3m41s / 50 turns / 10,517 output tokens** 降到 **$0.2663 / 53s / 15 turns / 2,860 output tokens**。
- 在 **Plain text vs rich text appending** 中，多个子项维持 **100%**，但 `Confirmation before write` 仍为 **0% → 0%**；该组成本从 **$0.6478** 降到 **$0.4307**，时间从 **3m33s** 降到 **1m12s**，输出 token 从 **9,860** 降到 **4,099**。
- 在 **Batch update safety with dry-run** 中，`Dry-run preview pass` **22% → 100%**，`Correct batchUpdate syntax` **0% → 100%**，`Runbook dry-run explanation` **27% → 100%**，但 `User confirmation before live run` 仍是 **0% → 0%**。
- 在 **Output formatting and pagination** 中，`--format flag used` **0% → 100%**，`--page-all flag present` **0% → 100%**，`FORMAT argument controls --format` **0% → 100%**，`Pagination flags documented` **0% → 100%**，但 `--output flag for file saving` 仍为 **0% → 0%**。
- 在 **Service account auth and PII screening** 中结果混合：`Sanitize explained in setup guide` **16% → 100%**，`No credential values output` **90% → 100%**，但 `GOOGLE_APPLICATION_CREDENTIALS env var` **72% → 22%** 出现下降，`--sanitize flag on get` 维持 **0% → 0%**。

## Link
- [https://tessl.io/eval-runs/019cc02f-bb26-76e0-a7c9-598a7337edb7](https://tessl.io/eval-runs/019cc02f-bb26-76e0-a7c9-598a7337edb7)
