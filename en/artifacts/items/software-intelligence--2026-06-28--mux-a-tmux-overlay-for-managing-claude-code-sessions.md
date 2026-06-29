---
source: hn
url: https://github.com/fashton28/mux
published_at: '2026-06-28T23:42:55'
authors:
- fashton28
topics:
- claude-code
- tmux
- session-management
- developer-tools
- human-ai-interaction
- coding-agents
relevance_score: 0.66
run_id: materialize-outputs
language_code: en
---

# Mux – A tmux overlay for managing Claude Code sessions

## Summary
Mux is a tmux overlay for people running several Claude Code sessions. It shows which session needs input and lets the user jump to that pane.

## Problem
- Running Claude Code in many tmux panes makes it easy to miss a blocked session waiting for input; this wastes time during agent-assisted coding.
- tmux alone does not show Claude status, working directory, time in state, and a live pane preview in one view.

## Approach
- The core method is simple: read Claude Code's own status files and match them to live panes on the current tmux server.
- It opens an fzf floating overlay inside tmux with one row per live Claude session.
- Rows show status, tmux session, working directory, and minutes since the status changed.
- It sorts rows by state so waiting sessions appear before working, idle, and unknown sessions; within each group, the longest-stuck session appears first.
- Enter switches to the selected pane; ctrl-x sends a guarded SIGTERM to kill a Claude session.

## Results
- The excerpt reports no benchmark, user study, latency, or adoption numbers.
- It claims 1-key jump behavior: pressing Enter switches to the selected Claude pane, including panes in other tmux windows.
- It refreshes the overlay and timers while open and reports time in state in minutes, with examples such as 2899m waiting and 304m waiting.
- It limits the list to live Claude sessions on the current tmux server, so each row can be opened directly.
- It exposes 5 subcommands: mux, mux list, mux preview <pane>, mux jump <pane> <window> <session>, and mux kill <pid>.
- It requires 3 external tools for normal use: tmux, fzf, and jq, with fzf >= 0.38.

## Link
- [https://github.com/fashton28/mux](https://github.com/fashton28/mux)
