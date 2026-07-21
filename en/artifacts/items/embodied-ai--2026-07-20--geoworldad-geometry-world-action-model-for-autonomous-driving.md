---
source: arxiv
url: https://arxiv.org/abs/2607.17521v1
published_at: '2026-07-20T03:56:07'
authors:
- Songyan Zhang
- Jinyuan Tian
- Hanbing Li
- Daqi Liu
- Hao Chen
- Wenhui Huang
- Fang Li
- Guang Chen
- Hangjun Ye
- Long Chen
- Kuiyuan Yang
- Chen Lv
topics:
- world-model
- autonomous-driving
- 3d-geometry
- trajectory-planning
- vision-action
- future-prediction
relevance_score: 0.66
run_id: materialize-outputs
language_code: en
---

# GeoWorldAD: Geometry World Action Model for Autonomous Driving

## Summary
GeoWorldAD plans autonomous-driving trajectories using explicit ego-aligned 3D geometry for the current scene and latent geometry tokens that predict short-term future evolution. It reports state-of-the-art closed-loop scores on NAVSIM v1 and v2, indicating that geometry-centered future guidance can improve driving progress while maintaining safety.

## Problem
- Vision- and video-action planners can predict driving actions from images but often lack explicit geometric grounding, making collision avoidance and efficient progress harder in dynamic 3D scenes.
- Current geometry alone can produce overly conservative behavior, while pixel-space world models provide redundant and weakly spatial future guidance.
- The problem matters because safe autonomous driving requires both accurate spatial constraints and anticipation of how agents and free space will change over the planning horizon.

## Approach
- GeoWorldAD uses EgoStreamVGGT, an ego-aligned variant of StreamVGGT, to extract multi-scale present-scene geometry tokens and estimate 4D reconstruction, depth, and camera motion.
- A Q-Former-style geometry world model uses ego state and present geometry to generate latent future geometry tokens for 4 future chunks covering 2 seconds; future depth prediction provides supervision.
- A trajectory-action model generates 64 proposals with 8 waypoints over a 4-second horizon, progressively refining them through 4 present-geometry stages and 1 future-geometry stage.
- Training jointly optimizes reconstruction, future-depth, trajectory, and proposal-scoring losses; the proposal score combines no-fault collision, drivable-area compliance, ego progress, time-to-collision, and comfort.

## Results
- On the NAVSIM v1 navtest split, GeoWorldAD reports a PDMS of 91.0, compared with 90.3 for DVGT-2 and 90.4 for EponaV2; it also reports NC 99.0, DAC 97.8, TTC 95.8, comfort 99.9, and EP 85.9.
- On the NAVSIM v2 navtest split, GeoWorldAD reports the highest listed EPDMS of 90.4, ahead of DVGT-2 at 89.6 and EponaV2 at 88.9.
- On NAVSIM v2, its component scores include NC 99.0, DAC 97.8, DDC 99.6, traffic-law compliance 99.7, EP 89.1, and TTC 98.6.
- The model is trained with four consecutive input frames, predicts four future depth frames over 2 seconds, and plans eight waypoints over 4 seconds; the provided excerpt does not include a complete ablation table quantifying the separate contributions of present versus future geometry.

## Link
- [https://arxiv.org/abs/2607.17521v1](https://arxiv.org/abs/2607.17521v1)
