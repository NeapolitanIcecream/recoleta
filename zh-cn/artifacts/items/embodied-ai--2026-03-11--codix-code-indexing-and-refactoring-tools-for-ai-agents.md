---
source: hn
url: https://github.com/ogregoire/codix
published_at: '2026-03-11T22:55:06'
authors:
- olivergregory
topics:
- code-indexing
- ai-coding-agents
- symbol-analysis
- refactoring-tools
- tree-sitter
- sqlite
relevance_score: 0.03
run_id: materialize-outputs
language_code: zh-CN
---

# Codix: Code indexing and refactoring tools for AI agents

## Summary
Codix 是一个面向 AI 编码代理的本地代码索引与查询工具，用 SQLite + tree-sitter 提供符号查找、引用分析和关系查询，减少用 grep 搜索代码时的低效与 token 浪费。它强调对代理友好：输出紧凑、支持 JSON、并在查询时自动增量刷新索引。

## Problem
- AI 编码代理在大代码库中导航时，常依赖 grep 和猜测，既不精确，也会消耗大量上下文 token。
- 代理需要可靠的符号级查询能力，如“定义在哪”“谁引用了它”“有哪些实现/调用关系”，否则重构和理解代码会很脆弱。
- 这很重要，因为更准确、更低 token 成本的代码导航能直接提升 AI 代理在修改、分析和重构代码时的效率与稳定性。

## Approach
- 用 **tree-sitter** 解析源代码，提取类、方法、字段等已索引符号及其关系，而不是做纯文本搜索。
- 将符号和关系存入本地 **SQLite** 数据库（`.codix/index.db`），提供 `find`、`refs`、`callers`、`impls` 等命令查询。
- 查询时基于文件修改时间自动检测陈旧索引并重建变更文件，保证结果“始终新鲜”；必要时可用 `codix index` 全量重建。
- 设计上专门面向 AI 代理：命令行无参数即可显示用法、文本输出紧凑节省 token、也支持 `-f json` 结构化输出，且匹配支持简单名与全限定名的 glob。
- 支持多语言安装特性（Go/Java/JavaScript/TypeScript/Python/Rust），但文中也明确说明当前实际仅 **Java** 可用，其它语言会报清晰错误。

## Results
- 文中**没有提供标准论文式定量实验结果**，没有给出准确率、召回率、速度基准或与 grep/ctags/LSP 的数值对比。
- 最强的具体主张是：通过符号级索引与关系查询，AI 代理可“无需在 grep 和猜测上燃烧 token”，从而更高效地导航代码库。
- 系统声称具备 **自动增量重索引**（基于 mtime）和 **本地 SQLite 持久化索引**，以支持快速、准确查询，但未给出耗时数字。
- 支持的查询能力包括：符号定义查找（`find`）、引用查找（`refs`）、调用者分析（`callers`）、实现查找（`impls`）；输出既可为紧凑文本，也可为 JSON。
- 限制也较明确：当前仅 Java 可实际使用；不支持局部变量/参数索引；不能识别反射、Javadoc `@link`/`@see` 或字符串字面量中的引用。

## Link
- [https://github.com/ogregoire/codix](https://github.com/ogregoire/codix)
