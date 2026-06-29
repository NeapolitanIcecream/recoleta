---
source: arxiv
url: https://arxiv.org/abs/2606.24101v1
published_at: '2026-06-23T03:30:20'
authors:
- Yanghong Mei
- Longteng Guo
- Ming-Ming Yu
- Guiyu Zhao
- Xingjian He
- Jing Liu
topics:
- world-model
- visual-navigation
- robot-planning
- multimodal-trajectory-prediction
- visual-foresight
- image-goal-navigation
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# NavWM: A Unified Navigation World Model for Foresight-Driven Planning

## Summary
NavWM is a navigation world model that uses predicted future images to choose among multiple candidate robot paths. It reports better trajectory prediction, future-frame generation, and image-goal navigation than prior visual navigation and world-model baselines.

## Problem
- Visual navigation policies can make short-sighted moves because they map camera input directly to actions without testing likely future states.
- Existing navigation world models often split perception, action prediction, and future-image generation into separate parts, which can waste shared spatial and temporal information.
- Single-trajectory action prediction can collapse to one path even when several safe routes are possible, which matters for cluttered indoor and outdoor robot navigation.

## Approach
- NavWM takes past RGB frames, the current frame, and a goal image, then predicts multiple future trajectories and the future observations for those trajectories.
- A Bidirectional Mamba backbone encodes visual history and goal inputs in a shared latent space.
- Learnable latent world tokens are trained with pseudo-labels from Depth Anything V2 and SAM, giving the model depth and semantic cues for planning.
- An anchor-based trajectory head predicts several candidate target points and waypoint sequences instead of one path.
- A Conditional Diffusion Transformer with flow matching generates future visual observations conditioned on candidate actions, so the planner can score paths by visual foresight.

## Results
- Offline trajectory prediction across Go Stanford, SCAND, RECON, and HuRoN improves over UniWM: ATE drops from 0.302 to 0.207, RPE from 0.116 to 0.066, AOE from 9.468 to 8.152, and MAOE from 13.221 to 12.855.
- Future-image generation improves over NWM and UniWM: PSNR reaches 17.340 versus 14.343 for NWM and 14.172 for UniWM.
- NavWM reports SSIM 0.507, LPIPS 0.243, and DreamSim 0.084; the closest listed baselines are SSIM 0.435 for UniWM, LPIPS 0.282 for UniWM, and DreamSim 0.091 for NWM.
- In image-goal navigation rollout, the paper reports success rate rising from 66% to 72% in seen environments.
- On zero-shot inference in unseen environments, including TartanDrive as the held-out testbed, the paper reports 44% navigation success.
- The default model has 1.5B parameters, uses 4 past frames to predict the next 4 frames, and trains for 100,000 teacher-forced steps plus 50,000 fine-tuning steps on predicted trajectories.

## Link
- [https://arxiv.org/abs/2606.24101v1](https://arxiv.org/abs/2606.24101v1)
