---
source: hn
url: https://github.com/oussamaKH63/peekai
published_at: '2026-06-21T23:38:15'
authors:
- ousskh63
topics:
- ai-agent-observability
- python-agents
- local-first-debugging
- llm-tracing
- multi-agent-workflows
- developer-tools
relevance_score: 0.64
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: PeekAI – Local-first observability for Python AI agents

## Summary
## 摘要
PeekAI 是一个用于 AI agent 的本地 Python 跟踪和调试工具。它记录 LLM 调用、工具调用、token、成本、错误和重放运行，不会把跟踪数据发送到托管服务。

## 问题
- Python agent 开发者在开发过程中需要检查 LLM 调用、工具使用、token 数量、成本、延迟和失败情况。
- LangSmith 和 Weights & Biases 等托管工具可能要求创建账户、上传云端数据并完成设置后，才能查看跟踪记录。
- 当跟踪记录可能包含提示词、输出、工具响应或用户数据，而开发者不想把这些数据发送给第三方时，本地存储很重要。

## 方法
- `peekai.init()` 在启动时对受支持的 SDK 客户端进行 monkey patch，因此现有的 OpenAI、Anthropic 或 LiteLLM 调用可以被跟踪，无需修改每个调用点。
- `@peekai.agent`、`@peekai.tool` 和 `@peekai.trace` 等装饰器会为 agent 工作流创建父子 span 树。
- 跟踪记录默认存储在本地 SQLite 数据库 `~/.peekai/peekai.db` 中，也可以使用自定义 `db_path`。
- CLI 提供跟踪列表、跟踪查看、统计、地图可视化、重放和清理命令。
- 重放可以重新运行过去的跟踪记录、替换模型，或注入更改后的工具响应，然后把重放保存为新的跟踪记录，便于并排比较。

## 结果
- 摘录中没有报告正式基准、准确率结果、延迟研究，也没有与 LangSmith、Weights & Biases 或基于 OpenTelemetry 的工具进行比较。
- 包含的 multi-agent 演示跟踪记录了 3 个 span：`researcher`、`writer` 和 `format_output`。
- 同一演示报告总运行时间为 3.6s、236 个 token，估算成本为 $0.000222。
- 该演示将 LLM 使用量拆分为：`researcher` 调用使用 102 个 token、成本 $0.000115；`writer` 调用使用 134 个 token、成本 $0.000107。
- 本地 UI 运行在 `http://localhost:8501`，包含 4 个页面：Dashboard、Traces、Trace View 和 Replay。
- 该包在配置中列出 3 个 SDK 集成目标：OpenAI、Anthropic 和 LiteLLM。

## Problem

## Approach

## Results

## Link
- [https://github.com/oussamaKH63/peekai](https://github.com/oussamaKH63/peekai)
