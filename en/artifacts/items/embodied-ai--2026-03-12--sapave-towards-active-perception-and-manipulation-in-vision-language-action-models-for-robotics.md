---
source: arxiv
url: http://arxiv.org/abs/2603.12193v1
published_at: '2026-03-12T17:23:46'
authors:
- Mengzhen Liu
- Enshen Zhou
- Cheng Chi
- Yi Han
- Shanyu Rong
- Liming Chen
- Pengwei Wang
- Zhongyuan Wang
- Shanghang Zhang
topics:
- vision-language-action
- active-perception
- robot-manipulation
- sim2real
- benchmark
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# SaPaVe: Towards Active Perception and Manipulation in Vision-Language-Action Models for Robotics

## Summary
SaPaVe is an end-to-end vision-language-action framework for active perception and manipulation in robotics. Its core idea is to decouple camera control from manipulation control, and to use a two-stage training process to combine “look clearly first” with “act afterward.” The paper also introduces a 200k-scale semantic camera control dataset and the first benchmark for active manipulation evaluation.

## Problem
- Existing VLA/robot manipulation methods mostly assume a fixed and near-optimal viewpoint, and tend to fail when there is occlusion, when the target is out of view, or when the viewpoint changes.
- Directly putting camera motion and robot-arm actions into the same action space requires large amounts of data with dual annotations, can interfere with existing manipulation priors, and leads to inefficient training.
- There is a lack of a standardized benchmark specifically for evaluating “active perception + active manipulation,” making these capabilities difficult to compare systematically and reproduce.

## Approach
- Decouple the action space into two parts: head camera actions and other manipulation actions, predicted with separate action heads to reduce mutual interference.
- Use a two-stage bottom-up training strategy: first learn only semantically driven camera motion on **ActiveViewPose-200K**, then jointly optimize camera and manipulation using hybrid data.
- Use a LoRA-based **Camera Adapter** to preserve the prior for semantic camera control—“how to look for a task”—without disrupting the original VLM/VLA weights.
- Introduce **Universal Spatial Knowledge Injection**, which encodes 3D geometric information such as depth and camera intrinsics/extrinsics and injects it into the action decoding process to improve spatial robustness under dynamic viewpoints.
- Propose **ActiveManip-Bench** for systematic evaluation of active manipulation in simulation, covering 12 tasks, 100 objects, and 20 scenes.

## Results
- On semantic active perception evaluation, SaPaVe Stage 1 achieves an average success rate of **84.3%** on **ActiveViewPose-200K**, surpassing **Gemini-2.5-Pro at 72.7%**, **Multi-SpatialMLLM at 70.2%**, and **Qwen2.5-VL-72B at 62.3%**; this is an **11.6 percentage point** improvement over Gemini (the paper earlier also claims up to about **16%**).
- Breaking down this task, SaPaVe scores **85.5/89.1/78.3** on **Val/Test1/Test2**, respectively, while Gemini-2.5-Pro scores **73.3/76.5/68.2**, showing that SaPaVe remains ahead even on Test2, which requires stronger semantic reasoning.
- On the simulated **ActiveManip-Bench**, SaPaVe (Active Camera) achieves an average success rate of **74.83%**, higher than **Fixed Camera at 36.17%**, **Fixed Camera + Wrist Camera at 52.33%**, and **Active Camera + Wrist Camera at 73.16%**.
- On the same simulation benchmark, fixed viewpoints fail noticeably on Out-of-View tasks; for example, **Out-of-View Pick-and-Place is only 11%** and **Out-of-View Articulated Manipulation is only 7%**, while SaPaVe reaches **72%** and **68%**, respectively.
- The figure caption claims an overall average success rate of **75.2%** on **ActiveManip-Bench**, and says the absolute improvement over fixed-view VLA models (such as **GR00T-N1**) can reach **58 percentage points**.
- On real-robot active manipulation, SaPaVe achieves an average success rate of **85.0%**, significantly higher than **π0 at 45.0%** and **GR00T-N1 at 53.75%**; this is a **40 percentage point** improvement over π0 and a **31.25 percentage point** improvement over GR00T-N1.

## Link
- [http://arxiv.org/abs/2603.12193v1](http://arxiv.org/abs/2603.12193v1)
