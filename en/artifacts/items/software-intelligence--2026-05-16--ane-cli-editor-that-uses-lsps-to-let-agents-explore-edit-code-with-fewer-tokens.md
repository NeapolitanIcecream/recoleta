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
language_code: en
---

# Ane: CLI editor that uses LSPs to let agents explore/edit code with fewer tokens

## Summary
ane is a terminal code editor built for humans and code agents, with chord commands that can read or edit narrow code regions through LSP and tree-sitter support.
It targets lower-token code exploration and precise CLI edits, but the excerpt provides no benchmark evidence.

## Problem
- Code agents often read full files or patch broad text ranges, which wastes context tokens and raises the chance of editing the wrong code.
- Terminal editors usually target interactive human use, while agent workflows need scriptable commands, narrow code selection, and machine-readable diffs.
- The tool matters for automated software work because an agent can inspect or change one function, signature, line, or symbol instead of sending a whole file through the model.

## Approach
- ane defines a 4-part chord grammar: action, positional, scope, and component. Example chords include `cifc` for changing function contents, `lefn` for listing function names, and `cefd` for changing a function definition.
- `ane exec` runs headless edits or reads from the command line and outputs unified diffs for changes, so an agent can call it as a tool.
- LSP-backed chords target language constructs such as functions, variables, structs, and members. Line, buffer, and delimiter chords work without LSP.
- The project supports Rust, Go, TypeScript/JavaScript, and Python for language-aware chords, with tree-sitter syntax highlighting across supported languages.
- The Rust crate exposes chord parsing, execution, buffer handling, and a ready-to-serialize LLM tool definition for Claude, OpenAI, and similar tool-use APIs.

## Results
- The excerpt gives no quantitative benchmark results, no dataset, no token-savings measurement, and no comparison against editors or code-agent tools.
- Concrete capability claim: `ane exec` can read or edit a single function body, function name, function definition, line, buffer, or delimiter scope and return a unified diff.
- Concrete design claim: the chord model has 4 parts, giving composable commands for actions such as change, delete, yank, list, jump, append, and prepend.
- Concrete language claim: language-aware chords are listed for 4 language groups: Rust, Go, TypeScript/JavaScript, and Python.
- Concrete architecture claim: the codebase uses 3 layers: data, commands, and frontend, with lower layers barred from importing higher layers.
- Maturity claim: the project is early, versioned around `0.1`, and the author states that chords, languages, and CLI/TUI features are still in progress.

## Link
- [https://github.com/prettysmartdev/ane](https://github.com/prettysmartdev/ane)
