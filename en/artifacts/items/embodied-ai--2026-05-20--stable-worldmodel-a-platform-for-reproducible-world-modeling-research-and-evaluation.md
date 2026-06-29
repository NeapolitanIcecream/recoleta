---
source: arxiv
url: https://arxiv.org/abs/2605.21800v1
published_at: '2026-05-20T22:58:15'
authors:
- Lucas Maes
- Quentin Le Lidec
- Luiz Facury
- Nassim Massaudi
- Ayush Chaurasia
- Francesco Capuano
- Richard Gao
- Taj Gillin
- Dan Haramati
- Damien Scieur
- Yann LeCun
- Randall Balestriero
topics:
- world-model
- robotics-benchmark
- reproducibility
- mpc-planning
- data-loading
- ood-evaluation
relevance_score: 0.66
run_id: materialize-outputs
language_code: en
---

# stable-worldmodel: A Platform for Reproducible World Modeling Research and Evaluation

## Summary
stable-worldmodel is an open-source platform for reproducible world-model research, covering data loading, baseline training, MPC planning, and controlled evaluation. The paper contributes shared infrastructure and benchmark coverage, with no new world-model architecture.

## Problem
- World-model papers often use separate codebases, data pipelines, planners, and evaluation setups, which makes results hard to compare.
- Video-heavy world-model training needs fast access to temporal blocks of frames, actions, and sensor streams; common formats such as MP4 and HDF5 can stall training.
- Standard simulator benchmarks often test settings close to the training distribution, so they can miss failures under changes in appearance, geometry, or physics.

## Approach
- swm uses a Lance-based data layer with conversion support for MP4, HDF5, and LeRobot datasets.
- It defines three main interfaces: World for Gymnasium-style environments and perturbations, Policy for action selection, and Solver for MPC planning.
- It includes tested implementations of world-model baselines such as DINO-WM, LeWorldModel, PLDM, and TD-MPC2, plus planning solvers such as CEM, iCEM, MPPI, gradient descent, projected gradient descent, and GRASP.
- Its benchmark suite covers Classic Control, MuJoCo, Atari, robotics tasks, OGBench, Push-T, and Craftax, with controllable visual, geometric, and physical factors of variation.

## Results
- On Push-T data loading, Lance local reaches 4,815 samples/s without caching, compared with HDF5 local at 1,416 samples/s and video local at 1,331 samples/s.
- For S3 streaming on Push-T, Lance reaches 3,184 samples/s without caching and 3,253 samples/s with caching; HDF5 over S3 reaches 9 samples/s without caching and 757 samples/s with caching.
- In the baseline comparison, Push-T success rates are TD-MPC2 12%, GCBC 75%, LeWM 94%, PLDM 78%, and DINO-WM 92%.
- On OGB-Cube, success rates are TD-MPC2 4%, GCBC 84%, LeWM 72%, PLDM 62%, and DINO-WM 86%.
- The paper reports zero-shot and out-of-distribution evaluation tools, but the provided excerpt gives no full quantitative OOD table; the concrete claim is that prediction MSE overlaps between successful and failed Push-T planning runs across 256 trajectories per setting, so raw prediction error is a weak indicator of planning success.

## Link
- [https://arxiv.org/abs/2605.21800v1](https://arxiv.org/abs/2605.21800v1)
