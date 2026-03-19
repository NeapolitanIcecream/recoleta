---
source: arxiv
url: http://arxiv.org/abs/2603.14498v1
published_at: '2026-03-15T17:30:49'
authors:
- Yuhao Zhang
- Wanxi Dong
- Yue Shi
- Yi Liang
- Jingnan Gao
- Qiaochu Yang
- Yaxing Lyu
- Zhixuan Liang
- Yibin Liu
- Congsheng Xu
- Xianda Guo
- Wei Sui
- Yaohui Jin
- Xiaokang Yang
- Yanyan Xu
- Yao Mu
topics:
- embodied-manipulation
- 3d-awareness
- real-time-inference
- diffusion-policy
- multi-view-fusion
relevance_score: 0.21
run_id: materialize-outputs
language_code: en
---

# R3DP: Real-Time 3D-Aware Policy for Embodied Manipulation

## Summary
R3DP proposes a real-time 3D-aware policy for embodied manipulation, incorporating high-quality 3D foundation model priors into diffusion policy while minimizing the high latency in real-time control. The core idea is a collaboration between a “slow but accurate” 3D model and a “fast and lightweight” temporal feature predictor, combined with explicit multi-view geometric fusion to improve manipulation success rates.

## Problem
- Embodied manipulation requires stable 3D spatial understanding and temporal consistency, but common 2D imitation learning policies mainly rely on RGB features and struggle with tasks involving depth, occlusion, and rich contact.
- Directly applying large 3D foundation models frame by frame for robot control introduces excessive inference latency, especially in multi-view settings where real-time performance is difficult to achieve.
- Although relying on depth/point cloud sensors can enhance 3D perception, it increases hardware complexity and is unstable on transparent, reflective, and textureless objects.

## Approach
- Proposes R3DP: integrates intermediate 3D features from large 3D vision foundation models such as VGGT into Diffusion Policy as a plug-and-play 3D perception module.
- Designs an asynchronous fast-slow collaboration module (AFSC): the slow VGGT runs only on sparse key frames, while lightweight Temporal Feature Prediction Network (TFPNet) predicts 3D features for other intermediate frames based on historical features and current RGB.
- TFPNet is pre-trained by distilling VGGT, leveraging temporal correlations to maintain feature continuity and stability under real-time constraints while explicitly introducing temporal context.
- Designs Multi-View Feature Fuser (MVFF): first fuses 2D and 3D features from each view, then explicitly injects camera intrinsics and extrinsics via PRoPE for geometrically consistent multi-view fusion.
- Expands the temporal window during training: each training sample uses 8 frames with stride 8, covering 64 frames in total; the visual backbone is frozen, and only the diffusion policy head is trained to control computational cost.

## Results
- On 10 RoboTwin tasks, R3DP achieves an average success rate of **69.0%** (τ=4) and **65.7%** (τ=8), clearly outperforming **DP-single 36.1%**, **DP-multi 17.6%**, **DP3 57.6%**, **DP3+DA2 28.2%**, and also exceeding **π0 59.9%**.
- The abstract claims that R3DP improves average success rates by **32.9%** and **51.4%** relative to single-view and multi-view Diffusion Policy, respectively.
- In terms of observation encoding latency, naive **DP+VGGT** takes **73.1 ms**, and with MVFF it becomes **78.3 ms**; in contrast, **R3DP(τ=4)** is reduced to **50.5 ms**, and **R3DP(τ=8)** to **40.3 ms**, representing up to a **44.8%** reduction relative to the naive integration.
- Task-level results show that R3DP(τ=4) leads on several difficult tasks, for example **Block Handover 95%** (vs DP-single **1%**, DP3 **48%**, π0 **71%**), **Blocks Stack Easy 69%** (vs DP-single **6%**, DP3 **26%**, π0 **79%**), and **Block Hammer Beat 77%** (vs DP-single **0%**, DP3 **49%**, π0 **47%**).
- On the transparent-object-related task **Tube Insert**, R3DP reaches **97%** (τ=4/8), matching **DP3 97%**, but clearly outperforming **DP3+DA2 32%**, **π0 68%**, and **DP-multi 64%**, supporting its claim of robustness in integrating RGB-only 3D priors.

## Link
- [http://arxiv.org/abs/2603.14498v1](http://arxiv.org/abs/2603.14498v1)
