---
source: arxiv
url: https://arxiv.org/abs/2606.04968v1
published_at: '2026-06-03T14:49:35'
authors:
- Yunpeng Mei
- Jiakai He
- Hongjie Cao
- Chenyu Wang
- Xiaowen Zhu
- Yihan Zhou
- Jiamin Wang
- Chenbo Xin
- Peng Cheng
- Yuxuan Yang
- Yijie Wang
- Xinhu Zheng
- Gao Huang
- Jie Chen
- Gang Wang
topics:
- vision-language-action
- robot-policy
- flow-matching
- offline-rl
- bimanual-manipulation
- robot-data-scaling
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Potential-Guided Flow Matching for Vision-Language-Action Policy Improvement

## Summary
ForesightFlow improves vision-language-action flow policies trained on mixed robot data by adding generated success-potential scores to each action chunk. It uses those scores for best-of-K action selection and avoids a separate critic.

## Problem
- Deployed robots collect mixed trajectories with successful actions, partial progress, recoverable errors, and failures; plain behavior cloning can copy failures.
- Filtered behavior cloning throws away useful sub-trajectories, while offline RL methods such as IDQL add a large critic and extra training cost.
- The paper targets long-horizon manipulation where sparse success labels make it hard to learn which local action chunks help task progress.

## Approach
- The policy generates an endpoint with both an action chunk `a` and a success-potential vector `s` aligned to the chunk horizon.
- Stage-level binary labels train the potential vector, so useful partial progress can be supervised even when a full rollout fails.
- Advantage-weighted flow matching upweights high-advantage actions, using weights `min(M, exp(A/tau))`.
- The action loss and potential loss are decoupled: advantage weights apply only to action velocities, while potential velocities train uniformly on success and failure samples.
- A one-step boundary estimator gives a context baseline for advantage computation, and inference samples K candidates and executes the one with the highest average generated potential.

## Results
- On five BEHAVIOR-1K simulation tasks, ForesightFlow reports the best average normalized score: `0.46` versus IDQL `0.44`, FQL `0.39`, Filtered BC `0.38`, and BC `0.35`.
- In simulation, it reports average success rate `39.6%`, close to IDQL `39.0%` and above FQL `34.4%`, Filtered BC `31.6%`, and BC `31.0%`; it uses `K=5` self-guided candidates.
- On five real-world bimanual tasks, it reports average score `0.62` and success rate `35.4%`, compared with IDQL `0.59` and `32.6%`, and Filtered BC `0.51` and `24.6%`.
- Training compute drops from IDQL `287` GPU hours to `178` GPU hours, a reported `38%` reduction.
- The value-related parameter overhead is about `1K` parameters versus IDQL's separate `~500M`-parameter critic; total parameters are `2.35B` versus `~2.84B`.
- At `K=5`, reported latency is `155 ms` for ForesightFlow versus `183 ms` for IDQL; a Radio ablation reports final-stage completion `51.0%` for decoupled training versus `42.0%` for coupled training and `44.0%` for BC.

## Link
- [https://arxiv.org/abs/2606.04968v1](https://arxiv.org/abs/2606.04968v1)
