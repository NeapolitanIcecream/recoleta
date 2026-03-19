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
- wearable-robotics
- imitation-learning
- data-glove
relevance_score: 0.53
run_id: materialize-outputs
language_code: en
---

# CDF-Glove: A Cable-Driven Force Feedback Glove for Dexterous Teleoperation

## Summary
This paper proposes CDF-Glove, a low-cost, lightweight, high-DoF data glove with force feedback for dexterous teleoperation and demonstration data collection. It aims to address the limitations of existing solutions, which often lack haptic feedback, are expensive, bulky, and unfavorable for collecting high-quality imitation learning data.

## Problem
- Imitation learning for dexterous manipulation relies heavily on high-quality teleoperated demonstration data, but existing data gloves often lack tactile/force feedback, making it difficult for operators to perceive contact in time and finely adjust finger posture.
- Existing high-DoF haptic gloves typically involve clear trade-offs among **cost, size, wearability, sensing dimensionality, and feedback capability**, making long-term stable data collection difficult.
- For complex dexterous manipulation, if hand joint measurements are inaccurate, latency is high, or closed-loop feedback is absent, teleoperation success rates are directly reduced, and the effectiveness of subsequent IL policy training is weakened.

## Approach
- Designed a **cable-driven** wearable force-feedback glove: it directly measures 16 finger DoFs and infers 4 additional DoFs based on kinematic coupling relationships, for a total of 20 finger DoF states.
- Uses a bimodal haptic mechanism: **LRA vibration feedback** for smaller contact force cues, and **servo cable force feedback** for resistance under larger contact forces; the threshold policy is `<0.1N` no feedback, `0.1~0.5N`/`0.5~1N` vibration feedback, and `>1N` force feedback.
- Built a **finger kinematic model** mapping encoder displacement to MCP/PIP/DIP joint angles, where 4 PIP angles are inferred from DIP angles and joint constraint relationships.
- Built a **force-feedback cable following model** that computes cable length changes in real time based on finger posture, allowing the servo to automatically release or retract cable during finger flexion/extension, so as to preserve natural operation and approximately constant tension.
- Validated the system on multiple dexterous hand platforms with different DoFs, and further collected a bimanual teleoperation dataset to train Diffusion Policy baselines for evaluating demonstration data quality.

## Results
- Hardware cost is about **US$230.51**, significantly lower than the **US$600** reported for **DOGlove** and **GEX Series** in the paper; total system weight is **0.49 kg**, with a sampling frequency of about **100 Hz**.
- The glove provides **16 directly measured DoFs + 4 coupled inferred DoFs**; in the index-finger DIP repeatability experiment, the mean contact angle was **63.15°** with a standard deviation of **0.29°**. The paper states that distal-joint repositioning accuracy/repeatability is better than **0.4°**.
- The latency of force feedback to the hand is about **200 ms**; the authors state that this latency mainly comes from **RS485 serial communication** and the mechanical response of the cable servo, but that it is sufficient for the quasi-static tasks in their dataset.
- In the water-bottle grasping experiment, under **blindfolded + sound-isolated** conditions, adding haptic feedback increased the success rate from **10% (1/10)** to **50% (5/10)**, a **4×** improvement; average completion time dropped from **18.30 s** to **8.52 s**.
- Under **non-blindfolded and non-sound-isolated** conditions, haptic feedback increased the success rate from **70% (7/10)** to **90% (9/10)**, and average completion time dropped from **3.11 s** to **2.51 s**.
- Diffusion Policy trained on their bimanual teleoperation data, compared with kinesthetic teaching, improved average success rate by **55%** and reduced average completion time by about **15.2 s**, a relative reduction of **47.2%**. The authors present this as the core evidence for improved demonstration data quality.

## Link
- [http://arxiv.org/abs/2603.05804v1](http://arxiv.org/abs/2603.05804v1)
