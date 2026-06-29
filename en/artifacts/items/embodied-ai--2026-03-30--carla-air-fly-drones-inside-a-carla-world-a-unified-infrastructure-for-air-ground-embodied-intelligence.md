---
source: arxiv
url: http://arxiv.org/abs/2603.28032v1
published_at: '2026-03-30T04:49:29'
authors:
- Tianle Zeng
- Hanxuan Chen
- Yanci Wen
- Hong Zhang
topics:
- air-ground-simulation
- uav-simulation
- embodied-ai
- vision-language-action
- reinforcement-learning
relevance_score: 0.83
run_id: materialize-outputs
language_code: en
---

# CARLA-Air: Fly Drones Inside a CARLA World -- A Unified Infrastructure for Air-Ground Embodied Intelligence

## Summary
CARLA-Air is a simulation platform that runs CARLA and AirSim inside one Unreal Engine process, so drones and ground agents share the same world state, physics tick, and rendering pipeline. It targets air-ground embodied intelligence workloads such as cooperative robotics, multimodal data collection, navigation, vision-language action, and reinforcement learning.

## Problem
- Existing open-source simulators split along domain lines: CARLA has realistic urban traffic and pedestrians but no native UAV flight, while AirSim has multirotor dynamics and aerial sensors but lacks populated ground scenes.
- Bridge-based co-simulation can connect separate simulators, but cross-process message passing adds synchronization cost and can break strict spatial-temporal alignment across sensors.
- This matters for perception, learning, and evaluation tasks that need synchronized aerial and ground observations from one physically coherent environment.

## Approach
- CARLA-Air merges CARLA and AirSim into a single Unreal Engine 4 process, with both native Python APIs and ROS 2 interfaces kept intact so existing code can run without modification.
- The main technical fix is for UE4's one-GameMode-per-world limit: the system inherits CARLA's GameMode for ground simulation, then spawns AirSim's aerial flight logic as a regular actor during `BeginPlay`.
- Because both platforms run in one process, they share one physics tick and one renderer, which gives synchronized sensing across aerial and ground agents.
- The platform supports up to 18 sensor modalities captured at each simulation tick, including RGB, depth, semantic segmentation, LiDAR, radar, IMU, GNSS, and barometer.
- It also includes an asset pipeline for custom robots, UAV setups, vehicles, and maps, plus built-in support for air-ground cooperation, embodied navigation, vision-language action, dataset construction, and RL policy training.

## Results
- Figure 1 reports per-frame inter-process data transfer under concurrent sensors: bridge-based co-simulation grows near-linearly with sensor count, while CARLA-Air stays effectively constant at **less than 0.5 ms per frame** because there is no cross-process serialization.
- The paper claims synchronized capture of **up to 18 sensor modalities** across aerial and ground platforms at every simulation tick.
- In the platform comparison table, CARLA-Air is the only listed system with simultaneous support for **urban traffic, pedestrians, UAV flight, single-process execution, shared rendering, native APIs, joint sensors, prebuilt binaries, test suite, custom assets, and open source release**.
- The excerpt does **not provide task-level benchmark numbers** such as navigation success rate, RL return, sim-to-real transfer, or dataset-scale comparisons against baselines.

## Link
- [http://arxiv.org/abs/2603.28032v1](http://arxiv.org/abs/2603.28032v1)
