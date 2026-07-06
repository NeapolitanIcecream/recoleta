---
source: hn
url: https://terminai.app
published_at: '2026-07-05T23:46:24'
authors:
- emosenkis
topics:
- terminal-ai
- code-intelligence
- developer-tools
- mcp
- human-ai-interaction
- agentic-coding
relevance_score: 0.62
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: AI integrated in any terminal that's invisible until you need it

## Summary
## 摘要
Terminai 用一个按需打开的 AI 覆盖层包装普通终端，可接入 Codex、Claude Code 或其他 CLI 代理。它的主要主张是通过读取权限和需用户批准的写入操作提供更安全的终端辅助，同时把模型认证和路由交给用户现有的 AI CLI。

## 问题
- 终端 AI 代理需要 shell 上下文，但当命令会影响文件、进程或远程系统时，直接写入权限可能带来风险。
- 许多用户已经有偏好的 AI CLI、模型凭证和提供商设置，因此强制使用新提供商路径的终端助手会增加使用成本。
- 该产品对开发者工作流有意义，因为终端工作常在同一个会话中混合检查、命令生成、调试和文件修改。

## 方法
- Terminai 作为用户 shell 或其他命令外层的包装器运行，可用 `terminai` 或 `terminai -- <command> [arg1 arg2...]` 启动。
- 按下 `Ctrl+Space` 会打开一个覆盖层终端，并在其中运行选定的 AI CLI。
- 被包装的 shell 通过 Terminai MCP 服务器暴露上下文，向代理提供读取权限和受控写入权限。
- 写入操作需要用户批准，因此代理排队的 shell 输入必须先获得用户批准，才能进入被包装的终端。
- Codex 和 Claude Code 有内置预设；如果自定义 CLI 能使用 MCP URL 和上下文提示，也可以接入。

## 结果
- 摘录中没有提供基准测试、用户研究、延迟指标、准确率指标或任务完成对比。
- 该产品声称支持 3 种代理路径：Codex、Claude Code 和用户提供的 CLI 代理。
- 它声称支持 2 个操作系统：Linux 和 macOS。
- 它声称 Terminai 发起 0 个出站网络连接，且不收集用户数据；已配置的 AI CLI 负责认证和模型选择。
- 安装路径包括 Homebrew、使用 `cargo install --path src` 从源码构建，以及 GitHub releases。
- 作者将该软件标为 alpha 质量，并称自己把它作为日常主力工具使用；原生滚动和输入处理被列为实现中的困难部分。

## Problem

## Approach

## Results

## Link
- [https://terminai.app](https://terminai.app)
