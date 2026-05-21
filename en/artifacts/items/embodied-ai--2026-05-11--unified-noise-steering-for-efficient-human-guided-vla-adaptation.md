---
source: arxiv
url: https://arxiv.org/abs/2605.10821v1
published_at: '2026-05-11T16:37:34'
authors:
- Junjie Lu
- Xinyao Qin
- Yuhua Jiang
- Kaixin Wang
- Chuheng Zhang
- Bin Liang
- Jun Yang
- Min Xu
- Li Zhao
topics:
- vision-language-action
- robot-policy-adaptation
- human-guided-learning
- noise-space-rl
- flow-matching
- real-world-manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Unified Noise Steering for Efficient Human-Guided VLA Adaptation

## Summary
UniSteer adapts diffusion or flow-matching VLA robot policies by converting human corrective actions into noise targets for a small noise actor. The method keeps the pretrained VLA frozen and reports higher real-world success with less human data than noise-space RL and action-space DAgger.

## Problem
- Pretrained VLA policies often fail under real-world shifts in object pose, scene layout, viewpoint, and contact dynamics.
- On-robot RL is slow and costly because failures consume time and sparse rewards give weak learning signals.
- Human corrections are given as actions, while noise-space VLA finetuning trains a policy over latent noise, so the two signals need a shared training target.

## Approach
- UniSteer freezes the flow-matching VLA decoder and trains a lightweight actor that chooses the initial noise variable.
- When a human takes over, the method approximately inverts the frozen decoder to map the corrected action chunk back to an initial noise target.
- The inversion runs backward through the Euler flow steps using fixed-point iteration.
- Corrected noise targets train the actor with an L2 supervision loss, while autonomous and corrected transitions also train a noise-space critic for RL.
- The same noise actor receives both reward-based updates and human-correction updates.

## Results
- On four real-world tasks, UniSteer raised average success from 20.0% for the initial policy to 90.0% after 66 minutes of adaptation.
- Average success was 90.0% for UniSteer, 55.0% for DSRL, and 60.0% for DAgger, giving UniSteer gains of 35 and 30 percentage points over those baselines.
- Task success rates for UniSteer were 90.0% on Pick up Spoon, 95.0% on Stack Blocks, 100.0% on Insert Square, and 75.0% on Fold Towel.
- On OOD object placements, UniSteer reached 100.0% success on Pick up Spoon, Stack Blocks, and Insert Square; DSRL reached 0.0%, 0.0%, and 25.0%, while DAgger reached 75.0%, 100.0%, and 25.0%.
- UniSteer used 0.98 pure human trajectories per round on average, while DAgger used 8 pure human trajectories per round.
- Fixed-point inversion had lower action reconstruction loss and lower time than optimization-based inversion: on Pick up Spoon, 0.00122 loss and 73.26 s total versus 0.06516 loss and 208.04 s; on Insert Square, 0.00018 loss and 40.42 s versus 0.05624 loss and 80.96 s.

## Link
- [https://arxiv.org/abs/2605.10821v1](https://arxiv.org/abs/2605.10821v1)
