---
kind: trend
trend_doc_id: 237
granularity: day
period_start: '2026-04-29T00:00:00'
period_end: '2026-04-30T00:00:00'
topics:
- robotics
- world models
- Vision-Language-Action
- 3D generation
- simulation
- social navigation
run_id: materialize-outputs
aliases:
- recoleta-trend-237
tags:
- recoleta/trend
- topic/robotics
- topic/world-models
- topic/vision-language-action
- topic/3d-generation
- topic/simulation
- topic/social-navigation
language_code: en
pass_output_id: 120
pass_kind: trend_synthesis
---

# Geometry enters the control loop for robot policies

## Overview
The day’s robotics work puts geometry inside execution. STARRY and X-WAM tie future RGB-D prediction to action diffusion, with reported gains on manipulation benchmarks. A survey on embodied 3D generation spells out the asset requirements behind this work, while outdoor navigation research tests language-grounded assistance in real streets.

## Findings

### World-action models for manipulation
Vision-Language-Action (VLA) policies are being built around predicted 3D structure and future contact. STARRY jointly denoises future spatial-temporal latents and actions, then uses predicted depth and end-effector geometry to bias attention toward handles, openings, contact surfaces, and nearby obstacles. It reports 93.82% clean and 93.30% randomized success on 50 RoboTwin 2.0 bimanual tasks, with real ARX R5 experiments averaging 70.8% success across three tasks.

X-WAM takes a broader world-action route. It predicts multi-view RGB-D video, robot states, and 32 future actions in one diffusion model. Its asynchronous denoising schedule lets actions decode with fewer steps than video, which matters for closed-loop control. The paper reports 79.2% average success on RoboCasa and 90.7% on RoboTwin 2.0 Randomized, while also evaluating visual and geometric prediction metrics.

#### Sources
- [STARRY: Spatial-Temporal Action-Centric World Modeling for Robotic Manipulation](../Inbox/2026-04-29--starry-spatial-temporal-action-centric-world-modeling-for-robotic-manipulation.md): STARRY summary, method, and benchmark results for joint world prediction and action generation.
- [Unified 4D World Action Modeling from Video Priors with Asynchronous Denoising](../Inbox/2026-04-29--unified-4d-world-action-modeling-from-video-priors-with-asynchronous-denoising.md): X-WAM summary, asynchronous denoising method, and RoboCasa/RoboTwin results.

### Simulation-ready 3D generation
The 3D generation survey sets a practical bar for embodied AI assets. Generated objects and scenes need valid geometry, physical parameters, executable kinematics, and simulator-compatible files. That means joints, mass, friction, material behavior, collision geometry, and formats such as URDF, MJCF, and USD matter as much as appearance.

The survey organizes 3D generation into object asset generation, interactive simulation environments, and sim-to-real support. It also compares major simulation platforms including MuJoCo, Isaac Sim, Habitat, AI2-THOR, OmniGibson, PyBullet, ManiSkill3, and Genesis. The open problems are concrete: limited physical annotations, weak agreement between visual quality and physical validity, fragmented evaluation, and sim-to-real gaps.

#### Sources
- [3D Generation for Embodied AI and Robotic Simulation: A Survey](../Inbox/2026-04-29--3d-generation-for-embodied-ai-and-robotic-simulation-a-survey.md): Survey summary with simulation-readiness criteria, taxonomy, platform comparison, and bottlenecks.

### Outdoor language-grounded social navigation
Walk With Me extends language-conditioned robotics into long outdoor routes. The system maps an abstract request to a concrete destination using GPS context and public map points of interest, then queries a walking-route API and turns the route into waypoints. A Vision-Language Model (VLM) handles destination grounding and safety reasoning, while a low-level VLA policy predicts local motion.

The evidence is mainly a real-world system demonstration. The evaluation covers 20 outdoor trials across last-mile delivery and blind guidance scenarios on an Athena 2.0 Pro robot. The paper claims kilometer-scale operation, but the available summary gives no success rate, collision rate, path-length distribution, completion time, or full-system baseline comparison.

#### Sources
- [Walk With Me: Long-Horizon Social Navigation for Human-Centric Outdoor Assistance](../Inbox/2026-04-29--walk-with-me-long-horizon-social-navigation-for-human-centric-outdoor-assistance.md): Walk With Me summary, system design, trial setup, and missing quantitative metrics.
