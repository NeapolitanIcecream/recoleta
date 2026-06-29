---
source: hn
url: https://github.com/ClickHouse/nerve
published_at: '2026-05-25T22:46:43'
authors:
- animetyan
topics:
- ai-agent-runtime
- self-hosted-agents
- multi-agent-software-engineering
- code-intelligence
- human-ai-interaction
- persistent-memory
relevance_score: 0.83
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Nerve – self hosted runtime for AI agents

## Summary
## 概述
Nerve 是一个自托管运行时，把 Claude Agent SDK 的代理变成可长期运行的个人代理或工作代理，具备记忆、任务、技能、定时任务和人工审批流程。它对基于代理的软件工作有用，因为它把持久化、调度、源数据接入和审批门槛打包成一个可部署服务。

## 问题
- 长期运行的代理需要跨会话保存状态、按计划执行任务，并且在需要决策时向人请求帮助；普通聊天界面不满足这些需求。
- 团队里的工作代理还需要审计轨迹、计划审批，以及在监控 CI、审查 PR 或编辑代码之前，安全处理不受信任的输入。
- 这个项目面向自托管，因此用户可以通过 CLI 代理，用自己的 Claude API key 或 Claude 订阅来运行这个运行时。

## 方法
- 这个运行时把 Claude Agent SDK 封装在一个 Python 进程里，配有 FastAPI 网关、React 网页界面、Telegram 通道、APScheduler 任务，以及可选的 Claude OAuth 代理。
- 它使用两层记忆：`MEMORY.md` 存放会注入提示词的精选热信息，`memU` 存在 SQLite 中，用于对话、事实、偏好和事件的语义回忆。
- 它把任务和技能存成由 SQLite 索引支持的 Markdown，因此代理可以在后续会话中读取、创建、更新和复用流程。
- 工作模式从一段自然语言目标开始，自己写 `TASK.md`，创建技能，设置定时任务，提出计划，并在实施前等待人工审批。
- 源数据接入会把 Telegram、Gmail、GitHub 通知和 GitHub 事件拉进共享收件箱，并带有提示注入警告和独立的消费者游标。

## 结果
- 摘要没有给出基准测试、用户研究、消融实验或任务完成指标，因此没有代理准确性或生产率提升的定量证据。
- 其声称的系统规模包括：大约 30 个自定义 MCP 工具、默认配置下最多 4 个并发代理会话，以及 3 种定时 AI 任务会话模式。
- 其声称的记忆控制包括：4 种记忆类型（`profile`、`event`、`knowledge`、`behavior`）、3 级质量过滤、余弦相似度 0.85 的语义去重，以及变更审计日志。
- 其声称的自动化节奏包括：每 15 分钟处理一次收件箱、每 4 小时做一次任务规划、每 12 小时提取一次技能，以及在个人模式下每周修订一次技能。
- 其声称的安全与审查功能包括：计划审批、拒绝和修订流程、无需 git 的文件快照差异、技能脚本 30 秒超时，以及完整的计划/会话日志。

## Problem

## Approach

## Results

## Link
- [https://github.com/ClickHouse/nerve](https://github.com/ClickHouse/nerve)
