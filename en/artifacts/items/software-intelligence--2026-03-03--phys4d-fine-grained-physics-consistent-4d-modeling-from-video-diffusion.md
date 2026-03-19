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
- 4d-world-model
- physics-consistency
- simulation-supervision
- reinforcement-learning
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# Phys4D: Fine-Grained Physics-Consistent 4D Modeling from Video Diffusion

## Summary
Phys4D progressively elevates pretrained video diffusion models into 4D world models with explicit geometry and motion representations, aiming to generate videos that not only “look right” but also better obey physical laws over time. It combines pseudo-supervision, simulation supervision, and reinforcement learning to improve fine-grained physical consistency, and introduces a corresponding 4D evaluation suite.

## Problem
- Existing video diffusion models are mostly trained to match appearance, and often exhibit problems such as local geometric inconsistency, unstable object motion, and long-term dynamics that violate causality or physical laws.
- Training physics-consistent 4D world models lacks scalable real supervision, especially because dense, temporally aligned depth and motion ground truth is difficult to obtain from real videos.
- Appearance-only metrics cannot determine whether a model has truly learned “how the world evolves,” so world-level 4D consistency evaluation is needed.

## Approach
- Uses a **three-stage training** setup: first large-scale pretraining of geometry/motion heads with pseudo-labels, then supervised fine-tuning on physics simulation data, and finally simulation-backed reinforcement learning to correct residual physical errors.
- Adds lightweight **depth head** and **motion head** modules on top of a pretrained video diffusion backbone to output per-frame depth and optical flow between adjacent frames, extending pure 2D video generation into explicit RGB-D-motion modeling.
- In the second stage, introduces a simulation-based **warp consistency loss**, requiring that depth at time t, after being transformed by the predicted motion field, should match the depth at t+1, thereby explicitly coupling geometry and motion.
- In the third stage, lifts generated results into 4D spatiotemporal point clouds and uses the **4D Chamfer Distance** to simulation ground truth as a reward; it treats the denoising process as a stochastic policy and optimizes it with PPO to make long-horizon trajectories more physically plausible.
- Builds a large-scale simulation data pipeline: about **250,000** environments, **1,250,000** videos, **20,800 hours** in total, **9** categories of physical phenomena, and **15 TB+** of annotations for geometry, motion, and reward supervision.

## Results
- On the **Physics-IQ** benchmark, **CogVideoX + Phys4D** improves the total score from **18.8** to **30.2** (+**11.4**); meanwhile, **MSE** drops from **0.013** to **0.009**, **ST-IoU** rises from **0.116** to **0.169**, **S-IoU** rises from **0.222** to **0.252**, and **WS-IoU** rises from **0.142** to **0.157**.
- For **WAN2.2**, Phys4D raises the total score from **16.8** to **25.6** (+**8.8**); **MSE** drops from **0.016** to **0.014**, **ST-IoU** rises from **0.088** to **0.107**, **S-IoU** rises from **0.150** to **0.214**, and **WS-IoU** rises from **0.105** to **0.122**.
- For **Open-Sora V1.2**, the total score improves from **14.5** to **22.4** (+**7.9**); **MSE** drops from **0.021** to **0.016**, **ST-IoU** rises from **0.072** to **0.098**, **S-IoU** rises from **0.135** to **0.195**, and **WS-IoU** rises from **0.092** to **0.112**.
- The paper also claims substantial improvements in fine-grained spatiotemporal consistency and physical plausibility while maintaining strong generative quality; the evaluation covers **198** test scenes, **3** viewpoints, and **2** variants, for a total of **1,188** test videos.

## Link
- [http://arxiv.org/abs/2603.03485v2](http://arxiv.org/abs/2603.03485v2)
