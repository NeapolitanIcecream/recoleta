---
kind: trend
trend_doc_id: 1508
granularity: week
period_start: '2026-06-08T00:00:00'
period_end: '2026-06-15T00:00:00'
topics:
- "\u7F16\u7801 agent"
- "agent \u6CBB\u7406"
- "\u8F6F\u4EF6\u5DE5\u7A0B\u57FA\u51C6\u6D4B\u8BD5"
- "agent \u8BB0\u5FC6"
- "\u8FD0\u884C\u65F6\u6267\u884C"
- "\u5F62\u5F0F\u5316\u65B9\u6CD5"
run_id: materialize-outputs
aliases:
- recoleta-trend-1508
tags:
- recoleta/trend
- "topic/\u7F16\u7801-agent"
- "topic/agent-\u6CBB\u7406"
- "topic/\u8F6F\u4EF6\u5DE5\u7A0B\u57FA\u51C6\u6D4B\u8BD5"
- "topic/agent-\u8BB0\u5FC6"
- "topic/\u8FD0\u884C\u65F6\u6267\u884C"
- "topic/\u5F62\u5F0F\u5316\u65B9\u6CD5"
language_code: zh-CN
---

# 编码 agent 正在按控制、记忆和成本来衡量

## 概览
本周的大语言模型 (LLM) 编码工作把自主性当作运维问题处理。Claw-SWE-Bench、Trace 和 PROJECTMEM 显示了重点：公平比较 agent harness，在运行时执行用户规则，并在跨会话中保留项目状态。

## 研究发现

### 运行时执行和动作限制
Agent 控制进入了执行循环。Trace 将用户纠正编译成带有适用性检查和验证器的规则，并在所有活动检查通过前阻止任务完成。在 ClawArena 中，它把留出偏好违规率降到分布内 37.6%、分布外 2.0%。

企业安全研究为生产环境 agent 增加了更宽的控制模型。它会在动作到达工具前检查计划、委托链、能力集和会话状态。Agent Joe 给出了一个更小的产品例子：一个仅支持 Rust、没有 shell 访问权限的编码 agent，用来降低执行任意终端命令的风险。Claude Code 的嵌套 sub-agent 说明了这些限制的必要性。嵌套能改善上下文隔离，但引用的例子包括每分钟 887,000 个 token，以及运行 23 个 sub-agent 后产生的 $47,000 账单。

#### 资料来源
- [Getting Better at Working With You: Compiling User Corrections into Runtime Enforcement for Coding Agents](../Inbox/2026-06-11--getting-better-at-working-with-you-compiling-user-corrections-into-runtime-enforcement-for-coding-agents.md): Trace 摘要，包含运行时检查和违规率结果。
- [A Five-Plane Reference Architecture for Runtime Governance of Production AI Agents](../Inbox/2026-06-10--a-five-plane-reference-architecture-for-runtime-governance-of-production-ai-agents.md): 带有能力控制和审计控制的运行时治理架构。
- [Show HN: Agent Joe – a Rust only coding agent with no shell access](../Inbox/2026-06-12--show-hn-agent-joe-a-rust-only-coding-agent-with-no-shell-access.md): Agent Joe 摘要，描述无 shell、仅限 Rust 的动作限制。
- [Claude Code v2.1.172: Sub-Agents Can Now Spawn Sub-Agents](../Inbox/2026-06-13--claude-code-v2-1-172-sub-agents-can-now-spawn-sub-agents.md): 嵌套 sub-agent 的限制、成本说法和 token 消耗示例。

### Harness 计量和 agent 基准测试
基准测试工作聚焦 agent harness，而不只看基础模型。Claw-SWE-Bench 固定任务集、提示、Docker 工作区、预算、补丁提取和评估器，让不同 harness 能在同一契约下比较。结果已经足以影响实际运行：使用同一个 GLM 5.1 模型时，最小 OpenClaw 适配器达到 19.1% Pass@1，而完整适配器达到 73.4%。

AgentBeats 处理相关的评估问题，把基准测试本身做成 judge agent。论文报告了一场持续五个月的竞赛，包含 298 个 judge agent 和 467 个 subject agent。EsoLang-Bench 增加了另一个压力测试。它把六个编码 agent 拉开了 88.4 个百分点，远高于同一摘要中 SWE-Bench Verified 报告的 6.6 个百分点差距。

