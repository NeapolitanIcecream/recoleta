---
source: hn
url: https://github.com/numentech-co/numentext
published_at: '2026-03-14T23:10:46'
authors:
- rlogman
topics:
- terminal-ide
- non-modal-editor
- lsp
- dap
- go-tooling
relevance_score: 0.02
run_id: materialize-outputs
---

# Show HN: NumenText, a non-modal editing terminal IDE with LSP/DAP

## Summary
NumenText 是一个用 Go 编写的终端 IDE，主打**非模态、菜单驱动**的编辑体验，并通过 LSP/DAP 协议提供现代代码智能与调试能力。它面向不想学习 Vim 式模态编辑、但仍希望在终端中获得完整 IDE 功能的用户。

## Problem
- 解决的问题是：终端中的开发工具往往要么过于简陋，要么强依赖 Vim/Helix 等模态编辑范式，导致一部分开发者上手门槛高。
- 这很重要，因为很多开发者希望在终端/远程环境中获得接近桌面 IDE 的体验，同时保留轻量、快速、单二进制部署的优势。
- 现有方案常常需要额外运行时或自行实现复杂语言支持，而这会增加维护成本和复杂度。

## Approach
- 核心方法是做一个**小型终端 IDE 外壳**：编辑器、终端、文件树、命令面板、构建运行等基础功能内置在一个 Go 单二进制中。
- 语言智能不自己重复造轮子，而是**委托给标准协议**：用 LSP 做补全、跳转、悬停、诊断；用 DAP 做断点和单步调试。
- 界面采用**非模态、菜单驱动**设计，默认快捷键贴近传统 IDE，如 Ctrl+S 保存、F5 运行、F9 构建，从而降低学习成本。
- 支持多标签编辑、集成 PTY 终端、查找替换、快速打开、可调整面板，以及 Vi/Helix 键位模式作为可选兼容层。
- 设计哲学是保持“**小、快、简单**”，把复杂语言能力交给外部语言服务器和调试器，自己只做协议集成与终端 IDE 体验。

## Results
- 提供了 **20+ languages** 的语法高亮，使用 Chroma 实现。
- LSP 自动检测并集成多个主流语言服务器：**gopls、pyright、clangd、rust-analyzer、typescript-language-server**。
- DAP 集成支持至少 **3 个**调试后端：**dlv、debugpy、lldb-vscode**，支持断点、step over/in/out。
- 构建/运行支持至少 **8 种语言**：C、C++、Go、Rust、Python、JavaScript、TypeScript、Java。
- 工程实现上强调 **single binary, no runtime dependencies**，需要 **Go 1.25 or later**。
- 文本中**没有提供基准测试或定量对比结果**（如性能、启动时间、内存占用、相对其他终端 IDE 的提升幅度）；最强的具体主张是其非模态终端 IDE 体验、协议驱动架构以及较完整的开发功能集成。

## Link
- [https://github.com/numentech-co/numentext](https://github.com/numentech-co/numentext)
