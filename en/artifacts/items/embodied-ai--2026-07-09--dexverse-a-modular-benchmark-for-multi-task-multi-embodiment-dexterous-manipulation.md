---
source: arxiv
url: https://arxiv.org/abs/2607.08751v1
published_at: '2026-07-09T17:50:47'
authors:
- Yunchao Yao
- Zhuxiu Xu
- Tianqi Zhang
- Zixian Liu
- Sikai Li
- Zhenyu Wei
- Feng Chen
- Dihong Huang
- Kechang Wan
- Chenyang Ma
- Shuqi Zhao
- Shenghua Gao
- Masayoshi Tomizuka
- Yi Ma
- Mingyu Ding
topics:
- dexterous-manipulation
- robot-benchmark
- multi-embodiment
- robot-policy-evaluation
- vision-language-action
- teleoperation-data
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# DexVerse: A Modular Benchmark for Multi-Task, Multi-Embodiment Dexterous Manipulation

## Summary
DexVerse is a modular simulation benchmark for testing dexterous robot policies across 100 tasks, 3 robot arms, 6 dexterous hands, visual conditions, and multiple observation types. It provides 3,180 VR-teleoperated demonstrations and shows that current policies achieve only limited success on contact-rich, precision, tool-use, and long-horizon tasks.

## Problem
- Existing manipulation benchmarks cover fewer dexterous skills, embodiments, visual conditions, or demonstration data, which limits controlled evaluation of general-purpose robot policies.
- Dexterous manipulation requires high-DoF hand control, contact regulation, object-affordance reasoning, bimanual coordination, and long-horizon execution.
- A unified benchmark matters because policy performance can change sharply across embodiments, sensory inputs, visual variations, and interaction types.

## Approach
- DexVerse defines 100 tasks across 8 categories: primitive, functional, articulated, non-prehensile, contact-rich, bimanual, multi-goal, and long-horizon manipulation.
- Its configuration-driven simulator separates task logic from robot embodiments and supports 3 arms, including Franka Research 3, UR10e, and xArm 7, plus 6 dexterous hands.
- The benchmark exposes controllable changes to textures, lighting, backgrounds, camera viewpoints, object poses, and dynamics.
- A VR teleoperation system uses Apple Vision Pro, inverse kinematics, and optimization-based hand retargeting to collect synchronized proprioceptive, RGB, depth, point-cloud, and state demonstrations.
- The authors train and compare Diffusion Policy, 3D Diffusion Policy, OpenVLA, and pi0.5 on the same 950-episode subset covering 19 tasks.

## Results
- Across 19 tasks, 3D Diffusion Policy and pi0.5 tie for the best mean online success rate at 0.34; Diffusion Policy reaches 0.32 and OpenVLA reaches 0.19.
- No method consistently dominates: Diffusion Policy leads Pick-and-Lift at 0.51, 3D Diffusion Policy leads Tool Use at 0.35, and pi0.5 leads Articulated Manipulation at 0.35 and Precision Contact at 0.29.
- Web-scale VLA pretraining provides no aggregate advantage over the best from-scratch diffusion policy: pi0.5 scores 0.34, matching 3D Diffusion Policy, while OpenVLA scores 0.19.
- PushT has a 0.00 success rate for all four policies; InsertPen, SlideUtilityKnife, and OpenLaptop also remain at or near zero, exposing failures in force regulation and sub-centimeter alignment.
- DexVerse contributes 100 tasks, 3 arms, 6 hands, 3,180 demonstrations, and configurable multimodal observations, making it broader than the benchmark suites compared in the paper.

## Link
- [https://arxiv.org/abs/2607.08751v1](https://arxiv.org/abs/2607.08751v1)
