---
source: arxiv
url: https://arxiv.org/abs/2605.22794v1
published_at: '2026-05-21T17:48:33'
authors:
- Qianshu Cai
- Yonggang Zhang
- Xianzhang Jia
- Wei Xue
- Jun Song
- Xinmei Tian
- Yike Guo
topics:
- software-foundation-model
- code-intelligence
- agent-self-improvement
- multi-agent-software-engineering
- automated-software-production
- human-ai-interaction
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# MOSS: Self-Evolution through Source-Level Rewriting in Autonomous Agent Systems

## Summary
MOSS lets a deployed agent system rewrite its own source code, including harness code, after collecting evidence of production failures. On OpenClaw, the paper claims one evolution cycle raised a four-task mean grader score from 0.25 to 0.61 without human code edits.

## Problem
- Deployed agents often keep repeating the same failures until a human ships an update.
- Earlier self-evolving agents edit prompts, skills, memory, or workflow graphs, so they cannot fix code-level failures in routing, hook ordering, session state, dispatch, or concurrency.
- This matters because harness bugs affect live users and become more likely as agent substrates add channels, plugins, persistent state, and multi-step execution.

## Approach
- MOSS builds failure batches from real user sessions. Periodic scans and user flags add weak or missing dialogue chunks; the default open batch is sealed at 8 chunks.
- It runs an iteration loop with a baseline evaluation, then 7 ordered stages: Locate, Plan, Plan-Review, Implement, Code-Review, Task-Evaluate, and Verdict.
- Source edits are made by external coding-agent CLIs, including Claude Code, OpenAI Codex, DeepSeek-TUI, and OpenCode. MOSS controls stage order, review gates, verdicts, and deployment.
- Candidate images are tested in ephemeral trial-worker containers that replay the failure batch before promotion.
- Promotion requires user consent through `moss evo apply`, then an in-place container swap with health probes and rollback.

## Results
- On OpenClaw, using 4 claweval compliance-audit tasks, the mean grader score rose from 0.25 to 0.61 after 1 evolution cycle, a +0.36 absolute gain and 2.44x the baseline score.
- Table 1 compares MOSS with 4 prior application-level self-evolving systems. MOSS is the only listed system that edits all 4 scopes: skills, prompts, memory, and harness code.
- The control surface exposes 9 `moss evo` subcommands: status, batches, batch, start, stop, restart, apply, flag, and catch-up.
- Task-Evaluate scores 4 to 7 keypoints per task on a 4-level scale: strong, adequate, weak, and missing.
- The swap safety path polls every 2 seconds, uses a 90-second probe window, probes every 5 seconds, and requires 3 consecutive passes across 4 health checks before committing; otherwise it rolls back.

## Link
- [https://arxiv.org/abs/2605.22794v1](https://arxiv.org/abs/2605.22794v1)
