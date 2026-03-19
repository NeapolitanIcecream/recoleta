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
- robot-manipulation
- task-and-motion-planning
- vision-language-planning
- open-vocabulary
- modular-robotics
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# TiPToP: A Modular Open-Vocabulary Planning System for Robotic Manipulation

## Summary
TiPToP is a modular open-vocabulary planning system for robotic manipulation: it takes RGB images and natural language as input and outputs multi-step manipulation trajectories. It combines pretrained vision foundation models with GPU-accelerated task-and-motion planning, enabling real-world and simulated tabletop manipulation with **zero robot training data**, and achieves performance comparable to or better than a VLA baseline fine-tuned on 350 hours of embodiment-specific demonstrations across multiple task types.

## Problem
- The goal is to enable robots to **work out of the box**, performing multi-step manipulation on **arbitrary objects** based on natural-language instructions and camera images, without requiring object-, environment-, or embodiment-specific tuning.
- Existing VLA models have a clean interface, but they typically require large amounts of robot data and lack cross-embodiment generalization and interpretability of failures; traditional TAMP systems are often deeply coupled to specific hardware and perception stacks, making them hard to reuse.
- This matters because a truly deployable general manipulation system must simultaneously provide **open-vocabulary understanding, geometric feasibility, multi-step reasoning, low data cost, and ease of deployment**.

## Approach
- The system builds a scene from a single initial observation (stereo RGB) and a language instruction: a depth model produces dense depth, a grasping model proposes 6-DoF grasp candidates, a VLM detects and names objects and converts the language goal into a symbolic goal, SAM-2 performs segmentation, and these are fused into an object-centric 3D scene representation.
- On the planning side, it uses GPU-parallel cuTAMP: first enumerating symbolic plan skeletons, then optimizing continuous variables such as grasp poses, placement poses, and joint configurations in parallel, while calling cuRobo to generate collision-free trajectories.
- On the execution side, a joint impedance controller tracks the entire planned trajectory; the system executes in **open loop** and does not rely on visual feedback during execution.
- The core mechanism can be understood most simply as: **first use foundation models to “understand the scene and task,” then use a classical planner to “compute a sequence of feasible grasp/place actions”**, rather than having a large model output actions end to end.
- The modular design makes it easy to swap components and localize failure sources, and the authors claim it can be **installed and deployed within 1 hour** on supported platforms, requiring only camera calibration and allowing relatively easy transfer to new embodiments.

## Results
- Across **28 tabletop manipulation tasks/scenes and 165 trials**, TiPToP achieved an overall success rate of **98/165 = 59.4%**, while \(\pi_{0.5}\)-DROID achieved **55/165 = 33.3%**; average task progress was **74.6% vs 52.4%**, respectively.
- Compared with the baseline: the baseline is **\(\pi_{0.5}\)-DROID**, fine-tuned on **350 hours of embodiment-specific demonstration data**; TiPToP uses **zero robot data**.
- By category: on **Simple** tasks the two are close, with TiPToP task progress at **84.0% vs 79.5%**, but a slightly lower success rate of **22/40 vs 27/40**; on **Distractor** tasks, TiPToP achieved **27/45 (60.0%) vs 12/45 (26.7%)**, with task progress **71.6% vs 41.1%**.
- On **Semantic** tasks, TiPToP achieved **26/40 (65.0%) vs 10/40 (25.0%)**, with task progress **71.3% vs 46.8%**; the paper states that TiPToP had a higher success rate on **7 of 8** semantic scenes, while the baseline had **4 scenes at 0/5**.
- On **Multi-step** tasks, TiPToP achieved **23/40 (57.5%) vs 6/40 (15.0%)**, with task progress **75.2% vs 52.2%**; for example, “Color cubes -> bowl (sim)” was **9/10 vs 0/10**, and “Three marbles -> cup” was **2/5 vs 0/5**.
- The paper also claims evaluation in both the **simulated and real world**, analyzes failure modes over **173 trials** in total, and demonstrates deployment feasibility on embodiments including **DROID, UR5e, Trossen WidowX AI**; however, the provided excerpt does not include more detailed module-level failure-rate figures.

## Link
- [http://arxiv.org/abs/2603.09971v1](http://arxiv.org/abs/2603.09971v1)
