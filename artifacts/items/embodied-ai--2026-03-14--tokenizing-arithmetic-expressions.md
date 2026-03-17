---
source: hn
url: https://xnacly.me/posts/2023/calculator-lexer/
published_at: '2026-03-14T22:57:12'
authors:
- ibobev
topics:
- lexical-analysis
- interpreter
- tokenization
- go
- tdd
relevance_score: 0.01
run_id: materialize-outputs
---

# Tokenizing Arithmetic Expressions

## Summary
这篇文章介绍了一个用 Go 实现算术表达式解释器的第一步：词法分析，把输入字符串切分成带类型的 token。它的重点是用 TDD 逐步实现一个支持数字、运算符、括号、空白和注释的 lexer，为后续解析 AST 和字节码执行打基础。

## Problem
- 要解决的问题是：如何把原始算术表达式文本可靠地转换成结构化 token 序列，供后续解析和执行使用。
- 这很重要，因为词法分析是解释器/编译器流水线的入口；如果 token 化不稳定，后面的优先级处理、AST 构建和执行都会出错。
- 文章聚焦一个最小表达式子集：`+ - * /`、括号，以及多种数字写法（如 `10_000`、`10e5`、`0.005`）。

## Approach
- 采用经典解释器分阶段设计：**lexing → parsing → compiling to bytecode → executing bytecode**，本文只实现第一阶段 lexer。
- 核心机制很简单：维护一个 `Lexer`，逐字符读取输入；遇到空白就跳过，遇到 `#` 就跳过整行注释，遇到符号就直接生成对应 token，遇到数字就进入 `number()` 连续读取完整数字串。
- token 类型用 Go 的 `iota` 常量表示，包括 `TOKEN_NUMBER`、运算符、左右括号和 `TOKEN_EOF`；每个 token 保存 `Type` 和原始字符串 `Raw`。
- 数字识别允许字符集合 `0-9`、`.`、`_`、`e`，因此支持整数、小数、科学计数形式的一部分表示以及下划线分隔数字。
- 实现过程遵循 TDD：先写表驱动测试，再补 `NewLexer`、`advance()`、`Lex()`、`number()` 等函数，逐步覆盖空输入、空白、注释、符号和数字等情况。

## Results
- 文中**没有给出标准基准数据、速度提升、准确率或与其他 lexer 的量化对比结果**。
- 给出的最具体结果是测试全部通过：空输入、空白、注释、符号、普通数字、带下划线数字、带 `e` 数字、带小数点数字等用例均 `PASS`。
- 支持识别的符号共有 **6 类**：`+`、`-`、`/`、`*`、`(`、`)`，并在 token 序列末尾附加 **1 个** `TOKEN_EOF`。
- 定义了 **9 种** token 类型（含 `TOKEN_UNKNOWN` 与 `TOKEN_EOF`）。
- 示例输入 `100_000+.5*(42-3.1415)/12` 被成功切分为 **12 个 token**（含 EOF），其中包含数字、加号、乘号、括号、减号、除号等结构。
- 文章声称该实现为后续 AST 构建、字节码编译和虚拟机执行奠定了可工作的前置基础，但这部分尚未在本文中实验验证。

## Link
- [https://xnacly.me/posts/2023/calculator-lexer/](https://xnacly.me/posts/2023/calculator-lexer/)
