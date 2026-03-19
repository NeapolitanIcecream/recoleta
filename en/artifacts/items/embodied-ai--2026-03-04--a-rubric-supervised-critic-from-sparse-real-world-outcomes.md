---
source: arxiv
url: http://arxiv.org/abs/2603.03800v1
published_at: '2026-03-04T07:23:54'
authors:
- Xingyao Wang
- Valerie Chen
- Heng Ji
- Graham Neubig
topics:
- reward-modeling
- process-supervision
- coding-agents
- human-in-the-loop
- trajectory-ranking
relevance_score: 0.16
run_id: materialize-outputs
language_code: en
---

# A Rubric-Supervised Critic from Sparse Real-World Outcomes

## Summary
This paper proposes a method for learning a “critic” model from sparse, noisy outcome signals in real production environments to evaluate the interaction trajectories of coding agents. The core idea is to split multi-turn human-agent interactions into segments and use 24 rubrics directly observable from the trajectories as dense supervision, so that even a very small number of real outcome labels can train a deployable scorer.

## Problem
- The paper addresses the fact that real-world coding agents usually collaborate with humans, and success signals are not simply unit-test passes but are **sparse, delayed, and noisy**, such as whether a PR is merged or whether code is ultimately retained; this makes evaluation, training, and selecting the best trajectory very difficult.
- This matters because without a reliable evaluator, it is hard to conduct A/B testing, RL training, data filtering, or inference-time reranking for real-world coding agents.
- Verifiable rewards from academic benchmarks alone do not represent real deployment; the authors point out that a critic trained only on benchmarks is nearly random on real data (AUC 0.45–0.48).

## Approach
- Multi-turn human-agent interactions are represented as **segments**: each segment starts from a user request and ends when the agent calls finish, serving as the smallest attributable unit of work.
- The authors design **Critic Rubrics**: 24 behavioral features covering agent mistakes, subsequent user feedback, and infrastructure issues; these labels depend only on the interaction trajectory itself and do not leak the final outcome.
- An LLM is used to automatically annotate rubrics for all segments, then combined with a very small amount of real outcome proxies to jointly train the critic; the training objective is to **jointly predict rubric + success**, a semi-supervised, multitask learning setup.
- Real outcome signals come from two proxy types: PR merge (coarse-grained binary classification) and **code survival** (the eventual retention ratio of code contributed by a segment), where code survival is finer-grained but sparser.
- The learned critic can be directly used for three downstream applications: best-of-N reranking, early stopping, and training-time data filtering/trajectory selection.

## Results
- In terms of data scale, the authors use **38,241** conversations and **151,837** segments; among them, only **5,349 (4%)** have code-survival labels and **9,750 (6%)** have PR-merge labels, but rubrics cover all segments.
- In benchmarks, the typical failure modes captured by the rubrics are strongly associated with failure: for example, incomplete implementation, insufficient testing, insufficient debugging, and insufficient analysis reduce success rates by **15–21 percentage points** (SWE-bench/SWE-Gym, **p < 0.001**, after FDR correction).
- Real-world supervision is necessary: a critic trained only on benchmarks is almost ineffective on real outcomes, with AUC only **0.45–0.48**, and can even hurt downstream selection performance on SWE-bench.
- For inference-time reranking, the critic improves SWE-bench **Best@8 by +15.9 relative to Random@8** (on the subset of trajectories that can be reranked).
- For early stopping, the critic achieves a **+17.7** improvement while reducing the number of attempts by **83%**; this shows it can not only choose better trajectories, but also stop poor trajectories earlier to save compute.
- The paper also claims that although code survival is sparser, it is more suitable than PR merge as a training signal; in addition, a rubric-enhanced critic generalizes better across different LLM backbones than a success-only critic, making it more suitable as a shared scoring function.

## Link
- [http://arxiv.org/abs/2603.03800v1](http://arxiv.org/abs/2603.03800v1)
