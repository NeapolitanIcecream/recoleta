---
source: arxiv
url: https://arxiv.org/abs/2604.24681v1
published_at: '2026-04-27T16:42:18'
authors:
- Yifan Xie
- YuAn Wang
- Guangyu Chen
- Jinkun Liu
- Yu Sun
- Wenbo Ding
topics:
- vision-language-action
- robot-manipulation
- human-demonstration-learning
- hand-motion-priors
- robot-data-scaling
- sim2real
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# Learning Human-Intention Priors from Large-Scale Human Demonstrations for Robotic Manipulation

## Summary
MoT-HRA uses large-scale human manipulation videos to pretrain a robot policy on spatial and hand-motion intent before mapping that intent to robot actions. The paper claims gains in hand motion generation and SimplerEnv robot manipulation, with a 66.1% average success rate on WidowX tasks.

## Problem
- Robot manipulation datasets are expensive, hardware-specific, and small compared with human video datasets.
- Human videos contain useful manipulation behavior, but raw clips mix scene context, hand motion, camera motion, and human-specific embodiment.
- The problem matters because a robot policy needs transferable intent, such as where to interact and how contact unfolds, without treating human hand motion as direct robot control.

## Approach
- The authors build HA-2.2M, a 2.2M-episode action-language dataset from HowTo100M, Ego4D, EPIC-KITCHENS, and Something-Something-V2.
- The curation pipeline filters hand-centric manipulation clips, reconstructs MANO-style hand pose with HaMeR, aligns scene depth with Depth Anything 3, segments actions with V-JEPA, and uses Gemini for labeling and clip merging.
- MoT-HRA factorizes control into three experts: a vision-language expert predicts an embodiment-agnostic 3D trajectory, an intention expert generates MANO-style hand motion, and a fine expert predicts robot action chunks.
- Read-only key-value transfer lets the robot-action expert use trajectory and intention features while blocking robot-action losses from overwriting the upstream human-motion prior.
- Training combines HA-2.2M for human-motion supervision with AgiBot-World for robot-action supervision, using a chunk horizon of 15.

## Results
- HA-2.2M contains 2.2M episodes: 1.4M from HowTo100M, 630K from Ego4D, 120K from EPIC-KITCHENS, and 50K from Something-Something-V2.
- On Ego4D hand motion generation, MoT-HRA reports ADE 0.136 m, DTW 0.127 m, Rot 28.95°, and Joint-Rot 34.16°, beating VITRA at 0.154 m, 0.146 m, 33.26°, and 41.81°.
- On OakInk hand motion generation, MoT-HRA reports ADE 0.184 m, DTW 0.176 m, Rot 38.47°, and Joint-Rot 40.12°, beating VITRA at 0.211 m, 0.201 m, 42.59°, and 41.72°.
- On SimplerEnv-WidowX, MoT-HRA reaches 66.1% average success, compared with ThinkACT at 43.8%, SpatialVLA at 42.7%, OpenVLA-OFT at 41.7%, RoboVLMs at 37.5%, π0-FAST at 32.1%, and π0 at 27.1%.
- On the four SimplerEnv tasks, MoT-HRA reports 78.1% on Spoon, 62.5% on Carrot, 40.6% on Stack, and 83.3% on Eggplant; SpatialVLA is higher only on Eggplant at 100.0%.
- The excerpt claims real-world manipulation gains, but it does not provide real-world success-rate numbers.

## Link
- [https://arxiv.org/abs/2604.24681v1](https://arxiv.org/abs/2604.24681v1)