#### 资料来源
- [Claw-SWE-Bench: A Benchmark for Evaluating OpenClaw-style Agent Harnesses on Coding Tasks](../Inbox/2026-06-10--claw-swe-bench-a-benchmark-for-evaluating-openclaw-style-agent-harnesses-on-coding-tasks.md): Claw-SWE-Bench 摘要，包含受控 harness 设计和 Pass@1 结果。
- [AgentBeats: Agentifying Agent Assessment for Openness, Standardization, and Reproducibility](../Inbox/2026-06-11--agentbeats-agentifying-agent-assessment-for-openness-standardization-and-reproducibility.md): AgentBeats 摘要，包含 judge-agent 评估和竞赛规模。
- [Frontier Coding Agents Use Metaprogramming to Adapt to Unfamiliar Programming Languages](../Inbox/2026-06-09--frontier-coding-agents-use-metaprogramming-to-adapt-to-unfamiliar-programming-languages.md): EsoLang-Bench 摘要，包含 agent 差距和陌生语言结果。

### 多 agent 编码的持久状态
状态成了工程中的一等对象。PROJECTMEM 在只追加的本地日志中记录问题、尝试、修复、决策和备注。它通过 Model Context Protocol (MCP) 暴露这段记忆；MCP 是一种把 agent 连接到外部上下文和动作的工具接口。它的动作前门控会在 agent 重复失败修复或编辑脆弱文件前发出警告。

DeLM 展示了同一需求的多 agent 版本。Agent 共享关于事实、失败假设、约束和部分解法的已验证要点，然后从队列中异步领取工作。在使用 Gemini 3 Flash 的 SWE-bench Verified 上，它报告每项任务成本 $0.12、65.7% Avg.@1；列出的基线为 $0.24 到 $0.26。Claude Code 的嵌套 agent 提供了独立上下文帧的商业示例，但成本证据支持设置明确的支出上限。

#### 资料来源
- [PROJECTMEM: A Local-First, Event-Sourced Memory and Judgment Layer for AI Coding Agents](../Inbox/2026-06-10--projectmem-a-local-first-event-sourced-memory-and-judgment-layer-for-ai-coding-agents.md): PROJECTMEM 摘要，包含事件日志、MCP 访问和动作前警告。
- [Decentralized Multi-Agent Systems with Shared Context](../Inbox/2026-06-09--decentralized-multi-agent-systems-with-shared-context.md): DeLM 摘要，包含共享已验证上下文和 SWE-bench 成本/性能结果。
- [Claude Code v2.1.172: Sub-Agents Can Now Spawn Sub-Agents](../Inbox/2026-06-13--claude-code-v2-1-172-sub-agents-can-now-spawn-sub-agents.md): Claude Code 嵌套 sub-agent 摘要，包含独立上下文帧和支出风险。

### 证明信号和更安全的软件工作
多个来源把验证视为 agent 工作循环的一部分。Jane Street 的形式化方法文章认为，agent 编写的代码会增加代码审查压力，而证明工具可以向 agent 提供测试之外的反馈。文章清楚给出了旧成本基线：seL4 花了 25 人年验证 8,700 行 C 代码，每行代码约需 23 行证明。

ComAct 展示了另一条通向更安全动作的路径：让专业软件控制变得可执行、可检查。在 CAD 工作流中，agent 通过 COM 接口编写 Python 脚本，然后用代码有效性和任务成功作为评估信号。报告的 ComCADBench 覆盖 SolidWorks、Inventor 和 AutoCAD 中的 1,000 个任务；摘要中基于 GUI 的 agent 成功率接近零。

#### 资料来源
- [Formal Methods and the Future of Programming](../Inbox/2026-06-14--formal-methods-and-the-future-of-programming.md): 形式化方法摘要，包含证明反馈说法和 seL4 成本基线。
- [ComAct: Reframing Professional Software Manipulation via COM-as-Action Paradigm](../Inbox/2026-06-11--comact-reframing-professional-software-manipulation-via-com-as-action-paradigm.md): ComAct 摘要，包含基于 COM 的执行、ComCADBench 和报告结果。
