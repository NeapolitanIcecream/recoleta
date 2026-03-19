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
- policy-ensemble
- policy-gradient
- importance-sampling
- dexterous-manipulation
relevance_score: 0.44
run_id: materialize-outputs
language_code: en
---

# Rethinking Policy Diversity in Ensemble Policy Gradient in Large-Scale Reinforcement Learning

## Summary
This paper studies how to control “policy diversity” in large-scale parallel reinforcement learning, rather than simply increasing it blindly. The authors propose CPO, which improves exploration quality, sample efficiency, and training stability by keeping follower policies near the leader while preserving moderate differences.

## Problem
- The paper addresses the following issue: under **tens of thousands of parallel environments**, a single policy does not explore diversely enough, while in multi-policy ensembles, if the policies differ too much, importance sampling becomes distorted and training becomes unstable.
- This matters because large-scale robot reinforcement learning, especially dexterous manipulation, increasingly relies on massive parallel simulation; if the additional collected data is not useful for learning, both compute and samples are wasted.
- Existing leader-follower ensemble methods (such as SAPG) can increase exploration, but they do not explicitly constrain the distance between follower and leader, which can lead to policy misalignment.

## Approach
- The core method is **Coupled Policy Optimization (CPO)**: in a leader-follower framework, each follower update includes a **KL divergence constraint relative to the leader**, so that followers explore around the leader instead of drifting too far away.
- Put simply, the authors want multiple policies to be “**spread out but not disconnected**.” This way, the data collected by followers remains useful to the leader, and the importance sampling ratios stay closer to 1.
- Theoretically, the paper analyzes the downsides of excessive inter-policy diversity: when policies are too far apart, the **effective sample size (ESS)** decreases, and gradient bias from PPO clipping increases; it also proves that deviation of the IS ratio from 1 can be controlled by an upper bound on the follower-leader KL.
- To prevent all followers from collapsing into a single cluster, the authors further add an **adversarial intrinsic reward**: they train a discriminator to identify policy identity from state-action pairs, encouraging different followers to cover different regions around the leader.
- In the experimental setup, the method is built on PPO/SAPG, using **24,576** parallel environments and **M=6** parallel policy blocks in Isaac Gym, and is evaluated on dexterous manipulation, gripper manipulation, and locomotion tasks.

## Results
- On **6 dexterous manipulation tasks**, after **2×10^10 environment steps**, CPO achieves the best or tied-best results on most tasks: ShadowHand **13762±414** (SAPG **12882±343**, PPO **10661±1050**), AllegroHand **14421±885** (PBT **13239±239**, SAPG **11989±817**), Reorientation **43.75±0.65** (SAPG **38.79±1.66**, PBT **2.92±4.27**, PPO **1.04±0.98**).
- The improvement on **Two-Arms Reorientation** is especially notable: CPO **35.30±2.77**, significantly higher than SAPG **5.11±3.41**, and also higher than PBT **26.43±11.12** and PPO **1.41±0.80**.
- On **Regrasping**, CPO scores **37.44±1.21**, close to and slightly better than SAPG **37.20±0.65** and PBT **35.26±2.82**; on **Throw**, CPO scores **21.69±2.44**, slightly below SAPG **22.51±1.15**, but still better than PBT **19.08±1.02** and PPO **15.69±3.34**.
- The authors claim that on many tasks, CPO can reach SAPG’s final performance using about **half the number of environment steps**, indicating higher sample efficiency; although the excerpt does not provide complete per-task curve values, this is a clear empirical claim of the paper.
- At the mechanism level, the KL constraint makes the **IS ratio closer to 1** when the leader uses follower data, thereby improving ESS, reducing PPO clipping bias, and producing a more structured exploration pattern in which “followers are distributed around the leader.”

## Link
- [http://arxiv.org/abs/2603.01741v2](http://arxiv.org/abs/2603.01741v2)
