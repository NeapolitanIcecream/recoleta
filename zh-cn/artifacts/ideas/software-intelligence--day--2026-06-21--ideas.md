---
kind: ideas
granularity: day
period_start: '2026-06-21T00:00:00'
period_end: '2026-06-22T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- agent evaluation
- coding agents
- open weights
- local observability
- cost governance
- architecture boundaries
tags:
- recoleta/ideas
- topic/agent-evaluation
- topic/coding-agents
- topic/open-weights
- topic/local-observability
- topic/cost-governance
- topic/architecture-boundaries
language_code: zh-CN
---

# 编码代理运行控制

## 摘要
代理团队现在有具体检查来处理三个常见失败点：较便宜的编码代理跨越模块边界、编码会话产生不清晰花费，以及代理在没有证明工作知识的情况下进入陌生语料。

## 接入编码代理钩子和 CI 的 YAML 模块契约
使用较便宜编码代理的团队可以把模块边界变成可执行规则。ANMA 的做法很直接：开发者为每个模块编写 YAML 契约，然后 `anma sync` 生成 Claude Code 指引、阻止编辑的钩子、后端配置、CI 检查，以及可选的 `CODEOWNERS` 条目。

有用的采用测试是选择一个已有依赖规则的小型仓库。用较便宜的模型，在普通 checkout 和带有生成指引并在 CI 中运行 `anma check` 的 checkout 上执行同一个边界敏感任务。ANMA 报告称，Claude Haiku 4.5 在 19 次普通仓库运行中有 13 次违反 Python 边界，在 20 次 ANMA 运行中为 0 次。一个 TypeScript 后续实验报告称，对照组 20 次运行中有 18 次违规，使用 ANMA 的 20 次运行中为 0 次。作者还说 Claude Opus 4.8 在没有 ANMA 的情况下也遵守了 Python 边界，所以实际目标是成本敏感的代理使用，以及对人或代理编写 diff 的 CI 治理。

### 资料来源
- [Show HN: ANMA, boundary contracts for cheaper AI coding agents](../Inbox/2026-06-21--show-hn-anma-boundary-contracts-for-cheaper-ai-coding-agents.md): 概述 ANMA 的 YAML 契约、生成的 Claude Code 指引、钩子、CI 检查、基准测试结果，以及针对较便宜代理的较窄主张。
- [Show HN: ANMA, boundary contracts for cheaper AI coding agents](../Inbox/2026-06-21--show-hn-anma-boundary-contracts-for-cheaper-ai-coding-agents.md): 给出 Python 基准测试结果，并说明其价值是为较便宜代理提供保险并支持 CI 治理。
- [Show HN: ANMA, boundary contracts for cheaper AI coding agents](../Inbox/2026-06-21--show-hn-anma-boundary-contracts-for-cheaper-ai-coding-agents.md): 列出生成的文件、`anma sync --check`、`anma check`、警告模式、JSON 输出，以及 CI 使用的退出码。

## Claude Code 和 Codex 会话的本地成本门禁
编码代理的花费可以在会话和轮次层面检查，避免最后变成财务意外。Lupen 读取本地 Claude Code 和 Codex JSONL 日志，按会话、轮次、步骤、技能组和子代理分组活动，然后根据 token 计数和公开价格表重新计算成本。

一个实用流程是在每个大量使用代理的工作日结束时运行本地报告，并把 `lupen budget --over 20 --last 7d` 或 `lupen verify` 加到高级用户使用的脚本中。两个检查都可以用代码 4 退出，让团队可以在不把提示词、文件路径、图片或 URL 上传到托管服务的情况下，发现成本漂移或失控会话。证据停留在功能层面，不是基准测试，所以团队应在短期试点中用自己的供应商发票和原始日志验证它。

### 资料来源
- [Show HN: Lupen – an itemized, verified receipt for Claude Code and Codex spend](../Inbox/2026-06-21--show-hn-lupen-an-itemized-verified-receipt-for-claude-code-and-codex-spend.md): 描述 Lupen 的本地 JSONL 读取、分组模型、重新计算成本、校验、预算检查，以及退出码 4。
- [Show HN: Lupen – an itemized, verified receipt for Claude Code and Codex spend](../Inbox/2026-06-21--show-hn-lupen-an-itemized-verified-receipt-for-claude-code-and-codex-spend.md): 展示按供应商、会话、轮次、步骤、技能组和子代理拆分的本地花费。
- [Show HN: Lupen – an itemized, verified receipt for Claude Code and Codex spend](../Inbox/2026-06-21--show-hn-lupen-an-itemized-verified-receipt-for-claude-code-and-codex-spend.md): 记录 CLI 报告、校验和预算门禁、本地-only 运行方式，以及附件跟踪。

## 把陌生仓库或文献分配给代理前的语料学习考试
团队可以先测试代理是否学会了陌生语料，再把开放式工作交给它。Machine Studying 将其定义为：先针对文档语料进行任务前学习阶段，然后回答隐藏的下游问题。StudyBench 把这种设置用于 DSPy 代码、OpenClaw 代码和近期机器学习文献，其指标奖励在较低推理 token 预算下的准确率。

实用版本是为私有仓库、产品手册或研究库设置一场小型内部考试。让代理用常规工具花时间学习语料，隐藏考试题，然后在固定 token 预算下给答案打分。早期结果提醒团队不要默认搜索访问就能解决问题：Qwen3.5-9B 在 DSPy 上只有在被强制使用 20 次搜索迭代时，宽松分数才从 9.6 提高到 29.4；报告中的微调基线也没有稳定提升代理专长。

### 资料来源
- [Machine Studying](../Inbox/2026-06-21--machine-studying.md): 定义 StudyBench、语料学习设置、专长指标、领域、工具设置和早期结果。
- [Machine Studying](../Inbox/2026-06-21--machine-studying.md): 说明在下游评估已知之前，学习可以改变权重、提示词、工具、索引、笔记或测试框架状态。
- [Machine Studying](../Inbox/2026-06-21--machine-studying.md): 报告在截止日期后领域中的专长缺口，以及用早期监督或自监督方法提升代理专长的困难。
