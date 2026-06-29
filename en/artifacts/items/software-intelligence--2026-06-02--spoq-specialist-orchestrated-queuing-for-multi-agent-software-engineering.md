---
source: arxiv
url: https://arxiv.org/abs/2606.03115v1
published_at: '2026-06-02T03:59:56'
authors:
- Royce Carbowitz
- Dheeraj Kumar
topics:
- multi-agent-software-engineering
- llm-orchestration
- code-intelligence
- human-ai-interaction
- task-scheduling
- software-quality-assurance
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# SPOQ: Specialist Orchestrated Queuing for Multi-Agent Software Engineering

## Summary
SPOQ is a multi-agent software engineering method that schedules dependent coding tasks in parallel waves, checks plans and code with score gates, and includes a human specialist as an active participant. It targets faster project execution with fewer defects than sequential agent handoffs.

## Problem
- Multi-agent coding systems often serialize work through role chat or handoffs, so independent tasks wait even when agents are available.
- Weak plan and code checks cause late rework, failed tests, and wasted model calls.
- Fully autonomous runs can miss requirement ambiguity and design tradeoffs where human judgment prevents bad task splits.

## Approach
- SPOQ turns an epic into atomic 1-4 hour tasks with explicit dependencies in a DAG.
- A topological sort assigns tasks to waves: tasks in the same wave run in parallel, and later waves wait for their prerequisites.
- Two validation gates score planning and code against 10 metrics each, with a 95% aggregate pass threshold before moving forward.
- A three-tier agent setup uses Opus workers for implementation, Sonnet reviewers for QA, and Haiku investigators for build-failure triage.
- Human-as-an-Agent lets a human specialist help decompose tasks, validate plans, and answer agent questions during execution.

## Results
- On unbounded synthetic DAGs, wave dispatch reached a critical-path ratio of 1.03-1.11 and reported speedup up to 14.3x.
- On a 2-slot local backend with real LLM calls, SPOQ reported a stable 1.4x speedup, matching the stated hardware concurrency ceiling.
- Across four full-stack planning tasks, structured planning raised coverage from 93.0 to 99.75, removed cyclic plans, and raised parallelism potential from 31.0 to 75.25.
- Dual validation reduced defects from 0.34 to 0.20 per task and raised test pass rate from 91.25% to 99.75%.
- Human-as-Agent planning reduced residual defects from 0.47 to 0.03 per task and raised pass rate from 96.5% to 99.75%.
- A deployment study reports 17 repositories, 8,589 commits, 1,822 completed tasks, 13,866 executed tests, and a 99.87% aggregate pass rate.

## Link
- [https://arxiv.org/abs/2606.03115v1](https://arxiv.org/abs/2606.03115v1)
