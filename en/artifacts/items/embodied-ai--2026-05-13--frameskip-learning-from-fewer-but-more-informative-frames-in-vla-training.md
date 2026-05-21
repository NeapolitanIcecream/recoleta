---
source: arxiv
url: https://arxiv.org/abs/2605.13757v1
published_at: '2026-05-13T16:38:05'
authors:
- Bin Yu
- Shijie Lian
- Xiaopeng Lin
- Zhaolong Shen
- Yuliang Wei
- Changti Wu
- Hang Yuan
- Haishan Liu
- Bailing Wang
- Cong Huang
- Kai Chen
topics:
- vision-language-action
- robot-policy
- frame-selection
- robot-data-scaling
- dexterous-manipulation
- dataloader-training
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# FrameSkip: Learning from Fewer but More Informative Frames in VLA Training

## Summary
FrameSkip is a training-time frame selection method for VLA policies. It keeps 20% of unique trajectory frames in the main setting and reports higher success than full-frame training across RoboCasa-GR1, SimplerEnv, and LIBERO.

## Problem
- Dense robot demonstrations contain many low-change frames, so uniform sampling gives much of the training budget to approach, carry, and other smooth segments.
- Critical events such as alignment, contact, grasp closure, and release are sparse, which can leave VLA policies weak at the steps that decide task success.
- This matters for robot data scaling because large teleoperation datasets can grow in size without giving proportional supervision on manipulation-critical transitions.

## Approach
- FrameSkip scores each frame using action variation, visual-action coherence, task-progress priors, and gripper or end-effector transitions.
- Action variation uses local action changes and short look-ahead variation; visual-action coherence uses DINOv2 visual feature change divided by local action change.
- Task progress uses either a dataset-adaptive Gaussian mixture over annotated critical-stage locations or a simpler middle-of-trajectory Gaussian prior.
- The dataloader keeps the highest-scoring frames under a target retention ratio, while preserving first and last frames, gripper-transition frames, and top-decile action-change frames.
- The VLA model, action head, loss, optimizer recipe, and inference path stay unchanged; training uses a 5:1 mix of pruned minibatches and full-frame anchor minibatches after warmup.

## Results
- Main setting: FrameSkip retains 20% of unique frames and raises macro-average success across RoboCasa-GR1, SimplerEnv, and LIBERO from 66.50% with full-frame training to 76.15%.
- RoboCasa-GR1: average success over 24 tasks rises from 47.8% with full-frame training to 59.5% with FrameSkip; the training set uses 24K GR1 teleoperation simulation demonstrations.
- SimplerEnv: average success over 4 held-out WidowX tasks rises from 55.2% to 71.55%.
- SimplerEnv task gains include Stack Green Block on Yellow Block from 29.2% to 45.59% and Put Eggplant in Yellow Basket from 54.2% to 95.83%.
- The reported macro average and the shown RoboCasa-GR1 and SimplerEnv averages imply a LIBERO average near 97.4% for FrameSkip and 96.5% for full-frame training if the three benchmark averages are weighted equally.

## Link
- [https://arxiv.org/abs/2605.13757v1](https://arxiv.org/abs/2605.13757v1)
