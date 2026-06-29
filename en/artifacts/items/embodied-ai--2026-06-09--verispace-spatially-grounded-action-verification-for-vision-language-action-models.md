---
source: arxiv
url: https://arxiv.org/abs/2606.10568v1
published_at: '2026-06-09T08:31:59'
authors:
- Guiyu Zhao
- Longteng Guo
- Junyou Zhu
- Jun Fu
- Yanghong Mei
- Bin Cao
- Jie Jiang
- Xingjian He
- Jing Liu
topics:
- vision-language-action
- action-verification
- robot-manipulation
- spatial-reasoning
- rgb-d-perception
- test-time-scaling
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# VeriSpace: Spatially Grounded Action Verification for Vision-Language-Action Models

## Summary
VeriSpace is a test-time action verifier for vision-language-action robot policies. It samples multiple actions, scores them with RGB-D spatial reasoning, and executes the highest-scoring action.

## Problem
- VLA policies often predict one action and execute it immediately, so small pose or gripper errors can cause missed grasps, collisions, or wrong task progress.
- Existing action verifiers that score candidates from 2D images can miss small 3D differences in contact, clearance, and object alignment.
- The problem matters because robot actions change the physical scene, and a bad action can make later recovery harder or unsafe.

## Approach
- A frozen VLA policy samples candidate 7D actions, including 6-DoF end-effector motion and gripper command. VeriSpace scores each candidate and selects the top-ranked action.
- The verifier uses RGB-D input. It back-projects depth into 3D scene coordinates using camera parameters, then encodes those coordinates with sinusoidal features and an MLP.
- Dual-path scene encoding creates explicit 3D geometry tokens and visual tokens with 3D position injected into CLIP image features.
- Geometry-guided local aggregation uses farthest point sampling and radius neighborhoods in 3D to capture local shape cues near object surfaces, edges, gaps, and possible contact zones.
- Training uses a Bradley-Terry pairwise preference loss for action ranking plus cross-entropy supervision for chain-of-thought spatial reasoning. The reported verifier uses LLaVA-7B with LoRA.

## Results
- On SimplerEnv-WidowX with OpenVLA, average success rose from 37.0% to 55.0% across 4 tasks and 50 trials per task, a gain of 18.0 percentage points.
- On the same OpenVLA setting, VeriSpace beat the strongest listed verifier baseline, Robomonkey, by 14.5 points on average: 55.0% versus 40.5%.
- OpenVLA task gains were 54.0% to 76.0% on Eggplant in Basket (+22.0), 22.0% to 34.0% on Carrot on Plate (+12.0), 28.0% to 62.0% on Stack Cubes (+34.0), and 44.0% to 48.0% on Spoon on Towel (+4.0).
- With π0-FAST, average success rose from 57.0% to 60.5%, a gain of 3.5 points. The strongest listed verifier baseline in that block was Robomonkey at 58.5%.
- The paper states that VeriSpace surpasses the previous best method on SIMPLER by 13.0 points, but the provided table excerpt shows a larger 14.5-point margin over the listed OpenVLA verifier baselines.
- The excerpt says real-world in-distribution and out-of-distribution experiments improved, but it does not provide the real-world success rates in the visible text.

## Link
- [https://arxiv.org/abs/2606.10568v1](https://arxiv.org/abs/2606.10568v1)
