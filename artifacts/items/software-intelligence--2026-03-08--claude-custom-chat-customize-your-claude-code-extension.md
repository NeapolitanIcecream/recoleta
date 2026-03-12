---
source: hn
url: https://github.com/mattiagaggi/claude-custom-chat
published_at: '2026-03-08T23:29:39'
authors:
- mattiagaggi
topics:
- vscode-extension
- code-intelligence
- self-modifying-tools
- claude-cli
- developer-workflow
relevance_score: 0.88
run_id: materialize-outputs
---

# Claude Custom Chat – customize your Claude Code extension

## Summary
这是一个面向 VS Code/Cursor 的 Claude Code 聊天扩展，核心卖点是“开发模式”下可让 Claude 在受限范围内查看并修改扩展自身源码，并通过快照回滚保证安全试验。它更像一个工程化产品/工具说明，而不是包含正式实验设计的研究论文。

## Problem
- 现有编辑器内的 Claude CLI 聊天体验较原生，缺少可定制 UI、源码内省与“自修改”工作流，导致开发者难以快速把 AI 助手变成适合自己流程的工具。
- 让模型直接改本地工具源码存在风险：容易改坏、难回退、跨窗口重载后状态丢失，因此需要受控修改与可靠恢复机制。
- 在多平台编辑器环境中集成 Claude CLI 还涉及安装、编译、进程管理、权限控制和可视化等工程复杂度，这会影响实际可用性。

## Approach
- 提供一个 VS Code/Cursor 扩展作为 Claude Code CLI 的自定义聊天前端，负责 UI、会话管理、权限处理、CLI 进程通信和图视图等功能。
- 引入 Dev Mode：激活后自动创建源码快照，并通过 MCP 暴露受限工具给 Claude，使其先调用 `get_extension_source` 获取结构概览，再用 Read/Write/Edit 只在扩展目录内修改代码。
- 用持久化快照实现安全自修改：每次进入开发模式会把 `src/` 内文件保存为 JSON 快照，记录时间戳、分支、commit hash，支持“回滚到最新快照”或“选择任意快照回滚”。
- 修改后自动编译并提示重载，结合 tips bar 展示开发模式状态、文件变更和编译信息，形成“提需求→Claude改代码→重载测试→不满意即回滚”的闭环。
- 通过路径校验、作用域限制、确认对话框和 git-ignore 的快照目录，降低模型访问越界或误改造成的风险。

## Results
- 文本**没有提供正式基准测试、消融实验或定量指标**，因此没有可报告的 accuracy / latency / success rate 等研究数据。
- 最强的具体主张是：该项目声称自己是“**first Claude extension that can modify itself**”，即首个可以自修改的 Claude 扩展，但文中未给出对比实验或第三方验证。
- 兼容性声明覆盖 **3 类操作系统**：macOS（ARM64/Intel）、Linux（Ubuntu/Debian/Fedora）和 Windows 10/11（PowerShell）。
- 编辑器支持声明覆盖 **至少 3 类环境**：VS Code、Cursor、以及其他 VS Code forks（如 Antigravity）。
- Dev Mode 中暴露 **4 类核心能力/工具入口**：`get_extension_source`、Read、Write、Edit；快照包含 **4 类关键信息**：timestamp、branch、commit hash、files。
- 快照机制的最具体工程结果是：快照持久化到 `.devmode-snapshots/`，可在**窗口重载和扩展重启后继续回滚**，并在回滚后触发自动重新编译。

## Link
- [https://github.com/mattiagaggi/claude-custom-chat](https://github.com/mattiagaggi/claude-custom-chat)
