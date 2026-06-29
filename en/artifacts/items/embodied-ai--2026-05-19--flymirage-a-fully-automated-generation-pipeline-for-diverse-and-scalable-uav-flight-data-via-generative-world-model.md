---
source: arxiv
url: https://arxiv.org/abs/2605.19600v1
published_at: '2026-05-19T09:41:04'
authors:
- Jinhan Li
- Xijie Huang
- Zhaoqi Wang
- Yijin Wang
- Weiqi Ge
- Qiyi He
- Mo Zhu
- Fei Gao
- Yuze Wu
- Xin Zhou
topics:
- aerial-vln
- uav-data-generation
- generative-world-model
- 3d-gaussian-splatting
- robot-data-scaling
- sim2real
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# FlyMirage: A Fully Automated Generation Pipeline for Diverse and Scalable UAV Flight Data via Generative World Model

## Summary
FlyMirage generates aerial vision-language navigation data by combining LLM scene design, Marble world generation, automatic 3DGS annotation, and UAV trajectory planning. The paper claims a 500-scene, 50K-trajectory dataset with 6-DoF dynamically feasible flight data.

## Problem
- Aerial VLN data is hard to scale because real UAV flights need skilled operators, and many simulated datasets still depend on manual scans or hand-built scenes.
- Existing simulated UAV datasets often use limited assets or prebuilt scenes, and many use planners that ignore UAV dynamics.
- Better data matters because aerial navigation models need varied scenes, object grounding, and flight paths that match UAV motion limits.

## Approach
- The system samples scene types from a taxonomy, asks GPT-5.4 or Gemini 3.1 for detailed scene descriptions, creates matching images with GPT Images 2.0, and gives the text-image pair to Marble 1.1 Plus to generate 3D Gaussian Splatting scenes.
- It renders RGB and depth views with GSplat, then uses Boxer for open-vocabulary object detection and 3D bounding boxes.
- It adds iterative camera exploration around the scene center and near distant objects, then reruns Boxer with distance pruning to reduce poor far-range boxes.
- It selects navigation targets from semantic boxes using visibility, safety, and 2.0 m to 10.0 m travel-distance checks.
- It runs EGO-Planner to generate dynamically feasible UAV trajectories, renders RGB/depth observations, and uses Qwen-3.5-Flash to filter poor trajectories and generate prompt variants.

## Results
- FlyMirage contains 500 generated 3DGS scenes across 6 categories: transportation, workplaces, commercial spaces, industrial facilities, leisure venues, and residential spaces.
- The dataset contains about 50,000 navigation trajectories with 6-DoF action space and kinematics. Table I compares this with OpenFly, which has 100K trajectories, 18 scenes, 4-DoF action space, A* planning, and no kinematics.
- The paper claims FlyMirage is the first automated aerial trajectory-generation pipeline in the comparison table to produce true 6-DoF trajectories; prior 6-DoF datasets such as UAV-Flow use human control.
- The generated scenes include 5,000+ unique object labels, with a typical scene containing 60 to 100 object instances. The paper compares this with InteriorGS at about 700 unique object categories.
- Mean trajectory length is 4.33 m and median length is 4.06 m. Continuous runs can combine up to 5 navigation tasks for long-horizon tasks of about 20 m.
- Generation cost is reported at about $2 per scene, with about 1 hour per scene and rendering on a consumer NVIDIA RTX 4070 GPU. The paper compares this with Matterport Pro2 scanning hardware at about $3,000 and UAV-Flow human-operated flights at about $100 per hour.

## Link
- [https://arxiv.org/abs/2605.19600v1](https://arxiv.org/abs/2605.19600v1)
