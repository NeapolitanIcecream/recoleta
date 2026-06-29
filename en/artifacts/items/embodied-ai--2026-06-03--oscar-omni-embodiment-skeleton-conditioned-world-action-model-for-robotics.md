---
source: arxiv
url: https://arxiv.org/abs/2606.04463v1
published_at: '2026-06-03T05:16:41'
authors:
- Zhuoyuan Wu
- Jun Gao
topics:
- world-model
- vision-language-action
- robot-policy-evaluation
- cross-embodiment
- robot-data-scaling
- sim2real
relevance_score: 0.98
run_id: materialize-outputs
language_code: en
---

# OSCAR: Omni-Embodiment Skeleton-Conditioned World Action Model for Robotics

## Summary
OSCAR is a 2B-parameter action-conditioned video world model for robot policy evaluation across robot arms and human hands. It uses 2D skeleton renderings as the action input, which gives the generator spatial motion cues without tying the condition to one robot's visual appearance.

## Problem
- Robot policy evaluation on real hardware is slow, costly, and hard to repeat at scale, so a useful video world model could screen policies before deployment.
- Existing action-conditioned video models often miss precise frame-level and pixel-level action following, which weakens their value as evaluation proxies.
- Many models train on narrow robot datasets or embodiment-specific action encodings, which limits transfer across Franka Panda, KUKA iiwa, AgiBot G1, Toyota HSR, and human hands.

## Approach
- OSCAR finetunes Cosmos-Predict2.5-2B with an initial RGB frame and a full sequence of rendered 2D kinematic skeletons.
- The skeleton condition is made by projecting robot URDF link points or MANO hand joints into the camera view, then drawing lines and joint dots on a black canvas.
- The skeleton video is encoded with the WAN 2.1 VAE, embedded as tokens, and added to the noisy video tokens inside the diffusion transformer during denoising.
- The training pipeline curates, filters, deduplicates, and captions robot and egocentric human videos, retaining 180,657 episodes from 2,165,359 public source episodes.
- Training uses two stages: 15k iterations on four robot embodiments, then continued training on the mixed robot and human dataset on a single NVIDIA GH200 GPU.

## Results
- On a 200-clip benchmark across four embodiments, OSCAR reaches PSNR 24.24 and SSIM 0.846, above Genie Envisioner at 23.29 PSNR and 0.838 SSIM.
- OSCAR reports LPIPS 0.094, FVD 7.08, FID 15.07, and latent L2 0.096; the next strongest listed baseline has LPIPS 0.140, FVD 15.37, FID 22.92, and latent L2 0.129.
- OSCAR runs at 2.214 FPS on the reported GH200 test, compared with Kinema4D at 0.089 FPS and Genie Envisioner at 1.382 FPS.
- The model is 2B parameters and outperforms the 14B-parameter Kinema4D on the table metrics: PSNR 24.24 vs 17.68, SSIM 0.846 vs 0.741, FVD 7.08 vs 17.07, and FID 15.07 vs 37.16.
- Ablations show skeleton conditioning with robot-only data is close to mesh rendering: PSNR 23.48 vs 23.11, SSIM 0.832 vs 0.831, and FVD 7.69 vs 7.89.
- Adding human data with a robot-only warm start improves over robot-only skeleton training: PSNR 24.24 vs 23.48, SSIM 0.846 vs 0.832, FVD 7.08 vs 7.69, and FID 15.07 vs 16.37. The excerpt claims strong correlation with RoboArena real-world policy evaluation, but it does not provide the correlation number.

## Link
- [https://arxiv.org/abs/2606.04463v1](https://arxiv.org/abs/2606.04463v1)
