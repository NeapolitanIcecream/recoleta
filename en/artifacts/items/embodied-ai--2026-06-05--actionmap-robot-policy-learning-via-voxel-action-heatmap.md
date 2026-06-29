---
source: arxiv
url: https://arxiv.org/abs/2606.06904v1
published_at: '2026-06-05T04:42:56'
authors:
- Pei Yang
- Hai Ci
- Yanzhe Chen
- Qi Lv
- Han Cai
- Mike Zheng Shou
topics:
- vision-language-action
- robot-policy-learning
- action-decoder
- voxel-heatmap
- data-efficiency
- manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# ActionMap: Robot Policy Learning via Voxel Action Heatmap

## Summary
ActionMap replaces single-point action decoders in vision-language-action robot policies with voxel heatmaps over translation, rotation, and gripper actions. It reports higher success rates, faster training, and better low-data performance on LIBERO and real Franka tasks without changing the VLA backbone.

## Problem
- Current VLA action decoders usually output one action point through token bins, L1 regression, or flow matching, so training loses the geometry of nearby actions.
- This matters for robot manipulation because small end-effector errors can cause grasp, sweep, or insertion failures.
- The paper tests whether action representation alone can improve VLA policies, separate from larger backbones or more robot data.

## Approach
- ActionMap is a drop-in MLP action head that reads the VLA action-token hidden states and replaces the native decoder.
- The head predicts separate probability grids for 3D translation, 3D rotation, and the binary gripper command.
- Training converts each ground-truth action into a soft Gaussian blob over the voxel grid and uses cross-entropy against the predicted heatmap.
- At inference, it recovers a continuous action with top-k soft argmax, using k=10 and temperature 1.0 in the main experiments; the gripper uses argmax.
- The paper plugs the head into OpenVLA-OFT and pi0.5 while leaving the rest of each policy unchanged.

## Results
- On LIBERO, ActionMap improves the four-suite average over OpenVLA-OFT L1 regression from 89.1% to 97.3%, a +8.2 point gain at matched 10K training steps.
- On LIBERO with pi0.5, it improves the four-suite average from 96.9% to 98.5%, a +1.6 point gain at matched 30K training steps.
- On LIBERO-Long, the largest gains are +26.6 points on OpenVLA-OFT and +4.8 points on pi0.5.
- At 10% LIBERO-Spatial data, equal to 43 demonstrations, ActionMap gets 93.2% while OpenVLA-OFT L1 regression gets 67.2%, a +26.0 point gap.
- On real Franka tasks at full data, ActionMap succeeds in 20/30 trials versus 7/30 for OpenVLA-OFT L1 regression; at 50 demonstrations per task, it gets 14/30 versus 4/30.
- On the Franka Pick task, ActionMap reports 4.8 mm grasp-position error at full data and 15.0 mm at 50 demonstrations, about 2 to 3 times lower error than the L1 regression head.

## Link
- [https://arxiv.org/abs/2606.06904v1](https://arxiv.org/abs/2606.06904v1)
