---
source: hn
url: https://github.com/gavraz/recon
published_at: '2026-03-14T23:21:07'
authors:
- gavra
topics:
- developer-tools
- tmux-dashboard
- agent-orchestration
- terminal-ui
- claude-code
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Show HN: Recon – A tmux-native dashboard for managing Claude Code

## Summary
Recon is a tmux-based terminal dashboard for centrally managing multiple Claude Code sessions, allowing users to inspect, switch, create, terminate, and resume agents without ever leaving the terminal. Its value lies in consolidating multi-agent programming workflows from scattered tmux sessions into a unified, visual, and scriptable control interface.

## Problem
- When users run multiple Claude Code agents at the same time, there is no unified interface to view each agent’s status, whether it is stuck, its recent activity, and its context usage.
- Relying only on manually switching between tmux sessions makes it difficult to quickly tell which sessions are working, which are waiting for approval, and which are idle, reducing multi-agent development efficiency.
- Resuming historical sessions, managing multiple sessions in the same repository, and exposing these states to automation scripts all require more reliable session identification and status detection mechanisms.

## Approach
- The core idea is simple: run each Claude Code instance in its own tmux session, then have Recon read tmux and Claude local state files to generate a centralized TUI dashboard.
- It uses `tmux list-panes` to obtain pane/session information, and maps processes reliably to Claude sessions through `~/.claude/sessions/{PID}.json` rather than relying on `ps` or working-directory heuristics.
- It reads `~/.claude/projects/.../*.jsonl` and status-bar text from `tmux capture-pane` to determine whether a session is Input, Work, Idle, or New, and displays the model, token context, and recent activity time.
- The interface provides two views: a tabular dashboard and a pixel-creature visualization reminiscent of virtual pets; it also supports `recon --json` as a scripting interface.
- It also provides operations such as creating new sessions, resuming sessions, naming resumed sessions, popup shortcuts, and room-based grouping by repository, embedding multi-session management directly into the tmux workflow.

## Results
- The text **does not provide formal benchmarks, user studies, or quantitative experimental results**, so there are no reportable figures for accuracy, latency, percentage efficiency gains, or comparisons against baseline tools.
- The most specific runtime characteristics provided include: a real-time status polling interval of **every 2 seconds**, and a room layout of a **2×2 grid with pagination**.
- It supports displaying token context usage, with example values including **45k/1M, 12k/200k, 8k/200k, 90k/200k, 3k/1M**.
- It shows an example of centralized display for at least **6** parallel sessions, covering 4 status categories: **Input / Work / Idle / New**.
- The main claimed improvements are reliable PID→session matching, centralized management without leaving the terminal, conflict-free multi-session use within the same repository, and the ability to resume historical sessions and output JSON for scripting.

## Link
- [https://github.com/gavraz/recon](https://github.com/gavraz/recon)
