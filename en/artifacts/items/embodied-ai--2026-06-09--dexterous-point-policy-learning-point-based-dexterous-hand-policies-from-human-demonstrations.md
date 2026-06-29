---
source: arxiv
url: https://arxiv.org/abs/2606.10614v1
published_at: '2026-06-09T09:13:36'
authors:
- Beomjun Kim
- Seong Hyeon Park
- Seunghoon Sim
- Seungjun Moon
- Sanghyeok Lee
- Jinwoo Shin
topics:
- dexterous-manipulation
- human-video-learning
- keypoint-policy
- robot-data-scaling
- vision-language-action
- robot-foundation-models
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Dexterous Point Policy: Learning Point-based Dexterous Hand Policies from Human Demonstrations

## Summary
Dexterous Point Policy trains a dexterous robot hand policy from human videos only, with no robot demonstrations. It uses shared 3D keypoints for human hands, robot hands, and task objects, then adds fingertip contact prediction for grasp force.

## Problem
- Robot policies trained on human videos often fail on real robots because pixels, joints, and hand morphology do not transfer cleanly across embodiments.
- Robot demonstrations are costly, and dexterous hand teleoperation is worse because multi-finger control has high action dimensionality.
- The paper targets zero-robot-data dexterous manipulation, which matters for scaling robot data beyond slow teleoperation.

## Approach
- The method represents both human and robot hands with six 3D keypoints: wrist plus five fingertips.
- It extracts task object points from video using a VLM for object names, SAM3 for masks, and depth estimation or stereo depth for 3D points.
- It trains an autoregressive transformer to predict future hand keypoints from language, object points, current hand keypoints, and camera pose.
- It pretrains on about 1M egocentric human-video episodes from VITRA, which aggregates Ego4D, Ego-Exo4D, Something-Something v2, and EPIC-KITCHENS.
- During task fine-tuning, it uses human videos with fingertip contact labels. At deployment, inverse kinematics maps predicted keypoints to robot joints, and predicted contact flags add small closing offsets for fingertip force.

## Results
- On 8 real-robot dexterous tasks, DPP reports 75.0% average success, compared with 3.7% for Point Policy and 1.0% for VITRA.
- On Pick and Place, DPP reports 81.7% average success: bottle 95.8%, box 75.0%, ball 70.8%, towel 87.5%, and teddy bear 79.2%.
- On Manipulation and Tool Use, DPP reports 63.9% average success: open 87.5%, brush 62.5%, and spray 41.7%.
- Contact prediction accounts for a +71.3 percentage point gain over a point-only baseline, according to the paper.
- Internet-scale human-video pretraining improves Pick and Place success from 67.5% to 81.7%, a +14.2 point gain.
- Generalization stays close to the training-object setting: 80.0% success in multi-object scenes and 76.7% on novel objects, versus 81.7% on standard Pick and Place.

## Link
- [https://arxiv.org/abs/2606.10614v1](https://arxiv.org/abs/2606.10614v1)
