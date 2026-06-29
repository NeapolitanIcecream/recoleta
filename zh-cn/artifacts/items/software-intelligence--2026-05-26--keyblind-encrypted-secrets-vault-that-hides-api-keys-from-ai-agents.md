---
source: hn
url: https://github.com/aarifmms/keyblind
published_at: '2026-05-26T22:47:33'
authors:
- aarifshaikhs
topics:
- ai-agent-security
- secrets-management
- mcp
- developer-tools
- code-intelligence
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Keyblind – encrypted secrets vault that hides API keys from AI agents

## Summary
## 概述
Keyblind 是一个面向 AI 编码代理的本地加密密钥库。它通过给代理提供假的 `.env` 值，并在命令运行时才解析真实密钥，把真实 API 密钥排除在模型上下文之外。

## 问题
- AI 编码工具可以读取 `.env` 文件，并把 API 密钥、令牌和密码发送到 LLM 对话或提交记录中。
- 摘要提到，2025 年有 10 万+ 条包含泄露密钥的 LLM 对话被搜索引擎索引。
- 泄露的密钥可能导致账户接管、云资源费用上涨、数据暴露和软件交付被破坏。

## 方法
- Keyblind 把密钥存到本地 SQLite 密钥库中，并用 AES-256-GCM 加密。
- 它使用 PBKDF2 生成加密密钥，迭代 60 万次，然后用机器指纹对密钥做 XOR 包装。
- 一个 MCP 服务器提供 6 个工具，让代理可以列出密钥名或解析密钥，但不会在转录中看到明文。
- `keyblind sandbox` 会把 `.env` 值替换成按项目和密钥名生成的确定性 HMAC-SHA256 假值。
- `keyblind run -- <command>` 会在运行时把真实密钥作为环境变量注入。

## 结果
- 摘要没有给出基准测试、用户研究、攻击评估，也没有和 1Password CLI、Bitwarden CLI 或 dotenv vault 这类工具做比较。
- 它声称支持任何兼容 MCP 的编辑器，包括 Claude Code、Cursor、Windsurf、Copilot、Cline 和 Zed。
- 它声称没有网络访问、没有遥测、没有云账户，并且本地密钥库存放在 `~/.keyblind/`，权限为 `0700`。
- 它声称支持多个密钥后端，包括内置加密密钥库、1Password 和 Bitwarden。
- 与安全相关的数字包括 AES-256-GCM 加密、PBKDF2 60 万次迭代、6 个 MCP 工具，以及 10 万+ 条暴露的 LLM 对话，这些是它的动机事件规模。

## Problem

## Approach

## Results

## Link
- [https://github.com/aarifmms/keyblind](https://github.com/aarifmms/keyblind)
