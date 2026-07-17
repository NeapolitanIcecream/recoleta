---
source: arxiv
url: https://arxiv.org/abs/2607.15065v1
published_at: '2026-07-16T14:37:43'
authors:
- Susie Lu
- Haonan Chen
- Weirui Ye
- Yilun Du
topics:
- world-models
- robotics
- action-conditioned-video
- robot-planning
- policy-evaluation
- fast-generation
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# DriftWorld: Fast World Modeling through Drifting

## Summary
DriftWorld is a single-step, action-conditioned world model that predicts future robot observations in one forward pass instead of using iterative diffusion sampling. Across five manipulation benchmarks, it reports 17× faster generation while maintaining or improving rollout quality and supporting faster planning and offline policy evaluation.

## Problem
- Diffusion-based robot world models require repeated denoising steps, making large-scale action search slow; a cited baseline spends 90–95% of each decision cycle on rollouts and takes at least 3 seconds per decision.
- Slow imagination limits how many candidate action sequences a robot can evaluate before acting, and increases the cost of ranking policies without real-world execution.

## Approach
- DriftWorld learns an action-conditioned drifting field during training that moves generated future-video samples toward a ground-truth future and away from generated negative samples.
- At inference, the model generates future frames from Gaussian noise, observation history, and a proposed action sequence in a single U-Net forward pass, avoiding iterative diffusion denoising.
- The model uses frame-wise FiLM action conditioning, factorized spatial-temporal convolutions, and DINOv2/v3 feature-space drifting for complex real-world scenes.
- Motion-weighted feature losses discourage the model from ignoring actions and simply copying the current observation.

## Results
- On five benchmarks—Bridge-V2, RT-1, Language Table, Push-T, and Robomimic—the paper reports 30+ fps generation and an average 17× speedup over diffusion-based world-model baselines.
- On Push-T 64-frame rollouts, DriftWorld achieves MSE 0.0007, SSIM 0.9925, PSNR 33.7753, and LPIPS 0.0050, with 0.0037 seconds per generated frame; the GPC baseline takes 0.0104 seconds per frame and achieves SSIM 0.9717.
- On Bridge-V2, DriftWorld reaches SSIM 0.821, PSNR 21.871, LPIPS 0.103, and FVD 101.16 in 0.0300 seconds per frame, compared with IRASim at SSIM 0.738 and 1.1031 seconds per frame.
- Using rollout-based action selection improves Push-T IoU from 0.635 to 0.781.
- For offline policy ranking, rollout scores correlate with ground-truth performance with Pearson coefficients of 0.9515 on Push-T, 0.9916 on Robomimic Lift, and 0.9250 on Robomimic Can.

## Link
- [https://arxiv.org/abs/2607.15065v1](https://arxiv.org/abs/2607.15065v1)
