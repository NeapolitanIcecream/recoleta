---
source: hn
url: https://github.com/mattiagaggi/claude-custom-chat
published_at: '2026-03-08T23:29:39'
authors:
- mattiagaggi
topics:
- vscode-extension
- claude-cli
- self-modifying-tool
- mcp
- developer-tools
relevance_score: 0.06
run_id: materialize-outputs
language_code: en
---

# Claude Custom Chat – customize your Claude Code extension

## Summary
This is a Claude Code CLI chat extension for VS Code/Cursor whose core selling point is that in "Dev Mode," Claude can read and modify the extension's own source code, while snapshot and rollback mechanisms reduce the risk of trial and error. It is more of a developer tool product description than a research paper, focusing on the self-modification workflow, editor integration, and safety boundary design.

## Problem
- Existing Claude CLI/editor chat experiences lack a **customizable native interface** and a closed-loop modification workflow for extension development.
- Letting a model directly modify host extension code carries significant risk; without **snapshots, rollback, and scope restrictions**, experimentation can easily break usability.
- For developers, the manual cycle of editing code, compiling, reloading, and undoing is cumbersome, reducing the efficiency of rapid UI/feature iteration.

## Approach
- Provides a VS Code/Cursor extension as a custom chat frontend for the Claude Code CLI, handling process management, session persistence, permission management, and the Webview UI.
- Introduces **Dev Mode**: when activated, it automatically creates a source snapshot and exposes restricted tools to Claude via MCP, allowing it to first call `get_extension_source` to inspect the structure, then perform Read/Write/Edit operations on files within the extension directory.
- After modifications, compilation is triggered automatically and the user is prompted to reload the window; if the result is unsatisfactory, "Rollback to Latest Snapshot" or "Pick and Rollback to Snapshot" can be used to restore the previous state.
- Safety mechanisms include: file path validation limited to the extension directory, confirmation required for all rollbacks, snapshots persisted to disk, and automatic recompilation and validation after rollback.
- Also provides engineering-oriented features such as a graph view, cost/Token tracking, and multi-session tabs to improve the development and debugging experience.

## Results
- The text **does not provide standard research experiments or quantitative evaluation results**; there are no datasets, metrics, baselines, or ablation studies.
- Specific capability claims: supports **VS Code, Cursor, and other VS Code forks**; supports **macOS (ARM64/Intel), Linux (Ubuntu/Debian/Fedora), Windows 10/11**.
- Runtime requirements include **Node.js 16+**, Git, the `@anthropic/claude` CLI, and a valid Claude API key or Pro/Max subscription.
- Dev Mode snapshot contents include **timestamp, Git branch, commit hash, and the full contents of all `src/` source files**, persisted as `snapshot-{timestamp}.json` in `.devmode-snapshots/`.
- Architecturally, the system is split into four layers: **Handlers / Managers / Webview / Claude CLI process**, and it claims support for automatic compilation, window reload, a visual status bar, and a Cytoscape.js-based code relationship graph view.
- The strongest practical claim is that this is the “**first Claude extension that can modify itself**,” and that after modification it enables a relatively safe, bootstrapped extension development workflow through snapshot rollback.

## Link
- [https://github.com/mattiagaggi/claude-custom-chat](https://github.com/mattiagaggi/claude-custom-chat)
