---
source: arxiv
url: http://arxiv.org/abs/2604.23001v1
published_at: '2026-04-24T20:41:59'
authors:
- Ziyao Wang
- Bingying Wang
- Hanrong Zhang
- Tingting Du
- Tianyang Chen
- Guoheng Sun
- Yexiao He
- Zheyu Shen
- Wanghao Ye
- Ang Li
topics:
- vision-language-action
- robotics-survey
- robot-datasets
- robot-benchmarks
- sim2real
- embodied-ai
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# Vision-Language-Action in Robotics: A Survey of Datasets, Benchmarks, and Data Engines

## Summary
This paper is a survey of vision-language-action robotics research focused on data, evaluation, and scalable data generation rather than model architecture. It argues that progress in VLA will depend on better datasets, benchmarks, and data engines, and it organizes the field around those three parts.

## Problem
- VLA research lacks a clear data-centric map of what training data exists, how benchmarks test generalization, and how scalable data pipelines work.
- Real robot data is expensive and narrow, while synthetic data scales more easily but often misses real visual and physical details, which hurts sim-to-real transfer.
- Existing benchmarks use different tasks, environments, and success criteria, so it is hard to compare methods or measure long-horizon and compositional generalization well.

## Approach
- The paper surveys VLA manipulation research through three categories: **datasets**, **benchmarks**, and **data engines**.
- It classifies datasets by real-world vs. synthetic sources, embodiment diversity, modality mix, and action-space design such as end-effector vs. joint control and absolute vs. delta actions.
- It analyzes benchmarks with a two-axis view: **task complexity** and **environment structure**, covering short-horizon tabletop tasks through long-horizon multi-scene settings.
- It groups data engines into **video-to-data**, **hardware-assisted collection**, and **generative engines** that create or augment robot training data.
- It distills open challenges around representation alignment across embodiments, multimodal supervision, reasoning evaluation, and scalable data generation with physical realism.

## Results
- This is a survey paper, so it does **not** report new model performance numbers or a new state-of-the-art result.
- It claims to be the **first survey** that studies VLA from a **data-centric** perspective, covering works from **2023 to 2025** in a unified taxonomy.
- It defines three main survey pillars: **datasets, benchmarks, data engines**, and highlights representative resources such as **Open X-Embodiment (22 robots)**, **Meta-World (50 tasks)**, and **COLOSSEUM (14 perturbation axes)**.
- It identifies a persistent **fidelity-cost trade-off**: real-world datasets provide better physical grounding but are costly, while synthetic datasets scale but have weaker realism and transfer.
- It finds that current benchmarks leave gaps in **compositional generalization** and **long-horizon reasoning** evaluation, especially when task difficulty and environment variability are entangled.
- It releases a **continuously updated repository** of VLA datasets and benchmarks at the GitHub link given in the paper.

## Link
- [http://arxiv.org/abs/2604.23001v1](http://arxiv.org/abs/2604.23001v1)
