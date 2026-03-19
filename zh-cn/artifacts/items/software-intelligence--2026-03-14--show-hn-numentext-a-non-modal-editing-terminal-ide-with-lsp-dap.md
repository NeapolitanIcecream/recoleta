---
source: hn
url: https://github.com/numentech-co/numentext
published_at: '2026-03-14T23:10:46'
authors:
- rlogman
topics:
- terminal-ide
- lsp
- dap
- code-editor
- go
relevance_score: 0.76
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: NumenText, a non-modal editing terminal IDE with LSP/DAP

## Summary
NumenText 是一个用 Go 编写的终端 IDE，主打非模态、菜单驱动和开箱即用的常见快捷键体验。它通过集成 LSP/DAP、构建运行与终端能力，在保持单二进制和轻量设计的前提下提供较完整的开发工作流。

## Problem
- 终端编辑器往往偏向 Vim 式模态交互，学习成本高，不适合想要“直接可用”IDE 体验的用户。
- 许多轻量终端工具缺少现代开发所需的语言智能、调试、构建运行和项目导航能力。
- 这很重要，因为开发者希望在终端环境中获得接近图形 IDE 的效率，同时避免复杂依赖和沉重安装。

## Approach
- 核心思路是做一个**非模态、菜单驱动**的终端 IDE：常见快捷键如 Ctrl+S、Ctrl+C、F5、F9 可直接使用，不要求学习 Vim 式操作。
- 它把“智能能力”委托给标准协议，而不是自己重做一遍语言功能：通过 **LSP** 提供补全、跳转、悬停、诊断，通过 **DAP** 提供断点和单步调试。
- 工程上采用 Go 实现，打包为**单一二进制**，无运行时依赖，保持“小而快”的设计哲学。
- 功能上整合多标签编辑、20+ 语言语法高亮、集成 PTY 终端、文件树、查找替换、命令面板、快速打开、可调面板，以及多语言构建运行。
- 同时兼容不同用户习惯，支持 Vi 和 Helix 键位模式切换，但默认仍以非模态体验为中心。

## Results
- 提供了 **20+ 语言**的语法高亮，覆盖面来自 Chroma。
- 可自动检测并接入多个语言服务器：**gopls、pyright、clangd、rust-analyzer、typescript-language-server**；调试器支持 **dlv、debugpy、lldb-vscode**。
- 内置构建/运行支持至少 **9 种语言**：C、C++、Go、Rust、Python、JavaScript、TypeScript、Java，以及相关工作流快捷键（如 **F5 运行、F9 构建**）。
- 架构上明确模块化：包含 editor、terminal、lsp、dap、runner、filetree、config 等组件，说明其已实现完整 IDE 主干而非单一编辑器。
- 文本中**没有提供基准测试、用户研究或与其他 IDE/编辑器的定量对比结果**，因此其“突破”主要体现在产品组合：在终端内以单二进制方式集成编辑、语言智能、调试与运行能力。

## Link
- [https://github.com/numentech-co/numentext](https://github.com/numentech-co/numentext)
