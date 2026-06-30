---
source: arxiv
url: https://arxiv.org/abs/2606.29879v1
published_at: '2026-06-29T07:17:13'
authors:
- Chen Yang
- Yuhao Wei
- Ze Xu
- Ziheng Zou
- Shuang Liang
- Delin Ouyang
- Lingfeng Qi
- Jie Li
- Guofa Li
topics:
- autonomous-driving
- vision-language-action
- world-model
- trajectory-planning
- bev-planning
- coarse-to-fine-refinement
relevance_score: 0.56
run_id: materialize-outputs
language_code: en
---

# LWDrive: Layer-Wise World-Model-Guided Vision-Language Model Planning for Autonomous Driving

## Summary
LWDrive is an autonomous-driving planner that turns a VLM trajectory into a candidate set, then refines it with world-model-supervised VLM features and BEV geometry.

## Problem
- Direct VLM trajectory decoding gives useful driving intent, but the output can be too coarse for lane-level geometry, obstacle constraints, and temporal consistency.
- Single-stage VLM feature fusion uses semantic information once, so later trajectory correction has weak access to the VLM's layer-wise representations.
- This matters because closed-loop driving plans need both high-level intent and accurate, future-aware motion under multi-view scene constraints.

## Approach
- The system adapts Qwen2.5-VL-3B to ego-centric driving scenes, then trains it to predict a coarse trajectory from current visual observations, ego status, navigation, and action queries.
- During training, a world-model head learns future-frame prediction in VAE latent space. This pushes the VLM hidden states to encode scene dynamics without requiring future frames at inference.
- The Foresight Cascade Planner initializes multiple candidate trajectories from action-query features, ego state, and learnable proposal embeddings.
- At selected VLM layers, Bridge Attention injects proposal memory, action-query memory, ego-state context, and VLM foresight features into each candidate.
- BEV refinement grounds each candidate with multi-view current-frame BEV features and predicts residual trajectory updates; a score head then selects the best candidate.

## Results
- On NAVSIM, LWDrive reports 92.0 PDMS using 4 cameras, above iPad at 91.7, DriveWorld-VLA at 91.3, Hydra-MDP++ at 91.0, and below the human-driver reference at 94.8.
- NAVSIM component scores are NC 98.8, DAC 98.4, TTC 96.2, Comfort 99.8, and Ego Progress 87.3.
- On NAVSIM-v2, LWDrive reports 89.6 EPDMS, above DriveWorld-VLA at 86.8, DriveVLA-W0 at 86.1, and DiffusionDrive at 84.5; the human-agent reference is 90.3.
- NAVSIM-v2 component scores are NC 98.8, DAC 98.4, DDC 99.0, TLC 99.7, EP 90.3, TTC 98.6, LK 96.3, HC 97.9, and EC 73.3.

## Link
- [https://arxiv.org/abs/2606.29879v1](https://arxiv.org/abs/2606.29879v1)
