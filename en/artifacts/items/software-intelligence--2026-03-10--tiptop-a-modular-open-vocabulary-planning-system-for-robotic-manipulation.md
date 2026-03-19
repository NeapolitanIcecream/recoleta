---
source: arxiv
url: http://arxiv.org/abs/2603.09971v1
published_at: '2026-03-10T17:59:00'
authors:
- William Shen
- Nishanth Kumar
- Sahit Chintalapudi
- Jie Wang
- Christopher Watson
- Edward Hu
- Jing Cao
- Dinesh Jayaraman
- Leslie Pack Kaelbling
- "Tom\xE1s Lozano-P\xE9rez"
topics:
- robotic-manipulation
- task-and-motion-planning
- vision-language-models
- open-vocabulary
- modular-robotics
relevance_score: 0.19
run_id: materialize-outputs
language_code: en
---

# TiPToP: A Modular Open-Vocabulary Planning System for Robotic Manipulation

## Summary
TiPToP is a modular open-vocabulary planning system for robotic manipulation: it takes a single RGB image and a natural-language instruction as input and outputs a complete manipulation trajectory. It combines pretrained vision/language foundation models with GPU-accelerated task and motion planning to complete multi-step pick-and-place tasks with zero robot training data.

## Problem
- The paper addresses the question of how to enable a robot to work **out of the box**, completing multi-step manipulation from natural language and camera images without relying on large amounts of robot-specific demonstration data or separate tuning for each hardware setup or scene.
- This matters because end-to-end VLA models, while powerful, usually require large training datasets, generalize unreliably across embodiments, and are hard to diagnose when they fail; traditional TAMP, meanwhile, often depends on manual modeling, tightly coupled systems, and is difficult to deploy.
- The goal is to generate executable manipulation plans even in the presence of unseen real-world objects, distractors, semantic ambiguity, and multi-step constraints.

## Approach
- The system is divided into three parts: **perception, planning, and execution**. It starts from a single stereo RGB observation and a text instruction, builds an object-level 3D scene representation, then generates a complete manipulation trajectory and executes it open-loop.
- The perception module combines multiple pretrained models: FoundationStereo for depth estimation, M2T2 for 6-DoF grasp prediction, Gemini Robotics-ER for open-vocabulary target detection and language grounding, and SAM-2 for segmentation. It then reconstructs an approximate 3D mesh for each object and assigns grasp candidates to the corresponding object.
- The planning module uses **cuTAMP**: it first enumerates action skeletons based on symbolic goals, then performs parallel sampling and differentiable optimization over grasp poses, placement poses, inverse kinematics, and trajectories; when necessary, it automatically inserts intermediate steps such as “move obstacles away before grasping the target.”
- The execution module uses a joint impedance controller to track the planned timed trajectory. The system uses **open-loop visual execution**: it looks at the scene only once during planning and does not replan based on new visual input during execution.
- The design emphasizes modularity and replaceability: new perception models can be swapped in independently, failures can be localized to specific modules, and the authors claim deployment on supported robots can be completed within 1 hour with only camera calibration.

## Results
- Across **28 tabletop manipulation tasks and 165 evaluation trials**, TiPToP achieved an overall success rate of **98/165 = 59.4%**, while the baseline **π0.5-DROID** achieved **55/165 = 33.3%**; average task progress was **74.6% vs 52.4%**, respectively. The paper also emphasizes that TiPToP **requires no robot training data**, whereas the baseline was fine-tuned on **350 hours** of embodiment-specific demonstrations.
- On **simple tasks**, the two are close: TiPToP achieved **22/40 = 55.0%**, and π0.5-DROID achieved **27/40 = 67.5%**; however, TiPToP had slightly higher task progress, **84.0% vs 79.5%**.
- On **distractor tasks**, TiPToP is clearly stronger: **27/45 = 60.0%** versus **12/45 = 26.7%**; task progress was **71.6% vs 41.1%**. For example, on *PB crackers → tray (hard)*, TiPToP achieved **5/5**, while the baseline achieved **0/5**.
- On **semantic tasks**, TiPToP achieved **26/40 = 65.0%** versus **10/40 = 25.0%**; task progress was **71.3% vs 46.8%**. For example, on *sort blocks by color*, TiPToP achieved **5/5, 100% TP**, while the baseline achieved **0/5, 32% TP**.
- On **multi-step tasks**, TiPToP achieved **23/40 = 57.5%** versus **6/40 = 15.0%**; task progress was **75.2% vs 52.2%**. For example, on *color cubes → bowl (sim)*, TiPToP achieved **9/10**, while the baseline achieved **0/10**.
- The strongest qualitative claim is that, under the conditions of zero training data, interpretable modules, and rapid deployment, TiPToP can match or exceed a strong VLA baseline; at the same time, its failures can be decomposed and analyzed by perception/planning/execution module, though the paper also explicitly notes that its open-loop execution fails under object slipping, unexpected motion, and trajectory errors.

## Link
- [http://arxiv.org/abs/2603.09971v1](http://arxiv.org/abs/2603.09971v1)
