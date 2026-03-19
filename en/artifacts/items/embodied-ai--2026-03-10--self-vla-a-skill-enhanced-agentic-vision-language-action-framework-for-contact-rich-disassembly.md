---
source: arxiv
url: http://arxiv.org/abs/2603.11080v1
published_at: '2026-03-10T22:30:28'
authors:
- Chang Liu
- Sibo Tian
- Xiao Liang
- Minghui Zheng
topics:
- vision-language-action
- robot-disassembly
- contact-rich-manipulation
- agentic-robotics
- skill-library
- failure-recovery
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# SELF-VLA: A Skill Enhanced Agentic Vision-Language-Action Framework for Contact-Rich Disassembly

## Summary
SELF-VLA proposes an agentic VLA framework for contact-rich disassembly tasks, combining an end-to-end vision-language-action policy with an explicit skill library and failure recovery. It is designed to address the extremely low success rates of traditional VLA methods in long-horizon, high-precision industrial disassembly, and significantly outperforms end-to-end baselines on CPU and RAM disassembly.

## Problem
- Existing robotic disassembly systems usually rely on staged engineering pipelines, with high costs for data preparation, modeling, and maintenance, and they are overly specialized to specific tasks and parts, resulting in poor generalization.
- Although end-to-end VLA performs well on everyday tabletop manipulation, it often nearly fails on industrial tasks like disassembly that are **long-horizon, contact-rich, and require strict step constraints**.
- This problem matters because e-waste is massive in scale, manual disassembly is costly and poses health risks, and recovery of high-value components depends on reliable automated disassembly capabilities.

## Approach
- The core idea is simple: **let the VLA handle “approaching and judging timing,” let explicit skills handle “critical contact operations,” and if failure occurs, let a corrective VLA pick up and continue.**
- The framework has three parts: the VLA-planner uses images and language to move the robot arm to a suitable pre-grasp state and outputs a special stop token; then the skill library is invoked to execute contact-rich disassembly trajectories; if grasping/placing fails, the VLA-corrector is triggered to re-grasp and resume execution.
- To avoid modifying the VLA output head, the authors encode the stop token into the gripper action dimension, using an out-of-physical-range value of 255 to indicate “switch to skill execution.”
- The skill library consists of structured waypoints recorded via manual teleoperation: the extraction stage uses relative-pose waypoints to adapt to different starting points, while the placement stage uses absolute-pose waypoints to reach a fixed target; the CPU skill contains 23 waypoints, and the RAM skill contains 8.
- The dataset consists of real tabletop disassembly demonstrations, with 528 demonstrations total (CPU 264, RAM 264), and LoRA fine-tuning is performed on four VLA backbone models, while planner, corrector, and end-to-end baselines are also trained, comparing 10Hz and 30Hz versions.

## Results
- On **RAM removal**, the best end-to-end result is **π0.5-Droid FT-10Hz: 7/20 final success (35%)**; the best SELF-VLA result is **π0.5-Droid FT-10Hz: 12/20 (60%)**, an improvement of **25 percentage points** over the strongest end-to-end baseline.
- On **CPU extraction**, the best end-to-end result is only **π0.5-Droid FT-30Hz: 2/20 final success (10%)**; the best SELF-VLA reaches **π0.5-Droid FT-10Hz: 17/20 (85%)**, an improvement of **75 percentage points**, indicating larger gains for more complex contact operations.
- For OpenVLA-OFT, on the CPU task, the best end-to-end result is only **0/20 final success (FT-10Hz)**, while SELF-VLA reaches **10/20 (50%)**; on the RAM task, end-to-end improves from **0/20** to SELF-VLA **4/20 (20%)**.
- For π0.5, on the CPU task, the best end-to-end result is **0/20**, while the best SELF-VLA result is **11/20 (55%)**; on the RAM task, the best end-to-end result is **4/20 (20%)**, while the best SELF-VLA result is **9/20 (45%)**.
- Pretrained models without fine-tuning are almost all **0/20**, showing that this scenario requires substantial task-specific adaptation; the authors also report that **10Hz fine-tuning usually outperforms 30Hz**, for example π0.5-Droid on CPU SELF-VLA with **17/20 vs 7/20**.

## Link
- [http://arxiv.org/abs/2603.11080v1](http://arxiv.org/abs/2603.11080v1)
