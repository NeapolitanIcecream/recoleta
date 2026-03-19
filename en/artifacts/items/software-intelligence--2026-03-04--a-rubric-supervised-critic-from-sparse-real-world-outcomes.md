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
- code-agents
- reward-modeling
- process-supervision
- software-engineering
- human-in-the-loop
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# A Rubric-Supervised Critic from Sparse Real-World Outcomes

## Summary
This paper proposes a method for learning a code-agent “critic” from sparse, delayed, and highly noisy user-agent outcome signals in real production environments. The core contribution is the use of 24 behavior rubrics that can be directly observed from interaction traces, converting large amounts of real-world trajectories without explicit outcome labels into trainable supervision signals.

## Problem
- The paper addresses the following issue: in reality, coding agents usually work collaboratively with humans, but success signals are not like those in academic benchmarks with clear step-by-step verifiable rewards; instead, they are **sparse, delayed, and noisy**, making evaluation, training, and inference-time selection difficult.
- This matters because in real software engineering settings, users care not only about whether unit tests pass, but also whether changes are correct, maintainable, reviewable, and whether they truly reduce human workload.
- Evaluators trained only on benchmarks cannot reliably transfer to production environments; the paper notes that such critics achieve only **0.45–0.48** AUC on real outcomes, close to random.

## Approach
- Real multi-turn human-agent interactions are split into **segments**: each segment starts from a user request and ends when the agent calls finish, serving as the smallest unit of supervision and attribution.
- **24 Critic Rubrics** are designed to cover agent behavior problems, user follow-up feedback patterns, infrastructure issues, and more; these labels look only at the trace itself, not the final PR outcome, thereby avoiding outcome leakage.
- An LLM is used to annotate rubrics for all segments, and then a small amount of real outcome proxy signals is used together for training, including **PR merge** and the finer-grained **code survival**.
- A **semi-supervised multi-task critic** is trained: one head predicts sparse success, and the other predicts dense rubrics. In this way, among **151,837** real segments, although only **4%** have code-survival labels and **6%** have PR-merge labels, the remaining **96%** can still provide learning signals through rubrics.
- The trained critic can be directly used for three purposes: **best-of-N reranking, early stopping, and training data filtering/data curation**.

## Results
- In terms of data scale, the authors use **38,241** real conversations and **151,837** segments; among them, only **5,349 (4%)** have code survival labels and **9,750 (6%)** have PR merge labels, directly illustrating the scarcity of supervision.
- Regarding rubric effectiveness, in **SWE-bench / SWE-Gym**, failure modes such as incomplete implementation, insufficient testing, insufficient debugging, and insufficient analysis reduce success rates by **15–21 percentage points**, with **p < 0.001** (after FDR correction). In real data, the effects are weaker and noisier, but for example reversion request still has a significant negative effect on code survival, **Δ = -0.13, q < 0.001**.
- The necessity of real supervision: critics trained only on benchmark trajectories perform close to random on real-world outcomes, with **AUC 0.45–0.48**, and may even harm downstream selection performance on SWE-bench.
- For inference-time reranking, the critic improves best-of-N selection on SWE-bench: on the rerankable subset of trajectories, **Best@8 improves by +15.9 over Random@8**.
- For early stopping, the critic supports more efficient allocation of inference compute: the paper reports an improvement of **+17.7** while **reducing the number of attempts by 83%**.
- The authors also claim that the critic can be used for training-time data filtering, using critic-selected real trajectories for supervised fine-tuning; the provided excerpt does not include more detailed quantitative comparison numbers.

## Link
- [http://arxiv.org/abs/2603.03800v1](http://arxiv.org/abs/2603.03800v1)
