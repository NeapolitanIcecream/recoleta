---
source: arxiv
url: https://arxiv.org/abs/2605.20774v1
published_at: '2026-05-20T06:15:30'
authors:
- Alex S. Huang
- Jiahui Zhang
- Shiqing Tang
- Yu Xiang
topics:
- vision-language-action
- real-world-evaluation
- robot-benchmark
- manipulation
- reproducibility
- vla-finetuning
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# VLA-REPLICA: A Low-Cost, Reproducible Benchmark for Real-World Evaluation of Vision-Language-Action Models

## Summary
VLA-REPLICA is a low-cost real-world benchmark for evaluating vision-language-action robot policies on reproducible manipulation tasks. It targets local lab evaluation instead of simulation-only tests or centralized robot evaluation services.

## Problem
- VLA models need real-world evaluation because simulation can overestimate performance when contact, lighting, camera pose, and object placement differ from the simulator.
- Existing real-world benchmarks often need costly hardware, focus on narrow task types, or require remote evaluation, which slows local testing.
- The paper addresses a practical gap: different labs need a way to run comparable VLA evaluations on physical robots without buying a high-end setup.

## Approach
- The benchmark uses off-the-shelf hardware: an SO-101 6-DoF arm, an Intel RealSense D455 top camera, a wrist webcam, a 32 inch light box, and commodity objects.
- Camera overlay tools, AprilTag alignment, fixed lighting, reference images, and predefined object placements let users recreate the same test scenes in different labs.
- The SO-101 action space is normalized through arm calibration, so demonstrations and policy actions can transfer across separately built arms.
- The task suite has 10 manipulation tasks covering pick-and-place, towel folding, opening an oven, whiteboard erasing, pouring or shaking, lifting, and button pressing.
- The dataset contains 500 expert demonstrations, with 50 demonstrations per task, and evaluation covers 50 in-distribution scenes plus 40 out-of-distribution scenes.

## Results
- The full hardware cost is about $1050, with listed parts including a ~$200 SO-101 arm, ~$425 RealSense D455, $13.98 webcam, $152.99 light box, and $215.99 object set.
- A user with no prior knowledge of the benchmark built the setup in under 1 hour, according to the paper's reproducibility check.
- The benchmark defines 90 total test scenes: 50 in-distribution scenes across 10 tasks and 40 out-of-distribution scenes across 8 tasks.
- All evaluated policies used the same 500 demonstrations and 40K training or fine-tuning steps.
- On 10 in-distribution tasks, average success rates were ACT 0.18, DiT-D 0.16, DiT-F 0.12, SmolVLA 0.26, X-VLA 0.14, π0 0.34, and π0.5 0.54.
- π0.5 had the best reported in-distribution average success rate at 0.54, with task-level scores including 1.0 on towel folding, 0.8 on putting bread on a plate, and 0.8 on putting a bowl on a coaster.

## Link
- [https://arxiv.org/abs/2605.20774v1](https://arxiv.org/abs/2605.20774v1)
