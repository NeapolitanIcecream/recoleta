---
source: arxiv
url: https://arxiv.org/abs/2605.13105v1
published_at: '2026-05-13T07:15:37'
authors:
- Yuanfang Peng
- Jingjing Fu
- Chuheng Zhang
- Li Zhao
- Jiang Bian
- Mingyu Liu
- Ling Zhang
- Jun Zhang
- Rui Wang
topics:
- vision-language-action
- rl-fine-tuning
- robot-manipulation
- visual-generalization
- sim2real
- policy-regularization
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# What to Ignore, What to React: Visually Robust RL Fine-Tuning of VLA Models

## Summary
PAIR-VLA adds action-distribution guidance to PPO fine-tuning so VLA robot policies ignore task-irrelevant visual changes and react to task-relevant ones. It improves ManiSkill3 pick-and-place success under OOD visual shifts for OpenVLA and π₀.₅ without changing inference-time architecture.

## Problem
- Standard PPO rewards tell the robot whether the task succeeded, but they do not tell it whether a visual change should leave the action unchanged or require a different action.
- VLA policies can fail under deployment visual shifts such as unseen distractors, table textures, lighting, camera viewpoints, and target object poses.
- This matters for robot manipulation because a distractor or texture change should often be ignored, while a moved target object can require a new grasp or trajectory.

## Approach
- PAIR-VLA fine-tunes OpenVLA and π₀.₅ with PPO plus two auxiliary losses computed on paired visual variants of the same observation.
- The task-preserving variant removes distractors and swaps background appearance while keeping the robot, target object, receptacle, and required manipulation fixed.
- The invariance loss minimizes KL divergence between action distributions for the original view and the task-preserving view.
- The task-altering variant perturbs the target object pose, which can change the required action.
- The sensitivity loss maximizes a clipped KL divergence between action distributions for the original view and the task-altering view; these losses are used only during training, so deployment has no extra inference cost.

## Results
- On ManiSkill3 pick-and-place, OpenVLA average OOD success improved from 77.90% with PPO to 87.00% with PAIR-VLA, a +9.10 point gain across table texture, lighting, target pose, and clutter tests.
- OpenVLA per-setting gains were 86.98%→94.53% on table texture, 72.14%→80.47% on lighting, 83.59%→90.63% on target pose, and 68.88%→82.36% on clutter.
- On π₀.₅, average OOD success improved from 46.25% with PPO to 62.87%, a +16.62 point gain.
- π₀.₅ per-setting gains were 63.54%→80.21% on table texture, 28.54%→51.67% on lighting, 56.46%→69.38% on target pose, and 36.46%→50.21% on clutter.
- Each reported success rate used 128 evaluation episodes, averaged over 3 independent runs.
- In an OpenVLA in-distribution test with 1 distractor, PAIR-VLA reached 90% success in about 80 training steps, while PPO needed about 240 steps, a roughly 3× training-step reduction.

## Link
- [https://arxiv.org/abs/2605.13105v1](https://arxiv.org/abs/2605.13105v1)
