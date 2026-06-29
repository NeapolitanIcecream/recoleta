---
source: arxiv
url: https://arxiv.org/abs/2606.06147v1
published_at: '2026-06-04T13:23:05'
authors:
- Shengtao Zheng
- Kai Li
- Weichen Zhang
- Yu Meng
- Chen Gao
- Xinlei Chen
- Yong Li
- Xiao-Ping Zhang
topics:
- uav-navigation
- vision-language-action
- world-model
- flow-matching
- simulated-benchmark
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# WorldFly: A World-Model-Based Vision-Language-Action Model for UAV Navigation

## Summary
WorldFly is a UAV vision-language-action model that predicts future camera views and navigation actions together. On a new Urban Canyon Traversal benchmark, it reports better success rate, path efficiency, and final-distance error than OpenFly and Pi-0-UAV.

## Problem
- Existing UAV VLA policies usually map past first-person images and language directly to actions, which fails when buildings occlude the route or sharp turns cause large view changes.
- This matters because low-altitude urban UAVs need to follow language instructions through intersections and narrow streets, including layouts not seen during training.
- The paper also addresses a benchmark gap by creating Urban Canyon Traversal, with long routes, large turns, and unseen-intersection tests.

## Approach
- WorldFly learns a joint distribution over future action chunks and future video frames conditioned on the language instruction and recent first-person observations.
- A world-model branch predicts future video latents, while an action branch predicts an 8D continuous action chunk that maps to 10 discrete OpenFly navigation primitives.
- Both branches use flow matching with the same noise timestep, so future visual states and actions are trained under aligned denoising conditions.
- Dual-branch coupling blocks use cross-attention between the video and action branches, letting planned actions condition imagined frames and imagined frames condition action prediction.
- Instructions are encoded with T5, and video frames are compressed with the LTX-Video VAE before transformer processing.

## Results
- Urban Canyon Traversal contains over 4,000 training trajectories built in AirSim urban maps, plus TEST-EASY with 100 trajectories from seen intersections and TEST-HARD with 100 trajectories from 14 new intersections.
- On TEST-EASY, WorldFly reaches 87% success rate, 73.25% SPL, and 7.92 m navigation error, compared with OpenFly at 72%, 58.55%, and 14.69 m.
- On TEST-HARD, WorldFly reaches 31% success rate, 27.86% SPL, and 31.08 m navigation error, compared with OpenFly at 16%, 14.92%, and 35.32 m.
- Against Pi-0-UAV on TEST-HARD, WorldFly improves success rate from 10% to 31% and SPL from 9.43% to 27.86%.
- The ablation without dual-branch coupling scores 76% success and 61.59% SPL on TEST-EASY, and 21% success and 18.14% SPL on TEST-HARD; full WorldFly scores 87% and 73.25%, then 31% and 27.86%.
- The paper reports action-only inference latency of about 7.81 seconds per step on one NVIDIA A100 using a 50-step flow-matching denoising schedule.

## Link
- [https://arxiv.org/abs/2606.06147v1](https://arxiv.org/abs/2606.06147v1)
