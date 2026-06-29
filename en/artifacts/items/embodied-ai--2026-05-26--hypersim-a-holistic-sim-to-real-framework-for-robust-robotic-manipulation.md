---
source: arxiv
url: https://arxiv.org/abs/2605.26638v1
published_at: '2026-05-26T07:19:04'
authors:
- Junyi Dong
- Haotian Luo
- Ziwei Xu
- Shengwei Bian
- Heng Zhang
- Sitong Mao
- Jingyi Guo
- Yang Xu
- Wenhao Chen
- Qiuyu Feng
- Yao Mu
- Ping Luo
- Shunbo Zhou
- Xiaodong Wu
topics:
- sim2real
- robot-manipulation
- synthetic-data
- vision-language-action
- robot-data-scaling
- gaussian-splatting
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# HyperSim: A Holistic Sim-To-Real Framework For Robust Robotic Manipulation

## Summary
HyperSim is a sim-to-real pipeline for robotic manipulation that combines high-fidelity scene rendering, adversarial synthetic trajectories, and sim-real co-training. It targets data scaling for robot policies while keeping real-world data collection small.

## Problem
- Robot policies need paired observation-action data, and collecting that data on hardware is slow, costly, and hard to scale.
- Standard simulation data often transfers poorly because scenes look too clean, object and pose coverage is narrow, and contact dynamics differ from real hardware.
- This matters because poor transfer forces teams to collect more real demonstrations or retune systems for each deployment setting.

## Approach
- HyperSim splits the scene into an interactive foreground and a reconstructed background. The foreground uses constraint-based object layout with 18 spatial solvers; the background uses geometry-aware 3D Gaussian Splatting with LiDAR, RGB, and IMU data.
- It generates trajectories by breaking manipulation into motion and interaction primitives around a bottleneck pose near the target object.
- During synthetic trajectory generation, it perturbs the target position and orientation at the bottleneck pose, then records recovery motions. This gives the policy examples of correction behavior.
- It trains ACT and pi0 with behavior cloning on simulation-only data for zero-shot deployment, then mixes simulation data with 35 real demonstrations for few-shot co-training.

## Results
- The study reports more than 400 real-world task executions on a Galaxea R1 robot, using a deep-bin sorting task with 20 fixed evaluation trials.
- In zero-shot transfer, 3DGS-ADSim reached 25% overall success rate (SR3) with ACT, compared with 5% for BaseSim. With pi0, 3DGS-ADSim reached 75% SR3, compared with 55% for BaseSim.
- In few-shot co-training with 35 real demonstrations, Real35&3DGS-ADSim reached 80% SR3 with ACT and 95% SR3 with pi0.
- The same few-shot setting reached 85% target alignment rate with ACT and 95% target alignment rate with pi0.
- Real-only baselines with 35 demonstrations reached 60% SR3 for ACT and 70% SR3 for pi0, below the mixed sim-real HyperSim results.
- The paper claims adversarial trajectories improve completion under physical perturbations by 35%.

## Link
- [https://arxiv.org/abs/2605.26638v1](https://arxiv.org/abs/2605.26638v1)
