---
source: arxiv
url: https://arxiv.org/abs/2606.24742v1
published_at: '2026-06-23T16:07:48'
authors:
- Zhihao Wang
- Jianxiong Li
- Yu Cui
- Yuan Gao
- Xianyuan Zhan
- Junzhi Yu
- Xiao Ma
topics:
- world-models
- robot-value-models
- robot-manipulation
- suboptimal-data
- policy-learning
- video-diffusion
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# World Value Models for Robotic Manipulation

## Summary
WVM uses a pretrained video world model to predict robot task progress from video and language. The paper claims better value estimates on expert and suboptimal manipulation data, then uses those estimates to improve policy learning from noisy demonstrations.

## Problem
- Robot value models need to judge task progress in videos with pauses, failed attempts, and retries, because policy learning often uses mixed-quality robot data.
- Many current value models use VLM backbones trained on static or sparse visual inputs, so they miss temporal cues needed for progress, hesitation, and regression.
- Existing VOC evaluation mostly checks expert trajectories, so it does not test whether a model can detect suboptimal segments.

## Approach
- WVM starts from Wan2.2-TI2V-5B, a pretrained video world model, and adds a lighter value DiT stream that predicts a chunk of per-frame values.
- The value stream attends to video latents through asymmetric Mixture-of-Transformers attention: value tokens read video features, while video tokens do not read value tokens.
- It predicts a distribution over value chunks with flow matching, instead of regressing one scalar value per frame.
- Training includes video co-training, prefix randomization to reduce shortcut use, and video rewinding to create rising, flat, and descending progress patterns.
- The paper also introduces Suboptimal-Value-Bench, with 800 human-annotated trajectories across 3 embodiments and 15 tasks, focused on hesitation and retry behavior.

## Results
- On Suboptimal-Value-Bench hesitation segments, WVM gets 0.05 average Hesitation-RMSE, better than GVL and Robometer at 0.14, RoboReward at 0.21, TopReward at 0.31, Robo-Dopamine at 0.49, and VLAC at 0.51.
- On retry segments, WVM gets 0.78 average Retry-VOC, compared with GVL at 0.62, TopReward at 0.00, Robometer at -0.16, and VLAC at -0.37.
- On expert demonstrations, WVM gets 0.95 average VOC, compared with RoboReward at 0.88, Robo-Dopamine at 0.82, Robometer at 0.81, GVL at 0.78, VLAC at 0.59, and TopReward at 0.42.
- Dataset-level expert VOC results include OXE 0.94, RoboCOIN 0.95, EgoDex 0.92, and self-collected data 0.99 for WVM.
- Ablations show the full WVM beats variants on suboptimal data: removing video co-training changes Hesitation-RMSE from 0.05 to 0.08 and Retry-VOC from 0.78 to 0.68; freezing the video stream gives 0.12 RMSE and 0.45 Retry-VOC.
- For downstream policy learning, WVM-guided AWR and filtered BC beat vanilla BC across 3 RoboSuite tasks and 3 real AgileX tasks, using only 10 suboptimal trajectories per simulated task and 50 per real task; the excerpt does not give exact success-rate values.

## Link
- [https://arxiv.org/abs/2606.24742v1](https://arxiv.org/abs/2606.24742v1)
