---
source: hn
url: https://github.com/ogregoire/codix
published_at: '2026-03-11T22:55:06'
authors:
- olivergregory
topics:
- code-indexing
- ai-agent-tools
- code-navigation
- symbol-analysis
- refactoring
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Codix: Code indexing and refactoring tools for AI agents

## Summary
Codix is a local code symbol indexing and query tool for AI coding agents, replacing grep-style code search with a more precise, lower-token-cost approach. It parses a codebase and stores it in a local SQLite database, enabling agents to more reliably perform symbol lookup, reference finding, relationship analysis, and some refactoring-related operations.

## Problem
- When navigating large codebases, AI agents often rely on `grep` or fuzzy guesswork, which both consumes tokens and can easily misidentify symbol definitions, references, and implementation relationships.
- The lack of an agent-friendly local code indexing layer that provides structured output and automatically stays fresh as code changes reduces the efficiency of automated software development.
- This matters because code intelligence, automated software production, and multi-agent collaboration all depend on stable understanding of program structure rather than fragile text matching.

## Approach
- The core mechanism is straightforward: first use **tree-sitter** to parse source files, extract symbols such as classes, methods, and fields along with their relationships, and then store the results in a local **SQLite** database for fast querying.
- It provides agent-oriented command interfaces such as `find`, `refs`, `callers`, and `impls`, supporting glob matching by simple name or fully qualified name and directly returning definitions, references, and relationships.
- On each query, it automatically checks file modification times and rebuilds stale indexes as needed, aiming to ensure results always reflect the latest code state; `codix index` can be used for a full rebuild when necessary.
- Output supports both compact text and JSON: the former saves tokens, while the latter is convenient for programmatic consumption by agents; running without arguments also provides discoverable help information.
- The current parsing framework claims support for Go, Java, JavaScript/TypeScript, Python, and Rust, but the text also clearly states that **only Java is actually usable at present**, and other languages will produce a clear error.

## Results
- The text **does not provide formal benchmark experiments or quantitative evaluation results**, so there are no exact figures for speed, accuracy, recall, or numerical comparisons against baseline tools.
- Its strongest concrete claim is that replacing `grep/find` with local indexing enables more “precise” symbol lookup for AI agents and reduces “burning tokens on grep and guesswork,” but **it does not provide percentages for token savings or improvements in task success rate**.
- At the system implementation level, it specifies a verifiable capability scope: it supports queries such as `find`, `refs`, `callers`, and `impls`; the index is stored in `.codix/index.db`; and during queries it automatically rebuilds indexes for modified files based on **mtime**.
- The list of supported languages contains **5 languages**: Go, Java, JavaScript/TypeScript, Python, and Rust; but the limitation is also explicit: **currently only Java is usable**.
- Indexed objects are limited to declared symbols (such as classes, methods, and fields); it **does not support** local variables or parameters, and it also **does not detect** references in reflection, Javadoc `@link/@see`, or string literals.

## Link
- [https://github.com/ogregoire/codix](https://github.com/ogregoire/codix)
