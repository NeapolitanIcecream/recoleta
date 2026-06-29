---
source: arxiv
url: https://arxiv.org/abs/2606.02194v1
published_at: '2026-06-01T12:49:14'
authors:
- Christian Scherer
- Joe Watson
- Theo Gruner
- Daniel Palenicek
- Ingmar Posner
- Jan Peters
topics:
- vision-language-action
- robot-foundation-model
- imitation-learning
- inverse-rl
- dexterous-manipulation
- policy-finetuning
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Coherent Off-Policy Improvement of Large Behavior Models with Learned Rewards

## Summary
CSIL++ uses inverse reinforcement learning with a coherent learned reward to improve pi-0.5 on sparse simulated manipulation tasks without the usual early RL performance drop. The work is relevant to VLA and large behavior model finetuning, with evidence limited to simulation in the provided excerpt.

## Problem
- Behavioral cloning can train strong large behavior models for robot control, but small rollout errors can move the robot into states outside the demonstration data.
- Sparse-reward RL finetuning can waste samples and can degrade the pretrained policy early in training.
- Dense hand-written rewards are hard to design for varied manipulation tasks, so the paper uses demonstrations to learn a dense reward.

## Approach
- The method trains a small BC policy on expert demonstrations and turns it into a coherent reward: `alpha * (log pi_BC(a|s) - log p(a|s))`.
- This reward gives high score to demonstrated actions in familiar states, low score to wrong actions in familiar states, and near-zero score in unseen states.
- The frozen pi-0.5 VLA proposes action chunks every 10 steps, while a smaller CSIL++ policy acts every step.
- CSIL++ uses an ensemble action, averaging the VLA action and the learned policy action, rather than adding a residual correction.
- The implementation adds a categorical critic, batch normalization, weight normalization, exact Gaussian KL estimation, per-camera image encoders, and spatial softmax pooling.

## Results
- On six simulated sparse-reward manipulation tasks, CSIL++ Ensemble matched or improved the pi-0.5 VLA baseline on every task in Table 1.
- CSIL++ Ensemble reached at least 90% success on 5 of 6 tasks: Square 0.94, Coffee 0.96, Mug Cleanup 0.90, Threading 0.92, and Hammer Cleanup 1.00.
- Threading showed the largest gain: pi-0.5 VLA was 0.14 success, while CSIL++ Ensemble reached 0.92 at 450k steps.
- Mug Cleanup improved from 0.68 for the VLA to 0.90 with CSIL++ Ensemble at 100k steps.
- Square improved from 0.84 for the VLA to 0.94 with CSIL++ Ensemble at 100k steps; Coffee improved from 0.78 to 0.96 at 200k steps.
- Nut Assembly was the main failure case: CSIL++ Ensemble stayed at 0.22, equal to the VLA baseline, while CSIL++ Residual reached 0.40 and XQC+OD Residual reached 0.34.

## Link
- [https://arxiv.org/abs/2606.02194v1](https://arxiv.org/abs/2606.02194v1)
