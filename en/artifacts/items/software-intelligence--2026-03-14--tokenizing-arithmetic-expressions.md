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
language_code: en
---

# Tokenizing Arithmetic Expressions

## Summary
This article is the first part of a series on building an arithmetic-expression interpreter, focusing on how to split an input string into processable lexical tokens. Using Go and test-driven development (TDD), it implements a simple lexer that supports basic arithmetic, parentheses, comments, and multiple number formats.

## Problem
- The problem to solve is: how to transform a raw character stream like `100_000+.5*(42-3.1415)/12` into a sequence of tokens that a later parser and interpreter can understand.
- This matters because lexical analysis is the first step in the interpreter/compiler pipeline; if numbers, operators, parentheses, whitespace, and comments cannot be recognized reliably, subsequent AST construction, bytecode generation, and execution cannot proceed.
- The article targets a minimal subset of an arithmetic language: addition, subtraction, multiplication, division, and parentheses for controlling precedence.

## Approach
- It follows the classic staged interpreter design: **lexical analysis → parsing → compiling to bytecode → executing bytecode**, and this article implements only the first step, the lexer.
- In Go, it defines a `Token` structure and a set of token types, including `NUMBER`, `PLUS`, `MINUS`, `ASTERISK`, `SLASH`, left and right parentheses, and `EOF`.
- The `Lexer` reads character by character using `bufio.Reader`; it advances the current position via `advance()` and uses `Lex()` to repeatedly recognize whitespace, comments, symbols, and numbers.
- Number recognition is handled by `number()`, which continuously accepts `0-9`, `.`, `_`, and `e`, thus supporting forms such as `123`, `10_000`, `10e5`, `0.005`, and `.5`.
- For development, it uses table-driven tests and TDD: first writing tests for empty input, whitespace, comments, symbols, numbers, and so on, then gradually filling in the implementation.

## Results
- It successfully implements a working arithmetic lexer supporting **4 operators**: `+`, `-`, `*`, `/`, and **2 parenthesis tokens**: `(`, `)`.
- It supports ignoring **4 kinds of whitespace**: space, newline `\n`, carriage return `\r`, and tab `\t`; it also supports comments starting with `#` and continuing to the end of the line.
- It supports at least **4 tested number formats**: regular integers `123`, underscored numbers `10_000`, scientific-notation style `10e5`, and decimals `0.005`; the examples also show that `.5` and `3.1415` can be recognized.
- All test sets shown in the article pass: `go test` for empty input, whitespace, comments, symbols, and multiple number formats all return **PASS**, but **no benchmark comparison data is provided for performance, accuracy, or against other lexers/tools**.
- The end-to-end example `100_000+.5*(42-3.1415)/12` is split into **11 valid tokens + 1 EOF**, showing that this lexer can already support the subsequent parsing and interpretation steps.

## Link
- [https://xnacly.me/posts/2023/calculator-lexer/](https://xnacly.me/posts/2023/calculator-lexer/)
