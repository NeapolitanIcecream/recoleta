---
source: hn
url: https://github.com/erikqu/workbench-cli
published_at: '2026-06-26T22:38:59'
authors:
- erikqu
topics:
- coding-agents
- terminal-ui
- multi-agent-engineering
- developer-tools
- human-ai-interaction
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# Workbench: A TUI for parallel coding agents

## Summary
## 摘要
Workbench 是一个全屏终端 UI，用于并行运行多个编码代理 CLI。摘录描述的是一个开发者工具，具备基于 tmux 的持久会话、文件查看器、shell 面板和 git diff 跟踪，但没有给出基准评测。

## 问题
- 使用编码代理的开发者常常需要同时处理多个独立终端、编辑器标签、文件预览和 git diff，这会让并行代理工作更难跟踪。
- 如果进程状态没有保存在界面之外，UI 重启时代理会话可能会丢失或中断。
- 这个问题重要，因为多代理编码工作流需要清晰的会话边界、快速上下文切换和可见的文件变更。

## 方法
- Workbench 将每个工作区作为独立代理会话运行，并为代理面板、shell 终端和打开的文件提供独立标签栏。
- 它使用私有 tmux 服务器，让代理和终端进程在重新启动和热重载重启后仍保持运行。
- 它支持可插拔的编码代理 harness：默认是 Claude Code，也可通过命令标志切换到 Gemini、Goose、OpenCode 和 Cursor。
- 它在同一个终端 UI 中加入文件浏览器、只读文件查看器和实时 git 工作树 diff。
- 该应用使用 Bun、React 19 和 Silvery 构建，并依赖 Bun >= 1.3.5 提供的 PTY 支持。

## 结果
- 摘录没有报告定量基准结果、用户研究、延迟数据或编码任务成功率。
- 它声称支持 5 个具名编码代理后端：Claude Code、Gemini、Goose、OpenCode 和 Cursor。
- 它声称通过 tmux 提供持久代理和终端会话，并使用 socket 路径 `~/.workbench/tmux-ui.sock`。
- 它声称提供丰富的查看器，支持语法高亮文本、Markdown 预览/源码、图像、PDF、视频播放和 Mermaid 图。
- 它包含回归测试工具：`bun run typecheck`、`bun test`、`bun run check`，以及一套 Playwright 截图测试。

## Problem

## Approach

## Results

## Link
- [https://github.com/erikqu/workbench-cli](https://github.com/erikqu/workbench-cli)
