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
## 摘要
ane 是一个面向人类和代码代理的终端代码编辑器。它通过 LSP 和 tree-sitter 支持，用和弦命令读取或编辑较小的代码区域。
它的目标是用更少 token 探查代码，并进行精确的 CLI 编辑，但摘录没有提供基准测试证据。

## 问题
- 代码代理经常读取完整文件或修补大范围文本，这会浪费上下文 token，并增加改错代码的概率。
- 终端编辑器通常面向人类交互使用，而代理工作流需要可脚本化的命令、较小范围的代码选择，以及机器可读的 diff。
- 这个工具对自动化软件工作有用，因为代理可以检查或修改一个函数、签名、行或符号，而不用把整个文件发送给模型。

## 方法
- ane 定义了一个 4 部分和弦语法：action、positional、scope 和 component。示例和弦包括用于修改函数内容的 `cifc`、用于列出函数名的 `lefn`，以及用于修改函数定义的 `cefd`。
- `ane exec` 从命令行以无界面方式执行编辑或读取，并为变更输出 unified diff，因此代理可以把它作为工具调用。
- 基于 LSP 的和弦面向函数、变量、结构体和成员等语言结构。行、缓冲区和分隔符和弦无需 LSP 即可工作。
- 该项目为 Rust、Go、TypeScript/JavaScript 和 Python 支持语言感知和弦，并在受支持语言中通过 tree-sitter 提供语法高亮。
- 这个 Rust crate 暴露和弦解析、执行、缓冲区处理，以及可直接序列化的 LLM 工具定义，供 Claude、OpenAI 和类似的工具调用 API 使用。

## 结果
- 摘录没有给出量化基准结果、数据集、token 节省测量，也没有与编辑器或代码代理工具进行比较。
- 具体能力声明：`ane exec` 可以读取或编辑单个函数体、函数名、函数定义、行、缓冲区或分隔符作用域，并返回 unified diff。
- 具体设计声明：和弦模型有 4 个部分，可组合出 change、delete、yank、list、jump、append 和 prepend 等操作命令。
- 具体语言声明：语言感知和弦列出了 4 个语言组：Rust、Go、TypeScript/JavaScript 和 Python。
- 具体架构声明：代码库使用 3 层：data、commands 和 frontend，低层禁止导入高层。
- 成熟度声明：该项目仍处于早期，版本约为 `0.1`，作者表示和弦、语言以及 CLI/TUI 功能仍在开发中。

## Problem

## Approach

## Results

## Link
- [https://github.com/prettysmartdev/ane](https://github.com/prettysmartdev/ane)
