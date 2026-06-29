---
source: hn
url: https://github.com/prettysmartdev/ane
published_at: '2026-05-16T23:08:01'
authors:
- archnet
topics:
- code-editing
- lsp
- code-agents
- cli-tools
- software-automation
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Ane: CLI editor that uses LSPs to let agents explore/edit code with fewer tokens

## Summary
## 概要
ane 是一款面向人类和代码代理的终端代码编辑器，带有 chord 命令，可通过 LSP 和 tree-sitter 支持读取或编辑狭窄的代码区域。
它主打更少的 token 消耗来浏览代码和做精确的 CLI 编辑，但摘录里没有基准数据。

## 问题
- 代码代理常常读取整份文件或应用很宽的文本补丁，这会浪费上下文 token，也更容易改错代码。
- 终端编辑器通常面向人类交互使用，而代理工作流需要可脚本化命令、窄范围代码选择和机器可读的 diff。
- 这个工具对自动化软件工作有用，因为代理可以检查或修改一个函数、签名、行或符号，而不是把整份文件送进模型。

## 方法
- ane 定义了一个四段式 chord 语法：action、positional、scope 和 component。示例 chord 包括 `cifc`，用于修改函数内容；`lefn`，用于列出函数名；以及 `cefd`，用于修改函数定义。
- `ane exec` 可以从命令行以无界面方式执行读取或编辑，并在修改时输出 unified diff，这样代理就能把它当作工具调用。
- 基于 LSP 的 chord 目标是函数、变量、结构体和成员等语言结构。行、buffer 和 delimiter chord 不依赖 LSP。
- 这个项目为 Rust、Go、TypeScript/JavaScript 和 Python 提供语言感知 chord，并在所有支持语言上使用 tree-sitter 做语法高亮。
- Rust crate 暴露了 chord 解析、执行、buffer 处理，以及一个可直接序列化的 LLM 工具定义，适用于 Claude、OpenAI 和类似的 tool-use API。

## 结果
- 摘录没有给出定量基准结果、数据集、token 节省测量，也没有和其他编辑器或代码代理工具做对比。
- 明确的能力主张：`ane exec` 可以读取或编辑单个函数体、函数名、函数定义、行、buffer 或 delimiter 范围，并返回 unified diff。
- 明确的设计主张：chord 模型有 4 个部分，因此可以把 change、delete、yank、list、jump、append 和 prepend 等操作组合成命令。
- 明确的语言主张：语言感知 chord 列出了 4 组语言，分别是 Rust、Go、TypeScript/JavaScript 和 Python。
- 明确的架构主张：代码库使用 3 层，分别是 data、commands 和 frontend，较低层不能导入较高层。
- 成熟度主张：这个项目还处在早期，版本大约是 `0.1`，作者说 chords、语言和 CLI/TUI 功能都还在推进中。

## Problem

## Approach

## Results

## Link
- [https://github.com/prettysmartdev/ane](https://github.com/prettysmartdev/ane)
