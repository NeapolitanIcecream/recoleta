---
source: hn
url: https://github.com/LiteLLM-Labs/lite-harness
published_at: '2026-05-30T23:51:21'
authors:
- detente18
topics:
- coding-agents
- self-hosted-agents
- code-intelligence
- human-ai-interaction
- agent-orchestration
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Lite-Harness – Self-Hosted Cursor Agents (Use Claude Code/OpenCode)

## Summary
## 摘要
Lite-Harness 是一个自托管服务器，用来从 Claude Code、Codex、OpenCode、Cursor 和相关工具部署 AI 编码代理。团队可以在同一个地方运行定时代理、管理会话、存储密钥，并处理审批请求。

## 问题
- 把 opencode 和 claude-code 分开作为不同服务器运行的团队，需要维护多套服务、API 形式、会话存储、MCP 输入和提示配置。
- 这会影响共享编码代理工作，因为每个 harness 都有自己的会话、工具和审批路径。

## 方法
- 将每个受支持的 harness 包装在一个兼容 OpenCode 的 API 服务器后面。
- 以单个 Docker 容器交付，并连接到 LiteLLM 网关，使用 `LITELLM_API_BASE`、`LITELLM_API_KEY` 和 `MASTER_KEY`。
- 在设置了密钥时，通过 E2B 或 Daytona 在隔离的 Linux 沙箱里按 cron 运行代理。
- 存储 vault 密钥，并在诸如 LinkedIn 私信等操作前通过 Inbox UI 路由人工审批。
- 通过挂载数据目录或设置 `DB_PATH` 来持久化历史记录和模型上下文。

## 结果
- 摘录中没有提供基准测试结果、准确率指标或用户研究数据。
- 声称支持 4 个 harness：`opencode`、`claude-code`、`github-copilot` 和 `codex`。
- 示例部署了一个每个工作日每 4 小时运行一次、每次发送前都需要人工审批的代理。
- 服务器通过 Docker 在本地的 `4096` 端口运行。
- 示例部署创建了 1 个代理，挂载了 vault 密钥，设置了计划任务，并启动了 1 次测试运行。

## Problem

## Approach

## Results

## Link
- [https://github.com/LiteLLM-Labs/lite-harness](https://github.com/LiteLLM-Labs/lite-harness)
