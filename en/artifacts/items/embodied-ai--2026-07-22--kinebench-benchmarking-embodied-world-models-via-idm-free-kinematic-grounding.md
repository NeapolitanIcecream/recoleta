---
source: arxiv
url: https://arxiv.org/abs/2607.19876v1
published_at: '2026-07-22T08:04:17'
authors:
- Zeyu Liu
- Zhangzhe Zhu
- Yang Zhang
- Chenyou Fan
- Chenjia Bai
- Xuelong Li
topics:
- embodied-world-models
- robot-foundation-models
- sim2real
- robot-benchmarking
- dexterous-manipulation
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# KineBench: Benchmarking Embodied World Models via IDM-Free Kinematic Grounding

## Summary
KineBench evaluates embodied world models by converting generated videos into 6D robot end-effector poses and testing those poses in a physics simulator. Its IDM-free grounding pipeline reduces ambiguity between world-model failures and action-extraction failures while adding 3D kinematic diagnostics.

## Problem
- Pixel-level and open-loop video metrics do not establish whether generated robot motions are physically executable.
- Existing closed-loop benchmarks rely on inverse dynamics models (IDMs), so failures can reflect either implausible video generation or poor IDM generalization to novel trajectories.

## Approach
- Segment the gripper with YOLOv11, estimate metric depth with fine-tuned MoGeV2, and recover 6D poses with CAD-constrained FoundationPose.
- Execute the recovered pose sequence in the ManiSkill3 physics simulator for closed-loop task evaluation.
- Measure trajectory smoothness with Spectral Arc Length (SPARC) and robot kinematic feasibility with the Maruyama Manipulability Index.
- Evaluate 20 manipulation tasks across basic execution, task transfer, visual out-of-distribution generalization, and complexity-scaling suites.

## Results
- On unseen trajectories, the explicit pipeline produced approximately 1.5–3 cm translational error with MoGeV2 depth, compared with errors on the order of 10 cm for the Dino3DFlowIDM baseline; its remaining rotational error was approximately 10 degrees.
- Closed-loop success rates varied substantially by model and suite: Wan2.2 5B reached 56.32% on basic execution, 11.90% on task transfer, and 55.50% on unseen visual OOD assets, while Wan2.1 1.3B reached 43.96%, 20.00%, and 52.83% on the same suites.
- In the complexity-scaling suite, Wan2.1 1.3B improved from 44.83% at 1.5k training steps to 73.33% at 15k steps; increasing data scale at 7.5k steps yielded 53.67% at scale 10, 52.00% at scale 25, and 51.17% at scale 50.
- SPARC and the Maruyama Manipulability Index showed task- and model-dependent associations with simulator success, providing complementary diagnostic signals rather than universally predictive metrics.
- The pipeline remains dependent on segmentation, depth quality, end-effector visibility, and orientation estimation, so it reduces—but does not eliminate—evaluation attribution ambiguity.

## Link
- [https://arxiv.org/abs/2607.19876v1](https://arxiv.org/abs/2607.19876v1)
