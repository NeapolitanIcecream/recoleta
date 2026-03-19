---
source: hn
url: https://github.com/houqp/kiorg
published_at: '2026-03-07T23:59:44'
authors:
- houqp
topics:
- file-manager
- vim-keybindings
- cross-platform
- egui
- developer-tools
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# Show HN: Kiorg – a battery included file manager for keyboard nerds

## Summary
Kiorg is a cross-platform file manager aimed at heavy keyboard users, emphasizing high-performance rendering, Vim-style operation, and “batteries-included” integrated functionality. It is more like an engineering project/product release than a research paper proposing a new algorithm.

## Problem
- Existing file managers often trade off among **keyboard efficiency, customizability, and cross-platform consistency**, making it hard to satisfy users who perform frequent file operations.
- For users who rely on keyboard navigation, there is a lack of solutions that integrate capabilities such as **fast jumping, preview, terminal, undo/redo, and bookmarks** into a single tool.
- This matters because file browsing and manipulation are high-frequency tasks for developers and power users, and interaction latency and fragmented functionality directly affect day-to-day efficiency.

## Approach
- The core approach is simple: build an **egui-based cross-platform file manager** using **Vim-style keybindings** as the primary interaction method.
- It integrates common capabilities through a **single self-contained binary**, including multi-tab support, fuzzy directory jumping, a built-in terminal, file preview, bookmarks, and state persistence, reducing external dependencies.
- It uses **TOML configuration** to expose customization for sorting, layout, shortcuts, and themes, allowing users to remap operations to match their habits.
- It adopts **asynchronous handling of long-running tasks** to avoid blocking UI rendering, and emphasizes a simple modular design rather than complex abstraction.

## Results
- The text **does not provide formal benchmark experiments or quantitative evaluation results**, so it is not possible to give paper-style SOTA numbers, datasets, or statistical significance comparisons.
- Clear product-level claims include support for **3 desktop platforms** (Linux, macOS, Windows).
- It claims to provide **1 self-contained binary** as a “battery included” distribution method, reducing installation complexity.
- The text includes qualitative performance-related claims: rendering and navigation are “**lightingly fast**,” and it recommends using `nextest` for running tests because it can be **2-3x** faster than `cargo test`; however, this refers to the testing toolchain, not a benchmark of Kiorg’s core functionality.
- In terms of feature coverage, it lists at least **10+** capabilities: multi-tab support, Vim shortcuts, fuzzy jumping, content preview, shortcut/theme customization, bookmarks, built-in terminal, state persistence, plugin system, undo/redo, and more.
- Overall, its main “breakthrough” is **feature integration and completeness of engineering implementation**, rather than a verifiable algorithmic or systems research breakthrough.

## Link
- [https://github.com/houqp/kiorg](https://github.com/houqp/kiorg)
