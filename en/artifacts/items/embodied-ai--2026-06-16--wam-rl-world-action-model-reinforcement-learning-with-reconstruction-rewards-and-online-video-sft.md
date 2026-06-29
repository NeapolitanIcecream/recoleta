---
source: arxiv
url: https://arxiv.org/abs/2606.17906v1
published_at: '2026-06-16T13:29:12'
authors:
- Zezhong Qian
- Xiaowei Chi
- Yu Qi
- Haozhan Li
- Zhi Yang Chen
- Shanghang Zhang
topics:
- world-action-model
- robot-rl
- world-model-adaptation
- reconstruction-rewards
- long-horizon-manipulation
- libero-rlbench
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# WAM-RL: World-Action Model Reinforcement Learning with Reconstruction Rewards and Online Video SFT

## Summary
WAM-RL trains both parts of a World-Action robot policy during online interaction: the video world model and the action model. This matters because WA models trained only on demonstrations struggle with fine manipulation, error recovery, and long-horizon tasks outside the demo data.

## Problem
- Existing WA models depend on expert trajectories, so policies stay close to demo support and learn limited fine-grained skills.
- Actor-only RL can improve short-horizon tasks, while long-horizon success remains limited by prediction errors in the world model.
- Online world-model updates can shift latent features and break the actor’s learned mapping from latent predictions to actions.

## Approach
- The method builds on Genie Envisioner-ACT, with a DiT video generator as the world model and an actor that reads intermediate latent features and outputs robot actions.
- During rollouts, the world model predicts future observations, the actor executes actions, and real observations are used to update both modules.
- The world model is updated with online video SFT on successful trajectories, with KL regularization that keeps latent features close to a frozen pretrained copy.
- The actor is optimized with policy gradients using a reconstruction reward that compares imagined future observations with executed future observations.
- The reward variants tested include pixel MSE, optical flow MSE, DINO feature MSE, and V-JEPA2 feature similarity; Flow-SDE supplies stochastic denoising transitions and action likelihoods for the flow-based actor.

## Results
- On LIBERO-Object, success improved from 68% for the Base model to 82% for WAM-RL; actor-only π_RL reached 78%.
- On RLBench Water Plants, success improved from 19% for Base to 22% for WAM-RL; actor-only π_RL reached 18%.
- In the RLBench Water Plants reward ablation, Pixel MSE reached 21%, Optical Flow MSE 19%, DINO MSE 16%, and V-JEPA2 17%, compared with Base at 19% and actor-only π_RL at 18%.
- Training used 8 NVIDIA A800 GPUs for 8 hours under mixed online RL and video fine-tuning.
- The paper reports qualitative recovery behavior after online video SFT, such as gripper repositioning and re-grasping after failed grasps; the excerpt gives no numeric recovery-rate metric.

## Link
- [https://arxiv.org/abs/2606.17906v1](https://arxiv.org/abs/2606.17906v1)
