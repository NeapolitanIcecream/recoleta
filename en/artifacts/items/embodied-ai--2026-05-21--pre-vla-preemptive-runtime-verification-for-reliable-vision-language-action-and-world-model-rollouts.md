---
source: arxiv
url: https://arxiv.org/abs/2605.22446v1
published_at: '2026-05-21T13:13:31'
authors:
- Zhen Sun
- Yongjian Guo
- Haoran Sun
- Luqiao Wang
- Wei Lu
- Jiachi Ji
- Shengzhe Ji
- Junwu Xiong
- Zhijun Meng
topics:
- vision-language-action
- world-models
- runtime-verification
- robot-safety
- libero
- action-filtering
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Pre-VLA: Preemptive Runtime Verification for Reliable Vision-Language-Action and World-Model Rollouts

## Summary
Pre-VLA checks VLA action chunks before robot execution or world-model rollout. On LIBERO, it raises RynnVLA-002 average success from 30.79% to 37.62% with 183.9 ms verification per action chunk.

## Problem
- VLA policies can generate unsafe or low-value action chunks under distribution shift, error buildup, or poor confidence calibration.
- Bad actions can cause collisions, object drops, kinematic violations, and failed long-horizon manipulation episodes.
- The same bad actions can waste world-model rendering compute and produce misleading rollouts with drift, blurry frames, distorted relations, or false success.

## Approach
- Pre-VLA encodes the language instruction, visual observation, proprioceptive state, and candidate action chunk with a frozen WorldVLA-style multimodal backbone built on Chameleon with action and state tokenizers.
- A modality-aware pooling layer separates text, image, state, and action tokens, mean-pools each group, and concatenates the four vectors.
- A lightweight dual-branch head predicts a binary safety confidence and a continuous critic-derived advantage score for each action chunk.
- Training uses PPO critic signals, K-step advantage estimation, failure backtracking penalties, task-level advantage normalization, Focal Loss, MSE advantage regression, and soft-threshold calibration.
- At runtime, a scheduler filters actions before execution or world-model rollout, resamples rejected candidates up to a budget, then uses the highest predicted advantage as fallback.

## Results
- On an independent LIBERO test set, Pre-VLA reports F1 = 0.8303 and accuracy = 0.9542 for action validity discrimination.
- It reduces the false pass rate for invalid actions to 0.0200 on the same LIBERO test setting.
- Across four LIBERO suites, it improves average closed-loop success over RynnVLA-002 from 30.79% to 37.62%, a gain of 6.83 percentage points.
- Average forward verification time is 183.9 ms per candidate action chunk; the paper also states a 100–200 ms pure forward range.
- The excerpt says task execution steps are reduced, but it does not provide step-count numbers.
- The excerpt claims fewer misleading world-model rollouts, including less target drift and fewer visual artifacts, but it gives no quantitative world-model metric.

## Link
- [https://arxiv.org/abs/2605.22446v1](https://arxiv.org/abs/2605.22446v1)
