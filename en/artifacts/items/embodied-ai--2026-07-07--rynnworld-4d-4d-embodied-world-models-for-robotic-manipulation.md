---
source: arxiv
url: https://arxiv.org/abs/2607.06559v1
published_at: '2026-07-07T17:58:15'
authors:
- Haoyu Zhao
- Xingyue Zhao
- Siteng Huang
- Xin Li
- Deli Zhao
- Zhongyu Li
topics:
- embodied-world-model
- vision-language-action
- robot-manipulation
- 4d-scene-flow
- robot-data-scaling
- dexterous-manipulation
relevance_score: 0.98
run_id: materialize-outputs
language_code: en
---

# RynnWorld-4D: 4D Embodied World Models for Robotic Manipulation

## Summary
RynnWorld-4D predicts future RGB, depth, and optical-flow video from one RGB-D image and a text instruction, then uses the model's hidden 4D features to choose robot actions. The paper targets manipulation tasks where 2D video prediction loses depth and motion cues needed for precise robot control.

## Problem
- Robots need predictions of how objects move in 3D during contact; RGB-only video models can miss depth, 6-DoF pose, and per-point motion.
- Existing NeRF, 3D Gaussian, and dynamic SfM methods often need multiple views, scene-specific optimization, or lack future generation from a single image.
- The gap matters because manipulation policies must output low-level actions, and depth or motion errors can break dexterous bimanual tasks.

## Approach
- The model uses RGB-DF: synchronized RGB frames, depth maps, and optical flow. Depth lifts pixels into 3D points, and optical flow links those points over time to form 3D scene flow.
- RynnWorld-4D extends the Wan video diffusion backbone into three branches, one each for RGB, depth, and flow.
- Joint Cross-Modal Attention is inserted every 3 transformer blocks across 30 layers, with 10 total joint modules, so each modality can attend to the other two at the same frame.
- Training uses Rynn4DDataset 1.0, built from egocentric human videos and robot manipulation videos with Qwen3-VL captions, Depth Anything 3 depth, and DPFlow optical flow pseudo-labels.
- RynnWorld-4D-Policy freezes the world model, reads intermediate RGB/depth/flow latents in one forward pass, compresses them with a Flow Former, and predicts action chunks with a flow-matching policy.

## Results
- Rynn4DDataset 1.0 contains over 254.4 million frames from Epic-Kitchens, EgoVid, RoboMIND, RDT-1B, Galaxea, RoboCoin, and AgiBot.
- The model predicts RGB, depth, and optical flow together; the paper says these outputs can be back-projected into 3D scene flow using pinhole-camera geometry.
- The policy inference path reports 1,106 ms total latency on an NVIDIA RTX 5090 with FP8 and FlashAttention 3: 990 ms for RynnWorld-4D, 85 ms for depth estimation, 18 ms for VAE and latent prep, 4 ms for Flow Former, and 8 ms for the action head.
- With K=10 action chunks per pass, the paper reports about 0.9 Hz planning frequency and about 9 Hz effective control frequency.
- The excerpt claims state-of-the-art real-world dexterous bimanual manipulation performance, especially on spatial precision and temporal coordination tasks, but it does not provide success rates or benchmark tables in the shown text.

## Link
- [https://arxiv.org/abs/2607.06559v1](https://arxiv.org/abs/2607.06559v1)
