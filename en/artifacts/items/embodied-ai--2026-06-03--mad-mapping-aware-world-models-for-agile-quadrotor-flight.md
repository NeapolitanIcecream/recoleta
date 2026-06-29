---
source: arxiv
url: https://arxiv.org/abs/2606.04534v1
published_at: '2026-06-03T07:17:57'
authors:
- Xinhong Zhang
- Runqing Wang
- Yunfan Ren
- Ding Yu
- Boyu Zhou
- Jian Sun
- Fang Deng
- Jie Chen
- Gang Wang
topics:
- world-models
- quadrotor-flight
- occupancy-mapping
- sim2real
- reinforcement-learning
- agile-navigation
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# MAD: Mapping-Aware World Models for Agile Quadrotor Flight

## Summary
MAD trains a quadrotor world model to predict local occupancy and visibility maps from depth and proprioception, then uses that latent state for agile flight policies. The paper reports better visual navigation than vision-only baselines and real-world forest flight at 5.05 m/s.

## Problem
- Agile quadrotors must avoid obstacles under partial visibility, short sensing range, and tight compute latency.
- Classical stacks use odometry, mapping, planning, and tracking, which adds hand engineering and can add latency or accumulated error.
- End-to-end visual policies can fly fast, but they often lack explicit spatial memory, making transfer and failure diagnosis harder.

## Approach
- MAD uses a DreamerV3-style recurrent state-space model trained on depth images, actions, rewards, continuation flags, and 9D proprioception.
- The model reconstructs robocentric occupancy grid maps and visibility grid maps instead of using raw depth reconstruction as the main training target.
- Occupancy loss is applied only in visible voxels, so unknown space is not treated as free or occupied during supervision.
- DiffAero generates grid-map supervision on GPU using a local 3D grid spanning 8 m × 8 m × 4 m with 0.4 m voxels, giving 4,000 voxels per map.
- The learned latent state is used in three policy modes: MAD-Dreamer for imagined rollouts, and MAD-PPO or MAD-SHAC as frozen feature encoders during simulator interaction.

## Results
- The GPU map-construction module reaches 4.84e8 voxel occupancy and visibility evaluations per second on one GPU.
- The simulator plus grid-map computation reaches 1.21e5 environment interactions per second on the reported workstation.
- The paper claims MAD-based agents get higher success rates, faster flight, and better cross-task transfer than matching vision-only baselines, but the excerpt does not include the exact success-rate tables.
- The learned policy reaches 9.66 m/s in simulation.
- The real quadrotor uses an Intel RealSense D435i and reaches 5.05 m/s in real-world forest experiments.
- The observation setup uses 18 × 32 depth images plus a 9D proprioceptive vector, and deployment exports the MAD encoder and actor as one onboard policy that outputs acceleration commands.

## Link
- [https://arxiv.org/abs/2606.04534v1](https://arxiv.org/abs/2606.04534v1)
