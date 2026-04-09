---
source: arxiv
url: http://arxiv.org/abs/2604.03552v1
published_at: '2026-04-04T02:36:54'
authors:
- Jason Chen
- I-Chun Arthur Liu
- Gaurav Sukhatme
- Daniel Seita
topics:
- bimanual-manipulation
- video-diffusion
- robot-data-generation
- cross-embodiment-transfer
- sim2real
- imitation-learning
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# CRAFT: Video Diffusion for Bimanual Robot Data Generation

## Summary
CRAFT generates photorealistic, action-labeled bimanual robot demonstrations by running trajectories in a simulator and converting them into videos with a Canny-guided video diffusion model. It targets data scarcity and weak visual diversity in bimanual imitation learning, especially for sim2real transfer, viewpoint changes, and cross-embodiment training.

## Problem
- Bimanual imitation learning needs many demonstrations, but real teleoperation data is expensive and usually covers limited viewpoints, object layouts, lighting, and robot embodiments.
- Existing augmentation methods usually change only one factor, such as viewpoint or embodiment, and often do not produce new action labels paired with the new visuals.
- This matters because dual-arm tasks depend on precise gripper-object contact and coordination, so narrow training data hurts robustness and transfer.

## Approach
- CRAFT starts from a small real dataset, builds a digital twin, replays and expands trajectories in simulation, and keeps successful new trajectories as extra supervision.
- It renders simulator videos, extracts Canny-edge control videos, and feeds those edges into a pre-trained video diffusion model together with a real reference image and a language instruction.
- The key idea is that Canny edges keep the motion and object structure that matter for manipulation while dropping simulator texture details, which gives the diffusion model room to generate realistic appearance.
- The generated videos inherit action labels from the simulator trajectories, so the method outputs action-consistent demonstrations rather than image-only edits.
- The same pipeline supports seven augmentation types: object pose, lighting, object color, background, cross-embodiment transfer, camera viewpoint, and joint wrist plus third-person multi-view generation.

## Results
- In simulation cross-embodiment transfer from bimanual UR5 to bimanual Franka, CRAFT (Ours) reaches **82.6%** on Lift Pot, **89.3%** on Place Cans, and **86.0%** on Stack Bowls, using **1000 generated demos** and **no target-robot demos**.
- On the same simulation tasks, CRAFT (Target) with no extra generated data gets **11.3%**, **6.0%**, and **21.6%**, while Shadow gets **2.0%**, **2.3%**, and **6.0%**.
- The paper reports that CRAFT (Ours) beats the target-robot collected-data baseline, which scores **55.0%**, **69.0%**, and **59.0%** on those three simulation tasks, while requiring **100 collected target demos**.
- In real-world cross-embodiment transfer from bimanual xArm7 to bimanual Franka, CRAFT (Ours) achieves **17/20**, **15/20**, and **16/20** successes on LR, PC, and SB, compared with **4/20**, **1/20**, and **2/20** for CRAFT (Target), **2/20**, **1/20**, and **1/20** for Shadow, and **5/20**, **2/20**, and **3/20** for collected target data.
- In an ablation on Stack Bowls, Canny guidance improves success from **10.3%** without Canny to **21.6%** with Canny; the collected-demo upper bound is **59.0%**.
- The excerpt does not give full quantitative results for all seven augmentation types, but it claims consistent gains over existing augmentation baselines and over straightforward data scaling across simulated and real bimanual tasks.

## Link
- [http://arxiv.org/abs/2604.03552v1](http://arxiv.org/abs/2604.03552v1)
