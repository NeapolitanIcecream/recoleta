---
source: arxiv
url: http://arxiv.org/abs/2603.05804v1
published_at: '2026-03-06T01:31:23'
authors:
- Huayue Liang
- Ruochong Li
- Yaodong Yang
- Long Zeng
- Yuanpei Chen
- Xueqian Wang
topics:
- dexterous-teleoperation
- haptic-feedback
- force-feedback-glove
- imitation-learning
- diffusion-policy
relevance_score: 0.83
run_id: materialize-outputs
language_code: en
---

# CDF-Glove: A Cable-Driven Force Feedback Glove for Dexterous Teleoperation

## Summary
This paper presents CDF-Glove, a low-cost, lightweight, cable-driven force-feedback glove for dexterous teleoperation, aimed at improving demonstration data quality and supporting imitation learning. Its core value lies in combining high-dimensional hand tracking with tactile/force feedback while keeping the cost down to about US$230 and releasing the design as open source.

## Problem
- Imitation learning in dexterous manipulation relies heavily on high-quality teleoperation demonstrations, but existing gloves often lack tactile feedback, making it difficult for operators to correct finger posture in real time based on contact state.
- Existing high-DoF tactile gloves usually make trade-offs among **high price, large size, weak feedback, and poor wearability**, which is unfavorable for long-duration data collection.
- If demonstration quality is low, the success rate and efficiency of trained policies are both limited, so better teleoperation interfaces are important for dexterous manipulation data collection.

## Approach
- Designed a **cable-driven force-feedback glove**: components are integrated on the back of the hand, and the fingers use steel cables/PTFE sheaths for transmission, balancing light weight, safety, and ease of replication.
- The glove provides **20 hand DoF states**: **16 measured directly** and **4 inferred through kinematic coupling**; it also combines with HTC Vive for 6D wrist tracking.
- Proposed a kinematic model from **encoder displacement to finger joint angles**: directly measures MCP/DIP, uses the DIP-PIP coupling relationship to infer PIP, and then maps to different dexterous hands.
- Proposed a force-feedback tracking model: computes cable length changes in real time from finger joint angles, and servo motors reel cables in/out to maintain tension; it also introduces a bimodal feedback strategy, using LRA vibration in the low-force range and cable-driven resistive force feedback in the high-force range.
- Used this system to collect bimanual teleoperation datasets and trained **Diffusion Policy** baselines, comparing them with policies trained on kinesthetic teaching data.

## Results
- Hardware metrics: glove weight **0.49 kg**, maximum sampling frequency about **100 Hz**, capable of measuring **16 DoF** with **4 DoF** inferred through coupling, and force-feedback latency to the hand of about **200 ms**.
- Accuracy metrics: in the index finger DIP repeatability experiment, the mean contact angle was **63.15°** with a standard deviation of **0.29°**; the authors claim distal-joint repeatability of **< 0.4° / about 0.4°**, and other MCP/PIP tests also remained **below 0.4°**.
- Cost metrics: total cost is about **$230.51**, lower than the **DOGlove $600** and **GEX Series $600** cited in the paper.
- Force-feedback effectiveness: in the water-bottle grasping experiment, under blindfolded + noise-reduction conditions, the success rate improved from **1/10 (10%)** to **5/10 (50%)**, a **4×** improvement, and average completion time dropped from **18.30 s** to **8.52 s**; under conditions without sensory occlusion, success rate improved from **7/10 (70%)** to **9/10 (90%)**, and completion time decreased from **3.11 s** to **2.51 s**.
- Imitation learning results: compared with kinesthetic teaching, policies trained on CDF-Glove teleoperation demonstrations achieved an **average success rate improvement of 55%**, and reduced average completion time by about **15.2 s**, i.e. a **47.2% relative reduction**.
- Generalization claim: the authors state that their kinematics and control stack have been validated on multiple dexterous hands with different kinematics/DoF, and that the code and hardware designs are open sourced; however, the excerpt does not provide more detailed cross-platform quantitative tables.

## Link
- [http://arxiv.org/abs/2603.05804v1](http://arxiv.org/abs/2603.05804v1)
