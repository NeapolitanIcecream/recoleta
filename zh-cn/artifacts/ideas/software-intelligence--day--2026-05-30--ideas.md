---
kind: ideas
granularity: day
period_start: '2026-05-30T00:00:00'
period_end: '2026-05-31T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- agent runtime
- autonomy governance
- workflow evaluation
- coding agents
- model routing
- deterministic validation
tags:
- recoleta/ideas
- topic/agent-runtime
- topic/autonomy-governance
- topic/workflow-evaluation
- topic/coding-agents
- topic/model-routing
- topic/deterministic-validation
language_code: zh-CN
---

# 运营中工作代理的控制措施

## Summary
代理部署正在进入日常运营工作：定时运行、密钥、沙箱、审批、轨迹和可重复的工作流测试。最实用的做法，是在现有编码代理外面加小型控制层、为个人代理做基于 recipe 的验收测试，以及在文件写入前保留人工审批的 ADR 草稿。

## Approval and audit controls for scheduled coding agents
使用 Claude Code、Codex、OpenCode 或 Cursor 的团队，可以把每个定时运行的代理看作一个有名称的进程，配上所有者、允许的工具、密钥作用域、过期时间、审批规则和终止开关。Lite-Harness 已经给出一个具体起点：一个自托管服务器、一个兼容 OpenCode 的 API、cron 运行、保险库密钥、沙箱、持久会话，以及一个用于在发送 LinkedIn 消息等动作前进行人工审批的 Inbox 界面。

围绕这个服务器，还需要补上一层小型清单和审计层。每次运行都应在不读原始日志的情况下回答四个问题：谁批准了代理，哪项能力或密钥允许这次动作，哪次审批放行了它，以及如何停止或让它过期。Autonomy Kernel 在这里给出了清晰的设计目标：动作要能追溯到一个 principal 和一条授权路径，而执行、身份、权限、通信和审计都放在代理下面处理。

一个有用的首个测试，是在同一个工程团队里做一个双代理试点：一个负责代码维护，另一个负责外联或分流。给每个代理一份清单，要求任何对外副作用先审批，再看一周的运行记录里是否有缺少所有者、缺少授权、过期密钥或未复核动作。

### Evidence
- [Show HN: Lite-Harness – Self-Hosted Cursor Agents (Use Claude Code/OpenCode)](../Inbox/2026-05-30--show-hn-lite-harness-self-hosted-cursor-agents-use-claude-code-opencode.md): Lite-Harness provides scheduled agent runs, secrets, sandboxes, persistent sessions, and human approval routing.
- [Show HN: Lite-Harness – Self-Hosted Cursor Agents (Use Claude Code/OpenCode)](../Inbox/2026-05-30--show-hn-lite-harness-self-hosted-cursor-agents-use-claude-code-opencode.md): The example deployment shows cron scheduling, vault keys, a sandbox check, a test run, and approval before each send.
- [A case for an Autonomy Kernel](../Inbox/2026-05-30--a-case-for-an-autonomy-kernel.md): Autonomy Kernel defines the runtime responsibilities: execution, identity, authority, communication, auditing, stoppability, and traceable authorization.

## Recipe-based acceptance tests for personal-agent workflows
部署用于日历、邮件、报告、出行、财务或网页任务的个人代理时，需要能跑完整配置的验收测试，包括提示词、模型选择、工具、记忆、委派、安全行为、延迟和轨迹。HermesBench 提供了一个可用的模式：它在 27 个 recipe 上评估完整的 Hermes 配置，发布 78.2 的基线分数，并把结果连到场景定义、评分维度、确定性检查、收尾决定和脱敏时间线。

实际可落地的做法，是为团队真正允许的工作流做一个本地 recipe 包。日历 recipe 可以检查代理在移动外部会议前是否先询问。财务 recipe 可以把抽取出的发票行与印刷总额对账。报告 recipe 可以要求给出来源链接，并标记没有依据的说法。Dimensional Design 支持这种做法：对需要精确性的步骤放在确定性的通过/失败门后面；软件无法验证输出的地方，用小范围、可记录的人类检查。

先从五个与真实故障或高风险副作用相关的 recipe 开始。为每次运行保存工件，包括提示词、模型/提供方、工具、轨迹、通过/失败检查和审阅备注。分数没有维护者能否看懂一次运行为何通过、失败，或需要人工决定那么重要。

### Evidence
- [Show HN: HermesBench – workflow reliability evals for personal AI agents](../Inbox/2026-05-30--show-hn-hermesbench-workflow-reliability-evals-for-personal-ai-agents.md): HermesBench evaluates complete agent configurations with recipes, traces, deterministic checks, and a public baseline across 27 workflows.
- [Show HN: HermesBench – workflow reliability evals for personal AI agents](../Inbox/2026-05-30--show-hn-hermesbench-workflow-reliability-evals-for-personal-ai-agents.md): The site describes visible limits, redacted traces, score axes, and a single-recipe quick-start path for current configurations.
- [The Manifesto for Dimensional Design](../Inbox/2026-05-30--the-manifesto-for-dimensional-design.md): Dimensional Design argues for deterministic pass-fail gates and small recorded human review around AI outputs that need exactness.

## Architecture Decision Record drafts generated from issue analysis
工程团队可以在实现开始前，先给带架构标签的 GitHub issue 或 Jira ticket 加一个 ADR 草稿步骤。arch-decision 展示了这个流程：读取需求，用并行代理检查代码库，识别约束和已有方案，提出选项，做出取舍表，等待批准，写出 ADR，再把它链接回源 issue。

这针对的是一种明确的技术债来源：团队跳过 ADR，因为一名高级工程师可能要花 2 到 4 个小时研究代码库、比较方案并写决策记录。文中提到的 refinedev/refine 运行找到了相关先例，识别出一个包约束，并建议把 `onParse` 回调放在 antd 包装器作用域内；随后一个社区 PR 按照来源所述，使用了相同的回调名、作用域和放置位置。

采用测试很简单。把工具跑在十个本该有 ADR 的已关闭 issue 上，向审阅者隐藏最终合并方案，再问一位 staff engineer，生成的选项和建议是否会改进原来的评审。审批门要保持强制，拒绝的草稿也要保存，因为它们能说明代理在哪些地方漏掉了项目上下文。

### Evidence
- [Arch-Decision – A multi-agent architecture tool for Claude Code](../Inbox/2026-05-30--arch-decision-a-multi-agent-architecture-tool-for-claude-code.md): arch-decision describes the ADR workflow, eight phases, parallel codebase exploration, generated options, a synthesizer, and a required human approval gate.
- [Arch-Decision – A multi-agent architecture tool for Claude Code](../Inbox/2026-05-30--arch-decision-a-multi-agent-architecture-tool-for-claude-code.md): The refinedev/refine case reports a recommendation that matched a later community PR in callback name, scope, and placement.
