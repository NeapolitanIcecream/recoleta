---
source: arxiv
url: https://arxiv.org/abs/2605.18722v1
published_at: '2026-05-18T17:50:32'
authors:
- Zongzheng Zhang
- Jingrui Pang
- Zhuo Yang
- Kun Li
- Minwen Liao
- Saining Zhang
- Guoxuan Chi
- Jinbang Guo
- Huan-ang Gao
- Modi Shi
- Dongyun Ge
- Yao Mu
- Jiayuan Gu
- Rui Chen
- Hao Dong
- Huazhe Xu
- Li Yi
- Yixin Zhu
- Hang Zhao
- Pengwei Wang
- Shanghang Zhang
- Guocai Yao
- Jianyu Chen
- Hongyang Li
- Hao Zhao
topics:
- vision-language-action
- dexterous-manipulation
- bimanual-robotics
- robot-data-scaling
- diffusion-policy
- sim2real
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# Dexora: Open-source VLA for High-DoF Bimanual Dexterity

## Summary
Dexora is an open-source vision-language-action system for dual-arm, dual-hand high-DoF robot manipulation. It combines a 36-DoF robot, matched simulation, large real and synthetic datasets, and quality-weighted diffusion policy training.

## Problem
- Existing VLA systems mainly target dual-arm grippers or single-arm dexterous hands, so they miss tasks that need two arms and articulated fingers.
- The gap matters for tasks such as bottle-cap twisting, pen use, cutting food, fetching books from tight shelves, and bimanual object separation.
- Real teleoperation data for high-DoF hands is noisy because of operator variation, tracking errors, occlusion, and latency.

## Approach
- The hardware uses two 6-DoF AIRBOT arms and two 12-DoF XHAND dexterous hands, giving 36 DoF in total.
- Teleoperation splits the control problem: a custom exoskeleton backpack records arm motion, while Apple Vision Pro hand tracking records finger motion.
- The same teleoperation interface drives the real robot and a MuJoCo digital twin, with four RGB views and full joint states logged at 20 Hz.
- The training corpus combines 100K simulated trajectories with 6.5M frames and 10K real teleoperated episodes with 2.92M frames.
- The policy is a diffusion transformer conditioned on language, multi-view images, and joint state; an offline discriminator scores clip quality and weights the diffusion loss so low-quality demonstrations count less during training.

## Results
- On 12 basic real-world tasks, Dexora reports an 89.6% average success rate, compared with 82.1% for GR00T N1, 50.4% for π0, and 34.2% for Diffusion Policy.
- Dexora reaches at least 90% success on 7 of 12 basic tasks and scores 100% on apple-to-plate, bowl-to-bowl, and cabinet-door opening.
- On 6 dexterous tasks, Dexora reports 66.7% average success, compared with 51.7% for GR00T N1, 26.7% for π0, and 6.7% for Diffusion Policy.
- Dexterous task gains include 65% on Use pen, 80% on Fetch book, 80% on Rough dough, and 25% on Twist cap; all baselines score 0% on Twist cap.
- The paper claims cross-embodiment transfer to single-arm grippers, dual-arm grippers, and single-arm low-DoF hands without changing the model architecture, but the excerpt does not provide detailed success-rate tables for those transfer tests.

## Link
- [https://arxiv.org/abs/2605.18722v1](https://arxiv.org/abs/2605.18722v1)
