---
source: arxiv
url: https://arxiv.org/abs/2607.14021v1
published_at: '2026-07-15T16:54:28'
authors:
- Honglu He
- Jacob Laufer
- Zhiwu Zheng
- David Elkan-gonzalez
- Raman Goyal
- Xinyi Li
- Su Lu
- Mishek Musa
- Berke Saat
- Nicolas Tan
- Colm Prendergast
topics:
- dexterous-manipulation
- robot-learning
- diffusion-policy
- multimodal-sensing
- industrial-robotics
- robot-benchmark
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Industrial Dexterity Benchmark: A Hardware-Software Benchmarking Platform for Industrial Dexterous Manipulation

## Summary
The paper introduces the Industrial Dexterity Benchmark (IDB), a hardware platform for testing industrial manipulation, together with imitation-learning infrastructure and a multimodal diffusion policy. On the datacenter cable-cleaning task evaluated here, the best sensor configuration achieved 78% combined grasp-and-insert success using about 100 teleoperated demonstrations per task phase.

## Problem
- Industrial tasks such as cable routing, connector insertion, and precision assembly remain difficult to automate because they combine tight clearances, deformable objects, occlusion, and contact-rich control.
- The problem matters because datacenter maintenance operates in densely populated racks with uptime targets above 99.99%, while classical vision-and-control pipelines can be brittle and costly to recalibrate for small task changes.

## Approach
- The authors design three low-cost IDB boards for datacenter cable manipulation, automotive cable harnesses, and gearbox assembly; this paper reports experiments only on the datacenter board.
- DAG-ROS provides ROS2-based teleoperation, time-aligned sensor collection, real-time control, dataset processing, and deployment infrastructure.
- AG-iDP3 combines RGB features from R3M, point-cloud features from PointNet, joint positions, and wrist force/torque data in a diffusion U-Net that predicts 15-action chunks; successive chunks are temporally ensembled into 50 Hz commands.
- A modality-gating mechanism supports sensor ablations and phase-specific inputs. Wrist wrench data was retained for insertion, where contact information helped, and gated off for grasp and cleaning.

## Results
- On the IDB Board #1 cable-cleaning task, evaluated with 48 trials per configuration, the best multimodal expansion Diffusion Policy reached 78% combined grasp-and-insert success.
- The 78% result exceeded the single-camera RGB Diffusion Policy baseline, which achieved 36% success, an absolute improvement of 42 percentage points.
- Each tested policy required approximately 100 teleoperated demonstrations per task phase.
- The evaluated model variants ranged from 68.8 million parameters for point-cloud-only iDP3 to 114.9 million for the two-camera RGB Diffusion Policy; the combined point-cloud-plus-RGB model used 94.6 million parameters.
- The reported evidence covers one task on IDB Board #1; the automotive cable-harness and gearbox boards are proposed benchmarks whose performance is reserved for future work.

## Link
- [https://arxiv.org/abs/2607.14021v1](https://arxiv.org/abs/2607.14021v1)
