---
source: arxiv
url: https://arxiv.org/abs/2605.09613v1
published_at: '2026-05-10T15:51:01'
authors:
- Narsimha Menga
- Parikshit Sakurikar
- Amirreza Rouhi
- Satya Sai Reddy
- Anirudh Govil
- Sri Harsha Chittajallu
- Rajat Aggarwal
- Anoop Namboodiri
- Sashi Reddi
topics:
- vision-language-action
- robot-data-scaling
- human-video-retargeting
- retail-robotics
- dexterous-manipulation
- humanoid-robotics
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# SABER: A Scalable Action-Based Embodied Dataset for Real-World VLA Adaptation

## Summary
SABER is a retail robotics dataset built from real in-store human video and used to adapt VLA policies to grocery-store manipulation. The paper claims that domain-specific action data raises GR00T N1.6 performance on RoboBenchMart retail tasks from 13.4% to 29.3% mean success.

## Problem
- General robot VLA models have weak coverage of retail tasks such as shelf picking, fridge opening, basket loading, floor retrieval, and handling varied packaging.
- Collecting robot teleoperation data inside active stores is expensive, disruptive, and hard to scale.
- The gap matters because a policy trained on broad robot data can fail when the store layout, objects, lighting, occlusion, and action sequence differ from its pretraining data.

## Approach
- SABER records about 100 hours of natural activity in real grocery stores using a head-mounted GoPro and a fixed DreamVu ALIA 360° camera.
- The dataset turns the video into three action streams: 25K LAPA latent-action episodes from egocentric video, 18.6K dexterous hand-pose episodes retargeted to robot joint space, and 1.2K whole-body motion episodes retargeted to a Unitree G1 humanoid.
- Human annotators review and correct hand and body pose estimates, then retargeting converts human motion into robot-compatible action targets.
- The authors post-train GR00T N1.6 with a shared-backbone multi-task recipe over the three SABER streams, plus a small amount of robot-native anchor data and task-aligned seed data.

## Results
- SABER contains 44.8K training samples from about 100 hours of real in-store capture.
- Dataset composition: 25K latent-action sequences, 18.6K hand-pose trajectories, and 1.2K whole-body synchronized motion sequences.
- SABER-MM post-training reaches 29.3% mean success across 10 RoboBenchMart retail manipulation tasks.
- The comparison baseline is simulation-only fine-tuning at 13.4% mean success on the same task set.
- The claimed gain is more than 2.19x over the fine-tuning baseline.
- A 10K-sample SABER subset is released publicly under CC BY-NC 4.0.

## Link
- [https://arxiv.org/abs/2605.09613v1](https://arxiv.org/abs/2605.09613v1)
