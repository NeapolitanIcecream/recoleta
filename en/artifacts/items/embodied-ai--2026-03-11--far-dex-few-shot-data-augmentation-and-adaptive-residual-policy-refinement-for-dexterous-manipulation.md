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
- imitation-learning
- sim2real
- residual-policy
- data-augmentation
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# FAR-Dex: Few-shot Data Augmentation and Adaptive Residual Policy Refinement for Dexterous Manipulation

## Summary
FAR-Dex targets three core bottlenecks in dexterous manipulation—“too few demonstrations, control is too hard, and real-world deployment is unstable”—and proposes a hierarchical framework composed of few-shot data augmentation and adaptive residual control. It is designed for coordinated control of robotic arms and multi-fingered hands, and reports strong success rates and real-time performance in both simulation and the real world.

## Problem
- This work addresses the problem of **coordinated robotic arm–dexterous hand manipulation from a small number of human demonstrations**; this matters because high-quality dexterous manipulation demonstrations are scarce, while real tasks require fine-grained contact and stable long-horizon control.
- Existing data generation methods often lack fine-grained hand–object interaction details, leading to **poor sim-to-real transfer**, while existing residual policies lack explicit spatiotemporal modeling, making it difficult to stably correct errors in long-horizon tasks.
- The joint control of a robotic arm and a multi-fingered hand has a high-dimensional action space. Without simultaneously improving **data quality** and **online correction capability**, it is difficult to achieve reliable real-world dexterous manipulation.

## Approach
- FAR-Dex contains two parts: **FAR-DexGen** first decomposes a very small number of demonstrations into “motion segments” and “skill segments,” then generates a large number of physically feasible new trajectories in IsaacLab by changing the object’s initial pose and combining motion planning with inverse kinematics.
- The core idea of the method can be understood simply as: **preserve the hand’s fine contact actions from the original demonstrations as much as possible, while recomputing the robotic arm trajectory as the object position changes**. This both expands the dataset and preserves contact details.
- During training, real demonstrations are merged with simulation-generated data, and a DP3-style base policy is used to learn actions; at the same time, **consistency model distillation** compresses the original multi-step diffusion/denoising inference into single-step inference to reduce latency.
- During online execution, **FAR-DexRes** then learns a residual policy: using multi-step trajectory segments and current observations, it generates per-dimension weights \(\sigma_t\) through cross-attention to adaptively correct the base action by “adjusting as much as needed.”
- The residual policy is trained with PPO warm-start, with the goal of preserving the smoothness of the base policy while providing finer-grained error compensation for contact phases and out-of-distribution states.

## Results
- In data generation, on the Insert Cylinder task, **FAR-DexGen** has a trajectory generation time of **10.3 ms/trajectory**, slightly slower than **MimicGen 8.3 ms** and **DemoGen 9.1 ms**, but still in a similar range.
- In data quality, using “the success rate obtained after training a unified DP3 on generated data” as a proxy metric, FAR-DexGen reaches **87.9%**, higher than **MimicGen 68.3%** and **DemoGen 74.5%**; improvements are **19.6%** and **13.4%**, respectively.
- In simulation task success rate, **FAR-DexRes** achieves on four tasks: **Insert Cylinder 93%**, **Pinch Pen 83%**, **Grasp Handle 88%**, and **Move Card 95%**.
- Compared with **ResiP**, one of the strongest baseline methods, FAR-DexRes improves success rates on the four tasks from **85%→93%**, **79%→83%**, **80%→88%**, and **87%→95%**, respectively, an average gain of about **7 percentage points**, consistent with the claim in the abstract.
- Compared with pure imitation learning baselines, FAR-DexRes is also significantly stronger; for example, relative to **DP3**: **83%→93%**, **77%→83%**, **80%→88%**, **53%→95%**; among these, Move Card shows the largest improvement at **+42 percentage points**.
- In inference latency, FAR-DexRes requires only **3.0/4.3/3.8/4.3 ms** per step, significantly lower than **DP3’s 29.1/31.5/29.8/29.6 ms** and **ResiP’s 29.3/32.5/31.9/30.2 ms**. The abstract also claims that real-world task success exceeds **80%**, but the excerpt does not provide more detailed per-task real-world results.

## Link
- [http://arxiv.org/abs/2603.10451v1](http://arxiv.org/abs/2603.10451v1)
