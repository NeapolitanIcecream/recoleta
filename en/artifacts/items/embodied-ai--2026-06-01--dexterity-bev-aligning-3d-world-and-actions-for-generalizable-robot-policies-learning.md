---
source: arxiv
url: https://arxiv.org/abs/2606.02274v1
published_at: '2026-06-01T14:01:11'
authors:
- Huayi Zhou
- Wei Gao
- Dekun Lu
- Ruiji Liu
- Zhanqi Zhang
- Ziyang Zhang
- Jian Chen
- Wenlve Zhou
- Sheng Xu
- Shumin Li
- Kangyi Guo
- Shichen Xu
- Zixin Huang
- Yongyi Su
- Kui Jia
topics:
- vision-language-action
- robot-foundation-model
- dexterous-manipulation
- bev-representation
- robot-data-scaling
- cross-embodiment
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Dexterity-BEV: Aligning 3D World and Actions for Generalizable Robot Policies Learning

## Summary
Dexterity-BEV trains robot manipulation policies with 3D-aligned visual inputs and actions, while keeping compatibility with 2D VLM backbones. The paper claims better cross-embodiment and camera-view generalization than 2D VLA baselines.

## Problem
- Current VLA policies often use 2D RGB inputs, so they miss explicit 3D geometry needed for precise manipulation.
- Robot datasets use different camera poses, robot frames, action conventions, and execution speeds, which adds avoidable variation to the learning target.
- This matters because generalist robot policies need to train across mixed embodiments and datasets without relearning camera-specific or robot-specific coordinate quirks.

## Approach
- Dex-BEV turns each image pixel into a 3D point using camera calibration and depth when available, creating an aligned vertex map that stays pixel-aligned with RGB features.
- It expresses multi-view visual geometry, robot proprioception, and output actions in one shared 3D coordinate frame.
- The shared frame is a canonical bird’s-eye-view frame, often the robot base frame or the bottom center of a tabletop workspace region.
- It builds synthetic BEV images by projecting aggregated colored point clouds from all cameras into a top-down view.
- For RGB-only cameras, it uses a vertex spectrum: each pixel gets several sampled depth hypotheses, which are encoded as 3D positional features for the VLM.

## Results
- On official LIBERO, Dex-BEV reaches 97.8% average success with one cross-embodiment checkpoint, compared with 98.1% for X-VLA, 94.2% for π₀, and 92.8% for the 2D ablation.
- On RoboTwin 2.0 Clean, Dex-BEV reaches 76.0% success, compared with 70.0% for X-VLA, 46.4% for π₀, and 64.8% for the 2D ablation.
- On RoboTwin 2.0 Randomized, Dex-BEV reaches 42.0% success, compared with 39.0% for X-VLA, 16.4% for π₀, and 35.2% for the 2D ablation.
- On modified LIBERO with changed camera views and scene or robot base poses, Dex-BEV reaches 89.9% average success; X-VLA and the 2D ablation are reported as below 10%.
- On modified LIBERO task suites, Dex-BEV reports 92.8% Spatial, 89.4% Object, 91.0% Goal, and 86.2% Long success.
- In the visible real-world excerpt, Dex-BEV completes Agilex Fold Mailer Box in 23/30 trials, or 76.7%, compared with 17/30, or 56.7%, for X-VLA and 13/30, or 43.3%, for π₀.

## Link
- [https://arxiv.org/abs/2606.02274v1](https://arxiv.org/abs/2606.02274v1)
