---
source: arxiv
url: https://arxiv.org/abs/2607.02466v1
published_at: '2026-07-02T17:33:37'
authors:
- Junhao Shi
- Siyin Wang
- Xiaopeng Yu
- Li Ji
- Jingjing Gong
- Xipeng Qiu
topics:
- vision-language-action
- robot-data-scaling
- generalist-robot-policy
- inverse-dynamics
- task-agnostic-pretraining
- robot-random-play
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Learning to Move Before Learning to Do: Task-Agnostic pretraining for VLAs

## Summary
TAP pretrains a VLA on task-agnostic robot motion before language-conditioned behavior cloning. The main claim is that cheap unlabeled interaction data can teach low-level physical control and reduce dependence on expert teleoperation.

## Problem
- VLA training usually needs observation-language-action triples collected by human teleoperation, which is expensive and slow to scale.
- Many robot trajectories without useful task labels are discarded, even though they contain contact, grasping, pushing, and object-motion information.
- This matters because generalist robot policies need more physical interaction data than teams can collect with annotated expert demonstrations alone.

## Approach
- TAP uses task-agnostic trajectories from two sources: unrelated Bridge trajectories in simulation and autonomous random play on a WidowX 250s robot.
- Stage 1 trains with inverse dynamics: given observation `o_t` and next observation `o_{t+1}`, the model predicts the 7D delta-pose action `a_t` that caused the change.
- The inverse-dynamics target makes the model attend to moving hands and objects instead of static background pixels.
- Stage 2 finetunes the same backbone and action head with a small set of language-labeled expert demonstrations, using standard behavior cloning.
- The real-world random-play pipeline builds a safe pose library, samples reachable waypoints, adds a contact heuristic, injects bounded Gaussian noise, and records the resulting trajectories.

## Results
- In SIMPLER, TAP-20k reaches 33.32% Avg-All success, compared with 23.15% for the same architecture trained with standard behavior cloning, 7.75% for OpenVLA, and 3.03% for RT-1-X.
- SIMPLER Avg-Partial success for TAP-20k is 45.82%, compared with 31.79% for standard behavior cloning, 42.30% for Octo, and 53.10% for π0.
- SIMPLER Avg-Entire success for TAP-20k is 20.82%, compared with 14.50% for standard behavior cloning, 20.33% for Octo, and 27.05% for π0.
- More task-agnostic pretraining improves SIMPLER Avg-All success across 8k, 14k, and 20k episodes: 24.47%, 30.21%, and 33.32%.
- In real-world WidowX tests with 30 hours of random play and 200 expert demonstrations per task, TAP averages 28% on carrot-on-plate versus 9% for training from scratch and 36% for NORA.
- On the real-world push-pumpkin task, TAP averages 61% versus 21% for training from scratch and 56% for NORA; under background texture shift it scores 65% versus 0% and 55%, and under viewpoint variation it scores 25% versus 0% and 0%.

## Link
- [https://arxiv.org/abs/2607.02466v1](https://arxiv.org/abs/2607.02466v1)
