---
source: arxiv
url: https://arxiv.org/abs/2606.20118v1
published_at: '2026-06-18T11:41:25'
authors:
- Jonghoon Lee
- Seong Hyeon Park
- Byungwoo Jeon
- Minha Lee
- Jinwoo Shin
topics:
- vision-language-action
- robot-data-augmentation
- multi-view-consistency
- object-swapping
- robot-data-scaling
- manipulation
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Pose6DAug: Physically Plausible Multi-view Object Swapping for Robot Data Augmentation

## Summary
Pose6DAug augments robot manipulation data by replacing objects in successful multi-view episodes with new 3D objects while keeping the original robot motion and contact geometry.

## Problem
- VLA policies such as GR00T-1.5 can fail on novel objects with new shapes or appearances.
- Collecting new multi-view teleoperation data for each failed object is slow and costly.
- 2D video editing can break cross-camera geometry, object identity, and gripper-object contact, which gives the policy noisy training data.

## Approach
- The method starts from a successful robot episode and keeps the recorded action trajectory.
- It reconstructs or supplies a target object mesh, removes the original object from each camera view, and inpaints the background.
- It transfers the original object's 6D pose trajectory to the target mesh in a shared world frame, then renders the same target object into all calibrated camera views.
- It restores the robot and gripper masks on top of the rendered object so occlusions stay consistent.
- It adds 3D-grounded perturbations: object rotation, translation along the gripper approach axis, and scaling to keep the object graspable.

## Results
- On RoboCasa365 Counter-to-Cabinet failure episodes with GR00T-1.5, Pose6DAug reaches 22.8% average success, versus 16.4% for VACE, 15.8% for MimicGen, and 0.0% for the base policy.
- On the same failure-episode setting, Pose6DAug reaches a 24.5% average turnover ratio, versus 18.2% for VACE and 17.2% for MimicGen.
- For in-distribution failure objects, Pose6DAug gets 21.2% success, versus 12.8% for VACE and 14.7% for MimicGen.
- For out-of-distribution failure objects, Pose6DAug gets 24.7% success, versus 21.2% for VACE and 17.3% for MimicGen.
- In the hard-object test on 8 unseen out-of-distribution meshes, training only on augmented episodes gives Pose6DAug 21.2% success, versus 15.0% for VACE and 5.7% for MimicGen.
- Pose6DAug recovers 7 of 8 hard objects, compared with 5 of 8 for VACE and 2 of 8 for MimicGen; it generates 176 augmented episodes like VACE, while MimicGen keeps only 33 valid rollouts after rollout failures.

## Link
- [https://arxiv.org/abs/2606.20118v1](https://arxiv.org/abs/2606.20118v1)
