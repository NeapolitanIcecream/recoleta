---
source: arxiv
url: https://arxiv.org/abs/2604.24086v1
published_at: '2026-04-27T06:20:15'
authors:
- Kai Yang
- Zedong Chu
- Yingnan Guo
- Zhengbo Wang
- Shichao Xie
- Yanfen Shen
- Xiaolong Wu
- Xing Li
- Mu Xu
topics:
- vision-language-action
- mobile-robot-navigation
- cloud-edge-control
- latency-compensation
- safe-rl
- robot-foundation-models
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# AsyncShield: A Plug-and-Play Edge Adapter for Asynchronous Cloud-based VLA Navigation

## Summary
AsyncShield is an edge-side adapter for cloud-based VLA robot navigation. It corrects delayed VLA waypoints with SE(2) pose realignment, then uses a safety-constrained RL policy to choose local sub-goals from LiDAR and corrected path inputs.

## Problem
- Cloud VLA models often run off-board, so network delay, jitter, packet loss, and outages make navigation commands arrive late.
- A mobile robot keeps moving during that delay, so waypoints generated in an old ego frame can point to the wrong place in the current ego frame and cause collisions.
- The problem matters because direct execution, temporal smoothing, and residual correction can fail when stale intents meet dynamic obstacles.

## Approach
- The edge device keeps a timestamped pose buffer and retrieves the robot pose at the VLA packet anchor time.
- It maps each delayed VLA waypoint into the current ego frame with an analytic SE(2) transform, turning time lag into a measured spatial offset.
- The adapter takes 5 realigned look-ahead waypoints spaced 0.2 m apart and 144 LiDAR proximity values.
- A PPO-Lagrangian policy outputs a universal local sub-goal, with reward terms for path tracking and a LiDAR-based cost when the minimum obstacle distance falls below the safe radius.
- Training uses randomized 10 m by 10 m scenes, 6 static and 6 dynamic obstacles, latency sampled from 0.3 to 1.5 s, packet loss up to 0.2, actuator lag, acceleration limits, noise, and angular bias.

## Results
- In 600 evaluation episodes under ideal network conditions, AsyncShield reached 80.0% success rate, 0.717 m CTE, 1.2% risk exposure rate, and 8.87 s time-to-goal. A2C2 reached 56.7% SR, RTC 40.0%, and Naive 20.0%.
- Under mixed degradation, AsyncShield reached 76.7% SR, 0.725 m CTE, 1.3% RER, and 9.29 s TTG. A2C2 dropped to 43.3% SR, RTC to 30.0%, and Naive to 16.7%.
- Under mixed degradation, AsyncShield reduced CTE versus A2C2 from 1.146 m to 0.725 m and versus Naive from 1.272 m to 0.725 m.
- The ablation without temporal alignment fell from 76.7% to 36.7% SR under mixed degradation, with CTE rising from 0.725 m to 1.194 m.
- The ablation without the RL adapter reached 53.3% SR and 1.443 m CTE under mixed degradation, which supports the need for learned intent-safety balancing.
- The ablation without safety constraints reached only 23.3% SR under mixed degradation, with 4.7% RER despite low 0.692 m CTE, showing that close path tracking can be unsafe when commands are stale.

## Link
- [https://arxiv.org/abs/2604.24086v1](https://arxiv.org/abs/2604.24086v1)
