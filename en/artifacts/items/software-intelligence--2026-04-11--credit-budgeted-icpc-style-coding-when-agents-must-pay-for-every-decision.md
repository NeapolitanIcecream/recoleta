---
source: arxiv
url: http://arxiv.org/abs/2604.10182v1
published_at: '2026-04-11T12:22:10'
authors:
- Lingfeng Zhou
- Junhao Shi
- Jin Gao
- Dequan Wang
topics:
- coding-agents
- benchmarking
- resource-aware-agents
- competitive-programming
- multi-agent-systems
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Credit-Budgeted ICPC-Style Coding: When Agents Must Pay for Every Decision

## Summary
USACOArena is a coding benchmark that charges agents for tokens, tests, and elapsed time, so they must trade off correctness against cost. The paper argues that current coding-agent evaluation misses this constraint and shows that strong agents still manage budgets poorly.

## Problem
- Current coding benchmarks score final correctness and usually ignore API cost, local testing cost, and wall-clock time.
- That gap matters for real software work and multi-agent systems, where wasteful search and coordination can exhaust a shared budget.
- The paper aims to measure whether coding agents can allocate limited resources well, not just produce correct code in an unconstrained setting.

## Approach
- The authors build **USACOArena**, an interactive ACM-ICPC-style environment based on 48 problems from the 2024–2025 USACO season, with 12 problems per match.
- Each agent gets a fixed credit budget. Credits are spent on LLM inference, hints/tests, and elapsed wall-clock time through a coefficient \(\alpha\); wrong submissions also add penalties.
- Ranking follows ICPC-style rules: total score is primary, consumed credit is the tiebreaker, and harder accepted problems are worth more points.
- Agents interact through a turn-based MCP/JSON protocol, and submitted code runs in a sandboxed online judge for reproducibility.
- Experiments compare frontier single agents, self-play between identical agents, and early multi-agent/swarm setups under the same budget rules.

## Results
- Across four contests and **5 runs per contest**, **Gemini-2.5-pro** and **GPT-5-Codex** consistently ranked **first** and **second** in the compute-only setting with **\(\alpha=0\)**.
- The benchmark is far from saturated: the theoretical maximum per contest is **54 points**, while top agents score around **15 points** on average.
- In the head-to-head profile, **Gemini-2.5-pro** had **avg. rank 1.3±0.47**, **70.0% win rate**, **max score 19**, **min score 4**; **GPT-5-Codex** had **avg. rank 1.7±0.47**, **30.0% win rate**, **max score 29**, **min score 3**.
- On the hardest contest mentioned, **USACO 2025 US Open**, **Gemini-2.5-pro** scored **14.6** versus **3.0** for **GPT-5-Codex**.
- In self-play, the paper reports **9 competitions** between identical **gemini-2.5-pro** agents, covering **18 competitors**, with high variance, few ties, and no simple link between more credit use and higher score.
- In an ablation on budget size, reducing the credit limit to **10M** dropped **Gemini-2.5-pro** from **13.2** to **8.3**, while increasing it to **40M** left performance near **13.0**, which the authors interpret as evidence that current agents are capability-limited before they become budget-limited.

## Link
- [http://arxiv.org/abs/2604.10182v1](http://arxiv.org/abs/2604.10182v1)
