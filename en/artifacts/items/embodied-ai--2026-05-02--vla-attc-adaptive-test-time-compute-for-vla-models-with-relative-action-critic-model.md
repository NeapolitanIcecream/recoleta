---
source: arxiv
url: https://arxiv.org/abs/2605.01194v1
published_at: '2026-05-02T02:13:11'
authors:
- Wenhao Li
- Xiu Su
- Dan Niu
- Yichao Cao
- Hongyan Xu
- Zhe Qu
- Lei Fan
- Shan You
- Chang Xu
topics:
- vision-language-action
- test-time-compute
- robot-manipulation
- action-critic
- preference-learning
- libero-long
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# VLA-ATTC: Adaptive Test-Time Compute for VLA Models with Relative Action Critic Model

## Summary
VLA-ATTC adds adaptive test-time compute to vision-language-action robot policies: it spends extra inference only when the base policy looks uncertain, then uses a Relative Action Critic to choose among sampled action chunks. The paper reports higher success on LIBERO-LONG and real robot tasks without fine-tuning the base VLA model.

## Problem
- VLA policies such as PI0 and PI0.5 usually emit actions in one fast pass, which can fail on long-horizon or ambiguous manipulation tasks.
- Running expensive candidate search at every timestep is too slow for robot control, and absolute action-value scoring is hard to train for action chunks.
- The problem matters because manipulation failures can break a long task after one bad action, while real robots still need high control frequency.

## Approach
- The method samples two action chunks with different random seeds and measures their Dynamic Time Warping distance. A high distance means high action uncertainty.
- If uncertainty is below a threshold set from an offline percentile, the robot executes the first action. If uncertainty is above the threshold, it enters a test-time deliberation step.
- During deliberation, the action head samples N candidate action chunks while reusing the same VLM prefilling pass, so the expensive vision-language encoding runs once.
- A Relative Action Critic compares action pairs, conditioned on VLM features, query features, action differences, and proprioceptive state. Tournament selection keeps the preferred action until one action remains.
- The critic is trained from automatically generated preference pairs: expert or high-step flow-matching actions are labeled better than low-step generated actions, with symmetric pair augmentation.

## Results
- On LIBERO-LONG, PI0 rises from 82.8% average success to 90.6% with adaptive VLA-ATTC (+7.8 points) and 92.2% with full deliberation (+9.4 points).
- On LIBERO-LONG, PI0.5 rises from 90.6% to 94.0% with adaptive VLA-ATTC (+3.4 points) and 95.4% with full deliberation (+4.8 points). The full setting cuts PI0.5 failure rate from 9.4% to 4.6%, a 51.1% reduction.
- On real-world Agilex Piper tasks, PI0 rises from 46.0% average success to 58.7% with adaptive VLA-ATTC (+12.7 points) and 63.3% with full deliberation (+17.3 points).
- On the same real-world tasks, PI0.5 rises from 52.0% to 62.0% with adaptive VLA-ATTC (+10.0 points) and 62.7% with full deliberation (+10.7 points).
- The paper reports a practical 20.8 Hz control frequency and notes that PI0 action decoding takes 27 ms of an 86 ms inference pass, which supports batched candidate sampling after one shared prefill.

## Link
- [https://arxiv.org/abs/2605.01194v1](https://arxiv.org/abs/2605.01194v1)
