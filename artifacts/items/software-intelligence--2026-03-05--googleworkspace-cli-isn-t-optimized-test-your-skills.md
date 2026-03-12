---
source: hn
url: https://tessl.io/eval-runs/019cc02f-bb26-76e0-a7c9-598a7337edb7
published_at: '2026-03-05T23:34:24'
authors:
- sjmaplesec
topics:
- cli-evaluation
- agent-tool-use
- schema-guided-execution
- google-workspace
- benchmarking
relevance_score: 0.88
run_id: materialize-outputs
---

# Googleworkspace/CLI isn't optimized – Test your skills

## Summary
这不是一篇传统论文，而是一份针对 Google Workspace CLI 使用技能的评测结果页，展示给智能体提供特定“技能/上下文 tile”后，执行相关 CLI 任务的成功率、成本与时延变化。核心结论是：把结构化操作知识注入给智能体，能显著提升任务完成率，并在部分任务上降低 token、时间与成本。

## Problem
- 解决的问题是：智能体在使用 Google Workspace/CLI 时，常因不了解正确命令语法、参数构造、安全规范和输出格式而失败。
- 这很重要，因为自动化软件生产与代理执行依赖稳定、可复现的工具调用；CLI 细节错误会直接导致任务失败、泄露风险或高成本反复试错。
- 该页面特别关注真实操作中的高频失误，如资源语法、flag 使用、dry-run 安全流程、分页与格式化、认证与 PII/secret 处理。

## Approach
- 核心方法是给智能体提供一个面向 Google Workspace CLI 的“技能 tile/上下文包”，把正确做法显式编码进去，再与无该上下文的基线进行对比。
- 这个 tile 似乎以**schema-first API inspection**为中心：先检查 schema/帮助文档，再按 schema 构造命令、资源路径和 flags。
- 它还把操作规范固化为可执行提示，包括：正确 CLI resource syntax、参数 flag 使用、`batchUpdate` 的 JSON 用法、`--format`/`--page-all` 等输出控制、安全 dry-run、确认步骤、以及不输出 secrets。
- 评测方式是按技能点逐项统计“with context vs without context”的成功率，并记录成本、耗时、轮次和 token 开销，从而衡量该上下文包对代理执行的增益。

## Results
- 总体上，使用该 tile 后**agent success rate 为 81%**，相对基线 **45%** 提升到 **1.8x**。
- 在 **Schema-first API inspection** 中，多项能力从低基线跃升到满分：schema inspection **15% → 100%**，correct CLI resource syntax **0% → 100%**，params flag used **0% → 100%**，schema-driven flag construction **13% → 100%**；该任务成本/时延从 **$1.1610, 3m41s, 50 turns, 10,517 output tokens** 降到 **$0.2663, 53s, 15 turns, 2,860 output tokens**。
- 在 **Plain text vs rich text appending** 中，多项保持或达到 **100%**：`+write for plain text`、`batchUpdate for table`、correct `+write` flags、`batchUpdate uses --json`、reason for split documented、no hardcoded credentials；但 **confirmation before write 仍为 0% → 0%**。成本/时延从 **$0.6478, 3m33s, 22 turns** 降到 **$0.4307, 1m12s, 24 turns**，输出 tokens **9,860 → 4,099**。
- 在 **Batch update safety with dry-run** 中，dry-run preview pass **22% → 100%**，correct `batchUpdate` syntax **0% → 100%**，runbook dry-run explanation **27% → 100%**，loops over all IDs 与 no secrets exposed 保持 **100%**；但 **user confirmation before live run 为 0% → 0%**。该项反而在带上下文时成本上升：**$0.2168 → $0.3692**，耗时 **1m04s → 1m42s**，输出 tokens **3,510 → 6,201**。
- 在 **Output formatting and pagination** 中，`--format` flag **0% → 100%**，`--page-all` **0% → 100%**，FORMAT argument controls `--format` **0% → 100%**，pagination flags documented **0% → 100%**，output filename matches format 保持 **100%**；但 `--output` flag for file saving **0% → 0%**。该项成本/输入 token 上升：**$0.2705 → $0.4985**，耗时 **1m10s → 1m34s**，输入 tokens **12 → 6,290**。
- 在 **Service account auth and PII screening** 中，带上下文后安全相关能力有改善但并不一致：no credential values output **90% → 100%**，sanitize explained in setup guide **16% → 100%**；但 `GOOGLE_APPLICATION_CREDENTIALS` env var **72% → 22%** 出现退化，`--sanitize` flag on get **0% → 0%** 仍未解决。成本从 **$0.2651 → $0.4179**，耗时从 **1m32s → 1m14s**。

## Link
- [https://tessl.io/eval-runs/019cc02f-bb26-76e0-a7c9-598a7337edb7](https://tessl.io/eval-runs/019cc02f-bb26-76e0-a7c9-598a7337edb7)
