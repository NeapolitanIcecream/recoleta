---
source: arxiv
url: http://arxiv.org/abs/2604.20779v1
published_at: '2026-04-22T17:08:19'
authors:
- Joachim Baumann
- Vishakh Padmakumar
- Xiang Li
- John Yang
- Diyi Yang
- Sanmi Koyejo
topics:
- coding-agents
- software-engineering-datasets
- human-ai-interaction
- code-intelligence
- agent-evaluation
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# SWE-chat: Coding Agent Interactions From Real Users in the Wild

## Summary
SWE-chat is a large dataset of real coding-agent sessions from open-source developers using public GitHub repositories. The paper uses it to measure how people actually work with coding agents, how much agent-written code survives, and where these systems fail in normal development workflows.

## Problem
- Research on coding agents relies heavily on curated benchmarks, but those benchmarks miss real user prompts, iterative back-and-forth, tool use, and what code developers actually keep.
- Without in-the-wild data, it is hard to measure practical usefulness, failure modes, human oversight, cost, or security impact.
- This matters because coding agents are already used at scale, and product or model decisions based only on benchmark results can misread real workflow performance.

## Approach
- The authors build **SWE-chat**, a living dataset collected from developers who opt into logging via the Entire.io CLI on public GitHub repositories.
- The dataset links full session transcripts to commits, including user prompts, agent responses, tool calls, token usage, code diffs, and line-level human-versus-agent authorship.
- At the time of writing, SWE-chat contains about **6,000 sessions**, **63,000 user prompts**, **355,000 agent tool calls**, **13,000 checkpoints**, and **2.7 million logged events** across **200+ repositories**.
- The paper adds annotations for session success, user persona, prompt intent, and user pushback, using validated LLM judges plus raw logs and code-attribution metrics such as code survival, cost per committed line, time per committed line, and Semgrep-based security findings.
- The core idea is simple: record real human-agent coding sessions end to end, then compare what the agent produced with what the developer actually committed and how the developer reacted during the session.

## Results
- SWE-chat is the **first** dataset in the comparison table that combines **real human prompts**, **agent tool trajectories**, **code diffs**, and **code authorship attribution**.
- Coding behavior is strongly split: **22.7%** of sessions are human-only, **36.5%** collaborative, and **40.8%** are **vibe coding** where the agent writes at least **99%** of committed code. Over a three-month window, vibe coding grew from **20%** to **over 40%** of sessions.
- Usage goes beyond patch writing: the most common specific prompt intent is **understanding code (19.0%)**; **creating new code** and **git operations** are each **13.4%**, and **debugging** is **13.0%**. About **one third** of agent tool calls are bash commands.
- Agent-written code is often discarded: overall **44.3% coding efficiency** and **50.3% code survival rate**; in collaborative sessions these drop to **38.2%** and **44.1%**, while vibe coding reaches **59.0%** and **64.6%**.
- Vibe coding is more expensive and slower per committed output: median **204K tokens per 100 committed lines**, about **3x** collaborative mode; median dollar cost is **$0.13 per 100 lines** versus **$0.05** collaborative and **$0.07** human-only; median time is **12.6 minutes per 100 lines** versus **4.8** collaborative and **8.6** human-only.
- Security outcomes are worse for vibe coding: introduced vulnerabilities are **0.76 per 1,000 committed lines**, versus **0.14** for collaborative and **0.08** for human-only, measured with Semgrep. The paper also reports that users push back often: **39%** of turns overall, with user interruptions in roughly **3.3% to 6.0%** of turns, while agents ask for clarification in only **1.1% to 2.6%** of turns.

## Link
- [http://arxiv.org/abs/2604.20779v1](http://arxiv.org/abs/2604.20779v1)
