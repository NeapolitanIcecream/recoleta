---
source: hn
url: https://modulus.so
published_at: '2026-03-07T22:31:18'
authors:
- dasubhajit
topics:
- multi-agent-coding
- shared-memory
- git-worktrees
- developer-tools
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Show HN: Modulus – Run multiple coding agents with shared project memory

## Summary
Modulus is a multi-agent programming tool for software development: it enables multiple AI coding agents to work in parallel while sharing project-level memory and using isolated workspaces. Its core selling points are reducing context copying, avoiding code conflicts, and consolidating changes produced by multiple agents for centralized review.

## Problem
- Existing AI coding assistants usually support only a single agent or a single task at a time, making it difficult to handle multiple tasks in parallel, such as fixing bugs and developing features.
- When multiple agents modify the same project simultaneously, inefficient issues easily arise, such as unsynchronized context, code conflicts, and repeated copying of README/API information.
- This matters because teams want to elevate AI from “chat-style assistance” to parallel, collaborative development labor, but that requires solving shared context and engineering isolation first.

## Approach
- Use **multiple AI agents running in parallel** so different agents can handle different development tasks at the same time, such as fixing a bug while developing a new feature.
- Through **shared project memory**, agents automatically obtain API schema, dependencies, recent changes, and cross-repository context, minimizing manual copy-pasting.
- Assign each agent an **independent isolated workspace**, built on git worktrees, to reduce file conflicts and mutual blocking at the mechanism level.
- Aggregate all code changes produced by agents in one place for review, and allow pull requests to be created directly.

## Results
- The text **does not provide quantitative experimental results** and gives no numerical comparison on speed, success rate, code quality, or baselines.
- The strongest concrete product claim is that it allows **multiple AI coding agents to work in parallel**, and claims to do so “**without conflicts**.”
- Another concrete claim is that agents can share project memory and automatically understand “**API schemas, dependencies, and recent changes across all repositories**,” thereby achieving “**Zero copy-pasting**.”
- The system also claims that each agent uses an independent workspace based on **git worktrees** to support concurrent development and avoid waiting.
- It supports **review all changes from all agents** in one interface and **directly create pull requests**.

## Link
- [https://modulus.so](https://modulus.so)
