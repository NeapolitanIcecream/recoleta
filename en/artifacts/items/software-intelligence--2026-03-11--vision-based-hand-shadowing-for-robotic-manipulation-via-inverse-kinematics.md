---
source: arxiv
url: http://arxiv.org/abs/2603.11383v1
published_at: '2026-03-11T23:53:28'
authors:
- Hendrik Chiche
- Antoine Jamme
- Trevor Rigoberto Martinez
topics:
- robot-teleoperation
- inverse-kinematics
- hand-tracking
- rgb-d-vision
- vision-language-action
relevance_score: 0.17
run_id: materialize-outputs
language_code: en
---

# Vision-Based Hand Shadowing for Robotic Manipulation via Inverse Kinematics

## Summary
This paper proposes a hand shadowing system based on a monocular egocentric RGB-D camera and analytical inverse kinematics, offline-mapping human hand motions to a low-cost SO-ARM101 robotic arm. It attempts to replace expensive teleoperation equipment with a zero-training, low-hardware-cost approach, and compares it with multiple VLA policies.

## Problem
- Reliably mapping natural human hand joint motions to joint commands for a low-cost robotic arm is not easy; traditional teleoperation often relies on exoskeletons, VR headsets, or master-slave robotic arms, which are expensive and complex.
- Pure imitation learning is feasible, but requires demonstration data, GPU training, and task-specific tuning, making deployment more demanding.
- In real-world settings, occlusion of the hand or target objects can break visual tracking, directly affecting grasp control and generalization, so this is an important problem for low-cost robotic manipulation.

## Approach
- An Intel RealSense D400 mounted on 3D-printed glasses is used to capture egocentric RGB-D video; MediaPipe Hands detects 21 2D keypoints per hand, which are then back-projected into 3D using the depth map.
- The 3D hand points are mapped into the SO-ARM101 base coordinate frame through a camera-to-robot coordinate transform, and an end-effector pose target is constructed from the geometric relationship among the thumb, index finger, and wrist.
- In PyBullet, damped least-squares inverse kinematics is used to solve for the 5-DOF arm joint angles, and EMA smoothing is applied to the joint solutions to reduce jitter.
- The gripper opening and closing is controlled using the geometric angle between the thumb and index finger, with a four-level fallback mechanism: fingertips, proximal joints, previous valid value, and a default half-open value, to mitigate missing depth and occlusion.
- Trajectories are first previewed in PyBullet, then replayed on the real robotic arm through LeRobot; the same pipeline can also export demonstration data for subsequent imitation learning training.

## Results
- On a structured pick-and-place benchmark (5 tiles, 10 trials each, 50 total), the IK retargeting pipeline achieves a **90% (45/50)** success rate, with **no training data required**.
- In the per-tile results, **tile #1/#2 achieve 10/10 and 10/10** because they are farther from the robot and permit more natural hand poses; **tile #5 drops to 7/10** because it is closer to the base and more prone to self-occlusion.
- Compared with 4 VLA policies: **ACT 92%** (50k steps, about 10 Hz) is slightly higher than the IK method in this paper; **SmolVLA 50%** (20k steps); **pi_0.5 40%** (3k steps); **GR00T N1.5 35%** (3k steps).
- In terms of latency, MediaPipe takes about **23 ms**, visualization overlay **110 ms**, and PyBullet IK about **80 ms**, for a total of **213 ms/frame** and an effective throughput of about **~5 FPS**. Therefore, the system is **not real-time 30 FPS**, but instead records first and processes offline.
- The authors claim the main advantages are **zero training, task agnostic, and low-cost hardware**; the main failure mode is **hand self-occlusion / environmental occlusion**, which prevents reliable estimation of keypoints or gripper angle.
- In unstructured real-world environments (grocery store, pharmacy), the IK method's success rate drops to **9.3% (N=75)** due to occlusion from surrounding objects, showing that the method still has clear limitations in occluded scenarios.

## Link
- [http://arxiv.org/abs/2603.11383v1](http://arxiv.org/abs/2603.11383v1)
