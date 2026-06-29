---
source: hn
url: https://github.com/botcircuits-ai/botcircuits-agent
published_at: '2026-05-31T23:21:43'
authors:
- nexcatara
topics:
- ai-agents
- workflow-automation
- llm-tool-use
- state-machines
- mcp
- human-ai-interaction
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# New AI Agent Architecture to fix LLM deviations and token costs

## Summary
## 摘要
BotCircuits 提出了一种代理设计：确定性工作流引擎控制多步流程，LLM 在每一步里负责推理和工具调用。这个摘录来自产品 README，所以只有架构和用法细节，没有基准证据。

## 问题
- 在长任务里，LLM 驱动的代理会偏离，因为模型同时决定做什么和如何路由流程。
- 多步自动化会消耗更多 token，因为模型在每一步都会重新评估控制流。
- 团队需要能通过 CLI、HTTP、聊天和定时任务运行的代理，同时还要让工具执行过程可见、可配置。

## 方法
- 工作流是放在 `.botcircuits/workflows/` 下的 JSON 记录；经过构建步骤后，每个工作流都会变成一个可调用工具。
- LLM 执行每个 `agentAction`，而引擎遵循 `start`、`next` 和已编译的分支条件。
- 自然语言分支条件会编译成带运算符和值的 `choices[]` 条目，`flow.variables` 告诉运行时在分支前如何强制转换输入。
- 技能是磁盘上的文件夹，里面有 `SKILL.md` 说明和可选的 `allowed-tools`，这样就能在不改系统提示词的情况下增加可重复的行为。
- MCP 服务器、内置文件/ shell / code 工具、FastAPI 网关和消息通道扩展了代理可以执行操作的地方。

## 结果
- 没有提供 token 成本、任务成功率、延迟或偏离率的基准结果。
- 这里最具体的主张是架构层面的：条件构建完成后，运行时分支可以在不再调用 LLM 的情况下发生。
- README 显示支持 3 个 LLM 提供方：Anthropic、OpenAI 和 Gemini。
- 工作流编写至少支持 2 种步骤类型：`start` 和 `agentAction`；分支使用 `conditions` 和 `next` 字段。
- 网关可以在一个 FastAPI 进程里路由至少 4 种通道类型：WhatsApp、Slack、通用 webhook 和 cron。
- 示例工作流有 11 个步骤：`step_1` 到 `step_10` 加上 `end`，并通过 `end_id` 控制提前终止。

## Problem

## Approach

## Results

## Link
- [https://github.com/botcircuits-ai/botcircuits-agent](https://github.com/botcircuits-ai/botcircuits-agent)
