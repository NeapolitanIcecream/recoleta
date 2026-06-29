---
source: arxiv
url: https://arxiv.org/abs/2605.04361v1
published_at: '2026-05-05T23:46:33'
authors:
- Saranyan Vigraham
topics:
- multi-agent-software-engineering
- agent-orchestration
- code-intelligence
- software-design
- context-injection
- llm-evaluation
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# When Context Hurts: The Crossover Effect of Knowledge Transfer on Multi-Agent Design Exploration

## Summary
The paper shows that context transfer in multi-agent software design can improve or reduce design tradeoff coverage depending on a task’s no-context baseline exploration. A single no-context trial is proposed as a diagnostic for whether artifacts should be injected.

## Problem
- Multi-agent coding systems often add transcripts, design docs, code, or retrieved documents by default, assuming extra context improves work.
- For software design, extra context can anchor agents to one solution and reduce exploration of architectural tradeoffs.
- This matters for agent orchestration because correct-looking code can hide narrow design search.

## Approach
- The authors ran more than 2,700 Claude Sonnet 4 multi-agent design runs across 10 software design tasks.
- Each team used 5 agents with distinct personas; conditions included transcript, topology/tradeoff list, design doc, anti-patterns, code, no context, and irrelevant context.
- They measured design exploration with direct tradeoff assessment: an evaluator LLM checked each deliberation for discussion of known tradeoffs and computed coverage.
- They tested mechanism by changing prompt pressure across 4 levels on 2 tasks to separate natural convergence from instruction-driven convergence.

## Results
- Baseline tradeoff coverage ranged from 0.033 on rate limiter to 0.540 on LRU cache, with n=20 trials per task.
- On rate limiter, anti-patterns raised coverage from 0.033 to 0.700 (+0.667, p<0.001, d=3.41), and transcripts raised it to 0.592 (+0.558, p<0.001, d=2.71).
- On Kubernetes operator, transcripts reduced coverage from 0.475 to 0.256 (-0.219, p<0.001, d=-1.14), and code reduced it to 0.325 (-0.150, p=0.016).
- Baseline exploration predicted the best artifact effect with Pearson r=-0.821 (p<0.001) and Spearman rho=-0.624 (p=0.024).
- Irrelevant context beat all relevant artifacts on ML training pipeline: coverage was 0.444 (+0.087) versus topology 0.431, baseline 0.356, transcript 0.231 (p=0.005 versus baseline), and code 0.256 (p=0.030 versus baseline).
- The paper claims conditional context injection: run a cheap no-context baseline first, then add artifacts only when baseline exploration is low.

## Link
- [https://arxiv.org/abs/2605.04361v1](https://arxiv.org/abs/2605.04361v1)
