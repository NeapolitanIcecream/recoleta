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
- humanoid-robotics
- dexterous-manipulation
- teleoperation
- imitation-learning
- motion-retargeting
relevance_score: 0.22
run_id: materialize-outputs
language_code: en
---

# HumDex:Humanoid Dexterous Manipulation Made Easy

## Summary
HumDex proposes a portable teleoperation system for humanoid whole-body dexterous manipulation, and combines pretraining on human data with finetuning on robot data to reduce demonstration cost and improve generalization. The paper focuses on making high-quality humanoid dexterous manipulation data collection easier and more stable, and on using these data more effectively for policy learning.

## Problem
- Humanoid whole-body dexterous manipulation depends on high-quality demonstration data, but existing teleoperation systems often struggle to balance **portability, precision, and robustness to occlusion**.
- Vision/VR solutions are prone to failure due to hand or tool occlusion, while optical motion capture/exoskeleton solutions rely on fixed infrastructure, limiting data collection in real-world environments.
- Relying only on robot teleoperation data is costly; although human demonstrations are easier to collect, there is an **embodiment gap** between humans and robots, making them difficult to use directly for precise manipulation learning.

## Approach
- Use **IMU-based** full-body tracking instead of purely vision-based tracking: 15 lightweight trackers capture whole-body motion, combined with pelvis-centric retargeting and an off-the-shelf low-level controller to achieve portable and high-precision humanoid whole-body teleoperation.
- For the 20-DoF dexterous hand, instead of solving frame-by-frame optimization, train a **lightweight MLP** that directly maps the 3D positions of 5 fingertips to the robot's 20-dimensional hand joint angles, producing smoother and more natural hand motions without manual parameter tuning.
- Use the system to collect both robot teleoperation data and human motion data efficiently.
- Propose a **two-stage imitation learning** approach: in the first stage, pretrain on human demonstrations to learn general motion priors; in the second stage, finetune using only robot data to adapt the policy to the robot body, thereby improving generalization with limited robot data.
- For missing human “proprioceptive states,” approximate them with the previous action, avoiding complex alignment between human and robot action spaces.

## Results
- In a data collection comparison, on 4 commonly executable tasks, HumDex reduced the average time required to collect 60 demonstrations from **59.8 min to 44.3 min**, an improvement of about **26%**; the baseline was a vision-based teleoperation system.
- On the same 4 tasks, teleoperation data collection success rate improved from the baseline **74.6%** to **91.7%**.
- Policies trained on the collected data improved average success rate on the same 4 tasks from **57.5%** to **80.0%**.
- On the highly occluded, high-dexterity **Scan&Pack** task, the baseline could not complete data collection due to occlusion issues (**0/60**), while HumDex achieved **54/60** successful data collection; the corresponding policy success rate was **20/30**, versus **0/30** for the baseline.
- Single-task examples: Hang Towel policy success rate improved from **11/30** to **19/30**; Open Door from **10/30** to **22/30**; Place Basket from **22/30** to **26/30**; Pick Bread from **26/30** to **29/30**.
- The paper also claims that the two-stage “human pretraining → robot finetuning” improves generalization to **new positions, new objects, and new backgrounds**, but aside from qualitative descriptions, the provided excerpt does not include more detailed quantitative table values for this part.

## Link
- [http://arxiv.org/abs/2603.12260v1](http://arxiv.org/abs/2603.12260v1)
