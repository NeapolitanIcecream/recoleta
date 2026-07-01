---
source: arxiv
url: https://arxiv.org/abs/2606.31329v1
published_at: '2026-06-30T08:31:35'
authors:
- Dongyoon Hwang
- Byungkun Lee
- Dongjin Kim
- Hyojin Jang
- Hoiyeong Jin
- Jueun Mun
- Minho Park
- Hojoon Lee
- Hyunseung Kim
- Jaegul Choo
topics:
- vision-language-action
- hierarchical-vla
- 3d-trajectory-guidance
- point-cloud-policy
- robot-manipulation
- sim2real
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# 3D HAMSTER: Bridging Planning and Control in Hierarchical Vision Language Action Models through 3D Trajectory Guidance

## Summary
3D HAMSTER trains a hierarchical VLA to plan robot end-effector paths as 3D waypoints, then feeds those waypoints to a point-cloud control policy. The main claim is that matching the planner and controller in 3D metric space improves trajectory accuracy and manipulation under visual, language, and spatial shifts.

## Problem
- Current hierarchical VLA systems often predict 2D image trajectories, while low-level robot policies often act on 3D point clouds.
- Lifting 2D waypoints into 3D by reading depth at each pixel can make the path stick to scene surfaces, which gives the controller distorted guidance.
- This matters because fine manipulation depends on depth, clearance, and contact positions, especially under viewpoint, texture, lighting, and object changes.

## Approach
- The planner is based on Qwen3-VL-8B-Instruct and predicts waypoint sequences in `(u, v, d)`, where `d` is metric depth.
- A separate depth encoder processes the depth map, projects depth tokens into the language model space, and fuses them with RGB tokens.
- A dense depth reconstruction loss trains the depth pathway to keep full-scene geometry, while the language-model loss trains text-form trajectory output; the loss uses `L = L_LM + 0.1 L_depth`.
- Training mixes 3D robot and spatial data with RGB-only preservation data: RLBench 606K, DROID 123K, InternData-M1 1.5M, RefSpatial 2.2M, RoboPoint 666K, PixMo 171K, LVIS 138K, and Honey-1M 749K samples.
- The low-level policy uses 3DFA: it unprojects the `(u, v, d)` waypoints into world coordinates, appends them to the scene point cloud with trajectory and scene embeddings, and predicts action chunks with rectified flow matching.

## Results
- On DroidSpatial-Bench, built from 148 held-out DROID pick-and-place episodes, full 3D HAMSTER reaches 65.5% Both accuracy at 10 cm, compared with 60.1% for RoboBrain-2.5-8B, 29.7% for Gemini-3.0-Pro, 16.2% for GPT-5.2, and 2.0% for Sonnet-4.6.
- At the 5 cm threshold, full 3D HAMSTER gets 63.5% Start, 66.2% End, and 41.9% Both accuracy on DroidSpatial-Bench; RoboBrain-2.5-8B gets 61.5%, 58.1%, and 39.2%.
- The ablation shows the base Qwen3-VL-8B is near zero on this task: 0.7% Both at both 5 cm and 10 cm. Adding 3D trajectory data raises Both to 27.7% at 5 cm and 50.0% at 10 cm.
- Adding the depth encoder raises Both accuracy to 42.6% at 5 cm and 62.8% at 10 cm; adding dense depth reconstruction gives 41.9% at 5 cm and 65.5% at 10 cm.
- The paper also reports simulation tests on 11 Colosseum tasks across 14 perturbation axes and real-world tests on a Franka Panda across 3 task families and 4 generalization axes. The excerpt does not provide the corresponding success-rate or score tables, so the concrete claim available here is that 3D guidance beats 2D HAMSTER guidance and unguided 3DFA, with the largest gains under appearance changes and unseen language, spatial, and visual conditions.

## Link
- [https://arxiv.org/abs/2606.31329v1](https://arxiv.org/abs/2606.31329v1)
