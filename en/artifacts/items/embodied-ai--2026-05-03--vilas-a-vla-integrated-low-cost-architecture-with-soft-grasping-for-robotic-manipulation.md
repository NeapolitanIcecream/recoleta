---
source: arxiv
url: https://arxiv.org/abs/2605.02037v1
published_at: '2026-05-03T20:04:42'
authors:
- Zijian An
- Hadi Khezam
- Bill Cai
- Ran Yang
- Shijie Geng
- Yiming Feng
- Yue
- Zheng
- Lifeng Zhou
topics:
- vision-language-action
- robot-manipulation
- low-cost-robotics
- soft-grasping
- teleoperation-data
- fragile-object-grasping
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# VILAS: A VLA-Integrated Low-cost Architecture with Soft Grasping for Robotic Manipulation

## Summary
VILAS is an $8,000 robotic manipulation platform for fine-tuning and deploying VLA policies on fragile-object grasping. It combines an industrial cobot, dual RGB-D cameras, teleoperation data collection, and a kirigami soft gripper extension.

## Problem
- Fragile objects such as grapes can be crushed by rigid grippers or abrupt robot motion, so manipulation needs gentle contact and stable grasping.
- Many VLA robot setups depend on expensive integrated hardware; the paper compares VILAS at about $8,000 against an ALOHA kit at about $33,000.
- Force sensors, tactile arrays, and force-control systems add cost and integration work, which limits access for VLA policy research.

## Approach
- The platform uses a Fairino FR5 arm, Jodell RG52-50 gripper, GELLO teleoperation arm, RealSense D455 base camera, RealSense D405 wrist camera, and a ZMQ-based control stack.
- A human operator collects demonstrations with GELLO. Each timestep stores a 7-DoF joint state, two RGB camera views, and a language prompt.
- A PEBA kirigami extension mounts on the parallel gripper and bends under compression, spreading contact over the fruit and reducing the need for force sensing.
- The authors fine-tune pi_0, pi_0.5, and GR00T N1.6 from public checkpoints on the same dataset: 100 episodes, 1,200 frames per episode, trained for 50,000 iterations on an NVIDIA H200.
- During deployment, the robot runs at 20 Hz. pi_0 and pi_0.5 output 50-action chunks, while GR00T N1.6 outputs 16-action chunks.

## Results
- Total hardware cost is about $8,000, compared with about $33,000 for ALOHA.
- On the grape task, each model was tested over 50 trials. Single-grasp success was 70% for pi_0, 84% for pi_0.5, and 82% for GR00T N1.6.
- Multi-grasp success, defined as at least two consecutive successful grasps, was 22% for pi_0, 36% for pi_0.5, and 58% for GR00T N1.6.
- Mean inference latency was 73.8 ms for pi_0, 82.8 ms for pi_0.5, and 63.6 ms for GR00T N1.6.
- Per-step inference cost was 1.48 ms for pi_0, 1.66 ms for pi_0.5, and 3.98 ms for GR00T N1.6, reflecting the shorter action horizon for GR00T N1.6.
- The strongest claim is system-level: current VLA policies can be fine-tuned and deployed for delicate real-world grasping on a lower-cost modular robot, with GR00T N1.6 giving the best sequential grasp reliability in this setup.

## Link
- [https://arxiv.org/abs/2605.02037v1](https://arxiv.org/abs/2605.02037v1)
