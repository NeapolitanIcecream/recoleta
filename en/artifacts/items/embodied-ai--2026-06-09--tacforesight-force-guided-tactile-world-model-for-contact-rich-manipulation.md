---
source: arxiv
url: https://arxiv.org/abs/2606.11184v1
published_at: '2026-06-09T17:59:03'
authors:
- Yujie Zang
- Yuhang Zheng
- Xian Nie
- Yupeng Zheng
- Shuai Tian
- Songen Gu
- Chen Gao
- Zining Wang
- Shuicheng Yan
- Wenchao Ding
topics:
- robot-world-model
- tactile-sensing
- force-feedback
- contact-rich-manipulation
- visuo-tactile-policy
- real-robot-evaluation
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation

## Summary
TacForeSight is a force-conditioned tactile world model and policy for real-robot contact-rich manipulation. It predicts short-horizon tactile latents from wrist force/torque and current tactile input, then uses those predictions to guide action generation.

## Problem
- Contact-rich tasks fail when the robot reacts only after slip, misalignment, or contact loss appears in tactile feedback.
- Wrist force/torque can change before fingertip tactile deformation becomes clear, so the policy needs to use force as an early signal for future contact state.
- The problem matters for wiping, swiping, insertion, locking, and recovery after mid-task disturbances, where small contact errors can stop the task.

## Approach
- TacForceWM encodes dual-finger tactile fields into compact latents and predicts future tactile latent chunks conditioned on high-rate 6-axis wrist force/torque.
- A temporal force encoder uses causal 1D convolutions and downsampling to align 120 Hz force/torque data with 30 Hz tactile observations.
- The latent dynamics predictor uses a Transformer with AdaLN force conditioning, trained with MSE on future tactile latents plus temporal-difference loss and SIGReg regularization.
- The policy compares current tactile latents with predicted future tactile latents through cross-attention, then uses a tactile-guided channel gate to fuse visual and tactile features.
- A conditional flow-matching action head predicts future action chunks from visual, tactile, force-derived, and proprioceptive features.

## Results
- On five real-robot contact-rich tasks, TacForeSight reports a 79.0% average completion score, compared with 43.0% for the strongest listed baseline, RDP.
- Task scores for TacForeSight are 100% on Vase Wiping, 85% on Card Swiping, 70% on Tube Adjustment and Insertion, 80% on Bulb Insertion and Locking, and 60% on Wire Insertion.
- Under in-process perturbations, TacForeSight reports an 86.7% average score, compared with 33.3% for RDP, the strongest listed perturbation baseline.
- Perturbation scores for TacForeSight are 90% on Wiping-P, 85% on Swiping-P, and 85% on Adjustment-P.
- The system runs at 20 Hz on an RTX 4090D GPU and was evaluated with 20 independent trials per method and task.
- TacForceWM has 11.8M parameters and was trained on 2,700 force-tactile interaction episodes; the downstream flow-matching policy has 68.9M parameters.

## Link
- [https://arxiv.org/abs/2606.11184v1](https://arxiv.org/abs/2606.11184v1)
