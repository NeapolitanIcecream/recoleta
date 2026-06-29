---
source: arxiv
url: https://arxiv.org/abs/2605.25829v1
published_at: '2026-05-25T13:28:33'
authors:
- Xinzhe Chen
- Sihua Ren
- Liqi Huang
- Haowen Sun
- Mingyang Li
- Xingyu Chen
- Zeyang Liu
- Xuguang Lan
topics:
- vision-language-action
- robot-manipulation
- se3-trajectory-prediction
- action-space-alignment
- world-action-models
- sim2real
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# OASIS: Observation-Action Space Alignment via SE(3) Trajectory Prediction for Robotic Manipulation

## Summary
OASIS is a visuomotor policy for robot manipulation that predicts future end-effector poses in SE(3) before decoding actions. The paper claims this pose-supervised intermediate makes 6-DoF action generation easier and improves simulation, real-robot, and out-of-distribution success rates.

## Problem
- VLA models and world action models often decode 6-DoF actions from image, language, or future-visual features that do not expose rigid-body pose structure.
- This leaves the action decoder to infer target end-effector poses and convert them into relative actions, which can hurt spatial generalization and long-horizon manipulation.
- The problem matters because manipulation depends on precise 3D position, rotation, and gripper timing, especially when camera views, backgrounds, or task layouts change.

## Approach
- OASIS uses a 3D-aware encoder that combines vision-language features from a Qwen2.5-0.5B VLM with metric-depth features from a frozen Depth Anything 3 DA3METRIC-LARGE model.
- A transformer trajectory predictor takes this representation and predicts an 8-step camera-frame SE(3) end-effector trajectory.
- Each predicted pose contains 3D position and axis-angle rotation, so the trajectory gives the action decoder explicit rigid-body pose information.
- The action decoder attends to the pose-supervised trajectory hidden states and the current robot state, then outputs an 8-step action chunk with 6-DoF relative actions and gripper commands.
- Training uses standard expert demonstrations with two losses: L1 trajectory loss and L1 action loss, with trajectory loss weight 0.1; the method does not use large-scale robot pretraining or extra spatial labels.

## Results
- On LIBERO, OASIS reports 97.6% average success across Spatial, Object, Goal, and Long, compared with Unified-VLA at 95.5%, UniVLA at 95.2%, QDepth-VLA at 94.9%, and pi0 at 94.1%.
- LIBERO suite scores are 99.0% Spatial, 98.8% Object, 97.4% Goal, and 95.2% Long; OASIS reports these without large-scale robot pretraining.
- On CALVIN ABC to D, OASIS reports a 4.57 average sequence length and 83.3% success over five consecutive tasks, compared with DreamVLA at 4.44 and 78.1%, Unified-VLA at 4.41 and 75.1%, and VPP at 4.33 and 76.9%.
- Ablations attribute the largest added gain to the SE(3) trajectory predictor: LIBERO-Long rises from 89.5% to 95.2%, and LIBERO-Spatial rises from 91.6% to 99.0%.
- In real-world tests on Franka Research 3 and Kinova Gen3 robots, OASIS reports 89.2% average success across multi-task, spatial-relationship, and long-horizon suites, outperforming pi0.5, RDT, Seer-Large, and ACT in the reported comparison.
- Under Goal-task out-of-distribution perturbations with unseen backgrounds, an altered camera viewpoint, and human interference, OASIS reports 90.8% average success.

## Link
- [https://arxiv.org/abs/2605.25829v1](https://arxiv.org/abs/2605.25829v1)
