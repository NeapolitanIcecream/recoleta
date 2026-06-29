---
kind: trend
trend_doc_id: 1255
granularity: day
period_start: '2026-05-30T00:00:00'
period_end: '2026-05-31T00:00:00'
topics:
- agent runtime
- autonomy governance
- workflow evaluation
- coding agents
- model routing
- deterministic validation
run_id: materialize-outputs
aliases:
- recoleta-trend-1255
tags:
- recoleta/trend
- topic/agent-runtime
- topic/autonomy-governance
- topic/workflow-evaluation
- topic/coding-agents
- topic/model-routing
- topic/deterministic-validation
language_code: zh-CN
---

# Agents 需要运行时、审计轨迹和工作流测试

## Overview
当天最清楚的信号是 agent 基础设施。Autonomy Kernel、Lite-Harness 和 HermesBench 都把 agents 当成长期运行的系统，认为它们需要权限检查、持久状态、审批和可追踪评估。证据主要是设计提案和早期工具，受控测量很少。

## Clusters

### Agent 权限与可停止性
Autonomy Kernel 给出了当天最强的设计主张。它定义了位于 agents 和 models 之下的运行时，负责执行、身份、权限、通信和审计。每个动作在运行前都必须能追溯到一个 principal 和一条授权路径。

这个提案有价值，因为它点出了长时间运行的 agents 缺少的操作层：作用域权限、租约、审计记录、可移植状态，以及可保证的停止路径。来源没有给出实现或基准，所以它的价值在于架构清晰，而不是实测性能。

#### Evidence
- [A case for an Autonomy Kernel](../Inbox/2026-05-30--a-case-for-an-autonomy-kernel.md): 总结了 autonomy kernel 模型、权限链、审计记录以及缺少实证结果。

### Self-hosted agent operations
Lite-Harness 把 coding-agent 的使用变成了运维问题。它把 Claude Code、Codex、OpenCode 和相关工具封装在一个兼容 OpenCode 的 API 后面，再加入定时运行、密钥、持久会话、沙箱和审批路由。

具体例子很关键：一个外联 agent 在工作日每四小时运行一次，保存 vault keys，启动测试运行，并在发送消息前请求人工批准。摘录给出了部署机制和支持的 harness，但没有可靠性指标或用户研究。

#### Evidence
- [Show HN: Lite-Harness – Self-Hosted Cursor Agents (Use Claude Code/OpenCode)](../Inbox/2026-05-30--show-hn-lite-harness-self-hosted-cursor-agents-use-claude-code-opencode.md): 总结了 Lite-Harness 对多个 coding harness、cron 调度、沙箱、vault keys、审批和持久化的支持。

### Workflow-level reliability checks
HermesBench 和 Dimensional Design 关注 agent 工作能否在上下文中被检查。HermesBench 会对一个完整的 personal-agent 配置按 27 个 recipes 打分，覆盖工具、记忆、安全、委派、延迟和 traces。它公开的基线是 78.2，并提供 recipes 定义和去敏时间线供检查。

Dimensional Design 为 AI 辅助工作补充了一条实用规则：在需要精确性的地方，把预测步骤放到确定性的通过/失败门槛之后。例子包括发票总额、复式记账平衡、纯文本协作，以及少量记录下来的人工检查。这是指导意见，不是基准测试，但它和这个时期对可见边界的重视一致。

#### Evidence
- [Show HN: HermesBench – workflow reliability evals for personal AI agents](../Inbox/2026-05-30--show-hn-hermesbench-workflow-reliability-evals-for-personal-ai-agents.md): 提供了 HermesBench 的范围、评分方法、27 个 recipes 上 78.2 的基线，以及基于 traces 的证据。
- [The Manifesto for Dimensional Design](../Inbox/2026-05-30--the-manifesto-for-dimensional-design.md): 总结了确定性验证、独立检查、低维格式，以及缺少实证基准结果。

### Coding decisions and model routing
Arch-Decision 把多 agent 编码工作应用到一个很窄的团队工件上：Architecture Decision Record（ADR），也就是记录软件设计决策原因的文档。它的八阶段流程会先读 issue，再用三个 agents 探索代码库，提出选项，等待批准，写出 ADR，并把它链接回去。

OpenRouter 给出了市场侧对应物。它的 gateway 暴露了 400 多个 models，并报告有 800 万用户、每月约 100 万亿 tokens。对 agent 构建者来说，这表明 model 选择是一个运行时依赖，可以按任务切换，而治理和审查仍留在外围系统中。

#### Evidence
- [Arch-Decision – A multi-agent architecture tool for Claude Code](../Inbox/2026-05-30--arch-decision-a-multi-agent-architecture-tool-for-claude-code.md): 总结了 Arch-Decision 的 ADR 工作流、多 agent 探索、审批门、案例研究和测量限制。
- [OpenRouter more than doubles valuation to $1.3B in a year](../Inbox/2026-05-30--openrouter-more-than-doubles-valuation-to-1-3b-in-a-year.md): 总结了 OpenRouter 的 gateway 角色、模型数量、用户数量、token 量、融资和估值数据。
