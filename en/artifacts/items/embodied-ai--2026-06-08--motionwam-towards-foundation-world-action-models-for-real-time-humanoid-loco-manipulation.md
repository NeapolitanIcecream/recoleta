---
source: arxiv
url: https://arxiv.org/abs/2606.09215v1
published_at: '2026-06-08T08:50:14'
authors:
- Jia Zheng
- Teli Ma
- Yudong Fan
- Zifan Wang
- Shuo Yang
- Junwei Liang
topics:
- world-action-models
- humanoid-loco-manipulation
- vision-language-action
- whole-body-control
- egocentric-video
- robot-data-scaling
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# MotionWAM: Towards Foundation World Action Models for Real-Time Humanoid Loco-Manipulation

## Summary
MotionWAM is a real-time World Action Model for Unitree G1 humanoid loco-manipulation from one egocentric camera. It uses video world-model features and whole-body motion tokens to control legs, torso, height, feet, and hands in one action space.

## Problem
- Existing WAM policies are too slow for closed-loop humanoid control because they run iterative denoising over video-action latents.
- Many humanoid systems split control into upper-body manipulation and lower-body base commands, which blocks task-driven foot actions such as pedal stepping or ball kicking.
- The problem matters because real humanoid tasks need coordinated balance, locomotion, torso motion, reaching, and object contact in the same policy loop.

## Approach
- MotionWAM pairs a Video DiT initialized from Cosmos-Predict2.5-2B with a Motion DiT that predicts whole-body motion latents.
- The Video DiT runs one forward pass at a high-noise flow step and exposes intermediate denoising activations; the policy uses those features instead of waiting for a fully generated future video.
- The action output is a unified motion latent decoded by SONIC into joint commands, with discrete motion tokens for whole-body movement and continuous channels for grippers or dexterous hands.
- Training has 3 stages: pretrain the video branch on about 2,136 hours of egocentric human and humanoid video, post-train video plus action on heterogeneous Unitree G1 data, then fine-tune on 200 teleoperated episodes per task across 9 target tasks.

## Results
- On 9 real-world Unitree G1 tasks with 20 trials per task, MotionWAM reaches 76.1% average success versus 43.9% for the strongest baseline, GR00T-N1.7, a 32.2 point gain.
- MotionWAM reports the largest task gains on Kick Soccer (+40), Load Cart (+40), Retrieve Item (+40), Wipe Board (+45), and Do Laundry (+30) compared with the strongest listed baseline results.
- In a 5-task ablation, the full 3-stage model reaches 70.0% average success; removing Stage 1 drops to 59.0%, and removing Stage 2 drops to 42.0%.
- MotionWAM runs at 4.9 Hz on one NVIDIA A100 with 2.5B trainable parameters, compared with 0.7 Hz for Cosmos Policy, 6.5 Hz for GR00T-N1.7, and 9.0 Hz for Qwen3DiT.
- The paper claims task-driven foot interaction on real hardware, including ball kicking and pedal stepping, which the evaluated decoupled upper-lower control designs cannot express through their action interfaces.

## Link
- [https://arxiv.org/abs/2606.09215v1](https://arxiv.org/abs/2606.09215v1)
