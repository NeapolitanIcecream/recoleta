---
source: arxiv
url: https://arxiv.org/abs/2605.17522v1
published_at: '2026-05-17T16:11:22'
authors:
- Sixu Lin
- Junliang Chen
- Huaiyuan Xu
- Zhuohao Li
- Guangming Wang
- Yixiong Jing
- Sheng Xu
- Runyi Zhao
- Brian Sheil
- Lap-Pui Chau
- Guiliang Liu
topics:
- robot-world-model
- flow-guided-manipulation
- vision-language-action
- 3d-motion-planning
- real-time-robot-control
- sim2real
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# RoboFlow4D: A Lightweight Flow World Model Toward Real-Time Flow-Guided Robotic Manipulation

## Summary
RoboFlow4D predicts multi-frame 3D gripper flows from RGB images and text, then uses those flows to guide a robot policy in a closed loop. It targets real-time manipulation by replacing multi-model 3D flow pipelines with one lightweight diffusion transformer model.

## Problem
- 2D flow planners operate in image space, so they miss depth and geometry needed for collision-free manipulation.
- Recent 3D flow planners often chain video generation, depth, grounding, and point tracking models, which adds latency and memory cost.
- Real robots need low-latency planning that can update from new observations during a task.

## Approach
- RoboFlow4D takes recent RGB frames, an optional set of 2D query points, and a language instruction as input.
- DINOv2 and SigLIP encode vision and text; a 3D Perceiver learns 3D-aware features by aligning with VGGT features.
- A diffusion transformer called FlowDiT denoises future 3D trajectories and outputs multi-frame flows with shape `keypoints × frames × 3D position`.
- The action policy receives both normal state inputs and an encoded flow plan, so it can track the predicted motion.
- Control runs as a slow-fast loop: RoboFlow4D plans lower-frequency atomic-task trajectories, while the policy executes higher-frequency action chunks.

## Results
- On LIBERO with Diffusion Policy, average success rises from 78.9% to 85.1%, a +6.2 point gain; suite gains are +8.2 Spatial, +1.7 Object, +6.8 Goal, and +8.0 Long.
- On LIBERO with a DiT policy, average success rises from 83.7% to 87.7%, a +4.0 point gain; suite gains are +6.0 Spatial, +0.7 Object, +3.0 Goal, and +6.4 Long.
- The paper reports a +11.0 point average gain on ManiSkill3 and shows DP improving from 12.3% to 22.0% average on the visible PushCube, PickCube, and StackCube table rows.
- Real-world tasks improve by 5 to 20 percentage points according to the paper excerpt.
- The authors claim under 1 second planning latency, a 120× speedup over modular flow pipelines, and more than 24% smaller model scale than other flow models.

## Link
- [https://arxiv.org/abs/2605.17522v1](https://arxiv.org/abs/2605.17522v1)
