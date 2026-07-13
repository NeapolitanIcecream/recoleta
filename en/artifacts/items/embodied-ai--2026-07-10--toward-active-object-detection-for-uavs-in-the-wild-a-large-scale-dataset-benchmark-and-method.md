---
source: arxiv
url: https://arxiv.org/abs/2607.09078v1
published_at: '2026-07-10T03:49:45'
authors:
- Tianpeng Liu
- Xinhua Jiang
- Li Liu
- Qinmu Shen
- Siwei Tang
- Zhen Liu
- Yongxiang Liu
topics:
- active-object-detection
- uav-perception
- world-model
- policy-generalization
- robot-data-scaling
- sim2real
relevance_score: 0.58
run_id: materialize-outputs
language_code: en
---

# Toward Active Object Detection for UAVs in the Wild: A Large-Scale Dataset, Benchmark and Method

## Summary
The paper introduces ATRNet-LUDO, a large real-world benchmark for UAV-ground active object detection, and AOD-JEPA, a JEPA-based world model for improving policy generalization. It reports higher recognition than passive perception and DRL baselines at similar UAV motion costs.

## Problem
- UAV detectors often fail when targets are occluded, small, or poorly viewed from a single position.
- Existing active object detection datasets focus on indoor robots or synthetic UAV scenes, limiting real-world evaluation.
- DRL-based active observation policies lose performance in test environments that differ from training environments.

## Approach
- Collect 121,000 multi-view panoramic images and 1.21 million local target patches covering 10 vehicle categories and 40 outdoor scenarios.
- Build 200 multi-target and 2,000 single-target environments from dense UAV viewpoints, with annotations for target boxes, categories, occlusion, UAV pose, and target location.
- Train an active observation policy with a JEPA world model that predicts the next observation in latent space after an action.
- Add AOD-specific scene purification using SAM3 masks so the state representation emphasizes target appearance, structure, and spatial context while reducing background interference.
- Define benchmark splits that test generalization across target-background layouts and unseen sampling regions, and compare seven AOD policy methods.

## Results
- Active observation improves target recognition by about 20 percentage points over passive object perception.
- In test environments with similar UAV movement costs, WMPL with AOD-JEPA improves target recognition by 2 to 3 percentage points over DRL baselines.
- ATRNet-LUDO contains 121,000 panoramic images, 1,210,000 local patches, 10 vehicle types, 40 scenarios, 200 multi-target environments, and 2,000 single-target environments.
- The dataset uses 8,000 × 6,000 panoramic images and 300 × 300 local patches, with an average 53-pixel error for predicted positions of fully occluded targets.

## Link
- [https://arxiv.org/abs/2607.09078v1](https://arxiv.org/abs/2607.09078v1)
