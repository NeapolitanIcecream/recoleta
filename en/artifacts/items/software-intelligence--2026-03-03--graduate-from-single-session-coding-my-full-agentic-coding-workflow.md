---
source: hn
url: https://medium.com/@btraut/assemble-your-agent-team-fbfb6b8904b2
published_at: '2026-03-03T23:48:02'
authors:
- btraut
topics:
- agentic-coding
- multi-agent-workflow
- code-intelligence
- developer-tooling
- persistent-memory
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Graduate from Single-Session Coding: My Full Agentic Coding Workflow

## Summary
This is an experience-based summary of an "agentic coding workflow" aimed at engineering practice. Its core goal is to upgrade single-session human-AI pair programming into a software delivery system that supports parallelism, memory, and automation. The article emphasizes connecting planning, implementation, testing, review, and operations into a closed loop through worktrees, multi-agent orchestration, persistent task memory, and toolized prompts.

## Problem
- Traditional single-session coding is **single-threaded**: when there is only one working copy, multiple agents will overwrite each other, making parallel development difficult.
- Long conversations consume context; after approaching or hitting the compaction boundary, agents become "dumber" and "lazier," and **context rot / context poisoning** can also occur.
- Many development activities still rely on manual handoffs: planning, implementation, testing, PRs, browser validation, production troubleshooting, secret management, and more lack a unified workflow, limiting efficiency.

## Approach
- Use **git worktrees + Conductor** to give each parallel task an isolated workspace, allowing multiple agents to work safely in parallel; Conductor handles worktree creation, management, and cleanup, and supports switching between Claude/Codex within the same harness.
- Use **Beads** as an external persistent memory and task layer for agents: first write the plan as a markdown spec, then break it into beads (including dependencies). New sessions execute according to beads, a parent agent dispatches child agents in parallel, and each child agent commits code, closes its bead, and sends back notes after completing its task.
- Use **Skills / AGENTS.md** to encode high-frequency workflows and local conventions, such as brainstorm, beads-create, beads-implement, as well as project-level/directory-level development conventions and CLI tool usage instructions.
- Use a **browser/CLI loop** to extend the agent execution surface: use agent-browser or Browser Bridge for web/Electron validation, and directly handle PRs, production issues, deployments, and secrets through CLIs/MCP such as gh, Sentry, Railway, and Doppler.
- For model selection, adopt division of labor: the author prefers **Codex for primary coding**, while using **Opus** for code review, maintenance tasks, and local CLI chores.

## Results
- The article **does not provide rigorous experiments, benchmark data, or reproducible experiment tables**, so there are no academically verifiable quantitative results.
- The clearest quantitative claim is that after using **Blacksmith** instead of GitHub Actions, the author says **build times were reduced by about 50% (cut my build times in half)**, with a higher free tier as well.
- The author claims this workflow upgrades them from "**pairing with one chat**" to "**running coordinated agents**," enabling multiple agents to collaborate on planning, implementation, review, and maintenance, but provides no figures for throughput, defect rate, or cycle time.
- The author also claims to have shared this method with "**several friends and peers**" and repeatedly received feedback that "**it works**," but **does not provide sample size, task types, or a comparison baseline**.
- On model comparison, the article makes the strong claim that "**Codex is clearly better than Claude at writing code**," but **does not provide benchmark names, scores, or task-level statistics**.
- Overall, the article's main contribution is more about **integrating a system-level workflow** than introducing a new algorithm: it combines worktrees, task memory, child-agent parallelism, skill prompts, and browser/CLI automation into a "software delivery operating system."

## Link
- [https://medium.com/@btraut/assemble-your-agent-team-fbfb6b8904b2](https://medium.com/@btraut/assemble-your-agent-team-fbfb6b8904b2)
