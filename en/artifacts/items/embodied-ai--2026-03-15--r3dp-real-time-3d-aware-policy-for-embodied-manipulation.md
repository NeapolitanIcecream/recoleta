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
- 3d-aware-policy
- diffusion-policy
- multi-view-fusion
- real-time-inference
- sim-benchmark
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# R3DP: Real-Time 3D-Aware Policy for Embodied Manipulation

## Summary
R3DP proposes a method to integrate priors from large-scale 3D foundation models into robot manipulation policies while maintaining real-time control speed. It targets the common conflict between 3D spatial understanding and latency in embodied manipulation, improving both success rate and inference efficiency on simulation benchmarks.

## Problem
- Existing imitation learning policies based on 2D vision lack explicit 3D spatial understanding, making them prone to failure on manipulation tasks involving occlusion, rich contact, and precise alignment.
- Directly integrating large 3D foundation models into the control loop frame by frame introduces excessive latency, making it difficult to satisfy real-time robot control requirements.
- Multi-view inputs are often combined through simple concatenation, without explicitly using camera intrinsics, extrinsics, and geometric relationships, resulting in unstable cross-view fusion.

## Approach
- Proposes **Asynchronous Fast-Slow Collaboration (AFSC)**: the slow branch calls the pretrained 3D model VGGT only on sparse key frames to extract high-quality 3D features; the fast branch quickly fills in features for intermediate frames, avoiding the need to run the heavy model on every frame.
- Proposes lightweight **TFPNet**: it uses historical frames and the previous timestep's 3D features to predict real-time 3D features for the current frame; this can be understood as “using past information to infer the current 3D representation,” maintaining temporal consistency at low cost.
- Proposes the **MVFF** multi-view feature fuser: it first fuses 2D and 3D features for each view, then explicitly injects camera intrinsics and extrinsics through PRoPE to obtain a more consistent multi-view 3D representation.
- These modules are connected as a plug-and-play perception front end to Diffusion Policy. During training, the VGGT and TFPNet backbones are frozen, and only the policy head is optimized, introducing 3D priors and temporal information at relatively low computational cost.

## Results
- On 10 tasks in RoboTwin, **R3DP($4)** achieves an average success rate of **69.0%**, improving by **32.9 percentage points** over **DP-single 36.1%** and by **51.4 percentage points** over **DP-multi 17.6%**.
- **R3DP($8)** achieves an average success rate of **65.7%**, still clearly higher than **DP3 57.6%**, **DP3+DA2 28.2%**, and **π0 59.9%**.
- On representative tasks, R3DP($4) reaches: **Block Hammer Beat 77%** (vs. **0%** for both DP-single/DP-multi and **49%** for DP3), **Block Handover 95%** (vs. **1%** for DP-single and **71%** for π0), and **Put Apple Cabinet 100%** (vs. **98%** for DP3).
- On the transparent-object-related **Tube Insert** task, R3DP reaches **97%**, matching **DP3 97%**, but significantly outperforming **DP3+DA2 32%** and **π0 68%**.
- In terms of inference latency, observed encoding time drops from **DP+VGGT 73.1 ms** in the naive setup to **R3DP($8) 40.3 ms**, a **44.8%** reduction compared with naive integration; **R3DP($4)** is **50.5 ms**, a **30.9%** reduction.
- The paper’s central claim is that by decoupling “heavy 3D understanding” from “fast policy execution,” R3DP achieves stronger 3D perception, higher success rates, and lower real-time inference latency without relying on depth sensors.

## Link
- [http://arxiv.org/abs/2603.14498v1](http://arxiv.org/abs/2603.14498v1)
