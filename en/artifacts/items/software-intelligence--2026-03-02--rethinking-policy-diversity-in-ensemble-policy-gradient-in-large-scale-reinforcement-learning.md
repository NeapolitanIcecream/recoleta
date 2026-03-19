---
source: arxiv
url: http://arxiv.org/abs/2603.01741v2
published_at: '2026-03-02T11:06:40'
authors:
- Naoki Shitanda
- Motoki Omura
- Tatsuya Harada
- Takayuki Osa
topics:
- reinforcement-learning
- policy-optimization
- ensemble-rl
- exploration
- importance-sampling
relevance_score: 0.19
run_id: materialize-outputs
language_code: en
---

# Rethinking Policy Diversity in Ensemble Policy Gradient in Large-Scale Reinforcement Learning

## Summary
This paper studies multi-policy ensemble exploration in large-scale parallel reinforcement learning and argues that “the more dispersed the policies, the better” does not hold. The authors propose CPO, which constrains the KL distance between followers and the leader to improve stability and sample efficiency while preserving exploration diversity.

## Problem
- In large-scale on-policy RL with **24,576** parallel environments, exploration by a single policy is insufficient, and simply increasing the amount of data does not effectively improve learning efficiency.
- Existing ensemble methods (such as SAPG) can broaden the exploration range, but **overly large inter-policy differences** cause the importance sampling ratio to deviate from 1 when the leader uses follower data, reducing effective sample size and increasing PPO clipping bias.
- This matters because high-dimensional tasks such as robotic dexterous manipulation require sufficient exploration while also depending critically on training stability and sample efficiency.

## Approach
- Proposes **Coupled Policy Optimization (CPO)**: in a leader-follower framework, a **KL divergence constraint** to the leader is added to follower updates, allowing followers to explore in a “controlled spread” around the leader.
- Theoretically, the paper makes three points: excessively large policy differences reduce **effective sample size (ESS)** and increase gradient bias introduced by PPO clipping; meanwhile, the follower-leader KL distance upper-bounds the degree of IS ratio deviation.
- In implementation, the follower update is written as an optimization problem with a KL constraint, approximately solved using an advantage-weighted objective, and then jointly trained with the original SAPG/PPO-style objective.
- To prevent all followers from becoming overly concentrated due to the KL constraint, the method adds an **adversarial reward**: a discriminator is trained to identify policy identity from state-action pairs, encouraging different followers to cover different regions.

## Results
- Experiments cover **10 tasks**: **6** dexterous manipulation tasks, **2** gripper manipulation tasks, and **2** locomotion tasks; using **24,576** parallel environments and **5** random seeds, compared against **PPO, DexPBT, SAPG**.
- On dexterous manipulation tasks after training for **2×10^10** environment steps, CPO achieves the best or tied-best final performance on multiple tasks: **ShadowHand 13762±414** (vs SAPG **12882±343**, PPO **10661±1050**), **AllegroHand 14421±885** (vs DexPBT **13239±239**, SAPG **11989±817**), **Reorientation 43.75±0.65** (vs SAPG **38.79±1.66**, PPO **1.04±0.98**), **Two-Arms Reorientation 35.30±2.77** (vs DexPBT **26.43±11.12**, SAPG **5.11±3.41**).
- On **Regrasping**, CPO reaches **37.44±1.21**, close to SAPG **37.20±0.65** and DexPBT **35.26±2.82**, still placing it in the top group; on **Throw**, CPO scores **21.69±2.44**, slightly below SAPG **22.51±1.15**, though the authors claim it still maintains consistently strong overall performance.
- The authors claim that on many tasks, CPO reaches SAPG’s final performance using **about half as many environment steps**, indicating higher sample efficiency; the excerpt does not provide more complete per-task curve values.
- In mechanistic analysis, the authors report that the KL constraint keeps the IS ratio closer to **1**, improves ESS, and causes followers to form a more structured distribution around the leader; these are strong empirical claims in the paper, but the excerpt does not provide complete ESS or KL tables.

## Link
- [http://arxiv.org/abs/2603.01741v2](http://arxiv.org/abs/2603.01741v2)
