---
source: hn
url: https://maggieappleton.com/zero-alignment
published_at: '2026-04-14T23:52:32'
authors:
- facundo_olano
topics:
- multi-agent-software-engineering
- code-intelligence
- collaborative-ai
- developer-tools
- human-ai-interaction
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# One Developer, Two Dozen Agents, Zero Alignment

## Summary
Ace is a GitHub Next research prototype for multiplayer coding with shared agents, chat, planning, and cloud workspaces. The talk argues that the main bottleneck in agent-driven software work is team alignment, not code generation speed.

## Problem
- Current coding agents are built as single-user tools, but software teams need shared planning, context, and coordination.
- Faster code generation shifts the bottleneck toward deciding what to build, avoiding duplicate work, and keeping teammates aligned before code lands in pull requests.
- Existing tools such as PRs, issues, and Slack do not handle the speed, volume, and shared context needs of agent-heavy development well.

## Approach
- Ace puts humans and coding agents in the same realtime session, with chat, prompt history, summaries, and shared context visible to everyone in that session.
- Each session runs on a cloud microVM with its own git branch, terminal, dev server, preview, commits, and diffs, so multiple people and agents can work on the same task without local setup friction.
- Teammates can join a session, inspect the full agent conversation, run commands, view the same preview, edit code together, and co-prompt the agent.
- For larger tasks, the team can co-edit a plan inside the workspace before asking the agent to implement it, moving alignment earlier in the workflow.
- Ace also adds dashboard summaries such as unfinished work, teammate activity, and recent repo changes to help users stay oriented across many parallel agent-driven tasks.

## Results
- The excerpt provides no formal benchmark results, dataset evaluations, or controlled quantitative comparisons.
- The strongest concrete claim is product-level: Ace supports one developer working with "two dozen agents" in a shared multiplayer workspace.
- The prototype is described as entering technical preview with planned user testing by a few thousand people.
- Claimed user-visible effects include shared cloud execution, multiplayer prompting, collaborative plan editing, realtime previews, automatic commits, GitHub PR creation, and persistent sessions that continue after one user disconnects.

## Link
- [https://maggieappleton.com/zero-alignment](https://maggieappleton.com/zero-alignment)
