---
kind: ideas
granularity: week
period_start: '2026-06-08T00:00:00'
period_end: '2026-06-15T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- agent governance
- software engineering benchmarks
- agent memory
- runtime enforcement
- formal methods
tags:
- recoleta/ideas
- topic/coding-agents
- topic/agent-governance
- topic/software-engineering-benchmarks
- topic/agent-memory
- topic/runtime-enforcement
- topic/formal-methods
language_code: zh-CN
---

# 编码代理运行时控制

## 摘要
编码代理采用现在需要围绕运行时循环做具体工作：在完成前强制执行重复的用户纠正，在同一评分契约下比较代理 harness，并在代理编辑文件前为其提供既往修复和失败尝试的本地记录。

## 面向重复编码代理纠正的完成前验证器
使用编码代理的团队可以为反复出现的用户纠正添加一个小型强制执行层：从聊天历史中提取持久规则，附上适用性检查，并在代理将任务标记为完成前运行验证器。最先有用的规则通常是开发者已经反复提出的普通规则，例如清理临时调试文件、修改状态前先询问、避免使用被禁止的命令，或在提出补丁前运行必需测试。

Trace 给出了一个具体模式。它把用户纠正改写为原子规则，将这些规则与每个用户的规则库进行匹配，并把每条规则编译成适用性检查、指令和验证器。在报告的诊断集中，Mem0 仍然违反了 57.5% 的适用偏好检查。在 ClawArena 上，Trace 将留出偏好违规率从 100.0% 降至分布内的 37.6%，分布外降至 2.0%。

一个实用试点可以从最近 20 份编码代理记录开始，选出用户最常重复的五条纠正，并把它们实现为代理完成步骤中的阻塞检查。衡量方式很简单：统计这五条纠正在留出任务中被违反的频率，以及代理需要多少额外用户轮次。

### 资料来源
- [Getting Better at Working With You: Compiling User Corrections into Runtime Enforcement for Coding Agents](../Inbox/2026-06-11--getting-better-at-working-with-you-compiling-user-corrections-into-runtime-enforcement-for-coding-agents.md): Trace 描述了纠正挖掘、规则编译、运行时验证器，以及报告的违规率下降。
- [Getting Better at Working With You: Compiling User Corrections into Runtime Enforcement for Coding Agents](../Inbox/2026-06-11--getting-better-at-working-with-you-compiling-user-corrections-into-runtime-enforcement-for-coding-agents.md): 该来源给出了可执行编码代理纠正的具体例子，包括清理、命令，以及终止前的工作区条件。

## 用于选择编码代理的固定 harness 评估运行
比较编码代理的工程团队应把 harness 当作产品组件来测试，并固定任务集、提示模板、Docker 工作区、挂钟时间预算、补丁提取、预测格式、评估器、API 成本和挂钟时间。这对采购和内部采用有用，因为即使基础模型不变，代理结果也可能随适配器和执行契约而变化。

Claw-SWE-Bench 展示了这种影响的规模。在其 350 个实例的多语言基准上，使用最小 direct-diff 适配器的 OpenClaw 达到 19.1% Pass@1，而使用完整适配器、同一 GLM 5.1 模型时达到 73.4%。在多轮扫描中，在固定模型下，harness 选择使 Pass@1 最多变化 27.4 个百分点。Lite-80 子集与完整基准的结果接近，成本约为完整运行的 22.9%，因此重复做 harness 检查更可行。

评估两三个编码代理产品的团队可以借用这个结构，不必采用整个基准。选择一小组内部问题修复任务，要求每个系统在相同超时和工具权限下返回仓库 diff，并在通过率旁报告总 token、缓存读取、挂钟时间和补丁提取失败案例。

### 资料来源
- [Claw-SWE-Bench: A Benchmark for Evaluating OpenClaw-style Agent Harnesses on Coding Tasks](../Inbox/2026-06-10--claw-swe-bench-a-benchmark-for-evaluating-openclaw-style-agent-harnesses-on-coding-tasks.md): Claw-SWE-Bench 固定了评估契约，并报告了在固定模型下由适配器和 harness 选择带来的大幅差异。
- [Claw-SWE-Bench: A Benchmark for Evaluating OpenClaw-style Agent Harnesses on Coding Tasks](../Inbox/2026-06-10--claw-swe-bench-a-benchmark-for-evaluating-openclaw-style-agent-harnesses-on-coding-tasks.md): 论文摘要报告了 19.1% 对 73.4% Pass@1 的适配器结果，并指出准确率相近的系统之间存在成本差异。

## 带编辑预检查的编码代理本地项目事件日志
仓库团队可以在编码代理编辑文件前提供本地事件日志，以减少重复调试循环。可用的最低配置是一份只追加的问题、尝试、修复、决策和备注记录，再加上文件编辑前的预检查，用来警告与该路径相关的既往失败修复、未解决问题或脆弱文件。

PROJECTMEM 是这一模式的具体实现。它存储纯文本类型化事件，以确定性方式重建紧凑的 AI 可读摘要，通过 MCP 和 CLI 工具暴露这些摘要，并在编辑前包含 `precheck_file(path)`。论文估计，重建项目上下文每个会话可能消耗 5,000 到 20,000 个 token，并报告已发布的 Python 包包含 14 个 MCP 工具、19 条 CLI 命令和 37 个自动化测试。它的评估是跨 10 个项目、为期两个月的自我研究，因此任务成功率主张仍需要受控检查。

一个低成本采用测试是在一个维护负担较重的仓库中加入该日志，运行两周。跟踪代理重复失败修复的频率、会话开始时重新读取上下文花费的 token 数，以及预检查警告阻止编辑已知高风险文件的频率。

### 资料来源
- [PROJECTMEM: A Local-First, Event-Sourced Memory and Judgment Layer for AI Coding Agents](../Inbox/2026-06-10--projectmem-a-local-first-event-sourced-memory-and-judgment-layer-for-ai-coding-agents.md): PROJECTMEM 描述了本地事件日志、MCP 访问、行动前警告层，以及报告的实现细节。
- [PROJECTMEM: A Local-First, Event-Sourced Memory and Judgment Layer for AI Coding Agents](../Inbox/2026-06-10--projectmem-a-local-first-event-sourced-memory-and-judgment-layer-for-ai-coding-agents.md): 摘要给出了 5,000–20,000 token 的上下文重建估计，以及只追加事件日志设计。
