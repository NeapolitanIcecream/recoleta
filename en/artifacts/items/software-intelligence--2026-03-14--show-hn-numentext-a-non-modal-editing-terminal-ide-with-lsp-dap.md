---
source: hn
url: https://github.com/numentech-co/numentext
published_at: '2026-03-14T23:10:46'
authors:
- rlogman
topics:
- terminal-ide
- lsp
- dap
- code-editor
- go
relevance_score: 0.76
run_id: materialize-outputs
language_code: en
---

# Show HN: NumenText, a non-modal editing terminal IDE with LSP/DAP

## Summary
NumenText is a terminal IDE written in Go, emphasizing a non-modal, menu-driven experience with familiar shortcuts that work out of the box. By integrating LSP/DAP, build-and-run, and terminal capabilities, it offers a relatively complete development workflow while remaining a single binary with a lightweight design.

## Problem
- Terminal editors often lean toward Vim-style modal interaction, which has a high learning curve and is not suitable for users who want an IDE experience that “just works.”
- Many lightweight terminal tools lack the language intelligence, debugging, build/run, and project navigation capabilities required for modern development.
- This matters because developers want efficiency close to a graphical IDE within a terminal environment, while avoiding complex dependencies and heavy installation.

## Approach
- The core idea is to build a **non-modal, menu-driven** terminal IDE: familiar shortcuts such as Ctrl+S, Ctrl+C, F5, and F9 can be used directly, without requiring users to learn Vim-style operations.
- It delegates “intelligent capabilities” to standard protocols rather than reimplementing language features itself: **LSP** provides completion, navigation, hover, and diagnostics, while **DAP** provides breakpoints and step debugging.
- Technically, it is implemented in Go and packaged as a **single binary** with no runtime dependencies, maintaining a “small and fast” design philosophy.
- Functionally, it integrates multi-tab editing, syntax highlighting for 20+ languages, an integrated PTY terminal, a file tree, find/replace, a command palette, quick open, resizable panels, and multi-language build/run support.
- At the same time, it accommodates different user habits by supporting switching between Vi and Helix keybinding modes, while still centering the default experience on non-modal interaction.

## Results
- It provides syntax highlighting for **20+ languages**, with coverage powered by Chroma.
- It can automatically detect and connect to multiple language servers: **gopls, pyright, clangd, rust-analyzer, typescript-language-server**; debugger support includes **dlv, debugpy, lldb-vscode**.
- Built-in build/run support covers at least **9 languages**: C, C++, Go, Rust, Python, JavaScript, TypeScript, and Java, along with related workflow shortcuts (such as **F5 to run, F9 to build**).
- The architecture is clearly modular, including components such as editor, terminal, lsp, dap, runner, filetree, and config, indicating that it has implemented a complete IDE backbone rather than being just a standalone editor.
- The text **does not provide benchmark tests, user studies, or quantitative comparisons with other IDEs/editors**, so its “breakthrough” is primarily reflected in the product combination: integrating editing, language intelligence, debugging, and execution inside the terminal in a single-binary form.

## Link
- [https://github.com/numentech-co/numentext](https://github.com/numentech-co/numentext)
