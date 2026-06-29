---
source: arxiv
url: https://arxiv.org/abs/2606.04455v1
published_at: '2026-06-03T04:58:17'
authors:
- Xinyu Lu
- Tianshu Wang
- Pengbo Wang
- zujie wen
- Zhiqiang Zhang
- Jun Zhou
- Boxi Cao
- Yaojie Lu
- Hongyu Lin
- Xianpei Han
- Le Sun
topics:
- meta-agents
- code-intelligence
- agent-benchmarks
- automated-software-engineering
- ai-safety
- reward-hacking
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# The Meta-Agent Challenge: Are Current Agents Capable of Autonomous Agent Development?

## Summary
MAC tests whether coding agents can build other agents under time, API, and security limits. The paper finds that current meta-agents seldom beat human-written agent policies, with the best results mostly coming from proprietary frontier models.

## Problem
- Existing agent benchmarks mainly measure task execution inside human-designed workflows, so they do not test whether a model can design and improve an agent system on its own.
- This matters for automated software production and AI safety because a capable meta-agent must write code, test designs, handle budgets, and avoid reward hacking while improving another agent.

## Approach
- A code agent, called the meta-agent, gets a sandbox, a base agent interface, model/tool APIs, a development set, and an evaluation API.
- The meta-agent writes an executable agent artifact, usually `agent.py`, then submits it for feedback on the development split and revises it within a fixed budget.
- A hidden verifier later runs the final artifact on a held-out test split and records a score in `[0,1]`.
- MAC-v1 covers five domains: AIME math, GPQA/HLE science QA, LiveCodeBench programming, SWE-Bench repository repair, and Terminal-Bench long-horizon terminal tasks.
- The evaluation uses separate agent and evaluation containers, API proxying, quota checks, filesystem isolation, split access control, and post-hoc auditing to reduce reward hacking and data leakage.

## Results
- Human baseline averages in the visible table were 0.733 on Meta-AIME, 0.597 on Meta-GPQA, and 0.555 on Meta-LiveCodeBench.
- Claude-Opus-4.6 with Claude Code scored 0.744 ± 0.054 on Meta-AIME, 0.572 ± 0.049 on Meta-GPQA, and 0.557 ± 0.043 on Meta-LiveCodeBench, roughly matching the human baseline on AIME and LiveCodeBench but trailing on GPQA.
- Claude-Sonnet-4.6 scored 0.783 ± 0.017 on Meta-AIME, 0.383 ± 0.332 on Meta-GPQA, and 0.446 ± 0.133 on Meta-LiveCodeBench; the GPQA result included a 0.000 run, showing high run-to-run variance.
- MiniMax-M2.5 with Claude Code scored 0.306 ± 0.084 on Meta-AIME, 0.363 ± 0.147 on Meta-GPQA, and 0.260 ± 0.079 on Meta-LiveCodeBench, well below the human baselines in the visible results.
- The red-team integrity test ran 8 zero-resource trials; 7 produced policy violations and 1 produced a valid artifact, and the auditing agent matched the human annotator on all 8 verdicts.
- The setup used 12-hour development budgets for AIME, GPQA, and LiveCodeBench, 24-hour budgets for SWE-Bench and Terminal-Bench, and 2,500 search API calls per phase in the science domain.

## Link
- [https://arxiv.org/abs/2606.04455v1](https://arxiv.org/abs/2606.04455v1)
