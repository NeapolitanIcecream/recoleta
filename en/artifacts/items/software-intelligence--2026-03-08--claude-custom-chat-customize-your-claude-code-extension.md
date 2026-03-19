---
source: hn
url: https://github.com/mattiagaggi/claude-custom-chat
published_at: '2026-03-08T23:29:39'
authors:
- mattiagaggi
topics:
- vscode-extension
- code-intelligence
- self-modifying-tools
- claude-cli
- developer-workflow
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Claude Custom Chat – customize your Claude Code extension

## Summary
This is a Claude Code chat extension for VS Code/Cursor whose core selling point is a “Dev Mode” that allows Claude, within a restricted scope, to view and modify the extension’s own source code, with snapshot rollback enabling safe experimentation. It is better understood as an engineered product/tool description rather than a research paper with a formal experimental design.

## Problem
- The existing in-editor Claude CLI chat experience is relatively basic, lacking a customizable UI, source-code introspection, and a “self-modification” workflow, making it difficult for developers to quickly turn the AI assistant into a tool suited to their own process.
- Letting the model directly modify local tool source code is risky: it can easily break things, be hard to roll back, and lose state after cross-window reloads, so controlled modification and a reliable recovery mechanism are needed.
- Integrating Claude CLI into a cross-platform editor environment also involves engineering complexity around installation, compilation, process management, permission control, and visualization, which affects practical usability.

## Approach
- Provide a VS Code/Cursor extension as a custom chat frontend for the Claude Code CLI, handling UI, session management, permission handling, CLI process communication, and graph view functionality.
- Introduce Dev Mode: when activated, it automatically creates source snapshots and exposes restricted tools to Claude through MCP, allowing it to first call `get_extension_source` to obtain a structural overview, then use Read/Write/Edit to modify code only within the extension directory.
- Use persistent snapshots to enable safe self-modification: each time development mode is entered, files under `src/` are saved as JSON snapshots, recording timestamp, branch, commit hash, and supporting “rollback to latest snapshot” or “pick any snapshot to roll back.”
- After modifications, automatically compile and prompt for reload; together with the tips bar showing Dev Mode status, file changes, and compilation information, this creates a closed loop of “describe the request → Claude changes the code → reload and test → roll back if unsatisfied.”
- Reduce the risk of out-of-bounds access or accidental changes by the model through path validation, scope restriction, confirmation dialogs, and a git-ignored snapshot directory.

## Results
- The text **does not provide formal benchmark tests, ablation studies, or quantitative metrics**, so there is no research data to report such as accuracy / latency / success rate.
- The strongest concrete claim is that the project describes itself as the “**first Claude extension that can modify itself**,” but the text provides no comparative experiments or third-party validation.
- Compatibility claims cover **3 categories of operating systems**: macOS (ARM64/Intel), Linux (Ubuntu/Debian/Fedora), and Windows 10/11 (PowerShell).
- Editor support claims cover **at least 3 categories of environments**: VS Code, Cursor, and other VS Code forks (such as Antigravity).
- Dev Mode exposes **4 categories of core capabilities/tool entry points**: `get_extension_source`, Read, Write, Edit; snapshots include **4 categories of key information**: timestamp, branch, commit hash, files.
- The most concrete engineering result of the snapshot mechanism is that snapshots are persisted to `.devmode-snapshots/`, allowing **rollback to continue after window reloads and extension restarts**, and triggering automatic recompilation after rollback.

## Link
- [https://github.com/mattiagaggi/claude-custom-chat](https://github.com/mattiagaggi/claude-custom-chat)
