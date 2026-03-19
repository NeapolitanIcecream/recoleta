---
source: arxiv
url: http://arxiv.org/abs/2603.03485v2
published_at: '2026-03-03T20:01:43'
authors:
- Haoran Lu
- Shang Wu
- Jianshu Zhang
- Maojiang Su
- Guo Ye
- Chenwei Xu
- Lie Lu
- Pranav Maneriker
- Fan Du
- Manling Li
- Zhaoran Wang
- Han Liu
topics:
- video-diffusion
- world-model
- physics-consistency
- 4d-modeling
- synthetic-data
- reinforcement-learning
relevance_score: 0.45
run_id: materialize-outputs
language_code: en
---

# Phys4D: Fine-Grained Physics-Consistent 4D Modeling from Video Diffusion

## Summary
Phys4D elevates pretrained video diffusion models into 4D world models that better obey physical laws. Instead of only generating visually appealing videos, it explicitly models geometry and motion evolving over time. The core contributions are a three-stage training pipeline, ultra-large-scale physics simulation data, and a 4D physical consistency evaluation suite that goes beyond appearance-based metrics.

## Problem
- Existing video diffusion/world models mainly fit appearance, and often exhibit fine-grained physical errors such as **local geometric inconsistency, unstable motion, and temporally non-causal behavior**.
- Training such physics-consistent 4D models requires **dense, temporally aligned supervision for geometry and motion**, but real videos are difficult to annotate at scale with this kind of labeling.
- Relying only on image-level or pixel-level losses makes it hard to guarantee **long-horizon, world-level** physical plausibility, so new training and evaluation methods are needed.

## Approach
- Use **RGB-D + optical flow/scene flow** as a 2.5D intermediate representation, so the video diffusion model predicts not only RGB but also per-frame depth and inter-frame motion, thereby explicitly representing the 4D world state.
- Propose a **three-stage training** scheme: first pretrain depth/motion heads on generated videos and internet videos using pseudo-labels; then perform supervised fine-tuning with simulation ground truth, adding a **warp consistency loss** that constrains “the current depth, after being transformed along the predicted motion, should match the next frame’s depth.”
- In the third stage, use **simulation-grounded reinforcement learning** to further correct residual physical errors that supervision does not fully cover: lift generated results into 4D point-cloud trajectories, and use **4D Chamfer Distance** to simulation ground truth as the reward, optimizing the sampling policy with PPO.
- Build a large-scale physics simulation data pipeline: based on Isaac Sim, covering **9 categories of physical phenomena**, about **20,000+** unique physical configurations, expanded from **200** base scenes to about **250,000** environments, producing **1,250,000** videos totaling **20,800 hours**, with **1080p/60FPS** and **15TB+** of multimodal annotations.
- Introduce a 4D world consistency evaluation that measures not only video-level physical plausibility but also **geometric consistency, motion stability, and long-horizon physical feasibility**.

## Results
- On **Physics-IQ**, **CogVideoX + Phys4D** versus the original CogVideoX: **Score 30.2% vs 18.8%** (+11.4 percentage points), **MSE 0.009 vs 0.013**, **ST-IoU 0.169 vs 0.116**, **S-IoU 0.252 vs 0.222**, **WS-IoU 0.157 vs 0.142**.
- **WAN2.2 + Phys4D** versus WAN2.2: **Score 25.6% vs 16.8%** (+8.8 percentage points), **MSE 0.014 vs 0.016**, **ST-IoU 0.107 vs 0.088**, **S-IoU 0.214 vs 0.150**, **WS-IoU 0.122 vs 0.105**.
- **Open-Sora V1.2 + Phys4D** versus the original Open-Sora: **Score 22.4% vs 14.5%** (+7.9 percentage points), **MSE 0.016 vs 0.021**, **ST-IoU 0.098 vs 0.072**, **S-IoU 0.195 vs 0.135**, **WS-IoU 0.112 vs 0.092**.
- Compared with the aggregated scores of commercial models listed in the paper, **CogVideoX + Phys4D 30.2%** is higher than **VideoPoet 20.3% / Pika 13.0% / Sora 10.0%**; however, the commercial models do not report the same detailed metrics, so strict comparability is limited.
- The paper also claims substantial gains in **fine-grained spatiotemporal consistency and physical consistency** while maintaining strong generative ability; beyond the Physics-IQ table, the excerpt does not provide more complete numerical results.

## Link
- [http://arxiv.org/abs/2603.03485v2](http://arxiv.org/abs/2603.03485v2)
