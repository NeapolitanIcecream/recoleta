---
source: hn
url: https://medium.com/@btraut/assemble-your-agent-team-fbfb6b8904b2
published_at: '2026-03-03T23:48:02'
authors:
- btraut
topics:
- agentic-coding
- multi-agent-workflow
- worktrees
- persistent-memory
- developer-tools
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Graduate from Single-Session Coding: My Full Agentic Coding Workflow

## Summary
This is an experience-based article about an "agentic coding workflow," arguing for upgrading from single-session AI coding to a multi-agent, parallel software development system with persistent memory and toolchain orchestration. Its core value lies in increasing parallelism, reducing context degradation, and connecting planning, implementation, testing, review, and operations into a reusable workflow.

## Problem
- The problem the article aims to solve is that a single AI coding session is **single-threaded**, making it difficult to advance multiple tasks in parallel; and when multiple agents share the same working copy, they can easily overwrite one another and conflict.
- Long conversations consume context, and once they approach or trigger the compaction boundary, agents become "dumber/lazier"; at the same time, **context rot** and **context poisoning** can occur, causing tasks to drift off course and become hard to correct.
- This matters because without externalized task management, context management, and an execution toolchain, AI agents struggle to reliably handle the full software lifecycle, from requirement planning to implementation, testing, deployment, and maintenance.

## Approach
- The core method is simple: break programming out of a single chat window and turn it into a **multi-agent collaboration system**. Use **worktrees** to give each agent its own independent code copy, enabling safe parallel development.
- Use **Conductor** as the multi-agent orchestration layer to manage workspaces/worktrees, sessions for different models, and transitions across stages such as planning/implementation/testing.
- Use **Beads** as an out-of-session **persistent memory and task system**: first distill requirements into a markdown spec, then break them down into beads; the parent agent reads the task dependency graph, dispatches child agents to complete work in parallel, and each child agent submits code, closes its bead, and writes notes back.
- Use **Skills, AGENTS.md, CLI/MCP, browser automation** to make best practices and operating procedures explicit, so agents can repeatedly execute tasks such as planning, implementation, PR management, production troubleshooting, and browser testing.
- The author also emphasizes choosing models by task: mainly using Codex to write code, and Opus for code review, maintenance, and local CLI chores, forming a combined stack of "models + tools + process."

## Results
- The article **does not provide formal experiments, benchmark data, or reproducible evaluations**, so there are no paper-style quantitative results to report.
- One of the clearest quantitative claims is that after using **Blacksmith** as an alternative to GitHub Actions, the author says their **build times were cut in half**, i.e. build times cut in half; however, no details are given on the specific project, absolute latency, or comparison configuration.
- The author claims this workflow has been shared with "**several friends and peers**" and has repeatedly received feedback that "it works," but provides no data on sample size, task types, success rate, or productivity gains.
- The article’s main breakthrough claim is at the engineering workflow level: through **worktrees + Conductor + Beads + Skills + browser/CLI loops**, developers can upgrade from "pair-programming with a chatbot" to "coordinating multiple agents to plan, code, review, and maintain real software in parallel."
- Another explicit but non-quantitative claim is that Codex is "clearly stronger than Claude" at writing code, though this too is the author’s experiential judgment and is not accompanied by standardized benchmark numbers.

## Link
- [https://medium.com/@btraut/assemble-your-agent-team-fbfb6b8904b2](https://medium.com/@btraut/assemble-your-agent-team-fbfb6b8904b2)
