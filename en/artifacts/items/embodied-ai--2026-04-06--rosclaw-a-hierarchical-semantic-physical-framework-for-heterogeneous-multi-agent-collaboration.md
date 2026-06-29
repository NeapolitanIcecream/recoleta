---
source: arxiv
url: http://arxiv.org/abs/2604.04664v1
published_at: '2026-04-06T13:16:24'
authors:
- Rongfeng Zhao
- Xuanhao Zhang
- Zhaochen Guo
- Xiang Shao
- Zhongpan Zhu
- Bin He
- Jie Chen
topics:
- multi-robot-coordination
- embodied-agent-framework
- vision-language-robotics
- sim-to-real
- digital-twin
- heterogeneous-robots
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# ROSClaw: A Hierarchical Semantic-Physical Framework for Heterogeneous Multi-Agent Collaboration

## Summary
ROSClaw is a system for coordinating different robots with one semantic-to-physical control loop. It combines language-level task planning, tool calling, digital-twin safety checks, and execution data logging so multi-robot tasks can run with less manual integration.

## Problem
- Existing embodied robot systems split planning, data collection, skill training, and deployment into separate stages, which creates mismatches between what the model plans and what the hardware can actually do.
- Long-horizon, multi-step tasks with heterogeneous robots are hard because high-level language models do not model joint limits, collisions, timing, or hardware-specific SDK details.
- Manual hardware testing and per-robot programming slow down multi-agent deployment and make cross-platform reuse expensive.

## Approach
- ROSClaw uses a three-layer architecture: a cognitive layer for low-frequency reasoning, a coordination layer for tool/API mapping and scheduling, and a physical layer for high-frequency robot control.
- It builds an **Online Tool Pool** that maps abstract instructions from an LLM/VLM agent into executable SDK, MCP, and API calls for different robot platforms.
- It adds an **e-URDF-based physical safeguard**: before execution, commands are checked in Isaac Lab with forward dynamics and collision validation against robot models and constraints.
- It records robot states, multimodal observations, and execution trajectories into a **Local Resource Pool** so the system can reuse experience and support later policy refinement.
- During deployment, one unified agent keeps task context across planning and execution and assigns subtasks to different robots based on workspace and capability constraints.

## Results
- The paper reports real-world validation in a **~60 m² smart home** setting with **three active robots** in the main collaborative task: a humanoid robot, a fixed robotic arm, and a mobile manipulator.
- In the demonstrated task, the robots complete a multi-step sequence: the mobile manipulator opens a door, the humanoid enters and carries a basket, the fixed arm picks a user-specified **kiwi** and places it into the basket, and the humanoid transports the basket to the sink.
- A second validation uses **seven physical gimbal units** with e-URDF safety checking and simulated choreography verification before real execution.
- The clearest quantitative claim is that ROSClaw cuts coordinated multi-gimbal dance generation time to **about 3 minutes**, with human input limited to the initial instruction.
- The paper also claims annotation and demonstration cost can drop **from days to hours**, but this is presented as a system claim in the text and not backed by a controlled benchmark table in the excerpt.
- The excerpt does **not** provide standard benchmark metrics, success rates, ablations, or direct numeric comparisons against named baselines for the multi-robot task.

## Link
- [http://arxiv.org/abs/2604.04664v1](http://arxiv.org/abs/2604.04664v1)
