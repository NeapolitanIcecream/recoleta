---
source: arxiv
url: http://arxiv.org/abs/2603.03960v1
published_at: '2026-03-04T11:38:12'
authors:
- Xiaohan Lei
- Min Wang
- Bohong Weng
- Wengang Zhou
- Houqiang Li
topics:
- dexterous-manipulation
- cross-embodiment-transfer
- 3d-point-clouds
- transformer-policy
- flow-matching
- robot-imitation-learning
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Structural Action Transformer for 3D Dexterous Manipulation

## Summary
This paper proposes the Structural Action Transformer (SAT) for cross-embodiment imitation learning with high-DoF dexterous hands, rewriting actions from a time-ordered sequence into a joint-ordered 3D structural sequence. This representation allows a single Transformer to naturally handle hands with different numbers of joints, enabling better transfer and sample efficiency on large-scale heterogeneous human/robot datasets.

## Problem
- The goal is to solve **cross-embodiment skill transfer for high-DoF dexterous hands on heterogeneous datasets**: different hand types, joint counts, and kinematic structures vary significantly, making it difficult for traditional imitation learning to share skills.
- Existing methods mostly use **2D observations** and **time-centric action representations $(T, D_a)$**, which struggle to express the 3D spatial relationships required for fine manipulation and cannot naturally align action dimensions across different embodiments.
- This matters because if data cannot be reused across human hands, robot hands, and simulation platforms, dexterous manipulation policies will be hard to scale into general-purpose high-DoF robot foundation models.

## Approach
- The core idea is to reconstruct an action chunk from the traditional **$(T, D_a)$ time sequence** into a **$(D_a, T)$ joint sequence**: each token no longer represents the full-hand action at a given time step, but instead represents **the trajectory of a single joint over a future time window**.
- With this design, different robots differ only in **sequence length $D_a$**; Transformers natively support variable-length sequences, so they can more naturally handle heterogeneous embodiments and learn correspondences between joint functions.
- To tell the model "which joint this is, what it does, and how it rotates," the authors design an **Embodied Joint Codebook**, using a triplet *(embodiment id, functional category, rotation axis)* to add structural-prior embeddings to each joint.
- The input uses **3D point cloud history + language instructions**: point clouds are processed with FPS + PointNet to extract local/global tokens, and language is encoded with T5; these observation tokens are fed together with structured action tokens into DiT.
- During training, the model does not directly regress actions, but instead uses **continuous-time flow matching** to learn the velocity field from Gaussian noise to action chunks; at inference time, it uses an ODE solver to generate the full action segment, which the paper says can be done with **1-NFE** generation.

## Results
- On **11 simulated dexterous manipulation tasks** (3 from Adroit, 4 from DexArt, 4 from Bi-DexHands), SAT achieves an **average success rate of 0.71±0.04**, outperforming all comparison methods.
- Compared with 3D baselines: SAT **0.71±0.04** vs **3D ManiFlow Policy 0.66±0.04** vs **3D Diffusion Policy 0.63±0.06**; this is an average success-rate gain of **0.05** and **0.08**, respectively.
- By dataset, SAT reaches **0.75±0.02 / 0.73±0.03 / 0.67±0.05** on **Adroit/DexArt/Bi-DexHands**; the strongest corresponding baseline, 3D ManiFlow, achieves **0.70±0.02 / 0.70±0.03 / 0.59±0.07**.
- Compared with 2D methods, SAT shows an even larger advantage: average success rate **0.71** versus **UniAct 0.50**, **HPT 0.47**, and **Diffusion Policy 0.42**.
- It is also highly parameter-efficient: SAT has only **19.36M** parameters, yet surpasses **218.9M** for 3D ManiFlow, **255.2M** for 3D Diffusion Policy, and **1053M** for UniAct.
- Ablations show that temporal compression dimensions **32/64/128** all achieve a **0.71** success rate; the **64-dimensional** configuration corresponds to **19.36M parameters, 0.99G FLOPs (1-NFE)**. The paper also claims better sample efficiency and effective cross-embodiment transfer, but the excerpt does not provide more detailed sample-efficiency curve values.

## Link
- [http://arxiv.org/abs/2603.03960v1](http://arxiv.org/abs/2603.03960v1)
