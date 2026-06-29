---
source: arxiv
url: https://arxiv.org/abs/2606.09813v1
published_at: '2026-06-08T17:55:41'
authors:
- Zhenyu Wu
- Xiuwei Xu
- Yukun Zhou
- Yifan Li
- Qiuping Deng
- Xiaofeng Wang
- Zheng Zhu
- Bingyao Yu
- Ziwei Wang
- Jiwen Lu
- Haibin Yan
topics:
- embodied-world-model
- action-conditioned-video
- robot-policy-evaluation
- contact-aware-control
- long-horizon-rollout
- dexterous-manipulation
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# iMaC: Translating Actions into Motion and Contact Images for Embodied World Models

## Summary
iMaC is an action-conditioned robot world model for long-horizon manipulation policy evaluation. It turns future robot actions into rendered robot-motion videos and pointcloud-based contact heatmaps, then uses them to guide multi-view RGB-D video rollout.

## Problem
- Robot policy evaluation in hardware is slow, costly, and hard to repeat across checkpoints.
- Existing action-conditioned video models often pass actions as compact vectors, which can miss centimeter-scale changes that decide contact, object motion, and task success.
- Long closed-loop rollouts amplify visual and geometric errors because each generated chunk becomes the next input.

## Approach
- iMaC uses the robot URDF and forward kinematics to convert future joint actions into motion images: rendered future robot observations from one head camera and two wrist cameras.
- It predicts RGB and depth in a six-panel mosaic, then lifts predicted depth into pointclouds for later chunks.
- It builds two contact-image streams: robot-to-scene distances and scene-to-gripper distances, colorized as dense heatmaps.
- A WAN2.2 image-to-video DiT receives the reference frame, noisy future video tokens, and the three control videos through latent-token addition.
- Training-time rollout feeds detached generated final frames into later chunks, reducing mismatch with closed-loop inference.

## Results
- On 8 real-robot long-horizon manipulation tasks, iMaC reports the best averaged FID, PSNR, SSIM, and FVD among listed methods: FID 36.96 ± 9.16, PSNR 16.39 ± 1.41, SSIM 0.735 ± 0.037, FVD 489.51 ± 92.65.
- Against Ctrl-World, iMaC improves FID from 48.64 ± 10.68 to 36.96 ± 9.16 and FVD from 591.47 ± 160.30 to 489.51 ± 92.65, with MSE 0.028 ± 0.010 versus 0.030 ± 0.012.
- Against ABot-PhysWorld, iMaC improves MSE from 0.041 ± 0.017 to 0.028 ± 0.010, FID from 74.23 ± 22.50 to 36.96 ± 9.16, and FVD from 642.98 ± 105.27 to 489.51 ± 92.65.
- For closed-loop policy evaluation, world-model success estimates correlate with real-world success on 6 of 8 tasks with r = 0.833 to 0.956.
- Two weaker tasks report r = 0.678 and r = 0.428; the paper attributes these failures to height relations poorly observed by the available cameras.
- The evaluation covers 2 VLA policy families, π0.5 and GigaBrain-0.5, with 3 checkpoints each and 30 episodes per evaluation group.

## Link
- [https://arxiv.org/abs/2606.09813v1](https://arxiv.org/abs/2606.09813v1)
