---
source: hn
url: https://github.com/houqp/kiorg
published_at: '2026-03-07T23:59:44'
authors:
- houqp
topics:
- file-manager
- keyboard-driven-ui
- cross-platform
- vim-keybindings
- developer-tooling
relevance_score: 0.28
run_id: materialize-outputs
language_code: en
---

# Show HN: Kiorg – a battery included file manager for keyboard nerds

## Summary
Kiorg is a cross-platform file manager aimed at keyboard-heavy users, emphasizing high performance, single-binary distribution, and an out-of-the-box experience. It combines Vim-style operation, content preview, a built-in terminal, and a plugin system, with the goal of improving file navigation and management efficiency.

## Problem
- Traditional file managers are often not friendly enough for keyboard-first users, with limited navigation and operational efficiency.
- Many tools either have fragmented functionality and depend heavily on external components, or lack cross-platform consistency and customizability.
- For users who need to quickly browse directories, preview many kinds of file content, and maintain low-latency interaction, this directly affects day-to-day productivity.

## Approach
- Provide a **cross-platform, performance-first** file manager built with egui, emphasizing fast rendering and navigation.
- Use **Vim-style shortcuts** as the core interaction mechanism, while supporting TOML-based customization of shortcuts, themes, and layout.
- Include a variety of “batteries-included” capabilities: multi-tab support, zoxide-like fuzzy directory jumping, a built-in terminal, bookmarks, state persistence, and undo/redo for file operations.
- Offer rich content preview covering code highlighting, images, videos, PDF, EPUB, and more, while supporting extension through a language-agnostic plugin system.
- Distribute it as a **single self-contained binary**, lowering the barrier to installation and use.

## Results
- The text does not provide quantitative results on standard benchmarks or datasets, so there are **no verifiable performance metrics**.
- It explicitly claims to provide “**Lightingly fast rendering and navigation**,” but gives no FPS, latency, throughput, or comparison figures against other file managers.
- The testing tool description mentions that `nextest` runs tests “**2-3x faster**” than `cargo test`, but this is a comparison of the development testing workflow, **not an evaluation result of Kiorg’s product capabilities themselves**.
- Specific verifiable product outcomes include support for **Linux/macOS/Windows**, availability of **pre-built binaries**, and a complete feature set including previews for multiple file types plus configurable themes and shortcuts.

## Link
- [https://github.com/houqp/kiorg](https://github.com/houqp/kiorg)
