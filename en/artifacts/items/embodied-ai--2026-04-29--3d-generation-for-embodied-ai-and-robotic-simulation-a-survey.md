---
source: arxiv
url: https://arxiv.org/abs/2604.26509v3
published_at: '2026-04-29T10:17:55'
authors:
- Tianwei Ye
- Yifan Mao
- Minwen Liao
- Jian Liu
- Chunchao Guo
- Dazhao Du
- Quanxin Shou
- Fangqi Zhu
- Song Guo
topics:
- 3d-generation
- robotic-simulation
- sim2real
- embodied-ai
- simulation-assets
- scene-generation
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# 3D Generation for Embodied AI and Robotic Simulation: A Survey

## Summary
This survey argues that 3D generation for embodied AI must produce simulator-ready assets and scenes, including geometry, articulation, physical parameters, and executable formats. It organizes the area around object assets, interactive environments, and sim-to-real transfer.

## Problem
- Robot learning, VLA models, and simulation-based training need many 3D objects and scenes that robots can manipulate, not just view.
- Current 3D generation work often optimizes shape or appearance while missing joints, mass, friction, material behavior, collision geometry, and URDF/MJCF/USD compatibility.
- The literature is split across graphics, vision, robotics, and simulators, which makes evaluation and reuse hard.

## Approach
- The survey defines simulation readiness with 4 requirements: geometric validity, physical parameterization, kinematic executability, and simulator compatibility.
- It groups the literature into 3 roles: Data Generator for object assets, Simulation Environments for interactive scenes, and Sim2Real Bridge for reconstruction, augmentation, and transfer.
- It reviews 3D representations used in embodied pipelines, including voxels, point clouds, meshes, scene graphs, SDFs, NeRFs, and 3D Gaussian Splatting.
- It connects generated content to simulator formats and engines, including URDF, MJCF, USD, MuJoCo, Isaac Sim, Habitat, AI2-THOR, OmniGibson, PyBullet, ManiSkill3, and Genesis.

## Results
- The paper reports no new model benchmark or robot-policy experiment; it is a survey.
- Its main claimed result is a 3-part taxonomy for 3D generation in embodied AI: Data Generator, Simulation Environments, and Sim2Real Bridge.
- It lists 4 simulation-readiness criteria: geometry, physics parameters, kinematics, and simulator file compatibility.
- It compares 8 major robotic simulation platforms in Table I: MuJoCo, Isaac Sim, Habitat 3.0, AI2-THOR, OmniGibson, PyBullet, ManiSkill3, and Genesis.
- It organizes object-generation methods by 4 asset types: articulated, physically grounded, deformable, and end-to-end simulation-ready pipelines.
- It claims the main open bottlenecks are limited physical annotations, weak alignment between visual quality and physical validity, fragmented evaluation, and persistent sim-to-real gaps.

## Link
- [https://arxiv.org/abs/2604.26509v3](https://arxiv.org/abs/2604.26509v3)
