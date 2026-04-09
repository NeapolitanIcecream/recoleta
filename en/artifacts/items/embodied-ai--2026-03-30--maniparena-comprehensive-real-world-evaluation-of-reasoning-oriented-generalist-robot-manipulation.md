---
source: arxiv
url: http://arxiv.org/abs/2603.28545v1
published_at: '2026-03-30T15:06:41'
authors:
- Yu Sun
- Meng Cao
- Ping Yang
- Rongtao Xu
- Yunxiao Yan
- Runze Xu
- Liang Ma
- Roy Gan
- Andy Zhai
- Qingxuan Chen
- Zunnan Xu
- Hao Wang
- Jincheng Yu
- Lucy Liang
- Qian Wang
- Ivan Laptev
- Ian D Reid
- Xiaodan Liang
topics:
- robot-benchmark
- vision-language-action
- generalist-robot-policy
- mobile-manipulation
- real-to-sim
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# ManipArena: Comprehensive Real-world Evaluation of Reasoning-Oriented Generalist Robot Manipulation

## Summary
ManipArena is a real-world benchmark for generalist robot manipulation, aimed at evaluating reasoning-heavy Vision-Language-Action and world-model systems under standardized physical conditions. It builds a shared evaluation setup with diverse tasks, controlled out-of-distribution tests, rich sensor streams, and matched simulation counterparts.

## Problem
- Existing robot benchmarks lean on simulation, so they miss real deployment issues such as perception noise, contact dynamics, latency, and hardware limits.
- Real-world evaluations are often run on different robots and lab setups, which makes comparisons hard to reproduce and hard to interpret.
- Generalist robot models need tests for semantic reasoning, spatial generalization, and long-horizon mobile manipulation, but prior benchmarks only cover parts of that space.

## Approach
- The benchmark defines **20 real-world tasks** across execution reasoning, semantic reasoning, and mobile manipulation, backed by **10,812 expert trajectories** collected over about **188 hours**.
- It uses a **single shared robot embodiment** and a **server-side inference protocol** where each participant submits **one model endpoint for all tasks**, so scores reflect policy quality rather than custom hardware or per-task specialization.
- Evaluation runs inside a **green-screen enclosed booth** with fixed lighting to isolate controlled variables, and uses a **stratified 10-trial design** per task: **T1-T4** in-domain, **T5-T8** shifted but in-distribution, **T9-T10** semantic OOD when available.
- Training diversity is designed along **three levels**: physical attributes, spatial layouts, and semantic composition, with explicit train/test separation for OOD objects.
- The benchmark also includes **rich observations** such as joint velocity and motor current, plus **Real2Sim** environments built with **3D Gaussian Splatting**, **Hunyuan3D** assets, and **IsaacLab** replay alignment.

## Results
- The excerpt does **not provide benchmark scores or baseline performance numbers**, so there are no quantitative model comparisons to report.
- The paper claims broader coverage than prior benchmarks: **20 tasks** total, including **10 execution**, **5 semantic**, and **5 mobile** tasks.
- The dataset contains **10,812 trajectories** and about **188 hours** of data.
- Mobile tasks are much longer than tabletop tasks: **2,878 vs. 665 average frames at 20 fps**, or about **4.3×** longer, and they make up **60.6%** of total dataset frames while accounting for **26.7%** of trajectories.
- Tabletop tasks use **56D** state/action per frame; mobile tasks use **62D**. Full collection records **112D** per frame before release-time filtering.
- Tabletop evaluation uses **15 tasks** scored over **10 trials** each, with **0-10 points per trial**, for up to **100 points per task** and **1,500 total points** across those evaluated tabletop tasks.

## Link
- [http://arxiv.org/abs/2603.28545v1](http://arxiv.org/abs/2603.28545v1)
