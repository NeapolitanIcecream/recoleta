---
kind: ideas
granularity: day
period_start: '2026-06-06T00:00:00'
period_end: '2026-06-07T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- agent control
- coding agents
- MCP
- desktop automation
- AI cost governance
- LLM safety
- context management
tags:
- recoleta/ideas
- topic/agent-control
- topic/coding-agents
- topic/mcp
- topic/desktop-automation
- topic/ai-cost-governance
- topic/llm-safety
- topic/context-management
language_code: zh-CN
---

# Agent control layers

## 摘要
Agent 部署已经走到这样一步：缺的工作落在模型调用之外，包括排队执行工具、受控桌面访问和预算化的上下文管理。现在出现的是一些小型控制层，团队可以拿它们去对照现有 agent 失败案例测试：429、危险的桌面操作、充满旧状态的长流程，以及大规模生成改动带来的审阅压力。

## Durable MCP queue for bursty agent tool calls
针对反复出现 429 或内部服务过载的 agent 团队，应在 agent 和共享 API 之间加一个小型任务队列。Aquifer 展示了这种层的形态：agent 通过 MCP 或 HTTP 提交任务，运行时把任务存入 SQLite，然后由按上游划分的 worker 按配置的请求速率和并发上限派发。示例配置把 `api.openai.com` 设为 10 RPS、3 个并发请求，把 `api.stripe.com` 设为 20 RPS、5 个并发请求，把内部后端设为 50 RPS、10 个并发请求。

一个有用的试点，是把一个高流量的 agent 工具包在持久化队列后面，记录失败调用、队列等待时间、重试次数和任务完成情况。测试应包含上游变慢，因为 Aquifer 的设计允许响应头把实际速率降到配置上限以下。这适合那些 agent 本来能工作，但一旦很多运行同时打到同一个后端就会失败的团队。

### 资料来源
- [Show HN: Aquifer – an MCP runtime for spiky agent tool traffic](../Inbox/2026-06-06--show-hn-aquifer-an-mcp-runtime-for-spiky-agent-tool-traffic.md): Aquifer queues MCP or HTTP jobs in SQLite, dispatches through per-upstream workers, supports live rate reduction, and gives concrete RPS and concurrency examples.
- [Show HN: Aquifer – an MCP runtime for spiky agent tool traffic](../Inbox/2026-06-06--show-hn-aquifer-an-mcp-runtime-for-spiky-agent-tool-traffic.md): The source describes distributed agents calling APIs in bursts and using Aquifer as a coordination layer before shared backends or external APIs.

## Accessibility-first MCP gateway for local desktop actions
做 coding agent 的用户仍会遇到离开编辑器的工作流：浏览器对话框、安装程序、原生应用和 OS 权限提示。clawdcursor 通过一个 MCP 入口暴露本地桌面操作，先尝试 accessibility tree，再退回到 OCR 或截图，并让每次调用都经过安全检查，从而让一种具体的桌面控制模式变得可行。它的紧凑接口只有 6 组工具，而 94 工具的完整接口仍保留给兼容和调试。

第一次落地测试应聚焦一个边界清楚的桌面工作流，例如填写本地应用表单、通过原生对话框保存文件，或完成一个基于浏览器的管理任务。评估时要记录哪些动作用了 accessibility 元数据，哪些动作回退到 OCR 或截图，哪些动作需要确认，以及批处理是否减少了工具调用次数。这样可以把桌面自动化放在具体用户任务上，也能从第一次试验开始把安全提示纳入工作流。

### 资料来源
- [AI Can now control your desktop](../Inbox/2026-06-06--ai-can-now-control-your-desktop.md): clawdcursor exposes desktop control through MCP, uses accessibility before OCR and screenshots, has 6 compact tool groups, and gates destructive actions through confirmation.
- [AI Can now control your desktop](../Inbox/2026-06-06--ai-can-now-control-your-desktop.md): The source describes the compact grouped surface, cross-platform support, accessibility-first operation, and batched deterministic actions.

## Budget-capped context rewriting tests for long agent runs
长时间运行的 coding agent 和基于语料的 agent 需要一种办法来清掉旧文件、失败路径、工具噪声和干扰证据。Context Sculpting 测试了一个双模型 harness，外层模型可以在内层 agent 的轮次之间放行、重写上下文、回滚或终止。可行性信号伴随着明确的成本提醒：在一个代码修复示例里，对照组在 7 轮、42.7 秒和约 $0.015 内通过，而使用 harness 的运行也通过了，但用了 12 轮、566.9 秒、约 $1.06，并触发了最大轮次保护。

一个实用测试应只在明确上限内允许上下文重写：最大重写次数、最大额外延迟、最大支出，以及在连续多次无改进编辑后立即停止。评估应比较通过率、总轮次、成本和审阅者可见的轨迹质量，任务应已知包含旧上下文或干扰文件。这样可以把上下文编辑变成针对特定长流程失败的可测干预，并在 agent 启动前先设好策略限制。

### 资料来源
- [Context Sculpting](../Inbox/2026-06-06--context-sculpting.md): Context Sculpting reports the two-model harness design, rewrite actions, pass-through results, active rewrite runs, and the coding repair cost and latency comparison.
