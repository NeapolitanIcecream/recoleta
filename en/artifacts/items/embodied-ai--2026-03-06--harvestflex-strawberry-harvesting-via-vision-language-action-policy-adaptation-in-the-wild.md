---
source: arxiv
url: http://arxiv.org/abs/2603.05982v1
published_at: '2026-03-06T07:26:45'
authors:
- Ziyang Zhao
- Shuheng Wang
- Zhonghua Miao
- Ya Xiong
topics:
- vision-language-action
- robot-harvesting
- sim2real
- policy-adaptation
- multiview-rgb
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# HarvestFlex: Strawberry Harvesting via Vision-Language-Action Policy Adaptation in the Wild

## Summary
This paper studies how to transfer open-source vision-language-action (VLA) policies to real greenhouse strawberry harvesting and achieve end-to-end closed-loop picking with very little real-world data. The core conclusion is: multi-view RGB input plus less than 4 hours of demonstration fine-tuning is already enough for VLA to achieve usable performance in real agricultural scenarios with heavy occlusion and contact-sensitive objects.

## Problem
- The paper addresses **real greenhouse strawberry harvesting**, a long-horizon, unstructured, and damage-sensitive robotic task; it matters because strawberry harvesting still relies heavily on manual labor, with high and unstable labor costs.
- Existing traditional modular approaches usually depend on detection, segmentation, depth, calibration, planning, and hand-engineered state machines, and they tend to accumulate errors when facing **occlusion, reflections, lighting changes, and state changes caused by contact**, with poor transfer across farms.
- The authors aim to answer three practical questions: whether open-source VLA can be used for fruit picking; what the trade-offs are among different models/fine-tuning strategies in success rate, speed, and damage rate; and whether asynchronous inference is better than synchronous deployment.

## Approach
- They built an end-to-end closed-loop system: inputs are **three RGB views** (left and right fixed cameras + wrist camera), robot state, and language instruction; output is an **8-dimensional action** (7D arm velocity control + 1 suction/release/idle pump command).
- They deliberately **do not use depth, point clouds, or explicit geometric calibration**, allowing VLA to go directly from vision and language to action and reducing task-specific engineering dependencies.
- They collected **3.71 hours of VR teleoperated demonstrations**, totaling **227 episodes and 491 valid picking attempts**, while retaining failure-recovery segments to better match the distribution of closed-loop deployment.
- Under a unified data and training budget, they fine-tuned three open-source VLAs: **pi0, pi0.5, wall-oss**, comparing **full fine-tuning** and **LoRA** as two adaptation methods.
- For deployment, they propose **asynchronous inference-control decoupling**: an inference thread generates chunks of action queues, while a 30 Hz real-time control thread executes continuously, reducing jitter and missed contact windows caused by inference latency.

## Results
- The paper claims this is the **first systematic study transferring VLA to real greenhouse tabletop strawberry harvesting**, and it compares multiple models and adaptation strategies under a **unified 50-trial real-greenhouse evaluation protocol**.
- The best result comes from **pi0.5 + full fine-tuning + 6 epochs**: **success rate SR = 74.0%**, **successful score SS = 82.6**, **cycle time = 32.6 s/pick**, **damage rate DR = 4.1%**.
- Also at 6 epochs, **LoRA pi0.5** reaches **SR = 64.0%**, **SS = 73.6**, **38.3 s/pick**, **DR = 3.8%**; this indicates LoRA is more parameter-efficient, but task completion is clearly lower than full fine-tuning.
- For the other models at 6 epochs with full fine-tuning: **pi0** achieves **SR 60.0% / 38.4 s / DR 4.2%**, and **wall-oss** achieves **SR 68.0% / 46.3 s / DR 3.9%**; overall, **pi0.5 performs best**.
- As training increases from **2 to 6 epochs**, **SR generally rises and cycle time decreases** for all models. For example, fully fine-tuned **pi0.5** improves from **30.0% SR / 44.2 s** to **74.0% SR / 32.6 s**.
- In terms of data and system scale, only **3.71 hours of real data** and **227 episodes** were enough to achieve “non-trivial” closed-loop harvesting. The paper also claims that **asynchronous deployment outperforms synchronous deployment**, but the provided excerpt does not include the specific comparison numbers.

## Link
- [http://arxiv.org/abs/2603.05982v1](http://arxiv.org/abs/2603.05982v1)
