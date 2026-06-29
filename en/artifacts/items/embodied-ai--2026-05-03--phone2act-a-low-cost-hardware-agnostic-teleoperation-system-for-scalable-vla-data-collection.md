---
source: arxiv
url: https://arxiv.org/abs/2605.01948v1
published_at: '2026-05-03T16:17:16'
authors:
- Om Mandhane
- Bipin Yadav
- Sangeetha Prasanna Ram
- Gopalakrishnan Narayanan
topics:
- vision-language-action
- robot-data-collection
- teleoperation
- lerobot
- generalist-robot-policy
- robot-data-scaling
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Phone2Act: A Low-Cost, Hardware-Agnostic Teleoperation System for Scalable VLA Data Collection

## Summary
Phone2Act turns an Android phone into a 6-DoF robot teleoperator and records synchronized demonstrations directly in LeRobot format. The paper targets VLA training data collection, where cost and robot-specific tooling limit dataset growth.

## Problem
- VLA robot policies need real manipulation demonstrations, but physical data collection costs more than web-scale data collection.
- Leader-follower arms, VR controllers, and platform-specific teleoperation stacks add hardware cost and engineering work.
- Labs using different robot arms need a common way to collect training-ready demonstrations without rewriting the control and logging stack for each robot.

## Approach
- The Android app uses Google ARCore to publish phone pose and button events at 50 Hz over WebSocket to ROS 2.
- A ROS 2 planner maps phone motion into robot Cartesian target poses, with clutching for repositioning, workspace limits, a zero-jump filter, and RPY delta handling.
- Robot-specific bridge nodes convert the shared target pose and gripper topics into each robot’s API calls; the paper describes a Dobot CR5 bridge and a dual-arm SO-101 setup.
- The Universal Recorder synchronizes RGB camera frames, joint states, end-effector poses, and gripper state at 20 Hz, then writes MP4 and Parquet files in the LeRobot dataset format.

## Results
- Fine-tuning GR00T-N1.5-3B on 130 Phone2Act episodes produced a 90% real-world success rate: 9 successes in 10 trials on a Dobot CR5 ball-to-basket task.
- The system collected demonstrations at 2–3 episodes per minute for the reported task.
- End-to-end phone-motion-to-robot-actuation latency was 350–440 ms, with a 395 ms average, measured by 240 FPS high-speed video under 2.4 GHz Wi-Fi.
- The recorder runs at 20 Hz, while phone pose input runs at 50 Hz.
- GR00T fine-tuning used one NVIDIA RTX A6000, effective batch size 48, peak learning rate 1e-4, bfloat16, 10-step action chunks, and a 7D action space.
- Training loss plateaued near 0.05 MSE by 2,000 steps; the paper also reports qualitative open-loop tracking on held-out trajectories.

## Link
- [https://arxiv.org/abs/2605.01948v1](https://arxiv.org/abs/2605.01948v1)
