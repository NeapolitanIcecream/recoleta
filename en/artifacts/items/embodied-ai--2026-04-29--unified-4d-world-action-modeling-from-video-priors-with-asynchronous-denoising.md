---
source: arxiv
url: https://arxiv.org/abs/2604.26694v2
published_at: '2026-04-29T14:01:54'
authors:
- Jun Guo
- Qiwei Li
- Peiyan Li
- Zilong Chen
- Nan Sun
- Yifei Su
- Heyun Wang
- Yuan Zhang
- Xinghang Li
- Huaping Liu
topics:
- world-action-model
- robot-foundation-model
- vision-language-action
- 4d-reconstruction
- asynchronous-denoising
- robot-data-scaling
relevance_score: 0.98
run_id: materialize-outputs
language_code: en
---

# Unified 4D World Action Modeling from Video Priors with Asynchronous Denoising

## Summary
X-WAM is a robot world-action model that predicts future multi-view RGB-D video, 3D structure, robot states, and actions in one diffusion model. Its main claim is that adding depth prediction and asynchronous denoising improves both policy success and 4D world generation.

## Problem
- Existing unified world-action models mostly predict 2D video and actions, so they lack direct 3D geometry for manipulation and reconstruction.
- High-quality video diffusion needs many denoising steps, while robot actions can be decoded with fewer steps; using the same schedule wastes control time.
- The problem matters because robot policies need fast actions for closed-loop control and spatial predictions for contact-rich manipulation.

## Approach
- X-WAM fine-tunes Wan2.2-TI2V-5B, a pretrained video Diffusion Transformer, on multi-view robot data.
- The model takes a language instruction, initial RGB views, and proprioceptive state, then predicts 8 future RGB frames, 8 future states, and 32 future actions.
- A depth branch copies the final few DiT blocks and reads RGB features through cross-attention, producing depth without doubling the token sequence.
- Asynchronous Noise Sampling decodes actions in fewer denoising steps than video; training samples video and action noise levels from a coupled distribution so the training schedule matches inference.
- The model trains on more than 5,800 hours of real and simulated robot data with a shared end-effector pose and gripper action format.

## Results
- On RoboCasa, X-WAM reports 79.2% average success rate across 24 tasks, compared with 67.1% for Cosmos Policy, a gain of 12.1 percentage points.
- On RoboTwin 2.0 Clean, it reports 89.8% success rate, compared with 88.7% for Motus, a gain of 1.1 percentage points.
- On RoboTwin 2.0 Randomized, it reports 90.7% success rate, compared with 87.0% for Motus, a gain of 3.7 percentage points.
- For prediction, the paper evaluates PSNR, SSIM, LPIPS, AbsRel, δ1, and Chamfer Distance, and claims better visual and geometric metrics than existing methods; the excerpt does not include those metric values.
- The paper also claims real-world deployment on a dual-arm earphone packing task, but the excerpt does not provide success-rate numbers for that experiment.

## Link
- [https://arxiv.org/abs/2604.26694v2](https://arxiv.org/abs/2604.26694v2)
