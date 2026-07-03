---
source: arxiv
url: https://arxiv.org/abs/2607.01804v1
published_at: '2026-07-02T07:18:53'
authors:
- Yi Pan
- Miao Pan
- Qi Lu
- Jiaming Huang
- Man Zhang
- Siteng Huang
- Xin Li
- Jie Zhang
- Yongliang Shen
- Xuhong Zhang
- Wenqi Zhang
topics:
- vision-language-action
- robot-policy
- adaptive-action-horizon
- inference-time-correction
- latent-dynamics
- embodied-ai
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# VLA-Corrector: Lightweight Detect-and-Correct Inference for Adaptive Action Horizon

## Summary
VLA-Corrector adds inference-time monitoring and correction to action-chunked vision-language-action policies. It raises task success while often reducing policy calls by cutting off stale action chunks and guiding the next replan.

## Problem
- Action-chunked VLA policies execute several predicted actions open-loop, so fresh camera observations do not affect control until the chunk ends.
- Longer horizons reduce policy-call cost, but they create more time for contact errors, pose drift, and slippage to compound into task failure.
- Fixed horizons are hard to tune because the best value changes with task difficulty, dynamics, and sim-to-real mismatch.

## Approach
- A frozen VLA backbone still generates action chunks; VLA-Corrector adds a separate 40M latent dynamics MLP trained on demonstration trajectories.
- The Latent-space Vision Monitor predicts the expected visual latent change for the executed action and compares it with the actual latent change from new camera frames.
- A sliding-window median and MAD threshold detect persistent mismatch; when drift persists for several steps, the system discards the rest of the current action queue.
- After an interrupt, Online Gradient Guidance modifies the flow-matching denoising step so the next action chunk points toward the latent correction direction.
- This creates an adaptive horizon: chunks run long when visual dynamics stay on track and shorten when execution drifts.

## Results
- On MetaWorld, pi0.5 average success rises from 48.70% to 64.35% (+15.65 points); its Very Hard split rises from 41.0% to 65.0% (+24.0 points).
- On MetaWorld, SmolVLA improves from 61.90% to 66.65% (+4.75 points), and X-VLA improves from 55.55% to 59.60% (+4.05 points).
- On LIBERO, few-shot pi0.5 plus VLA-Corrector improves average success from 94.00% to 97.80% (+3.80 points), above the fully fine-tuned pi0.5 baseline at 96.95%.
- For pi0.5 at horizon 50, success improves from 48.72% to 58.70%, average policy calls drop from 5.15 to 4.98, and success-per-call efficiency gains 24.6%.
- For SmolVLA at horizon 10, success improves from 61.90% to 73.00%, policy calls drop from 19.27 to 15.64, and success-per-call efficiency gains 45.3%.
- Corrector training uses limited data well: on MetaWorld at horizon 50, using the full post-holdout corrector training split improves average success from 48.72% to 54.32%, while r=0.6 reaches 52.20%.

## Link
- [https://arxiv.org/abs/2607.01804v1](https://arxiv.org/abs/2607.01804v1)
