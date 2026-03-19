---
source: arxiv
url: http://arxiv.org/abs/2603.10451v1
published_at: '2026-03-11T06:10:03'
authors:
- Yushan Bai
- Fulin Chen
- Hongzheng Sun
- Yuchuang Tong
- En Li
- Zhengtao Zhang
topics:
- dexterous-manipulation
- few-shot-learning
- data-augmentation
- residual-policy-learning
- sim-to-real
relevance_score: 0.28
run_id: materialize-outputs
language_code: en
---

# FAR-Dex: Few-shot Data Augmentation and Adaptive Residual Policy Refinement for Dexterous Manipulation

## Summary
FAR-Dex targets dexterous manipulation learning under few-shot conditions by combining “expanding high-quality data from a small number of demonstrations” with “online adaptive residual error correction” for coordinated control of multi-fingered hands and robotic arms. It attempts to simultaneously address the problems of scarce demonstrations, difficulty controlling high-dimensional actions, and insufficient precision and robustness in long-horizon tasks.

## Problem
- Dexterous manipulation requires coordination between a robotic arm and a multi-fingered hand, but the joint action space is high-dimensional, errors tend to accumulate in long-horizon tasks, and stable control is difficult.
- There are few real high-quality demonstrations, and fine-grained 3D hand-object interaction information is lacking, leading to insufficient imitation learning data, poor generalization, and difficulty in real-world deployment.
- Existing data augmentation methods often suffer from a simulation-to-reality gap, while existing residual policies lack explicit spatiotemporal modeling, making stage-sensitive fine-grained correction difficult.

## Approach
- A hierarchical framework FAR-Dex is proposed: first, **FAR-DexGen** generates large-scale, physically feasible synthetic trajectories from only a few demonstrations per task, and then **FAR-DexRes** performs online residual refinement on the base policy.
- The core idea of data generation is straightforward: split demonstration trajectories into an “object-approach motion segment” and a “contact/manipulation skill segment”; after changing the object’s initial pose, recompute the robotic arm trajectory and replay/collect it in IsaacLab, thereby obtaining more data with fine-grained contact information. In the real system described in the paper, only **2 expert demonstrations** are collected per task, with a sampling frequency of **20 Hz**.
- The base policy is built on DP3, but uses a consistency model to distill the original multi-step denoising inference into single-step prediction, reducing inference latency under high-dimensional point-cloud conditioning; the point-cloud encoder is replaced with a four-stage recursive PointNet, producing a **128-dimensional** embedding.
- The residual refinement module works as follows: the base action first outputs a “primary action,” then cross-attention reads the most recent **H=8** steps of observations and trajectory segments to generate adaptive weights aligned with the action dimensions sigma; the residual action is scaled dimension-wise and then added back. The residual policy is trained with PPO to achieve dynamic error correction according to task stage.

## Results
- **Data generation quality** (Insert Cylinder, all evaluated upstream with DP3): FAR-DexGen achieves **87.9%**, outperforming DemoGen’s **74.5%** and MimicGen’s **68.3%**; this is an improvement of **13.4 percentage points** over DemoGen and **19.6 percentage points** over MimicGen.
- **Data generation time**: FAR-DexGen takes **10.3 ms/trajectory**, slightly slower than DemoGen’s **9.1 ms** and MimicGen’s **8.3 ms**, but the paper emphasizes that the gap from the fastest method is only about **2 ms**.
- **Simulation task success rate** (FAR-DexRes): Insert Cylinder **93%**, Pinch Pen **83%**, Grasp Handle **88%**, Move Card **95%**. Among the strongest corresponding baselines, ResiP scores **85%/79%/80%** on the first three, and IDP3 scores **86%** on Move Card, so FAR-DexRes is higher by **8/4/8/9 percentage points**, respectively.
- **Single-step inference time** (FAR-DexRes): Insert Cylinder **3.0 ms**, Pinch Pen **4.3 ms**, Grasp Handle **3.8 ms**, Move Card **4.3 ms**; this is much faster than DP3’s **29.1/31.5/29.8/29.6 ms**, and also slightly faster than or comparable to fast baselines such as ACT+3D, ManiCM, and Flow Policy.
- **Overall claimed results**: the abstract states that FAR-Dex improves task success rates by **7%** over existing best methods, achieves over **80%** success on real-world tasks, and has strong positional generalization ability. The excerpt does not provide more complete per-task real-world details.

## Link
- [http://arxiv.org/abs/2603.10451v1](http://arxiv.org/abs/2603.10451v1)
