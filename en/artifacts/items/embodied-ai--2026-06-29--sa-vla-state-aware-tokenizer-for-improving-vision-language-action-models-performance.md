---
source: arxiv
url: https://arxiv.org/abs/2606.30113v1
published_at: '2026-06-29T10:45:53'
authors:
- Tengyue Jiang
- Chunpu Xu
- Jiayue Kang
- Yao Mu
topics:
- vision-language-action
- action-tokenization
- state-conditioned-decoding
- sim2real
- robot-manipulation
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# SA-VLA: State-aware tokenizer for improving Vision-Language-Action Models' performance

## Summary
SA-VLA improves discrete action tokenizers for VLA robot policies by decoding action tokens with the robot's current proprioceptive state. The paper reports higher success on RoboTwin manipulation tasks and zero-shot sim-to-real trials.

## Problem
- Discrete VLA policies must recover continuous robot actions from action tokens, but common tokenizers map each token to one fixed action prototype.
- Manipulation depends on joint configuration, object pose, and contact state, so the same token can need different continuous controls in different states.
- This compression gap matters because poor action reconstruction lowers task success even when the vision-language model predicts useful action tokens.

## Approach
- SA-VLA conditions action decoding on the current robot state, usually joint angles, while keeping a discrete action-token interface for LLM-based VLA policies.
- Method A injects state through cross-attention between state features and action features inside the VQ-VAE encoder and decoder.
- Method B uses a lightweight MLP adapter to predict per-action-dimension scaling factors from state; actions are divided by the scale before quantization and multiplied back after decoding.
- Method B lets one codebook token decode to a family of state-dependent continuous actions, which expands the effective support of a finite VQ codebook.
- The VLA uses text tokens, 256-bin discretized state tokens, SigLIP image tokens from 224×224 images, and fixed-length action tokens for autoregressive or parallel decoding.

## Results
- On 12 RoboTwin tasks with 1,600 trajectories per task and 100 rollouts per task, Method B reaches 0.56 average success with autoregressive decoding and 0.56 with parallel decoding.
- The strongest baseline in the RoboTwin table, VQ-BET, reaches 0.29 average success; binning reaches 0.24 and FAST reaches 0.17.
- Method A also improves over baselines, with 0.55 average success under autoregressive decoding and 0.52 under parallel decoding on RoboTwin.
- The state ablation shows gains over tokenizers without state: no-state PD is 0.43, no-state AR is 0.51, Method A is 0.52 PD and 0.55 AR, and Method B is 0.56 for both PD and AR.
- In zero-shot sim-to-real tests on Click Bell, Place Container Plate, and Pick Diverse Bottles with 20 trials each, Method B AR averages 0.33 success versus VQ-BET at 0.15, binning at 0.10, and FAST at 0.08.
- Real-world Method B AR records 10/20 on Click Bell, 7/20 on Place Container Plate, and 3/20 on Pick Diverse Bottles; Method B PD averages 0.27.

## Link
- [https://arxiv.org/abs/2606.30113v1](https://arxiv.org/abs/2606.30113v1)
