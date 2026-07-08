---
source: arxiv
url: https://arxiv.org/abs/2607.06323v1
published_at: '2026-07-07T14:22:31'
authors:
- Xinye Yang
- Zhiyuan Ma
- Hongze Yu
- Yuanpei Chen
- Yaodong Yang
- Xiaojie Chai
- Xinlei Chen
- Chao Yu
topics:
- dexterous-manipulation
- latent-action-space
- residual-rl
- imitation-learning
- real-world-robot-learning
- motion-prior
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# LAMP: Latent Motion Prior-Guided Real-World Learning for Dexterous Hand Manipulation

## Summary
LAMP improves real-world dexterous hand learning by using a learned 2-D latent motion space for hand control during both imitation learning and residual RL. On four real robot tasks, it reports 98.75% average final success after online RL.

## Problem
- Dexterous hands have high-dimensional actions, so small imitation errors can compound into lost contact, drops, or stalled execution.
- Online RL in raw finger-joint space explores unsafe or useless hand motions, which wastes real robot trials and can damage hardware or objects.
- The problem matters because contact-rich manipulation needs reliable correction after demonstrations, especially when only small task-specific datasets are available.

## Approach
- LMPM trains an encoder on recent hand-action history and maps an 8-step hand-target history to a Gaussian prior in a 2-D latent space.
- A decoder maps each latent command back to a 6-D executable Ruiyan hand target, so the policy still sends normal hand commands to the robot.
- Behavior cloning predicts the 6-D arm command in the native arm space and predicts a latent hand offset around the current LMPM prior center.
- Online residual RL starts from the cloned policy, adds native arm residuals, and adds hand residuals in the same latent space before decoding the final hand target.
- The method uses real robot data from a Franka Research 3 arm, a Ruiyan dexterous hand, two RGB cameras, and task-specific demonstrations.

## Results
- Across Grasp & Place, Open Drawer, Pull Tissue, and Assemble Box, full LMPM reaches 56.25% average imitation-learning success and 98.75% average final RL success.
- Final RL success is 100% on Grasp & Place, 100% on Open Drawer, 95% on Pull Tissue, and 100% on Assemble Box.
- The method starts from small demonstration sets: 50 demos for Grasp & Place, 20 for Open Drawer, 20 for Pull Tissue, and 30 for Assemble Box.
- Removing the low-dimensional bottleneck drops average final RL success to 55.0%, with task scores of 35%, 85%, 80%, and 20%.
- Removing the history-conditioned encoder drops average final RL success to 73.75%, with task scores of 95%, 90%, 60%, and 50%.
- Raw BC without LMPM performs poorly: average IL success is 5.0%, and average final RL success is 3.75%.

## Link
- [https://arxiv.org/abs/2607.06323v1](https://arxiv.org/abs/2607.06323v1)
