---
source: arxiv
url: https://arxiv.org/abs/2605.13778v1
published_at: '2026-05-13T16:57:51'
authors:
- Jiahui Niu
- Kefan Gu
- Yucheng Zhao
- Shengwen Liang
- Tiancai Wang
- Xing Hu
- Ying Wang
- Huawei Li
topics:
- vision-language-action
- diffusion-policy
- speculative-inference
- robot-replanning
- latency-optimization
- dexterous-manipulation
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Realtime-VLA FLASH: Speculative Inference Framework for Diffusion-based VLAs

## Summary
Realtime-VLA FLASH speeds up diffusion-based vision-language-action policies by replacing many full replanning calls with cheap drafted action chunks that the main Action Expert checks in parallel. On LIBERO, it cuts average inference latency from 58.0 ms to 19.1 ms with a small success-rate drop.

## Problem
- Diffusion-based VLAs such as $\pi_0$ need repeated multi-step action denoising during robot replanning, which makes each full inference round slow.
- Slow replanning matters because robots may act on stale action chunks in fast tasks, such as grasping objects on a moving conveyor belt.
- Existing speculative decoding methods fit discrete autoregressive tokens, but dVLAs output continuous action chunks and lack token probabilities for acceptance checks.

## Approach
- FLASH adds two inference paths: the normal full path and a faster flash path used during many replanning rounds.
- A small draft model, about 110M parameters versus a roughly 2.7B-parameter VLM, predicts a full future action chunk in parallel from current visual features, language, and robot state.
- The main model's Action Expert verifies the draft without full sequential denoising: it samples a few flow-matching timesteps, reconstructs action endpoints in parallel, and checks whether they stay close to the draft.
- The robot executes the longest verified prefix of the drafted action chunk. If no prefix passes the distance threshold, FLASH falls back to the full path.
- A phase-aware fallback checks gripper switches and returns to full inference near grasp or release phases, where small action errors can cause failure.

## Results
- On LIBERO, Torch-$\pi_0$ averages 94.1% success, 58.0 ms task-level latency, and 5.0 ms per-action latency. FLASH+Triton-$\pi_0$ averages 93.8% success, 19.1 ms latency, and 1.9 ms per-action latency.
- FLASH+Triton-$\pi_0$ reports a 3.04x task-level speedup over Torch-$\pi_0$ with a 0.3 percentage-point average success-rate drop.
- A flash-path round costs 7.8 ms with Triton optimization, compared with 58.0 ms for the original full-inference round.
- FLASH without Triton reduces average LIBERO latency to 34.9 ms, giving a 1.66x speedup with 93.4% average success.
- FLASH+Triton handles 66.8% of LIBERO replanning rounds through the flash path, and accepted prefixes cover 69.7% of the 12-action replan window on average.
- In real-world conveyor-belt sorting, the paper reports successful grasping at belt speeds up to 15 m/min, where the compared methods fail.

## Link
- [https://arxiv.org/abs/2605.13778v1](https://arxiv.org/abs/2605.13778v1)
