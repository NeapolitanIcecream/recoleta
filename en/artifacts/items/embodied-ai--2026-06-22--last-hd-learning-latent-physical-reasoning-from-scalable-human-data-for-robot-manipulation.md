---
source: arxiv
url: https://arxiv.org/abs/2606.23685v1
published_at: '2026-06-22T17:59:52'
authors:
- Jiaming Liu
- Yinxi Wang
- Chenyang Gu
- Siyuan Qian
- Xiangju Mi
- Hao Chen
- Jiawei Chen
- Qingpo Wuwu
- Xiaoqi Li
- Nuowei Han
- Yiming Zhang
- Xuheng Zhang
- Yang Yue
- Yeqing Yang
- Lei Wang
- Peng Jia
- Hao Tang
- Shanghang Zhang
topics:
- vision-language-action
- human-to-robot-transfer
- latent-world-models
- robot-manipulation
- dexterous-manipulation
- human-demonstrations
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# LaST-HD: Learning Latent Physical Reasoning from Scalable Human Data for Robot Manipulation

## Summary
LaST-HD trains a VLA robot policy to learn from human-hand demonstrations by aligning human and robot trajectories in a shared latent dynamics space. It pairs this with a low-cost motion-capture glove and a mixed human-robot training recipe for manipulation across grippers and dexterous hands.

## Problem
- Robot VLA policies need many real-robot demonstrations, but teleoperation is slow, hardware-bound, and costly.
- Human-hand demonstrations are easier to collect, but direct transfer fails when human hands and robot grippers or dexterous hands differ in shape, joints, and dynamics.
- The paper targets cross-embodiment manipulation learning where human data can improve robot generalization to new objects, positions, and scenes.

## Approach
- LaST-HD uses a Mixture-of-Transformers VLA model built on Janus-Pro, SigLIP-Large, and a 1.5B DeepSeek-LLM backbone, with one expert for latent reasoning and one expert for action generation.
- An action-conditioned world model is trained on unpaired human-hand and robot trajectories. Its forward-dynamics features become latent targets for the VLA reasoning expert.
- The policy learns robot actions with flow matching while its latent tokens are supervised by cosine similarity to the world-model targets.
- The OOL Glove records 21 hand-wrist keypoints and turns human motions into supervision for grippers and dexterous hands through fingertip-distance rules and inverse-kinematics retargeting.
- Training uses mixed human-robot co-training, then human-hand online correction at failure states while replaying older data to reduce forgetting.

## Results
- In-domain evaluation covers 6 real-world tasks across 3 embodiments. LaST-HD averages 0.73 success, compared with 0.62 for π0.5, 0.52 for Cosmos-Policy, and 0.63 for LaST0.
- On in-domain tasks, LaST-HD reaches 0.95 on Sort Fruits and 0.80 on Put Items to Bag and Zip. The mixed human-robot variant averages 0.68 using 50 robot demonstrations and 50 OOL Glove demonstrations per task.
- In generalization with extra human data only, LaST-HD reaches a 0.56 global average, compared with 0.46 for LaST0 with the same unseen human-data setting.
- By scenario, LaST-HD with unseen human data averages 0.41 on unseen positions, 0.58 on unseen objects, and 0.68 on unseen backgrounds across the 6 tasks.
- OOL Glove is reported as under 100 g per glove, over 200 Hz, under 10 ms latency, with sub-millimeter average RMS keypoint position error, and 4-5× faster data collection than robot teleoperation.
- Human-hand online correction is reported to push novel-environment accuracy above 90% using 20 minutes of OOL Glove data; in the shown Sort Fruits correction study, 20 trajectories reach 100% on unseen background and 60 trajectories reach 100% on unseen object.

## Link
- [https://arxiv.org/abs/2606.23685v1](https://arxiv.org/abs/2606.23685v1)
