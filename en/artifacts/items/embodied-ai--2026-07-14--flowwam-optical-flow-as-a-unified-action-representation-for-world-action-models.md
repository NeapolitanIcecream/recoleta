---
source: arxiv
url: https://arxiv.org/abs/2607.13017v1
published_at: '2026-07-14T17:57:12'
authors:
- Yixiang Chen
- Peiyan Li
- Yuan Xu
- Qisen Ma
- Jiabing Yang
- Kai Wang
- Jianhua Yang
- Dong An
- He Guan
- Gaoteng Liu
- Jianlou Si
- Jun Huang
- Jing Liu
- Nianfeng Liu
- Yan Huang
- Liang Wang
topics:
- robot-foundation-model
- world-action-model
- optical-flow-actions
- action-conditioned-world-model
- robot-data-scaling
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# FlowWAM: Optical Flow as a Unified Action Representation for World Action Models

## Summary
FlowWAM uses optical flow as a video-native action representation for both robot policy learning and action-conditioned world modeling. It reports 92.94% success on RoboTwin 2.0 Clean, 92.14% on Random, and a 63.71 EWMScore on WorldArena.

## Problem
- World Action Models need an action representation that matches pretrained video generators while preserving the dense temporal motion needed for accurate robot control.
- Numerical actions are embodiment-specific, while prior visual action signals such as masks and ray maps provide limited temporal motion information.
- This matters because weak action representations can reduce both executable policy performance and the fidelity of action-conditioned future-video prediction.

## Approach
- Encode per-pixel optical flow as HSV RGB-like flow videos, preserving motion direction and magnitude in a format compatible with video-generation models.
- Use a dual-stream diffusion transformer with shared VAE and transformer components to jointly model RGB and flow videos.
- In policy mode, generate future flow and decode the model's RGB-flow features into low-level robot action chunks with an action expert.
- In world-model mode, provide a target flow sequence and generate RGB futures that follow the specified motion.
- Pretrain the video generator on action-unlabeled videos using extracted optical flow, then fine-tune the action expert on labeled robot demonstrations; motion-aware reweighting emphasizes moving regions.

## Results
- On RoboTwin 2.0's 50 bimanual tasks, evaluated with 100 rollouts per task, FlowWAM achieves 92.94% success in Clean and 92.14% in Random, compared with 91.88% and 91.78% for the reported Fast-WAM baseline.
- Action-unlabeled EgoDex pretraining improves FlowWAM from 82.40% to 92.94% on Clean and from 80.80% to 92.14% on Random.
- On WorldArena's 121-frame, 24 fps rollouts, FlowWAM obtains the best reported EWMScore of 63.71, with Trajectory Accuracy of 64.26; the table reports 54.27 Trajectory Accuracy and 62.34 EWMScore for GigaWorld-1.
- The abstract reports an 18.4% relative improvement in trajectory accuracy on WorldArena and states that FlowWAM outperforms both VLA and WAM baselines.
- The excerpt does not provide complete ablations, real-robot results, or the full statistical treatment, so the reported gains primarily establish benchmark performance rather than robustness across all deployment conditions.

## Link
- [https://arxiv.org/abs/2607.13017v1](https://arxiv.org/abs/2607.13017v1)
