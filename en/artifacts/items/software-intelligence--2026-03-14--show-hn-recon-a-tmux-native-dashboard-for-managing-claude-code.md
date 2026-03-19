---
source: hn
url: https://github.com/gavraz/recon
published_at: '2026-03-14T23:21:07'
authors:
- gavra
topics:
- code-intelligence
- multi-agent-software-engineering
- human-ai-interaction
- terminal-ui
- tmux-tooling
relevance_score: 0.89
run_id: materialize-outputs
language_code: en
---

# Show HN: Recon – A tmux-native dashboard for managing Claude Code

## Summary
Recon is a **tmux-native** terminal dashboard for centrally managing multiple Claude Code agent sessions, allowing users to view status, switch, create, terminate, and resume sessions without leaving the terminal. Its main value is improving visibility and operational efficiency in multi-agent coding workflows.

## Problem
- When multiple Claude Code sessions run in parallel, it is difficult for users to quickly know what each agent is doing, whether it is stuck, and whether it needs human approval.
- Manually switching, finding, restoring, and managing multiple sessions in tmux is costly, especially in multi-repo, multi-task parallel development.
- Existing approaches often rely on `ps` parsing or working-directory heuristic matching, which can be inaccurate and undermine automation and stable management.

## Approach
- Run each Claude Code instance in an independent tmux session, with Recon providing a unified TUI dashboard for centralized management.
- Precisely associate Claude processes with session IDs by reading `~/.claude/sessions/{PID}.json`, avoiding the use of `ps` or CWD heuristics.
- Aggregate information such as session status, context usage, model, and recent activity time through `tmux list-panes`, `tmux capture-pane`, and incremental parsing of `~/.claude/projects/.../*.jsonl`.
- Use a status-bar detection mechanism to identify whether a session is `Input`, `Work`, `Idle`, or `New`, and display this in real time in both the table view and the Tamagotchi-style pixel creature view.
- Provide commands such as `launch/new/resume --json` and tmux popup shortcuts, so creating, restoring, jumping to, and scripting automation can all be handled from a single entry point.

## Results
- The excerpt does not provide standard benchmarks, controlled experiments, or formal quantitative metrics, so there are **no academic-style performance numbers to report**.
- The system claims to support unified management of multiple Claude Code sessions, with a refresh frequency of **polling every 2 seconds**, and uses **incremental JSONL parsing** for real-time status updates.
- The interface can display specific context quota numbers, such as **45k/1M, 12k/200k, 90k/200k**, helping users judge token usage.
- It supports room grouping by working directory using **a 2×2 paginated grid**; users can view, switch, terminate, create, and restore sessions within a single dashboard.
- It claims to handle **multiple sessions in the same repository without conflicts**, and supports `recon --json` for integration with scripts and automation workflows.
- Compared with manual tmux management, its strongest specific improvement claim is that users can pop up the dashboard with **a single hotkey**, quickly identify which agents are working, sleeping, or waiting for approval, and jump directly to the corresponding session.

## Link
- [https://github.com/gavraz/recon](https://github.com/gavraz/recon)
