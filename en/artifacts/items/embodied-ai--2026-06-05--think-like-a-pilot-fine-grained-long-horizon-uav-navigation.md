---
source: arxiv
url: https://arxiv.org/abs/2606.06836v1
published_at: '2026-06-05T02:23:05'
authors:
- Xiangyi Zheng
- Xiangyu Wang
- Qinan Liao
- Zimu Tang
- Yue Liao
- Dongyue Lyu
- Guodong Wang
- Junjie Liu
- Si Liu
topics:
- uav-navigation
- vision-language-action
- long-horizon-control
- pilot-reasoning
- continuous-control
- benchmark
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# Think Like a Pilot: Fine-Grained Long-Horizon UAV Navigation

## Summary
FLIGHT is a benchmark and VLA model for long-horizon UAV navigation with natural-language instructions and continuous flight control. The paper targets the gap between high-level route following and low-latency UAV control by adding pilot-style reasoning and a fast-slow control architecture.

## Problem
- Language-guided UAVs need to follow multi-stage instructions while producing smooth 6-DoF motion, which matters for delivery, inspection, rescue, and other missions where waypoint lists or manual control are too rigid.
- Existing UAV VLN benchmarks often use discrete actions or sparse waypoints, so they do not test fine-grained continuous control during long missions.
- Large VLMs can track semantics and subgoals, but frame-by-frame VLM control is too slow for stable UAV flight.

## Approach
- The authors introduce FLIGHT, with two task types: Long-horizon Flow, which chains multiple UAV motion primitives, and Fine-grained VLN, which adds dense landmark and action descriptions to navigation.
- They collect simulated UAV trajectories in Unrealzoo scenes, mainly from human pilots, recording FPV video, full 6-DoF trajectory points, and relative continuous action sequences.
- They generate segment-level semantic labels with VLMs, aided by UAV motion metadata such as attitude and turning intervals, then merge labels into natural-language instructions.
- Pilot Reasoning text describes the current flight state and likely next step at critical segments, using current and future segment labels with human verification.
- FLIGHT VLA splits control into a slow Streaming Pilot VLM for video reasoning and task-state memory, and a fast diffusion action model for high-frequency continuous action prediction.

## Results
- The dataset contains 6,689 Fine-grained VLN trajectories and 4,098 Long-horizon Flow trajectories.
- Long-horizon Flow includes 13,815 action instances, averaging 3.37 action instances per trajectory, with 17.8 m average destination distance and 32.8 m average trajectory length.
- Fine-grained VLN samples continuous actions at 10 Hz, with 475 actions per trajectory on average and 154.5 m average trajectory length.
- Compared with Aerial VLN, FLIGHT-FG VLN has shorter average paths, 154 m vs. 661 m, but denser grounding: 6.23 verbs per 100 m vs. 2.17, 12.26 nouns per 100 m vs. 3.25, and 6.55 adjectives per 100 m vs. 0.96.
- FLIGHT-FG VLN has 295.45 action steps per 100 m, compared with 30.86 in Aerial VLN; FLIGHT uses continuous action sequences while Aerial VLN uses discrete action classification.
- The excerpt says FLIGHT VLA beats LAG, NaVid, OpenVLA, and MemoryVLA across all evaluation metrics, but it does not provide the closed-loop metric values or percentage gains.

## Link
- [https://arxiv.org/abs/2606.06836v1](https://arxiv.org/abs/2606.06836v1)
