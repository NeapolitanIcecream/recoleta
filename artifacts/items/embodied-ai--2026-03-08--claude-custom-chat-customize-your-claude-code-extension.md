---
source: hn
url: https://github.com/mattiagaggi/claude-custom-chat
published_at: '2026-03-08T23:29:39'
authors:
- mattiagaggi
topics:
- vscode-extension
- claude-cli
- self-modifying-tool
- mcp
- developer-tools
relevance_score: 0.06
run_id: materialize-outputs
---

# Claude Custom Chat – customize your Claude Code extension

## Summary
这是一个面向 VS Code/Cursor 的 Claude Code CLI 聊天扩展，核心卖点是“开发模式”下可让 Claude 读取并修改扩展自身源码，并通过快照与回滚机制降低试错风险。它更像开发工具产品说明而非研究论文，重点在自修改工作流、编辑器集成和安全边界设计。

## Problem
- 现有 Claude CLI/编辑器聊天体验缺少**可定制的原生界面**与面向扩展开发的闭环修改流程。
- 让模型直接改宿主扩展代码有较高风险；如果没有**快照、回滚、作用域限制**，试验容易破坏可用性。
- 对开发者而言，手动改代码、编译、重载、撤销的循环繁琐，降低了快速 UI/功能迭代效率。

## Approach
- 提供一个 VS Code/Cursor 扩展，作为 Claude Code CLI 的自定义聊天前端，负责进程管理、会话持久化、权限管理和 Webview UI。
- 引入 **Dev Mode**：激活后自动创建源码快照，并通过 MCP 向 Claude 暴露受限工具，使其能先调用 `get_extension_source` 获取结构，再对扩展目录内文件执行 Read/Write/Edit。
- 修改后自动触发编译，并提示用户重载窗口；若效果不佳，可用“回滚到最新快照”或“选择任意快照回滚”恢复状态。
- 安全机制包括：文件路径校验仅限扩展目录、所有回滚需确认、快照持久化到磁盘、回滚后自动重编译验证。
- 额外提供图谱视图、成本/Token 跟踪、多会话标签等工程化功能，增强开发和调试体验。

## Results
- 文本**没有提供标准研究实验或量化评测结果**，没有数据集、指标、基线或消融实验。
- 具体能力声明：支持 **VS Code、Cursor 及其他 VS Code forks**；支持 **macOS（ARM64/Intel）、Linux（Ubuntu/Debian/Fedora）、Windows 10/11**。
- 运行依赖要求包括 **Node.js 16+**、Git、`@anthropic/claude` CLI，以及有效 Claude API key 或 Pro/Max 订阅。
- Dev Mode 快照内容包含 **时间戳、Git branch、commit hash、全部 `src/` 源文件内容**，以 `snapshot-{timestamp}.json` 形式持久化到 `.devmode-snapshots/`。
- 架构上将系统拆为 **Handlers / Managers / Webview / Claude CLI process** 四层，并声明支持自动编译、窗口重载、可视化提示栏和基于 Cytoscape.js 的代码关系图视图。
- 最强的实际主张是：这是“**第一个可以修改自身的 Claude 扩展**”，并能在修改后通过快照回滚实现相对安全的自举式扩展开发流程。

## Link
- [https://github.com/mattiagaggi/claude-custom-chat](https://github.com/mattiagaggi/claude-custom-chat)
