---
source: arxiv
url: https://arxiv.org/abs/2606.31232v1
published_at: '2026-06-30T07:08:24'
authors:
- Zhenghao Zhang
- Yuanxiang Wang
- Zhenyu Guan
- Yujia Yang
- Bingkang Shi
- Tianyu Zong
- Hongzhu Yi
- Guoqing Chao
- Xingchen Chen
- Tiankun Yang
- Chenxi Bao
- Tao Yu
- Jingjing Zhou
- Jungang Xu
topics:
- world-model
- latent-dynamics
- visual-control
- robot-manipulation
- planning
- representation-learning
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# Delta-JEPA: Learning Action-Sensitive World Models via Latent Difference Decoding

## Summary
Delta-JEPA is a reconstruction-free latent world model for visual continuous-control planning. Its main idea is to decode the executed action from the change between two latent states, which pushes the latent dynamics to preserve action effects.

## Problem
- JEPA-style latent world models can collapse to near-constant embeddings when trained only with latent prediction loss, so low loss can hide unusable planning states.
- Pixel reconstruction adds compute and can spend capacity on visual detail that does not help control.
- Planning needs latent rollouts where different candidate actions lead to different predicted states.

## Approach
- An encoder maps images to latent states, and a dynamics predictor forecasts the next latent state from the current latent state and continuous action.
- The Latent Difference Action Decoder computes Δz = z_{t+1} - z_t and reconstructs the executed action from that displacement.
- The model trains end-to-end with two losses: latent next-state mean squared error and action reconstruction mean squared error, weighted by λ.
- A multi-step version decodes a sequence of N actions from z_{t+N} - z_t using a small Transformer with N learned action queries.
- The method avoids pixel reconstruction, frozen encoders, stop-gradient branches, and distribution-matching regularizers.

## Results
- On planning success rate over 3 seeds, Delta-JEPA is best on all 4 tasks: Two-Room 100.00±0.00, Reacher 81.33±0.50, Push-T 89.07±1.90, and OGB-Cube 79.27±1.81.
- Against the strongest baseline per task, it gains +6.27 points on Two-Room over PLDM 93.73±1.03, +0.33 on Reacher over Sub-JEPA 81.00±2.40, +4.54 on Push-T over LeWM 84.53±1.50, and +15.14 on OGB-Cube over LeWM 64.13±1.89.
- The displacement decoder beats endpoint-concat action decoding on all 4 tasks: +4.07 points on Two-Room, +1.07 on Reacher, +12.60 on Push-T, and +0.67 on OGB-Cube.
- On Reacher target ablations, decoding raw action performs best at 81.33±0.50, compared with Δ finger position 64.93±1.10, Δ joint position 80.47±2.10, and both deltas 76.40±1.40.
- A Push-T λ ablation reports near collapse at λ=0, weak performance at λ=0.1, stable higher planning success for mid-range λ values, and the best result at λ=50.0.

## Link
- [https://arxiv.org/abs/2606.31232v1](https://arxiv.org/abs/2606.31232v1)
