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
language_code: en
---

# Tokenizing Arithmetic Expressions

## Summary
This article introduces the first step in implementing an arithmetic expression interpreter in Go: lexical analysis, which splits an input string into typed tokens. Its focus is on using TDD to incrementally build a lexer that supports numbers, operators, parentheses, whitespace, and comments, laying the groundwork for later AST parsing and bytecode execution.

## Problem
- The problem to solve is: how to reliably convert raw arithmetic expression text into a structured token sequence for subsequent parsing and execution.
- This matters because lexical analysis is the entry point of the interpreter/compiler pipeline; if tokenization is unstable, later precedence handling, AST construction, and execution will all go wrong.
- The article focuses on a minimal expression subset: `+ - * /`, parentheses, and several numeric formats (such as `10_000`, `10e5`, `0.005`).

## Approach
- It adopts a classic phased interpreter design: **lexing → parsing → compiling to bytecode → executing bytecode**, and this article implements only the first-stage lexer.
- The core mechanism is simple: maintain a `Lexer` that reads the input character by character; skip whitespace, skip whole-line comments when encountering `#`, directly emit the corresponding token when encountering a symbol, and enter `number()` to continuously read a complete numeric string when encountering a digit.
- Token types are represented with Go `iota` constants, including `TOKEN_NUMBER`, operators, left and right parentheses, and `TOKEN_EOF`; each token stores `Type` and the original string `Raw`.
- Number recognition allows the character set `0-9`, `.`, `_`, `e`, so it supports integers, decimals, some forms of scientific notation, and underscore-separated digits.
- The implementation follows TDD: write table-driven tests first, then add functions such as `NewLexer`, `advance()`, `Lex()`, and `number()`, gradually covering cases like empty input, whitespace, comments, symbols, and numbers.

## Results
- The article **does not provide standard benchmark data, speed improvements, accuracy figures, or quantitative comparisons with other lexers**.
- The most concrete result given is that all tests pass: cases for empty input, whitespace, comments, symbols, ordinary numbers, numbers with underscores, numbers with `e`, and numbers with decimal points all `PASS`.
- There are **6 supported symbol categories**: `+`, `-`, `/`, `*`, `(`, `)`, and **1** `TOKEN_EOF` is appended to the end of the token sequence.
- It defines **9 token types** (including `TOKEN_UNKNOWN` and `TOKEN_EOF`).
- The example input `100_000+.5*(42-3.1415)/12` is successfully split into **12 tokens** (including EOF), containing structures such as numbers, plus, multiplication, parentheses, subtraction, and division.
- The article claims this implementation establishes a working foundation for subsequent AST construction, bytecode compilation, and virtual machine execution, but those parts are not experimentally validated in this article.

## Link
- [https://xnacly.me/posts/2023/calculator-lexer/](https://xnacly.me/posts/2023/calculator-lexer/)
