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
- robotics
- vision-language-action
- active-perception
- manipulation
- benchmark
- 3d-geometry
relevance_score: 0.26
run_id: materialize-outputs
language_code: en
---

# SaPaVe: Towards Active Perception and Manipulation in Vision-Language-Action Models for Robotics

## Summary
SaPaVe is an end-to-end vision-language-action framework for active perception and manipulation in robotics. Its core idea is to decouple camera motion from manipulation actions and learn them in two stages. The paper also introduces a 200K-scale semantic camera control dataset and the first benchmark for active manipulation, aiming to improve success rates under occlusion, poor viewpoints, and targets leaving the field of view.

## Problem
- Existing VLA/robot manipulation methods mostly assume **fixed and near-optimal camera viewpoints**, and tend to fail under occlusion, when targets leave the field of view, or when viewpoints change.
- Placing camera control and manipulation directly into a **unified action space** can disrupt existing manipulation priors and also requires expensive synchronized camera+manipulation annotated data.
- There is a lack of dedicated **large-scale datasets and standard benchmarks** for evaluating “active manipulation,” making it difficult to train methods systematically and compare them reproducibly.

## Approach
- Proposes **SaPaVe**: decouples head camera actions from other manipulation actions, predicting them with different action heads to reduce interference.
- Uses a **two-stage bottom-up training** strategy: first learns **semantically driven camera movement** on **ActiveViewPose-200K**, then jointly fine-tunes active manipulation with mixed data.
- Introduces a **Camera Adapter** (based on LoRA) to preserve semantic camera control capability; this module is frozen in the second stage to avoid damaging the learned active perception priors.
- Designs **Universal Spatial Knowledge Injection**, which encodes 3D geometric information such as depth and camera intrinsics/extrinsics and injects it into the action decoding process, improving spatial robustness under dynamic viewpoints.
- Proposes **ActiveManip-Bench**: the first simulation benchmark dedicated to evaluating active manipulation, covering 12 tasks, 100 objects, and 20 scenes.

## Results
- On the semantic active perception evaluation of **ActiveViewPose-200K**, SaPaVe (Stage 1) achieves an average success rate of **84.3% avg**, outperforming **Gemini-2.5-Pro 72.7%**, **Multi-SpatialMLLM 70.2%**, and **Qwen2.5-VL-72B 62.3%**; this is an average improvement of **11.6 percentage points** over Gemini. Breakdown: Val **85.5**, Test1 **89.1**, Test2 **78.3**.
- In simulation on **ActiveManip-Bench**, SaPaVe (Active Camera) achieves an average success rate of **74.83%**, outperforming **Fixed Camera 36.17%**, **Fixed Camera + Wrist Camera 52.33%**, and **Active Camera + Wrist Camera 73.16%**.
- In the per-task simulation results, SaPaVe reaches **72%** on **Out-of-View Pick-and-Place**, while **Fixed Camera** achieves only **11%**; on **Out-of-View Articulated Manipulation**, it reaches **68%**, while **Fixed Camera** achieves only **7%**, showing that active viewpoints are especially critical in scenarios where the target is “not visible.”
- Figure 1 and the main text claim an average success rate of about **75.2%** on ActiveManip-Bench, and compared with recent VLA baselines, it can obtain **up to 58 percentage points absolute improvement** (the paper gives the fixed-view GR00T-N1 as an example comparison).
- In **real-robot** active manipulation, SaPaVe achieves an average success rate of **85.0%**, higher than **GR00T-N1 53.75%** and **π0 45.0%**; this is an improvement of **31.25 percentage points** over GR00T-N1 and **40 percentage points** over π0.
- Real-world breakdown: Occluded Pick-and-Place **90%**, Out-of-View Pick-and-Place **85%**, Occluded Articulated Manipulation **85%**, Out-of-View Articulated Manipulation **80%**; the corresponding results for GR00T-N1 are **60/55/50/50**, and for π0 are **55/45/45/35**.

## Link
- [http://arxiv.org/abs/2603.12193v1](http://arxiv.org/abs/2603.12193v1)
