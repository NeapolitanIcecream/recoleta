---
source: arxiv
url: https://arxiv.org/abs/2606.23680v1
published_at: '2026-06-22T17:59:20'
authors:
- Sikai Li
- Shuning Li
- Zhenyu Wei
- Yunchao Yao
- Chenran Li
- Mingyu Ding
topics:
- dexterous-manipulation
- humanoid-locomotion
- loco-manipulation
- latent-action-space
- reinforcement-learning
- motion-priors
relevance_score: 0.57
run_id: materialize-outputs
language_code: en
---

# CoorDex: Coordinating Body and Hand Priors for Continuous Dexterous Humanoid Loco-Manipulation

## Summary
CoorDex trains a humanoid with a dexterous hand to grasp, carry, open, and turn objects while walking, using separate learned priors for the body and fingers.

## Problem
- Humanoid loco-manipulation often splits walking and manipulation into separate phases, which avoids the harder case where the robot must grasp while its body is still moving.
- High-DoF hands make direct reinforcement learning hard because the policy must coordinate balance, wrist placement, finger preshape, contact, and object transport at the same time.
- The problem matters because real humanoids need finger-level manipulation during motion, not only gripper-style open-close actions after stopping.

## Approach
- CoorDex trains two motion priors: a body prior for locomotion, reaching, and wrist placement, and a wrist-stabilized hand prior for active finger joints.
- Each prior starts with a privileged motion-tracking teacher trained from simulated demonstrations, then gets distilled into a proprioception-conditioned latent prior and decoder.
- Downstream PPO keeps both priors frozen and predicts residual corrections in latent space instead of raw joint targets.
- A shared coordination trunk reads task state, object geometry, contact features, proprioception, prior means, and the previous residual; separate residual heads output body and hand latent corrections.
- The decoded actions are joint-position targets for a 29-DoF Unitree G1 body and a 20-DoF WUJI hand, with latent dimensions of 16 for the body and 12 for the hand.

## Results
- Evaluation uses 50,000 episodes collected with 10,000 parallel Isaac Lab simulation environments.
- On WalkGrab, CoorDex reaches 0.55 success, 0.00 fall rate, and 0.40 drop rate; it keeps moving near the bottle with about 0.25 m/s forward velocity at the grasp point.
- On OpenFridge, it reaches 0.66 success and 0.00 fall rate, with a door angle of 57.76° against a 60° target.
- On WalkPickTurn, it reaches 0.89 success, 0.01 fall rate, 0.10 drop rate, and 9.98° minimum heading error for the 180° turn task.
- WalkGrab ablations under the same PPO budget fail with direct or weaker action spaces: All Joint Space has 0 success, 1.00 reach, 0.00 grasp, 0.86 stop, and 0.04 fall; Body Prior + Hand Joint Space has 0 success, 0.96 reach, 0.01 grasp, 0.90 stop, and 0.04 fall.
- With both priors available, Monolithic Latent Residual still has 0.00 success, 0.40 action rate, and 0.02 fall, while CoorDex has 0.55 success, 0.22 action rate, and 0.00 fall.

## Link
- [https://arxiv.org/abs/2606.23680v1](https://arxiv.org/abs/2606.23680v1)
