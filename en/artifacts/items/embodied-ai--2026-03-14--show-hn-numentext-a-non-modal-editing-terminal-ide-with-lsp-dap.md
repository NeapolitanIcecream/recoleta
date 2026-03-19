---
source: hn
url: https://github.com/numentech-co/numentext
published_at: '2026-03-14T23:10:46'
authors:
- rlogman
topics:
- terminal-ide
- non-modal-editor
- lsp
- dap
- go-tooling
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Show HN: NumenText, a non-modal editing terminal IDE with LSP/DAP

## Summary
NumenText is a terminal IDE written in Go, centered on a **non-modal, menu-driven** editing experience, and provides modern code intelligence and debugging capabilities through the LSP/DAP protocols. It is aimed at users who do not want to learn Vim-style modal editing but still want full IDE functionality in the terminal.

## Problem
- The problem it addresses is that development tools in the terminal are often either too minimal or heavily dependent on modal editing paradigms such as Vim/Helix, creating a high learning barrier for some developers.
- This matters because many developers want an experience close to a desktop IDE in terminal/remote environments while retaining the advantages of being lightweight, fast, and deployable as a single binary.
- Existing solutions often require additional runtimes or reimplement complex language support themselves, which increases maintenance cost and complexity.

## Approach
- The core approach is to build a **small terminal IDE shell**: editor, terminal, file tree, command palette, build/run, and other core features are built into a single Go binary.
- Instead of reinventing language intelligence itself, it **delegates to standard protocols**: LSP for completion, navigation, hover, and diagnostics; DAP for breakpoints and step debugging.
- The interface uses a **non-modal, menu-driven** design, with default shortcuts aligned with traditional IDEs, such as Ctrl+S to save, F5 to run, and F9 to build, thereby lowering the learning curve.
- It supports multi-tab editing, an integrated PTY terminal, find/replace, quick open, resizable panels, and Vi/Helix keybinding modes as an optional compatibility layer.
- The design philosophy is to remain **small, fast, and simple**, handing complex language capabilities off to external language servers and debuggers while focusing itself on protocol integration and the terminal IDE experience.

## Results
- It provides syntax highlighting for **20+ languages**, implemented using Chroma.
- LSP automatically detects and integrates several mainstream language servers: **gopls, pyright, clangd, rust-analyzer, typescript-language-server**.
- DAP integration supports at least **3** debugging backends: **dlv, debugpy, lldb-vscode**, with support for breakpoints and step over/in/out.
- Build/run supports at least **8 languages**: C, C++, Go, Rust, Python, JavaScript, TypeScript, Java.
- From an implementation standpoint, it emphasizes **single binary, no runtime dependencies**, and requires **Go 1.25 or later**.
- The text **does not provide benchmark tests or quantitative comparison results** (such as performance, startup time, memory usage, or degree of improvement over other terminal IDEs); the strongest concrete claims are its non-modal terminal IDE experience, protocol-driven architecture, and relatively complete integration of development features.

## Link
- [https://github.com/numentech-co/numentext](https://github.com/numentech-co/numentext)
