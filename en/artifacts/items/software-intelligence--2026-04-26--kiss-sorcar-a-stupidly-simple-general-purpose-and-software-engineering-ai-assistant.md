---
source: arxiv
url: http://arxiv.org/abs/2604.23822v1
published_at: '2026-04-26T17:59:06'
authors:
- Koushik Sen
topics:
- software-engineering-agent
- code-intelligence
- llm-agents
- vscode-extension
- terminal-bench
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# KISS Sorcar: A Stupidly-Simple General-Purpose and Software Engineering AI Assistant

## Summary
KISS Sorcar is a local, open-source VS Code assistant for software engineering and general tasks built on a small five-layer agent stack. The paper claims that a simple layered design plus strict continuation, tool use, and git isolation can match or beat stronger commercial coding agents on Terminal Bench 2.0.

## Problem
- LLM coding assistants fail on long tasks because context windows run out, one bad step can derail the session, and agents loop in dead ends.
- Generated code often needs cleanup because agents stop before running checks such as linters, type checkers, and tests.
- Changes are hard to inspect or undo when an agent edits the live working tree directly, which matters in real software development.

## Approach
- The system uses a five-layer inheritance stack, with each layer adding one job: ReAct execution with budget tracking, continuation across context-limited sub-sessions, coding and browser tools, persistent chat history, and git worktree isolation.
- Continuation is handled by forcing the agent to end a sub-session with a chronological summary of what it did, why it did it, and relevant code snippets; the next sub-session starts from those summaries.
- The software engineering layer gives the model shell, read, edit, write, browser, user-question, Docker, and optional parallel sub-agent tools.
- The outer worktree layer creates a separate git branch and worktree per task, preserves dirty local state through a baseline commit, and supports crash recovery from git metadata.
- The authors keep the framework small, about 1,850 lines of code across the core five agent classes, and report building the system with the system itself over 4.5 months.

## Results
- On Terminal Bench 2.0, KISS Sorcar reports a **62.2% overall pass rate** with **Claude Opus 4.6**, equal to **277/445** trial runs across **89 tasks** with **5 trials per task**.
- It reports **78.7% pass@any** (**70/89** tasks solved at least once) and **43.8% pass@all** (**39/89** tasks solved in all five trials).
- The paper compares this to **Claude Code at 58%** and **Cursor Composer 2 at 61.7%** on the same benchmark, claiming a small edge over both.
- Trial cost and runtime are reported as **$0.45 median** and **$0.90 mean** per trial, with **202 s median** and **446 s mean** duration.
- Task stability is mixed: **39 always-pass tasks**, **19 always-fail tasks**, and **31 mixed-result tasks**.
- Evaluation details matter for the score: the authors **hard-skip 9 tasks** they judged infeasible after prior attempts, and skipped tasks still count as failures.

## Link
- [http://arxiv.org/abs/2604.23822v1](http://arxiv.org/abs/2604.23822v1)
