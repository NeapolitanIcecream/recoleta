---
source: arxiv
url: https://arxiv.org/abs/2607.02322v1
published_at: '2026-07-02T15:30:26'
authors:
- Jincheng Tang
- Yilong Zhu
- Zhengyuan Xie
- Jiang-Jiang Liu
- Jiaxing Zhang
topics:
- vision-language-action
- robot-data-collection
- spatial-generalization
- dynamic-camera
- manipulation
- shortcut-learning
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# The Moving Eye: Enhancing VLA Spatial Generalization via Hybrid Dynamic Data Collection

## Summary
The paper claims that VLA policies fail under camera and object shifts because training data binds camera pose, robot base, and object positions together. It tests a real dual-arm collection setup that mixes moving-camera episodes with static multi-view episodes and finds the best Gr00t pen-task mix at Moving:Multi-Fixed = 1:3.

## Problem
- It targets poor spatial generalization in VLA manipulation when camera pose or object layout changes.
- The authors identify three shortcut sources: camera-base coupling, camera-object coupling, and object-position coupling.
- This matters for real robots because fixed cameras can move, camera rigs differ across datasets, and mobile or handheld views change during task execution.

## Approach
- A dual-arm setup uses one So-101 arm for manipulation and an Airbot arm as a mobile environmental camera.
- The paper compares Fixed View, Multi-Fixed View, and Moving View data. Moving View uses continuous camera trajectories within the same bounded region as Multi-Fixed View.
- Training data mixes Moving and Multi-Fixed episodes as Moving:Multi-Fixed = 1:k; for Gr00t n1, the best reported pen-task ratio is 1:3.
- Collection also randomizes target and receptacle positions to reduce object-position shortcuts.
- Policies map wrist-camera and environmental-camera observations plus language to actions, then are tested on held-out camera poses, moving camera trajectories, and shifted object configurations.

## Results
- On the pen task with 2400 samples, Fixed View training reached 85.0% success on the fixed ID test but 43.0% on the moving-camera OOD test. Mixed Data reached 86.0% ID and 83.0% OOD.
- In the object-position coupling test, the Multi-Fixed baseline scored 95.0 ± 3.5% with the holder at the training position and 71.9 ± 5.2% after shifting the holder by one diameter. Mixed 1:3 scored 91.9 ± 2.4% and 90.6 ± 6.3%.
- For Gr00t on the moving-camera pen test, success by Moving:Multi-Fixed ratio was 54.8 ± 10.7% for 1:0, 83.3 ± 7.1% for 1:1, 89.0 ± 5.7% for 1:3, and 80.5 ± 6.1% for 0:1.
- Evaluation used 400 pen-task episodes, 40 moving camera trajectories, 40 static camera poses, 5 target-container relative positions, and 8 pen orientations.
- The excerpt claims the data strategy helps ACT, Diffusion, Pi0, and Gr00t, but the provided text does not include the cross-architecture numbers.

## Link
- [https://arxiv.org/abs/2607.02322v1](https://arxiv.org/abs/2607.02322v1)
