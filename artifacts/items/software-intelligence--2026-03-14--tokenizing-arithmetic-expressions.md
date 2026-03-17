---
source: hn
url: https://xnacly.me/posts/2023/calculator-lexer/
published_at: '2026-03-14T22:57:12'
authors:
- ibobev
topics:
- lexer
- arithmetic-parser
- interpreter
- go
- tdd
relevance_score: 0.47
run_id: materialize-outputs
---

# Tokenizing Arithmetic Expressions

## Summary
这篇文章是一个算术表达式解释器系列的第一部分，重点讲如何把输入字符串切分成可处理的词法记号（token）。它用 Go 和测试驱动开发（TDD）实现了一个支持基础算术、括号、注释与多种数字格式的简单 lexer。

## Problem
- 要解决的问题是：如何把像 `100_000+.5*(42-3.1415)/12` 这样的原始字符流，转换成后续解析器和解释器能理解的 token 序列。
- 这很重要，因为词法分析是解释器/编译器流水线的第一步；如果不能稳定识别数字、运算符、括号、空白和注释，后续 AST、字节码生成与执行都无法进行。
- 文章面向一个最小算术语言子集：加、减、乘、除，以及括号控制优先级。

## Approach
- 采用经典解释器分阶段设计：**lexical analysis → parsing → compiling to bytecode → executing bytecode**，本文只实现第一步 lexer。
- 用 Go 定义 `Token` 结构和一组 token 类型，包括 `NUMBER`、`PLUS`、`MINUS`、`ASTERISK`、`SLASH`、左右括号和 `EOF`。
- `Lexer` 基于 `bufio.Reader` 逐字符读取；通过 `advance()` 推进当前位置，通过 `Lex()` 循环识别空白、注释、符号和数字。
- 数字识别由 `number()` 完成，连续接收 `0-9`、`.`、`_`、`e`，因此支持如 `123`、`10_000`、`10e5`、`0.005`、`.5` 这类形式。
- 开发方式上使用表驱动测试和 TDD，先写空输入、空白、注释、符号、数字等测试，再逐步补齐实现。

## Results
- 成功实现了一个可运行的 arithmetic lexer，支持 **4 种运算符**：`+`、`-`、`*`、`/`，以及 **2 种括号 token**：`(`、`)`。
- 支持忽略 **4 类空白字符**：空格、换行 `\n`、回车 `\r`、制表符 `\t`；支持以 `#` 开头直到行尾的注释。
- 支持至少 **4 类数字格式测试**：普通整数 `123`、带下划线 `10_000`、科学记数式样 `10e5`、小数 `0.005`；示例还展示了 `.5` 与 `3.1415` 可被识别。
- 文中展示的测试集合全部通过：空输入、空白、注释、符号、以及多种数字格式的 `go test` 均为 **PASS**，但**没有提供性能、准确率或与其他 lexer/工具的基准对比数据**。
- 端到端示例 `100_000+.5*(42-3.1415)/12` 被切分为 **11 个有效 token + 1 个 EOF**，说明该 lexer 已能支撑后续解析与解释步骤。

## Link
- [https://xnacly.me/posts/2023/calculator-lexer/](https://xnacly.me/posts/2023/calculator-lexer/)
