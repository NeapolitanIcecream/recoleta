---
source: arxiv
url: https://arxiv.org/abs/2606.29957v1
published_at: '2026-06-29T08:35:15'
authors:
- Yifan Wu
- Zhuokai Zhao
- Songlin Li
- Ho Hin Lee
- Jiacheng Zhu
- Shirley Wu
- Tianhe Yu
- Serena Li
- Lizhu Zhang
- Xiangjun Fan
- Shengzhi Li
topics:
- coding-agents
- software-benchmarks
- multi-turn-evaluation
- user-simulation
- code-intelligence
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# SWE-Together: Evaluating Coding Agents in Interactive User Sessions

## Summary
SWE-Together is a 109-task benchmark that tests coding agents in replayed multi-turn user sessions, rather than only with one-shot task prompts. It measures both final repository correctness and how much corrective user feedback the agent needs.

## Problem
- Most coding-agent benchmarks give the full task up front and score only the final code, while real users clarify goals, add constraints, and correct errors over several turns.
- This matters because two agents can reach similar final code quality while requiring very different amounts of user effort.
- Real session logs are hard to benchmark directly because many lack a reproducible repository state, a clear goal, or a local outcome that can be checked.

## Approach
- The authors filter 11,260 recorded user-agent coding sessions down to 109 repository-level tasks with recoverable commits, clear user goals, and locally checkable outcomes.
- Each task starts with the original user's first request and restores the repository in a pinned sandbox.
- A state-conditioned LLM user simulator watches the evaluated agent's trajectory and sends feedback only when trigger conditions from the original session apply.
- Final code is scored with deterministic verifier evidence plus a fixed per-task rubric judged against the final repository state.
- The benchmark also reports User Correction, which counts explicit corrections plus 0.2 times softer nudges, and Intent Coverage, which checks whether simulator messages stay aligned with the original user intents.

## Results
- The final suite has 109 tasks from 11,260 raw sessions, a 0.97% conversion rate. Sources include DataClaw 29 tasks, Pi-staging 23, Hyperswitch 9, and SWE-chat 48.
- Seven frontier models were evaluated with the opencode harness, using 2 replicates per task and a success threshold of judge score >= 0.85.
- Claude Opus 4.8 led the evaluated agents with 63% pass@1, 59% stable solve rate, 52% pass², 0.801 mean judge score, and 1.38 mean User Correction.
- GPT-5.5 ranked second by mean judge score with 58% pass@1, 55% stable solve rate, 48% pass², 0.763 mean judge score, and 1.59 User Correction.
- The reference patch baseline was about 78% pass@1, so the best evaluated agent was about 15 percentage points behind it.
- User Correction was strongly inversely correlated with capability across the seven models: Pearson -0.92 with pass@1 and -0.84 with stable solve rate.

## Link
- [https://arxiv.org/abs/2606.29957v1](https://arxiv.org/abs/2606.29957v1)
