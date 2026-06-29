---
kind: ideas
granularity: day
period_start: '2026-06-20T00:00:00'
period_end: '2026-06-21T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- AI agents
- coding agents
- agent memory
- governance
- code review
- local search
tags:
- recoleta/ideas
- topic/ai-agents
- topic/coding-agents
- topic/agent-memory
- topic/governance
- topic/code-review
- topic/local-search
language_code: zh-CN
---

# 内部智能体的运行控制

## Summary
智能体采用正在转向模型周边的运行控制：任务租约、证据包、带来源的记忆、API 调用检查和带身份信息的日志。实际工作是在现有开发者和内部工具工作流中加入这些控制，使失败可见且测试成本较低。

## 用于并行编码智能体的 worktree 租约和状态包
在同一个代码库中运行多个编码智能体的团队，可以为每个任务加一层小型控制：一个 Git worktree、一个租约文件、一个门禁结果，以及一个状态包，列出任务拥有的文件、已改动文件、命令、测试和证据。GlueRun-go 展示了这种模式的具体实现。它的 worker 会写入一个有 schema 支持的数据包，auditor 检查数据包和门禁结果，确定性 decider 在使用模型兜底前选择重试、改变范围、升级或搁置。

有用的测试是运行层面的。在一个带有真实测试命令的代码库中，让两三个智能体处理彼此独立的任务，然后检查评审者能否在先不阅读每个 diff 的情况下回答三个问题：这个任务拥有哪些文件，产出了什么证明，门禁失败后应该怎么处理。GlueRun-go 报告称，分离式调度让 `gluerun reconcile --actuate` 在数秒内返回，同时 worker 继续在后台运行；崩溃检测也从 60 分钟的过期租约窗口降到约一个 reconcile 周期。对于当前智能体运行会留下过期分支、所有权不清或难以评审变更的团队，这足以支持一次试用。

### Evidence
- [Show HN: Agentic coding workflows built on Git worktrees and task evidence](../Inbox/2026-06-20--show-hn-agentic-coding-workflows-built-on-git-worktrees-and-task-evidence.md): 概述 GlueRun-go 的 worktree 隔离、JSON 租约、状态包、auditor、确定性恢复动作、分离式调度、崩溃检测和回归测试。
- [Show HN: Agentic coding workflows built on Git worktrees and task evidence](../Inbox/2026-06-20--show-hn-agentic-coding-workflows-built-on-git-worktrees-and-task-evidence.md): 详细说明状态包内容、门禁结果、审计结论、恢复动作、分离式调度，以及一个周期内的崩溃归因。

## 带来源的公司记忆，包含确定性缺口报告和 API 调用检查
内部智能体需要一个记忆层，在智能体行动前说明哪些声明有支持、已过期、相互矛盾或缺失。Vitrus 给出了可构建的形式：把 Markdown 和带类型的边 sidecar 作为事实来源，把索引作为可丢弃基础设施重建，并返回带来源、置信度、新鲜度和确定性缺口列表的答案。它的 API 路径还增加了一项有用控制：导入 OpenAPI 规范，搜索正确端点，验证端点名称和参数，然后只在调用通过检查后执行。

这适合内部支持智能体、入职引导智能体，以及已经会查阅 runbook、决策记录、工单和 API 文档的工程助手。首次部署可以限定在一个服务领域，并用简单失败案例来评估：无支持的答案、过期决策、缺失的引用文档、已废弃端点、错误参数类型和未授权结果。Vitrus 报告称其 eval gate 上的 `source-hit ≥90%`，在受控合成语料上的缺口召回率和精确率均为 `100%`，ACL 泄漏测试中未授权结果为 `0`，并有超过 200 项测试。缺口结果来自合成语料，因此上线范围应保持较窄，但其机制已经足够具体，可以用于服务团队试点。

### Evidence
- [Show HN: Vitrus – the company brain that tells you what it doesn't know](../Inbox/2026-06-20--show-hn-vitrus-the-company-brain-that-tells-you-what-it-doesn-t-know.md): 描述 Vitrus 的带来源答案、置信度、新鲜度、确定性缺口、作为事实来源的 Markdown、检索方法、OpenAPI 验证、ACL 测试和报告的评估结果。
- [Show HN: Vitrus – the company brain that tells you what it doesn't know](../Inbox/2026-06-20--show-hn-vitrus-the-company-brain-that-tells-you-what-it-doesn-t-know.md): 展示 API 导入、搜索、验证和调用路径，包括对缺失参数、错误类型、未知参数、未知端点、已废弃端点和失败关闭内容工具的检查。

## 智能体身份、任务范围权限和明确拒绝原因
让智能体访问 IT 系统的公司，应在日志中区分智能体身份和人类身份，同时保留人类负责人。Amazon 描述的模式很具体：日志显示某个具名智能体代表某个具名人类执行了操作，权限按任务限定，破坏性操作有静态防护栏，被阻止的操作会返回生产影响等原因。这个原因很重要，因为只看到通用权限失败的智能体，可能会尝试另一条路径来完成同一个有害任务。

一个实际采用检查是，为一个内部智能体配置独立账号、任务专用策略，以及针对影响生产操作的拒绝消息。审计日志应能回答谁拥有该请求、哪个智能体执行了操作、它触达了什么资源，以及任何被阻止的操作为何被阻止。Amazon 没有提供基准或量化安全结果，因此这应被视为一种治理设计，并在有边界的工作流中测试，例如数据库维护请求或由工单驱动的基础设施变更。

### Evidence
- [Why Amazon hates 'human-in-the-loop' AI governance](../Inbox/2026-06-20--why-amazon-hates-human-in-the-loop-ai-governance.md): 概述 Amazon 的治理观点：重复审批会变弱，智能体获得独立身份，权限按任务风险限定，并提供拒绝原因。
- [Why Amazon hates 'human-in-the-loop' AI governance](../Inbox/2026-06-20--why-amazon-hates-human-in-the-loop-ai-governance.md): 给出具体日志模式：一个具名智能体代表一个具名人类执行操作，同时保留人类责任。
