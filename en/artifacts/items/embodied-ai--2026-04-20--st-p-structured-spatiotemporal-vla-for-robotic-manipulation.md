---
source: arxiv
url: http://arxiv.org/abs/2604.17880v1
published_at: '2026-04-20T06:48:47'
authors:
- Chuanhao Ma
- Hanyu Zhou
- Shihan Peng
- Yan Li
- Tao Gu
- Luxin Yan
topics:
- vision-language-action
- robotic-manipulation
- spatiotemporal-reasoning
- long-horizon-control
- hierarchical-policy
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# ST-$π$: Structured SpatioTemporal VLA for Robotic Manipulation

## Summary
ST-$\pi$ is a vision-language-action model for robotic manipulation that adds explicit spatiotemporal structure to both task planning and action generation. It targets long-horizon, multi-stage manipulation where standard VLA models often drift or lose track of sub-task boundaries.

## Problem
- Existing VLA and 4D-VLA systems usually predict actions from fused observations in an implicit way, which makes long sequences of sub-tasks hard to separate and execute reliably.
- Fine-grained manipulation needs two things at once: explicit sub-task boundaries at the planning level and stable step-by-step control inside each sub-task.
- This matters for assembly and household tasks where errors accumulate across stages and later actions depend on earlier ones being completed in the right place and order.

## Approach
- The model has two parts: **ST-VLM** for chunk-level planning and **ST-AE** for step-level control.
- ST-VLM builds a 4D representation from image sequences, geometry features, and timestamps, then predicts a sequence of chunk-level action prompts. Each prompt includes semantic intent, a spatial target, and a temporal duration for one sub-task.
- The planning module uses causal attention across prompts so later sub-tasks depend on earlier ones, which gives an explicit ordered decomposition of a long task.
- ST-AE takes one chunk-level prompt at a time and generates low-level action steps with two generators: a spatial generator for trajectory shape and a temporal generator for step order and consistency.
- Action generation uses flow matching, with a time-dependent fusion that shifts guidance from spatial shaping early in denoising to temporal refinement later.

## Results
- The paper introduces **STAR**, a real-world dataset on a Franka Research 3 robot with **30 manipulation tasks**, **50 demonstrations per task**, and about **300k interaction steps**. It includes sub-task descriptions, target locations, and execution durations.
- On the shown benchmark table, **4D-VLA** is the strongest listed baseline with **88.6% average success rate**. ST-$\pi$ claims consistent gains over prior VLA baselines, but the provided excerpt does **not** include the full ST-$\pi$ result row, so its exact average improvement is not visible here.
- Visible baseline numbers show why long-horizon settings are hard: **OpenVLA** gets **53.7%** success on the Long suite, **Octo 51.1%**, **SpatialVLA 55.5%**, **TraceVLA 54.1%**, while **4D-VLA** reaches **79.1%**.
- The excerpt also reports completion time for several baselines. For average completion time, **OpenVLA** has **8.0s**, **Octo 7.0s**, and **SpatialVLA 6.6s**. The ST-$\pi$ completion-time numbers are not visible in the provided text.
- Strong concrete claim: the method improves long-horizon manipulation by combining explicit chunk-level sub-task planning with dual-generator step-level action refinement, rather than relying on implicit spatiotemporal representations alone.

## Link
- [http://arxiv.org/abs/2604.17880v1](http://arxiv.org/abs/2604.17880v1)
