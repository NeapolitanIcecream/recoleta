---
source: arxiv
url: http://arxiv.org/abs/2603.04356v1
published_at: '2026-03-04T18:20:03'
authors:
- Soroush Nasiriany
- Sepehr Nasiriany
- Abhiram Maddukuri
- Yuke Zhu
topics:
- robot-learning
- simulation-benchmark
- mobile-manipulation
- foundation-models
- lifelong-learning
relevance_score: 0.34
run_id: materialize-outputs
language_code: en
---

# RoboCasa365: A Large-Scale Simulation Framework for Training and Benchmarking Generalist Robots

## Summary
RoboCasa365 is a large-scale simulation framework for training and benchmarking generalist household robots, focused on addressing the lack of a reproducible, systematic, large-scale benchmark. It integrates tasks, environments, demonstration data, and multiple learning settings into a single platform for studying robot generalization.

## Problem
- Existing robot learning lacks a **large-scale, reproducible, systematic** benchmark for generalist robots, making it difficult to objectively measure how far we are from “general-purpose household robots.”
- Real-world data collection and evaluation are costly, noisy, and hard to reproduce, limiting research into how **task diversity, environment variation, and dataset scale** affect generalization.
- Existing simulation frameworks usually have too few tasks, narrow environments, and small datasets, making it hard to support unified comparisons across multi-task training, foundation model training, and lifelong learning.

## Approach
- Build a large-scale kitchen mobile manipulation simulation benchmark with **365 tasks, 2,500 pretraining kitchen environments, and 10 target environments**, covering atomic skills, composite tasks, long-horizon planning, semantic reasoning, and memory-related tasks.
- Provide large-scale data: **30k pretraining human demonstrations**, **25k target-task human demonstrations**, and **synthetic demonstrations at the scale of 60 atomic tasks × 10k = 600k** generated with MimicGen; the paper summarizes this as **600+ hours of human data** and **1600+ hours of synthetic data**.
- Use an LLM to first generate high-level kitchen activities and task blueprints, then implement them as 300 composite tasks, systematically expanding task coverage.
- Define three standard evaluation settings: **large-scale multi-task training, robot foundation model pretraining + downstream finetuning, and lifelong learning**, and run systematic experiments with methods including Diffusion Policy, π0, π0.5, and GR00T N1.5.

## Results
- **Scale claim**: RoboCasa365 includes **365 everyday tasks** (**65 atomic + 300 composite**), **2,500 kitchen environments**, and **2,000+ hours** of robot interaction data; the authors describe it as the first simulation framework to simultaneously provide “hundreds of tasks + thousands of environments + large-scale high-quality demonstrations + a systematic benchmark.”
- **Multi-task training (300 pretraining tasks, Table 1)**: GR00T N1.5 performs best, with success rates of **Atomic 43.0% / Composite-Seen 9.6% / Composite-Unseen 4.4% / Avg 20.0%**; compared with **π0.5: 39.6/7.1/1.2/16.9**, **π0: 36.3/5.2/0.7/15.0**, and **Diffusion Policy: 15.7/0.2/1.25/6.1**. This shows that composite and unseen tasks are significantly harder.
- **Foundation model training (Table 2, GR00T N1.5)**: Average success rate improves from **Target-only 10% data: 21.0%** to **Pretraining+Target 10% data: 35.9%**; with **100% target data**, it improves from **43.7%** to **51.1%**. In particular, **Composite-Unseen** improves from **33.3%** to **42.1%** under **100% data**.
- **Data efficiency claim**: The authors claim pretraining brings about a **3× data efficiency improvement**, meaning “pretraining + less target data” can achieve performance close to “target-only training + about 3× more data.”
- **Lifelong learning (Table 3)**: Performance on old tasks drops substantially as phases progress, showing catastrophic forgetting. For example, atomic-task performance falls from **Phase 1: 41.5%** to **Phase 2: 13.9%**, **Phase 3: 13.9%**, and **Phase 4: 10.6%**; **2–3 stage** tasks in Phase 2 fall from **24.5%** to **1.7%** by Phase 4. This indicates that continual learning of long-horizon tasks remains very difficult.

## Link
- [http://arxiv.org/abs/2603.04356v1](http://arxiv.org/abs/2603.04356v1)
