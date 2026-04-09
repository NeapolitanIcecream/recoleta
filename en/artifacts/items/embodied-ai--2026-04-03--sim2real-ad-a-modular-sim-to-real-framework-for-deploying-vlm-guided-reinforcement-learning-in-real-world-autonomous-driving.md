---
source: arxiv
url: http://arxiv.org/abs/2604.03497v1
published_at: '2026-04-03T22:41:45'
authors:
- Zilin Huang
- Zhengyang Wan
- Zihao Sheng
- Boyue Wang
- Junwei You
- Yue Leng
- Sikai Chen
topics:
- sim2real
- autonomous-driving
- vlm-guided-rl
- closed-loop-deployment
- birds-eye-view
relevance_score: 0.56
run_id: materialize-outputs
language_code: en
---

# Sim2Real-AD: A Modular Sim-to-Real Framework for Deploying VLM-Guided Reinforcement Learning in Real-World Autonomous Driving

## Summary
Sim2Real-AD is a sim-to-real deployment pipeline for autonomous driving policies trained in CARLA with VLM-guided reinforcement learning. It targets zero-shot transfer to a full-scale real vehicle by bridging simulator-only observations and simulator-specific control outputs without using real-world RL training data.

## Problem
- CARLA-trained VLM-guided RL policies often consume privileged bird's-eye-view semantic inputs and emit control signals tied to simulator dynamics, so they fail when moved directly to a real car.
- The paper focuses on two coupled gaps: an observation gap between clean simulator BEV and noisy monocular real-camera input, and a dynamics gap between simulator controls and real vehicle response.
- This matters because strong simulation results for driving RL do not help deployment if the policy cannot run safely in closed loop on a physical vehicle.

## Approach
- The framework splits transfer into four modules: Geometric Observation Bridge (GOB), Physics-Aware Action Mapping (PAM), Two-Phase Progressive Training (TPT), and a Real-time Deployment Pipeline (RDP).
- GOB converts a front-view monocular image into a simulator-compatible multi-channel BEV using pre-trained semantic segmentation plus inverse perspective mapping, so the policy sees a representation closer to its CARLA training input.
- PAM changes the policy output space from simulator-native low-level controls to physical quantities such as curvature and target speed, then maps those to a specific vehicle through a calibrated bicycle model and PID controller.
- TPT adapts the policy in two stages: first to the new action semantics under clean simulator BEV, then to noisier IPM-generated BEV observations. This separates the two shifts instead of forcing the policy to learn both at once.
- The system is instantiated with DriveVLM-RL, where VLM components are used only during training for reward design and removed at test time, so deployment uses a lightweight neural driving policy.

## Results
- Zero-shot real-world deployment on a full-scale Ford E-Transit reports success rates of **90%** for car-following, **80%** for obstacle avoidance, and **75%** for stop-sign interaction.
- The paper claims deployment uses **no real-world RL training data** and only lightweight platform calibration of about **30 minutes**.
- Simulation studies are said to preserve the relative performance ordering of representative RL algorithms across different reward paradigms and to validate the contribution of each module.
- The excerpt does not provide benchmark tables, dataset sizes, trial counts, or direct numeric comparisons against prior sim-to-real baselines, so the strongest quantitative evidence in the provided text is the three real-vehicle success rates above.
- The authors claim this is among the first demonstrations of zero-shot closed-loop deployment of a CARLA-trained VLM-guided RL policy on a full-scale real vehicle without any real-world RL training data.

## Link
- [http://arxiv.org/abs/2604.03497v1](http://arxiv.org/abs/2604.03497v1)
