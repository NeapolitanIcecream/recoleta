---
source: hn
url: https://code.claude.com/docs/en/interactive-mode
published_at: '2026-03-10T23:12:09'
authors:
- mfiguiere
topics:
- cli-tooling
- interactive-mode
- context-management
- developer-tools
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Side questions with /btw in Claude Code

## Summary
This is product documentation about the `/btw` side-question feature in Claude Code interactive mode, not a robotics or machine learning research paper. Its core value is to quickly answer temporary questions based on the current context without interrupting the main task or polluting the main conversation history.

## Problem
- It addresses the small “while I’m here, let me ask...” questions that often come up during long tasks: if inserted directly into the main conversation, they interrupt the current workflow and add contextual noise.
- This matters because interactive coding agents need to balance continuous task execution, context costs, and users’ temporary information needs.
- The document also implicitly addresses a practical problem: how to make follow-up questions cheaper while not affecting the ongoing main response.

## Approach
- The core mechanism is the introduction of the `/btw` command: it can see the current session context, but it does not add this side question to the main conversation history.
- `/btw` can run independently while Claude is processing the main response, so it does not interrupt the main turn.
- It **has no tool access**: it cannot read files, run commands, or search, and can only answer based on information already in the context.
- It is **single-turn**: it returns only one answer, and if you need to ask follow-up questions, you must switch to a normal prompt.
- For cost control, the document states that `/btw` reuses the parent conversation’s prompt cache, so the extra cost is low; it defines this as the “opposite” of a subagent—the former has full context but no tools, while the latter has tools but starts from an empty context.

## Results
- The document provides no experimental data, benchmarks, or quantitative metrics, so there are **no quantitative results to report**.
- The strongest concrete functional claim is that `/btw` can be used while the main task is running and **does not interrupt** the ongoing main response.
- Another explicit claim is that `/btw` **is not added to the conversation history**, thereby reducing pollution of the main context.
- The constraints are also explicitly stated: **0 follow-up turns** (single reply), **0 tool access** (cannot read files / execute commands / search).
- On cost, there is only a qualitative statement: because it reuses the parent session’s prompt cache, the **additional cost is “very low”**, but no token, latency, or pricing figures are given.

## Link
- [https://code.claude.com/docs/en/interactive-mode](https://code.claude.com/docs/en/interactive-mode)
