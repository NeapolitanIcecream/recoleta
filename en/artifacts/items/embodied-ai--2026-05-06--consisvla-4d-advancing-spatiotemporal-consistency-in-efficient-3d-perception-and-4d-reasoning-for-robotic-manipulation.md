---
source: arxiv
url: https://arxiv.org/abs/2605.05126v1
published_at: '2026-05-06T16:55:44'
authors:
- Wei Li
- Jizhihui Liu
- Li Yixing
- Junwen Tong
- Rui Shao
- Liqiang Nie
topics:
- vision-language-action
- robot-manipulation
- 3d-perception
- spatiotemporal-reasoning
- generalist-robot-policy
- efficient-inference
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# ConsisVLA-4D: Advancing Spatiotemporal Consistency in Efficient 3D-Perception and 4D-Reasoning for Robotic Manipulation

## Summary
ConsisVLA-4D is a VLA robot manipulation model that adds compact multi-view 3D perception and future-scene reasoning to action prediction. It reports higher LIBERO and real-world performance than OpenVLA while using far fewer visual tokens.

## Problem
- 2D-only VLA models can confuse object identity, object relations, and scene changes during manipulation.
- Depth maps, point clouds, or long frame histories add sensor and compute cost, which matters for real robot inference.
- The paper targets action stability when object layouts are complex or change after the robot moves.

## Approach
- CV-Aligner uses SigLIP image-text similarity and FiLM conditioning to keep the Top-K instruction-relevant visual tokens; the default K is 32.
- Single-Fusion cross-attends those object tokens to VGGT 3D features so the same object can be matched across main, left, and right views.
- CO-Fuser combines DINOv2 geometric features with VGGT features across three views, then stores cross-object geometry in compact latent tokens.
- CS-Thinker trains auxiliary predictions for future dynamic object tokens and multi-view depth tokens; at inference, those learned tokens guide action decoding without explicit depth or object rollout.
- SC-Attn decodes the action chunk in parallel and trains with action L1 loss plus dynamic-object and depth losses.

## Results
- Compared with OpenVLA, the paper claims a 21.6% performance improvement and a 2.3x inference speedup on LIBERO.
- On real-world robot platforms, it claims a 41.5% performance improvement and a 2.4x inference speedup over OpenVLA.
- CV-Aligner uses about 1/8 of the original visual tokens after instruction-guided object selection.
- CO-Fuser compresses geometric information to about 1/12-1/8 of the original visual tokens.
- CS-Thinker's learned dynamic and depth tokens take less than 10% of the observation-instruction sequence during inference.

## Link
- [https://arxiv.org/abs/2605.05126v1](https://arxiv.org/abs/2605.05126v1)
