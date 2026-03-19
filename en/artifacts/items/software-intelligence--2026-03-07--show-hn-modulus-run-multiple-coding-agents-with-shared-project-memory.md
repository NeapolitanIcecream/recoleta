---
source: hn
url: https://modulus.so
published_at: '2026-03-07T22:31:18'
authors:
- dasubhajit
topics:
- multi-agent
- coding-agents
- shared-memory
- git-worktrees
- developer-tools
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Show HN: Modulus – Run multiple coding agents with shared project memory

## Summary
Modulus is a multi-agent collaboration tool for programming scenarios. It advocates letting multiple AI coding agents share project memory while completing development tasks in parallel and in isolated workspaces. Its core value lies in reducing context copying, avoiding code conflicts, and centralizing review of changes produced by multiple agents.

## Problem
- Traditional single-agent or multi-window AI programming workflows struggle to handle multiple tasks in parallel, such as fixing bugs while developing new features.
- If multiple agents operate directly on the same codebase, conflicts, inconsistent context, and waiting overhead can easily arise.
- Existing tools often require manually copying READMEs, API schemas, or recent changes to agents, creating high friction and information gaps.

## Approach
- Use **multiple AI coding agents running in parallel** so that different agents can handle different development tasks at the same time.
- Through **shared project memory**, agents automatically obtain API schemas, dependencies, and recent changes across repositories, eliminating the need to manually paste context.
- Assign each agent an **independent isolated workspace**, using git worktrees under the hood to avoid overwriting one another and prevent code conflicts.
- Provide a **unified review interface** that consolidates all agent changes and supports creating pull request directly.

## Results
- The text claims it can **execute multiple coding tasks in parallel**, for example, “fixing a bug while building a feature,” but **does not provide quantitative benchmarks or experimental metrics**.
- The text explicitly states that each agent has an **independent workspace**, implemented with **git worktrees** to achieve “no conflicts, no waiting,” but **does not provide data on conflict rates, throughput, or time reduction**.
- The text claims agents can automatically share **API schemas, dependencies, recent changes across all repositories** and achieve “**Zero copy-pasting**,” but **does not provide figures such as the percentage reduction in manual work**.
- The text claims users can **review all agent changes in one place and create PRs directly**, but **does not provide user studies, adoption rates, or data on development-efficiency improvements**.

## Link
- [https://modulus.so](https://modulus.so)
