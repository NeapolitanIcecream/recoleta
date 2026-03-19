---
source: arxiv
url: http://arxiv.org/abs/2603.12260v1
published_at: '2026-03-12T17:59:39'
authors:
- Liang Heng
- Yihe Tang
- Jiajun Xu
- Henghui Bao
- Di Huang
- Yue Wang
topics:
- humanoid-teleoperation
- dexterous-manipulation
- imu-motion-tracking
- imitation-learning
- human-to-robot-transfer
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# HumDex:Humanoid Dexterous Manipulation Made Easy

## Summary
HumDex proposes a portable teleoperation system for humanoid whole-body dexterous manipulation, and combines pre-training on human data with fine-tuning on robot data to reduce the cost of collecting high-quality demonstrations. The core goal is to maintain high precision while overcoming visual occlusion and fixed infrastructure constraints, thereby improving data collection efficiency and policy generalization for complex whole-body manipulation tasks.

## Problem
- Humanoid whole-body dexterous manipulation relies heavily on high-quality demonstrations, but existing teleoperation solutions are either not portable or severely affected by occlusion, making it difficult to efficiently collect data for complex tasks.
- Vision/VR solutions require the hands to remain within the field of view at all times, which causes tracking failures or jitter in real-world scenarios such as tool use, bimanual coordination, and long-horizon tasks.
- Human motion data is easier to collect, but the morphological differences between humans and humanoid robots are large, so training directly on human data leads to imprecise execution and manipulation failures.

## Approach
- Use **IMU-based** full-body tracking to replace camera-dependent approaches, capturing full-body motion with 15 lightweight trackers without line-of-sight occlusion, and combine it with pelvis-centric retargeting to reduce the impact of IMU global drift.
- Control the body and hands separately: the body uses an existing low-level motion tracking controller, while the hands use a lightweight MLP to directly regress the 3D positions of 5 fingertips into 20-DoF robotic hand joint angles, enabling constant-time dexterous hand retargeting without manual parameter tuning.
- First generate paired data through offline optimization to train the hand retargeting network, then directly predict hand joint angles during real-time teleoperation to obtain smoother and more natural hand motions.
- Propose a two-stage imitation learning framework: in the first stage, pre-train on diverse human demonstrations to learn general motion priors; in the second stage, fine-tune using only robot teleoperation data to adapt to the robot embodiment and bridge the embodiment gap.
- For robot proprioceptive states missing from the human data, use the previous action as an approximation, thus avoiding complex alignment between human and robot action spaces.

## Results
- On 4 shared tasks that both humans and robots can perform, the average time to collect 60 demonstration episodes dropped from **59.8 min** to **44.3 min**, an improvement of about **26%** over the vision baseline.
- On the shared tasks, teleoperation data collection success rate increased from the baseline **74.6%** to **91.7%**; the average success rate of policies trained on this data increased from **57.5%** to **80.0%**.
- On the highly occluded, highly dexterous **Scan&Pack** task, the vision baseline achieved **0/60** teleoperation successes, while HumDex reached **54/60**, or about **90%** success; the corresponding policy success rate was **20/30**, while the baseline was infeasible on this task.
- By task, policy success rates reached: **Hang Towel 19/30 vs 11/30**、**Open Door 22/30 vs 10/30**、**Place Basket 26/30 vs 22/30**、**Pick Bread 29/30 vs 26/30** (HumDex vs baseline).
- At the hardware level, the system supports **10+ hours** of continuous operation and **50+ meters** of connection range; its custom low-cost design can cost less than **$200**, each node weighs less than **20g**, and continuous battery life exceeds **20 hours**.
- The abstract also claims that the two-stage training significantly improves generalization to **new positions, new objects, and new backgrounds**, without needing to collect robot data under those settings; however, in the provided excerpt, no more complete quantitative generalization table is given beyond the tables above.

## Link
- [http://arxiv.org/abs/2603.12260v1](http://arxiv.org/abs/2603.12260v1)
