---
source: arxiv
url: https://arxiv.org/abs/2607.05396v1
published_at: '2026-07-06T17:59:59'
authors:
- Wenhao Li
- Xueying Jiang
- Quanhao Qian
- Deli Zhao
- Shijian Lu
- Gongjie Zhang
- Ran Xu
topics:
- vision-language-action
- robot-manipulation
- viewpoint-generalization
- hand-eye-calibration
- monocular-rgb
- robot-foundation-models
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# From Fixed to Free Cameras: Calibration-Free View-Robust Vision-Language-Action Model

## Summary
CamVLA is a calibration-free VLA method that keeps robot manipulation usable when the camera moves or is remounted. It predicts actions in the camera frame, estimates the camera-to-robot pose from one RGB image, and converts the action into the robot base frame.

## Problem
- Standard VLAs predict robot base-frame actions from camera-view images, so a camera pose change can break the learned visual-to-action mapping.
- Prior viewpoint-tolerant VLA methods often require known camera extrinsics at deployment, which fails when cameras drift, are bumped, or are remounted.
- The paper reports that π0 on RLBench drops from about 65.3% success in the training view to 6.3% after a 15° camera rotation.

## Approach
- CamVLA has two heads: an action head predicts the end-effector delta action in the local camera frame, and a geometric head predicts a 6-DoF hand-eye matrix between the camera and robot base.
- The model uses a single monocular RGB image, robot state, and language instruction. It does not need depth, external camera calibration, or multi-view input at deployment.
- A deterministic transform rotates the predicted camera-frame translation and rotation deltas into base-frame robot actions.
- The method predicts translation in the hand-eye pose for geometric supervision, although relative action execution depends on the predicted rotation.

## Results
- On RLBench unseen viewpoints across 6 tasks, π0 improves from 33.2% to 51.4% mean success with CamVLA, an absolute gain of 18.2 points.
- On the same RLBench setup, GR00T N1.7 improves from 28.4% to 38.4% mean success with CamVLA, an absolute gain of 10.0 points.
- In real-world Franka experiments across 5 household tasks, π0 + CamVLA gets 79.0%, 68.0%, 55.3%, and 29.3% mean success at 0°, 5°, 10°, and 15° camera offsets, compared with π0 at 63.3%, 53.3%, 39.3%, and 16.0%.
- In the same real-world setup, GR00T N1.7 + CamVLA gets 80.7%, 72.3%, 53.0%, and 33.0% at 0°, 5°, 10°, and 15°, compared with GR00T at 64.7%, 52.0%, 35.7%, and 14.7%.
- Real-world hand-eye errors are 1.35 cm / 2.49° at 0°, 2.12 cm / 4.73° at 5°, 7.91 cm / 5.98° at 10°, and 27.16 cm / 9.39° at 15°.
- The geometric head adds 6.30M parameters, 1.0G FLOPs, and 1 ms latency on an RTX 4090: 3244.4M parameters, 661.9G FLOPs, and 62 ms inference versus π0 at 3238.1M, 660.9G, and 61 ms.

## Link
- [https://arxiv.org/abs/2607.05396v1](https://arxiv.org/abs/2607.05396v1)
