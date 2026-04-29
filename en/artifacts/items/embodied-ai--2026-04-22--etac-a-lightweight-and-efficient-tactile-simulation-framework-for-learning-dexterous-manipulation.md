---
source: arxiv
url: http://arxiv.org/abs/2604.20295v1
published_at: '2026-04-22T07:51:20'
authors:
- Zhe Xu
- Feiyu Zhao
- Xiyan Huang
- Chenxi Xiao
topics:
- tactile-simulation
- dexterous-manipulation
- reinforcement-learning
- sim2real
- robot-learning
relevance_score: 0.81
run_id: materialize-outputs
language_code: en
---

# ETac: A Lightweight and Efficient Tactile Simulation Framework for Learning Dexterous Manipulation

## Summary
ETac is a tactile simulation framework for dexterous manipulation that aims to keep FEM-like deformation quality without FEM-level cost. It combines a simple physics prior with a small learned correction model, then uses the simulated tactile field to train blind grasping policies at large RL scale.

## Problem
- Tactile RL needs many simulated interactions, but high-fidelity soft-body simulators such as FEM are too slow for large parallel training.
- Faster tactile simulators often only model local indentation and miss deformation propagation across the elastomer, which hurts realism, especially on curved sensor surfaces.
- This matters because modern tactile hands depend on rich contact patterns, not just binary contact or force signals, for stable dexterous manipulation.

## Approach
- ETac discretizes the tactile sensor surface into 3D nodes and detects contact with signed distance fields. Nodes in contact are "active" nodes.
- It estimates deformation of non-contacted "passive" nodes with two parts: an exponential distance-decay propagation term and a lightweight residual network.
- The decay term gives a fast physical prior for how indentation spreads across the elastomer surface.
- The residual network, built with a PointNet-style encoder and MLP decoder, corrects errors from the linear decay model and captures nonlinear effects such as curvature, anisotropy, and interaction between contact points.
- The propagation parameters are trained to match FEM-generated deformation data, then the resulting displacement field is used as tactile input for PPO on a blind grasping task with a ShadowHand.

## Results
- On deformation estimation against FEM ground truth, ETac reports the best RMSE among lightweight baselines: **0.058 ± 0.034 mm** on a flat elastomer and **0.116 ± 0.049 mm** on a curved elastomer, versus **TacSL: 0.194 / 0.445 mm** and **Taxim: 0.163 / 0.447 mm**.
- The full model beats its own ablations: linear-only gets **0.151 / 0.256 mm** RMSE and residual-only gets **0.074 / 0.128 mm** on flat/curved elastomers.
- For real sensor response prediction, data generated with ETac gives **3.94%** L1 loss on a flat sensor and **3.61%** on a curved sensor, compared with **2.46%** and **2.75%** using FEM data.
- In RL throughput on one RTX 4090, ETac supports **4,096 parallel environments** and reaches **869 total FPS** at that scale. The paper states this is **11×** higher FPS and **128×** more parallel environments than FEM on the same GPU.
- Reported total FPS for ETac is **669, 956, 878, 869** at **64, 256, 1024, 4096** environments. Taxim reaches **508, 620, 650** at **64, 256, 1024** and runs out of memory at **4096**; TacSL reaches **698, 975, 918, 886**.
- In blind grasping over four object types, the full-hand tactile setup reaches **84.45% ± 13.09** average success, compared with **72.90% ± 21.06** for fingertip sensors and **62.97% ± 37.82** for a non-tactile baseline using object pose. The paper highlights this as a **21.48 percentage point** gain over the baseline.

## Link
- [http://arxiv.org/abs/2604.20295v1](http://arxiv.org/abs/2604.20295v1)
