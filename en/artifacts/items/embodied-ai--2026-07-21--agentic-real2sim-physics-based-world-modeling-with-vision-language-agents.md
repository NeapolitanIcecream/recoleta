---
source: arxiv
url: https://arxiv.org/abs/2607.19190v1
published_at: '2026-07-21T15:23:38'
authors:
- Guanxiong Chen
- Qianjun Xia
- Jiawei Peng
- Heng Zhang
- Bole Ma
- Justin Qian
- Ziyi Jiao
- Bingyang Zhou
- Luoxin Ye
- Kaifeng Zhang
- Kunyi Wang
- Weijia Zeng
- Yunuo Chen
- Pengzhi Yang
- Ziqiu Zeng
- Huamin Wang
- Chao Liu
- Alan Yuille
- Fan Shi
- Changxi Zheng
- Yunzhu Li
- Chenfanfu Jiang
- Peter Yichen Chen
topics:
- real-to-sim
- world-modeling
- vision-language-agents
- robot-manipulation
- simulator-in-the-loop
- digital-twins
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Agentic Real2Sim: Physics-based World Modeling with Vision-Language Agents

## Summary
Agentic Real2Sim converts recorded robot-object interactions into physics-based, simulatable episode twins. It combines vision-language agents with deterministic perception, scene assembly, and simulator-in-the-loop refinement, supporting rigid manipulation and qualitative extensions to deformable and humanoid episodes.

## Problem
- Real-to-sim conversion requires recovering geometry, object states, physical parameters, camera and robot alignment, contacts, and trajectories; manual tuning makes this process slow and brittle.
- The problem matters because reusable, real-world-aligned simulation episodes could support robot policy learning and evaluation across diverse interaction types.

## Approach
- A shared episode contract stores observations, actors, geometry, simulator states, physical and alignment parameters, the simulation backend, and replay metrics.
- Four linked stages use agents for object discovery, keyframe and mask selection, physical-prior inference, scene preparation, and repair decisions, while deterministic tools perform segmentation, mesh recovery, depth estimation, pose tracking, calibration, and grasp optimization.
- The system loads reconstructed episodes into MuJoCo and uses grasp sweeps or an agentic replay-refinement loop to adjust object placement based on simulation evidence.
- Domain adapters reuse the contract for PhysTwin-style deformable interaction and BFM-Zero-style humanoid motion, but these extensions are evaluated qualitatively rather than with aggregate scores.

## Results
- On 100 randomly sampled DROID manipulation episodes, the Gemma 4 31B backend produced 48 replay successes, 8 partial outcomes, and 44 failures; success required a judge score of at least 8/10.
- Replay-success counts across four VLM backends were 48/100 for Gemma 4 31B, 45/100 for Qwen 3.6 35B, 43/100 for GPT-5.4, and 37/100 for Claude Haiku 4.5.
- Model bills ranged from $2.62 for Gemma 4 31B to $82.30 for GPT-5.4; Claude cost 3.5x, Qwen 5.0x, and GPT-5.4 31.4x as much as Gemma under the reported configuration.
- Deformable-object and humanoid conversions show representative real-simulation matches and failure cases, but the paper reports no quantitative aggregate results for those domains.
- The results support comparable observed replay outcomes from an open 31B VLM, while also showing that absolute replay success remained below 50% for every backend and remained sensitive to upstream perception and simulation errors.

## Link
- [https://arxiv.org/abs/2607.19190v1](https://arxiv.org/abs/2607.19190v1)
