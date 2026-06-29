---
source: hn
url: https://github.com/erikqu/workbench-cli
published_at: '2026-06-26T22:38:59'
authors:
- erikqu
topics:
- coding-agents
- terminal-ui
- multi-agent-engineering
- developer-tools
- human-ai-interaction
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# Workbench: A TUI for parallel coding agents

## Summary
Workbench is a full-screen terminal UI for running multiple coding-agent CLIs in parallel. The excerpt describes a developer tool with tmux-backed persistence, file viewers, shell panes, and git diff tracking, but it gives no benchmark evaluation.

## Problem
- Developers using coding agents often juggle separate terminals, editor tabs, file previews, and git diffs, which makes parallel agent work harder to track.
- Agent sessions can be lost or disrupted when a UI restarts unless the process state lives outside the interface.
- The problem matters because multi-agent coding workflows need clear session boundaries, fast context switching, and visible file changes.

## Approach
- Workbench runs each workspace as its own agent session with an independent tab strip for agent panes, shell terminals, and open files.
- It uses a private tmux server so agent and terminal processes stay alive across relaunches and hot-reload restarts.
- It supports pluggable coding-agent harnesses: Claude Code by default, plus Gemini, Goose, OpenCode, and Cursor via a command flag.
- It adds a file Explorer, read-only file viewers, and a live git working-tree diff inside the same terminal UI.
- The app is built with Bun, React 19, and Silvery, with PTY support from Bun >= 1.3.5.

## Results
- The excerpt reports no quantitative benchmark results, user study, latency data, or coding-task success rates.
- It claims support for 5 named coding-agent backends: Claude Code, Gemini, Goose, OpenCode, and Cursor.
- It claims persistent agent and terminal sessions through tmux, using the socket path `~/.workbench/tmux-ui.sock`.
- It claims rich viewers for syntax-highlighted text, Markdown preview/source, images, PDFs, video playback, and Mermaid diagrams.
- It includes regression tooling: `bun run typecheck`, `bun test`, `bun run check`, and a Playwright screenshot suite.

## Link
- [https://github.com/erikqu/workbench-cli](https://github.com/erikqu/workbench-cli)
