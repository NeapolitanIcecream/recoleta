---
source: arxiv
url: https://arxiv.org/abs/2607.19338v1
published_at: '2026-07-21T17:56:49'
authors:
- Qijia He
- Jiayi Cheng
- Chenqian Le
- Rui Wang
- Xunmei Liu
- Yixian Chen
- Jie Mei
- Zhihao Wang
- Xupeng Chen
- Yuhuan Chen
- Tao Wang
topics:
- coding-agents
- cost-aware-routing
- test-time-recovery
- conformal-calibration
- software-engineering
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# CodeRescue: Budget-Calibrated Recovery Routing for Coding Agents

## Summary
CodeRescue routes a failed coding-agent attempt to reflect, replan, or escalate, balancing solve rate against recovery cost. A supervised router plus conformal calibration supports multiple deployment budgets without retraining.

## Problem
- After a cheap coding model fails, systems often escalate immediately, although execution feedback may enable a cheaper repair or fresh attempt.
- The problem matters because coding-agent recovery actions have different costs and non-monotone success patterns, so a fixed action or binary cascade cannot reliably optimize quality under changing budgets.

## Approach
- A cheap model first attempts each programming task. For failures, a router observes the problem, execution verdict, and stderr trace, then selects **reflect** (repair with feedback), **replan** (generate a fresh cheap solution), or **escalate** (use a stronger model).
- The router is a fine-tuned Qwen3.5-4B model trained on execution rollouts, with each example labeled by its cheapest successful recovery action.
- It scores actions with normalized label probabilities and chooses the action maximizing router score minus a cost penalty: `s(a|x) - λc(a,x)`.
- A Conformal Risk Control layer selects `λ` for a user-specified mean-cost budget from a calibration split, allowing budget changes through table lookup rather than router retraining. Its guarantee is marginal expected-cost control under exchangeability, not solve-rate control.

## Results
- Across APPS, TACO, BigCodeBench, LiveCodeBench, and CodeContests, the study attempted approximately **27,300** problems; the training split contained **4,656** examples, with **360** calibration and **360** test problems.
- The fine-tuned router achieved **0.817 solve rate** at **5.51 m$** mean recovery cost, compared with **0.686 / 7.22 m$** for always-escalate, **0.453 / 1.59 m$** for always-replan, and **0.275 / 1.24 m$** for always-reflect.
- The abstract reports that, in the main GPT-5.4-nano/GPT-5.4 setting, one CRC-calibrated frontier point exceeded always-escalate's solve rate while using **35%** of its mean recovery cost.
- The experiments show complementary success patterns for cheap recovery and escalation, supporting a discrete cost-quality frontier rather than a uniformly ordered recovery ladder.
- The formal CRC result guarantees expected recovery cost at or below the requested budget under its exchangeability, bounded-cost, and feasibility assumptions; empirical solve-rate changes remain dataset- and router-dependent.

## Link
- [https://arxiv.org/abs/2607.19338v1](https://arxiv.org/abs/2607.19338v1)
