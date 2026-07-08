---
source: arxiv
url: https://arxiv.org/abs/2607.06558v1
published_at: '2026-07-07T17:58:11'
authors:
- Haoyu Zhao
- Xingyue Zhao
- Hangyu Li
- Biao Gong
- Kehan Li
- Siteng Huang
- Xin Li
- Deli Zhao
- Zhongyu Li
topics:
- action-conditioned-world-model
- digital-teleoperation
- robot-data-scaling
- sim2real
- dexterous-manipulation
- imitation-learning
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# RynnWorld-Teleop: An Action-Conditioned World Model for Digital Teleoperation

## Summary
RynnWorld-Teleop claims that robot demonstrations can be collected through a real-time, action-conditioned video world model instead of a physical robot. It turns operator hand poses into generated robot egocentric video and aligned robot actions for imitation learning.

## Problem
- Robot learning needs large, varied trajectory data, but physical teleoperation ties each demo to robot hardware, workspace setup, object availability, and manual resets.
- Existing human-to-robot video translation gives robot-looking videos without recoverable robot actions, so it cannot produce full state-action training data.
- Existing action-conditioned egocentric world models stay human-centric, so they do not close the visual and action gap for robot policy training.

## Approach
- The operator provides a hand-pose stream. RynnWorld-Teleop conditions on that stream plus one reference image and generates robot-centric egocentric video.
- The hand poses are rendered as 21-joint depth-aware skeleton videos, where joint color and size encode camera-space depth before a VAE maps them into video latent space.
- A Wan2.2-TI2V-5B video Diffusion Transformer gets a separate pose patch-embedding branch with distribution alignment and a learnable gate for pose control.
- Training uses human egocentric video pretraining, then robot-domain adaptation on paired human-robot teleoperation data.
- A causal student model is distilled from a bidirectional teacher with streaming autoregressive generation, KV caching, 4-step sampling, and chunked re-anchoring for long rollouts.

## Results
- The distilled model runs at 40+ FPS for interactive generation on one NVIDIA H100 GPU.
- Training data includes VITRA with 30.7M frames and 1.23M slices, EgoDex with 74.0M frames and 0.91M slices, and the authors' robot data with 0.43M frames and 5.3K slices.
- The robot-domain data contains 1,800 real-world demonstration episodes across 4 tasks: 500 Dual Picking, 500 Block Pushing, 500 Bimanual Lifting, and 300 Lid Placement.
- The generated policy dataset pairs RGB frames with 54-dimensional robot actions covering dual 7-DoF arms and dual 20-DoF dexterous hands.
- The paper claims policies trained only on generated data achieve zero-shot Sim2Real transfer across dexterous bimanual tasks, and that adding generated data to real datasets improves success rates. The excerpt does not provide the actual success-rate values or baseline table.
- The data pipeline synthesizes skeleton-conditioned video at 16 FPS and uses 81-frame chunks for re-anchoring during long-horizon generation.

## Link
- [https://arxiv.org/abs/2607.06558v1](https://arxiv.org/abs/2607.06558v1)
