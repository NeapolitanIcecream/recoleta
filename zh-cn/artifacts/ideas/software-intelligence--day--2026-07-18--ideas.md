---
kind: ideas
granularity: day
period_start: '2026-07-18T00:00:00'
period_end: '2026-07-19T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- AI agents
- harness engineering
- agent security
- reliability
- observability
tags:
- recoleta/ideas
- topic/ai-agents
- topic/harness-engineering
- topic/agent-security
- topic/reliability
- topic/observability
language_code: zh-CN
---

# 面向智能体工作流可靠性的容量感知控制

## 摘要
智能体工作流运营者可以将使用容量和计量故障视为执行条件，而不是外部服务事故。最实际的改进包括同时使用工作流风险和当前配额状况的准入控制，以及将生产故障转化为持久化运行标准和检查项的追踪记录到代码库流程。

## 面向高影响智能体运行的配额感知准入控制
在 Gmail、GitHub、数据库或 shell 工具之间运行智能体的团队，应同时依据智能体检测到的能力和当前配额状况，决定是否启动、延后或缩小一次运行。SafeAI 表明，源代码和配置可以在执行前暴露这些能力；而 Cofounder 的职位描述则将运行标准、可靠性、成本、追踪记录和集成质量视为一个统一的运营面。Codex Resets 记录了与故障、异常快速的消耗和流量增长相关的多次额度恢复，这表明可用容量可能独立于工作流正确性发生变化。

具体改进是增加一个预检步骤，将静态能力清单与实时剩余配额、近期错误率以及运行重试成本估算结合起来。在容量受限时，只读或可恢复的工作可以继续执行；包含外部写入或部分完成成本较高的工作流则可以排队或要求审批。一项成本较低的检查方式，是在模拟配额耗尽的条件下重放近期追踪记录，并比较启用和不启用预检策略时的不完整副作用、重复操作和恢复时间。

### 资料来源
- [We built an open-source static AI risk analyzer in 5 days using AI coding agents](../Inbox/2026-07-18--we-built-an-open-source-static-ai-risk-analyzer-in-5-days-using-ai-coding-agents.md): SafeAI 在运行时验证之前执行提交时的框架和能力分析。
- [Hiring Private equity firm doing 9M in revenue](../Inbox/2026-07-18--hiring-private-equity-firm-doing-9m-in-revenue.md): 该职位明确将运行标准、执行可靠性、可观测性、成本和集成质量结合起来。
- [Codex Resets](../Inbox/2026-07-18--codex-resets.md): 保存的公告描述了异常快速的使用消耗和多次额度重置，而原因当时仍在调查中。

## 更新代码库运行标准的生产事故追踪记录
智能体平台的 SRE 应让生产事故的收尾步骤更新代码库指导和可执行检查项，供后续智能体运行使用。Harness Engineering 提议将已接受的工作、修正、失败、权限关系和证明流程作为代码库上下文持续保留下来；Cofounder 则将追踪记录、指标、结构化日志、测试和运行标准确定为工作流的核心基础设施。Codex 的重置历史提供了缺失的运营触发条件：其中一次事故被追溯为长时间运行会话压缩期间缓存命中率下降，其他重置则发生在多起可靠性事故或无法解释的配额消耗之后。

对于每起事故，工作流都应将受影响的追踪记录关联到新增或修订的运行标准、恢复规则或回归测试样例。例如，记录长会话中的压缩和缓存行为，或验证请求被拒绝后的幂等恢复。这样，事故经验就能在执行时发挥作用，而不是只留在事后复盘中。可以在一小组已关闭的事故上测试这一流程：针对修订后的 harness 重新运行相关追踪记录，并检查它是否能检测到原始故障模式，或安全地将其控制住。

### 资料来源
- [Harness Engineering](../Inbox/2026-07-18--harness-engineering.md): Harness Engineering 认为修正、失败和用户响应应转化为可复用的上下文、边界、工具、示例和检查项。
- [Hiring Private equity firm doing 9M in revenue](../Inbox/2026-07-18--hiring-private-equity-firm-doing-9m-in-revenue.md): 该平台职位要求单元测试和集成测试、指标、追踪记录及结构化日志。
- [Codex Resets](../Inbox/2026-07-18--codex-resets.md): 一则保存的公告将更快的配额消耗归因于长时间运行会话压缩期间缓存命中率下降。
