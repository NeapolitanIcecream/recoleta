---
source: arxiv
url: http://arxiv.org/abs/2603.11383v1
published_at: '2026-03-11T23:53:28'
authors:
- Hendrik Chiche
- Antoine Jamme
- Trevor Rigoberto Martinez
topics:
- inverse-kinematics
- hand-tracking
- robot-teleoperation
- vision-based-manipulation
- sim-to-real
relevance_score: 0.69
run_id: materialize-outputs
language_code: en
---

# Vision-Based Hand Shadowing for Robotic Manipulation via Inverse Kinematics

## Summary
This paper proposes an offline hand-shadowing pipeline from a single egocentric RGB-D camera to robot control, using analytical inverse kinematics to convert human hand motions into joint commands for the low-cost SO-ARM101 robotic arm. It aims to replace expensive teleoperation hardware or data-driven policy training with a zero-training approach, and compares the method with multiple VLA policies.

## Problem
- Target problem: how to map natural human hand motions to robot joint control at low cost for teleoperation, trajectory replay, and demonstration data collection.
- Importance: traditional teleoperation often depends on expensive equipment such as VR, exoskeletons, or master-slave manipulators; imitation learning/VLA methods also require demonstration data, GPU training, and task adaptation costs.
- The main challenges are hand keypoint detection, depth recovery, coordinate transformation, gripper aperture mapping, and hand-geometry distortion caused by occlusion under a monocular egocentric viewpoint.

## Approach
- Use an Intel RealSense D400 mounted on 3D-printed glasses to capture egocentric RGB-D video at **640×480, 30 FPS**, and use MediaPipe Hands on CPU to detect **21 keypoints** per hand.
- Back-project 2D keypoints into 3D through the depth map, then map camera coordinates into the robot coordinate frame via a rigid transformation; the camera mounting angle is fixed at **50°**, and calibration is completed using translation/rotation parameters exported from CAD.
- Use the midpoint of the thumb and index-finger MCP joints as the target end-effector position; construct the target orientation from the thumb/index-finger geometry; if fingertips are not visible, fall back to orientation estimation based on the wrist and palm.
- Solve damped least-squares inverse kinematics in PyBullet, and apply EMA smoothing to joint angles; gripper control is driven by the thumb–index finger angle, with a **four-level fallback mechanism** (fingertips, proximal joints, previous frame, default half-open).
- The generated trajectory is first previewed in PyBullet, then replayed to the real SO-ARM101 through LeRobot; the same pipeline can also export demonstration data for training policies such as ACT, SmolVLA, π0.5, and GR00T N1.5.

## Results
- On a structured pick-and-place benchmark (**5 grid locations × 10 trials each = 50 trials**), the IK retargeting method achieves a **90% (45/50)** success rate, with **no training required**.
- Results by location show that the farthest **tile #1/#2 are 10/10 and 10/10**, while **tile #5**, which is closer to the robot base and more prone to self-occlusion of the hand, is **7/10**.
- Compared with 4 VLA policies: **ACT 92%**, **IK 90%**, **SmolVLA 50%**, **π0.5 40%**, **GR00T N1.5 35%**; the VLA methods were trained on **50 demonstration trajectories**, with ACT trained for **50k steps**, SmolVLA for **20k steps**, and π0.5/GR00T for **3k steps**.
- In terms of speed, the pipeline has a total processing latency of about **213 ms/frame**, including MediaPipe **23 ms**, visualization overlay **110 ms**, and PyBullet IK **80 ms**, for an overall throughput of only about **5 FPS**, so it is **offline processing** rather than real-time 30 FPS control.
- In unstructured real-world environments (grocery store, pharmacy), hand occlusion caused by surrounding objects reduces the IK method's success rate to **9.3% (N=75)**, indicating that its main bottleneck is the robustness of marker-free hand tracking under occlusion.
- The paper's strongest claim is that, in controlled settings, this analytical IK approach comes close to or even approaches the best learning-based method with **zero training** (**only 2 percentage points lower** than ACT), but its generalization in the wild remains clearly limited by occlusion.

## Link
- [http://arxiv.org/abs/2603.11383v1](http://arxiv.org/abs/2603.11383v1)
