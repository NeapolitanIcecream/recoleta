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
language_code: en
---

# Codix: Code indexing and refactoring tools for AI agents

## Summary
Codix is a local code indexing and query tool for AI coding agents. Using SQLite + tree-sitter, it provides symbol lookup, reference analysis, and relationship queries, reducing the inefficiency and token waste of searching code with grep. It emphasizes agent-friendliness: compact output, JSON support, and automatic incremental index refresh during queries.

## Problem
- When navigating large codebases, AI coding agents often rely on grep and guesswork, which is neither precise nor efficient and consumes a large amount of context tokens.
- Agents need reliable symbol-level query capabilities, such as “where is this defined,” “who references it,” and “what implementations/call relationships exist,” otherwise refactoring and code understanding become fragile.
- This matters because more accurate, lower-token-cost code navigation can directly improve the efficiency and stability of AI agents when modifying, analyzing, and refactoring code.

## Approach
- Uses **tree-sitter** to parse source code and extract indexed symbols such as classes, methods, and fields, along with their relationships, rather than doing plain-text search.
- Stores symbols and relationships in a local **SQLite** database (`.codix/index.db`), and provides commands such as `find`, `refs`, `callers`, and `impls` for querying.
- During queries, it automatically detects stale indexes based on file modification time and rebuilds changed files, keeping results “always fresh”; when needed, `codix index` can be used for a full rebuild.
- It is deliberately designed for AI agents: running the CLI with no arguments shows usage, text output is compact to save tokens, `-f json` provides structured output, and matching supports globs over both simple names and fully qualified names.
- Supports multi-language installation features (Go/Java/JavaScript/TypeScript/Python/Rust), but the text also explicitly states that currently only **Java** is actually usable; other languages will produce clear errors.

## Results
- The text **does not provide standard paper-style quantitative experimental results**; it gives no accuracy, recall, speed benchmarks, or numerical comparisons against grep/ctags/LSP.
- The strongest concrete claim is that, through symbol-level indexing and relationship queries, AI agents can “navigate code without burning tokens on grep and guesswork,” enabling more efficient codebase navigation.
- The system claims to support **automatic incremental re-indexing** (based on mtime) and **local SQLite persistent indexes** to enable fast, accurate queries, but provides no timing numbers.
- Supported query capabilities include: symbol definition lookup (`find`), reference lookup (`refs`), caller analysis (`callers`), and implementation lookup (`impls`); output can be either compact text or JSON.
- Limitations are also clear: currently only Java is practically usable; local variables/parameters are not indexed; and it cannot recognize references in reflection, Javadoc `@link`/`@see`, or string literals.

## Link
- [https://github.com/ogregoire/codix](https://github.com/ogregoire/codix)
