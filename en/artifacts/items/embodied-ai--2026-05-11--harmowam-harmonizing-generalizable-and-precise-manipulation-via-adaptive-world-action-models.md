---
source: arxiv
url: https://arxiv.org/abs/2605.10942v1
published_at: '2026-05-11T17:59:56'
authors:
- Qiuxuan Feng
- Jiale Yu
- Jiaming Liu
- Yueru Jia
- Zhuangzhe Wu
- Hao Chen
- Zezhong Qian
- Shuo Gu
- Peng Jia
- Siwei Ma
- Shanghang Zhang
topics:
- world-action-models
- vision-language-action
- robot-manipulation
- world-model
- adaptive-gating
- zero-shot-generalization
relevance_score: 0.98
run_id: materialize-outputs
language_code: en
---

# HarmoWAM: Harmonizing Generalizable and Precise Manipulation via Adaptive World Action Models

## Summary
HarmoWAM is a robot manipulation policy that combines a video world model with two action experts and a learned gate. It targets the gap between policies that can reach objects in new scenes and policies that can manipulate objects with fine control.

## Problem
- Existing World Action Models split into two patterns: video-first action inference has strong object-reaching behavior, while joint video-action modeling has better fine manipulation near the target.
- In the paper's two-task study, Imagine-then-Execute reaches targets at 10/10 in all OOD transit cases, yet interaction success falls as low as 2/10. Joint Modeling keeps 95% average OOD interaction success when initialized near the object, yet OOD transit falls to 32%.
- This matters because real robot tasks need both long transit to the right object and accurate contact, grasping, stacking, pouring, writing, or dual-arm coordination.

## Approach
- HarmoWAM uses Wan2.2-TI2V-5B as a world model, further trained on about 1.9M robot trajectories. It predicts 13 future video frames at 256x320 resolution with 5 denoising steps.
- A predictive expert is a 1B-parameter diffusion Transformer with 28 Transformer blocks. It uses current visual, text, and world-model latent features to generate temporally consistent action chunks for precise interaction.
- A reactive expert uses predicted future frames plus world-model latent features. DINOv2 extracts visual features, then an orientation decoder maps them to robot actions for transit and target approach.
- A Process-Adaptive Gating Mechanism classifies the current phase as transit or interaction from visual tokens. At inference, scores above 0.5 route control to the predictive expert; scores at or below 0.5 route control to the reactive expert.
- Training has two stages: world-model finetuning with flow matching, then action-expert and gate finetuning with diffusion loss, Smooth L1 action loss, and binary cross-entropy gate loss.

## Results
- Evaluation covers 6 real-world tasks: 4 single-arm tasks and 2 dual-arm tasks, with 100 demonstration trajectories per task and 20 independent evaluation episodes per task.
- In in-domain settings, HarmoWAM reports average gains of 15 percentage points over prior VLA models and 11 percentage points over prior WAMs.
- In OOD settings with background, position, and object variation, HarmoWAM reports average gains of 33 percentage points over prior VLA models and 29 percentage points over prior WAMs.
- The motivation study reports Imagine-then-Execute interaction success below 75% in-domain and below 55% OOD on average, while Joint Modeling OOD transit drops to 32%.
- Inference runs at 48 Hz with an action chunk size of 12.
- The paper also claims stronger long-horizon real-world deployment performance, but the excerpt does not provide exact long-horizon success rates.

## Link
- [https://arxiv.org/abs/2605.10942v1](https://arxiv.org/abs/2605.10942v1)
