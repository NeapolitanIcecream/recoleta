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
- 3d-point-clouds
- imitation-learning
- cross-embodiment-transfer
- transformer-policy
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# Structural Action Transformer for 3D Dexterous Manipulation

## Summary
This paper proposes the Structural Action Transformer (SAT), which rewrites the actions of high-DoF dexterous hands from “time-ordered action vectors” into “joint-ordered trajectory sequences,” enabling more natural skill transfer across different robot embodiments. It combines 3D point clouds, language conditioning, and joint structural encoding to achieve stronger performance and higher sample efficiency in heterogeneous imitation learning and dexterous manipulation.

## Problem
- Existing imitation learning methods for dexterous manipulation mostly use time-centric action representations $(T,D_a)$. When the DoF is high, it becomes difficult to learn the complex joint correlations within a single action vector.
- Different robot hands vary in joint count, kinematic structure, and function, so fixed-dimensional action representations are not suitable for cross-embodiment transfer, limiting learning from heterogeneous human/robot data.
- Many general-purpose robot policies rely on 2D observations and struggle to capture the 3D spatial relationships required for fine-grained dexterous manipulation, which hurts high-precision manipulation performance.

## Approach
- Proposes a structural-centric action representation: an action chunk is represented as $D_a \times T$, where each joint is treated as a token whose features are that joint’s full future trajectory over a time window; different robots then differ only in the number of tokens, allowing a Transformer to natively handle variable-length sequences.
- Uses an Embodied Joint Codebook to add structural priors for each joint, encoding its **embodiment ID, functional category, rotation axis**, helping the model identify correspondences between functionally similar joints across different hands.
- On the observation side, directly uses **3D point cloud history + language instruction**: local/global point cloud tokens are extracted through FPS + PointNet, then concatenated with T5 language tokens to form the conditioning input.
- On the generation side, uses a DiT-based Structural Action Transformer to learn the action velocity field under a conditional flow matching framework, and generates the full action chunk through ODE solving; the paper emphasizes **1-NFE** inference.
- The authors claim this is the **first** policy framework to tokenize actions along the “structural dimension” rather than the “temporal dimension” for high-DoF heterogeneous manipulator policy learning.

## Results
- On **11 simulation tasks** (3 Adroit, 4 DexArt, 4 Bi-DexHands), SAT achieves an average success rate of **0.71±0.04**, outperforming: 3D ManiFlow Policy **0.66±0.04**, 3D Diffusion Policy **0.63±0.06**, UniAct **0.50±0.05**, HPT **0.47±0.04**, and Diffusion Policy **0.42±0.04**.
- By benchmark, SAT reaches **0.75±0.02** on **Adroit**, higher than 3D ManiFlow’s **0.70±0.02** and 3D Diffusion Policy’s **0.68±0.03**.
- On **DexArt**, SAT achieves **0.73±0.03**, higher than 3D ManiFlow’s **0.70±0.03** and 3D Diffusion Policy’s **0.69±0.02**.
- On **Bi-DexHands**, SAT achieves **0.67±0.05**, higher than 3D ManiFlow’s **0.59±0.07** and 3D Diffusion Policy’s **0.55±0.14**.
- Parameter efficiency is notable: SAT uses only **19.36M** parameters, yet outperforms 3D ManiFlow with **218.9M**, 3D Diffusion Policy with **255.2M**, and UniAct with **1053M**.
- Temporal compression ablations show that when token dim varies across **16/32/64/128/256**, the success rates are **0.66/0.71/0.71/0.71/0.70**, respectively; **32 dimensions** already reaches one of the best performance levels, with only **8.65M** parameters and **0.77G** 1-NFE FLOPs, indicating that this structural representation is effective even with smaller models.

## Link
- [http://arxiv.org/abs/2603.03960v1](http://arxiv.org/abs/2603.03960v1)
