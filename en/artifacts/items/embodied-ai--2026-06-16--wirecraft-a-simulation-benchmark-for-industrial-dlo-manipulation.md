---
source: arxiv
url: https://arxiv.org/abs/2606.18097v1
published_at: '2026-06-16T15:59:46'
authors:
- Chongyu Zhu
- Ramy ElMallah
- Hyegang Kim
- Zachary Tang
- Jiachen Rao
- Artem Arutyunov
- Seungyeon Ha
- Chi-Guhn Lee
topics:
- deformable-linear-objects
- robot-manipulation
- simulation-benchmark
- vision-language-action
- sim2real
- industrial-assembly
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# WireCraft: A Simulation Benchmark for Industrial DLO Manipulation

## Summary
WireCraft is a simulation benchmark for industrial wire and cable manipulation tasks: connector insertion, clip routing, and channel seating. It tests RL, imitation learning, and VLA policies with shared task definitions, metrics, and data formats.

## Problem
- Industrial assembly often requires robots to route, seat, and insert deformable linear objects such as wires and cables; these objects bend, occlude themselves, and change shape during contact.
- Existing DLO benchmarks focus on generic shape control or free-space manipulation, while many industrial wire studies use fixed hardware, fixtures, and sensing setups that are hard to reuse.
- The gap matters because policy comparisons and sim-to-real studies need common tasks, assets, data schemas, and metrics.

## Approach
- WireCraft builds on Isaac Lab 2.2.1 and Isaac Sim 4.5, with configurable industrial assets for connectors, ports, clips, channels, and 3D-printable task boards.
- It supports two wire models: an articulated rigid-body chain for faster rollout generation and a FEM deformable-body model for higher-fidelity bending and contact.
- The benchmark covers three task families: connector insertion, clip routing, and channel seating, with randomized wire initialization and task-specific randomization.
- It provides demonstrations from scripted simulation policies, RL rollouts, simulation teleoperation, and real UR5 trajectories in a LeRobot-compatible schema.
- It evaluates PPO, SACfD, Vision PPO, ACT, Diffusion Policy, Diffusion Transformer VLA, and π0.5 under shared success metrics.

## Results
- On Ethernet connector insertion with 3 mm clearance, privileged state RL reaches high insertion success: State PPO achieves 95.86±1.93% insert success and SACfD achieves 92.40±5.91%.
- Vision PPO performs much worse on the same Ethernet insertion task: 51.63±4.82% reach success and 17.74±1.21% insert success, showing a large reach-to-insert drop.
- Across connector types, State PPO stays above 92% insert success: Cylinder 93.75±1.25%, Cuboid 95.00±3.75%, Ethernet 95.86±1.93%, and DisplayPort 92.92±3.15%.
- Vision PPO degrades on harder visual alignment cases: Cuboid insert success is 6.25±3.31% and DisplayPort insert success is 3.32±1.45%.
- Privileged State PPO also solves the initial non-insertion tasks in simulation: 95.32±0.93% success on 1-clip routing and 82.33±0.31% on straight-channel seating.
- In real-world UR5 Ethernet insertion with ACT at a 40k-step checkpoint, simulation-only data gives 0/10 insertions, while real+scripted simulation data gives 4/10 insertions; the paper treats this as evidence of a remaining sim-to-real gap, not a final ranking of data mixtures.

## Link
- [https://arxiv.org/abs/2606.18097v1](https://arxiv.org/abs/2606.18097v1)
