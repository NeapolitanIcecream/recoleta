---
source: arxiv
url: https://arxiv.org/abs/2607.06564v1
published_at: '2026-07-07T17:59:47'
authors:
- Jiaming Liu
- Qingpo Wuwu
- Nuowei Han
- Hao Chen
- Zhuoyang Liu
- Fan Fei
- Yueru Jia
- Chenyang Gu
- Yandong Guo
- Boxin Shi
- Shanghang Zhang
topics:
- vision-language-action
- robot-foundation-model
- point-cloud-reasoning
- temporal-action-modeling
- robot-data-scaling
- dexterous-manipulation
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Lift3D-VLA: Lifting VLA Models to 3D Geometry and Dynamics-Aware Manipulation

## Summary
Lift3D-VLA adds explicit point-cloud reasoning and temporal action decoding to a VLA robot policy. The paper claims higher manipulation success in simulation and real robots than prior VLA baselines.

## Problem
- VLA policies often use 2D images, so they can miss reachability, contact, occlusion, and other 3D constraints that matter for physical manipulation.
- Prior 3D VLA methods either need scarce 3D robot data or lose geometry when projecting between 2D and 3D formats.
- Lift3D, the authors' earlier method, improves 3D perception but does not directly train on point-cloud geometry over time or decode temporally structured action chunks.

## Approach
- The model reuses a pretrained 2D VLA vision encoder for point clouds by projecting 3D points onto six virtual planes and averaging the matching pretrained 2D positional embeddings.
- A point-cloud tokenizer samples and groups 1024 input points into 256 tokens, then feeds them through the shared 2D vision encoder alongside RGB tokens.
- Geometry-Centric Masked Autoencoding trains the encoder to reconstruct masked points in the current point cloud and predict the next-frame point cloud geometry.
- The system uses VGGT to synthesize pseudo point clouds for RGB-only robot datasets, then trains on 140K trajectories for GC-MAE and 400K trajectories for robot pretraining.
- Layer-wise temporal action modeling assigns different action steps in a chunk to intermediate and deep LLaMA2-7B layers, so multiple layers predict the sequence rather than using only a final action head.

## Results
- Evaluation covers 22 simulated tasks and 8 real-world manipulation tasks.
- On MetaWorld, Lift3D-VLA reports a 10.8% higher mean success rate than the best prior VLA method in the excerpt.
- On RLBench, it reports an 11.1% higher mean success rate than the best prior VLA method in the excerpt.
- In real-world tasks, it outperforms the strongest baseline by 4 percentage points; the excerpt does not provide the absolute success rates.
- The paper also claims stronger out-of-distribution generalization to unseen objects, backgrounds, and lighting, plus long-horizon performance on repeated egg-scooping under changing scene conditions.

## Link
- [https://arxiv.org/abs/2607.06564v1](https://arxiv.org/abs/2607.06564v1)
