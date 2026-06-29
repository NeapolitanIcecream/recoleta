---
source: arxiv
url: https://arxiv.org/abs/2606.23574v1
published_at: '2026-06-22T16:39:28'
authors:
- Yule Liu
- Shuai Liu
- Jiaheng Wei
- Xinlei He
topics:
- vla-watermarking
- world-action-models
- robot-policy-provenance
- latent-noise-watermark
- black-box-verification
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# A Watermark for Vision-Language-Action and World Action Models

## Summary
This paper proposes a latent-noise watermark for VLA and WAM robot policies so an owner can verify a deployed black-box service from executed actions. It claims reliable ownership detection and multi-key identification across π0.5 and LingBot-VA with little task-performance change.

## Problem
- VLA and WAM robot policies are valuable services trained with proprietary data, but owners may only audit the action commands sent to the robot, not weights or latent seeds.
- Existing backdoor watermarks require weight edits and fit multi-user identification poorly; output-side frequency marks can be found and filtered from the action stream.
- The problem matters because a partner can wrap or resell a policy service while keeping the weights hidden, so ownership proof must work through partial, post-processed robot actions.

## Approach
- The owner replaces selected Gaussian sampler seeds with a keyed mixture: z_fp = sqrt(1-β^2) z + β r_k. Since z and r_k are Gaussian, z_fp still follows N(0,I).
- A secret keyed selector marks only some action chunks, with per-episode cap m and maximum gap P, so an attacker does not know which chunks carry the signal.
- During audit, the owner records executed channels only, such as 7 of 32 channels for single-arm robots or 14 channels for dual-arm robots.
- The verifier recovers each latent seed by gradient-based MAP optimization: it searches for a seed whose generated actions match the observed executed channels while staying likely under the Gaussian prior.
- It scores recovered seeds against candidate-key references with a matched filter, normalizes scores with decoy keys, sums rollout scores, and ranks keys for multi-user identification.

## Results
- The evaluation uses 2 policy families, π0.5 and LingBot-VA, across 2 robot suites, LIBERO-10 and RoboTwin, for 4 policy-robot combinations.
- With 16 audit rollouts, binary ownership verification reaches TPR 1.00 at 1% FPR in all 4 combinations.
- The same grouped evidence identifies the assigned key in the multi-key setting; the excerpt does not give the exact key-identification accuracy.
- Task success rate changes by at most a few percentage points across the 4 combinations.
- Under canonical output-side attacks and owner-side variants, the weakest reported cell still reaches TPR 0.84 at 1% FPR after aggregation.
- Aggressive smoothing or jitter on π0.5/LIBERO-10 is a failure case, with TPR below 0.2 even with larger rollout budgets.

## Link
- [https://arxiv.org/abs/2606.23574v1](https://arxiv.org/abs/2606.23574v1)
