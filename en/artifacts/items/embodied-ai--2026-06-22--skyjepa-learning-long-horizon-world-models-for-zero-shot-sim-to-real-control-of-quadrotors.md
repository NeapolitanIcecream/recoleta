---
source: arxiv
url: https://arxiv.org/abs/2606.23444v1
published_at: '2026-06-22T15:00:59'
authors:
- Pratyaksh Rao
- Wancong Zhang
- Randall Balestriero
- Yann LeCun
- Giuseppe Loianno
topics:
- quadrotor-control
- world-models
- sim2real
- latent-dynamics
- model-based-control
- jepa
relevance_score: 0.76
run_id: materialize-outputs
language_code: en
---

# SkyJEPA: Learning Long-Horizon World Models for Zero-Shot Sim-to-Real Control of Quadrotors

## Summary
SkyJEPA trains a JEPA-style latent world model for quadrotor control, then uses it inside a sampling-based controller for zero-shot sim-to-real flight. The paper targets long-horizon prediction without state reconstruction at every step.

## Problem
- Learned quadrotor dynamics models often predict the next state autoregressively, so small one-step errors compound over long control horizons.
- A controller needs predictions in physical state variables such as position, velocity, attitude, and angular velocity, not only abstract embeddings.
- Real quadrotor data collection is costly and can damage hardware, especially for aggressive maneuvers and platform changes.

## Approach
- The model encodes a history window of states and actions into latent vectors, then predicts future latent states over a horizon instead of reconstructing full future states.
- Training uses a multi-step latent prediction loss plus SIGReg, an anti-collapse regularizer that pushes latent embeddings toward an isotropic Gaussian through random 1D projections.
- A second-stage physics-inspired prober freezes the latent model and maps predicted latents to metric states through residual-corrected kinematics.
- The prober predicts residual translational acceleration in R^3 and a 3x4 residual angular-acceleration map tied to the 4 rotor forces.
- The learned model is placed inside a sampling-based optimal controller and trained on domain-randomized simulation data for zero-shot outdoor deployment.

## Results
- The provided excerpt gives no exact metric values, dataset sizes, baseline scores, or closed-loop success rates.
- Claimed evaluations include open-loop prediction tests and outdoor closed-loop flight experiments.
- Claimed comparisons include current dynamics learning baselines and ablations over key design choices, but the excerpt does not give numeric deltas.
- Claimed effects are improved long-horizon prediction, real-time execution on embedded hardware, and zero-shot sim-to-real transfer across trajectories and platform variations.
- Concrete numeric details in the method include a quadrotor action vector with 4 motor forces, state terms for 3D position, 3D velocity, SO(3) attitude, and 3D angular velocity, plus a 3x4 residual angular map in the prober.

## Link
- [https://arxiv.org/abs/2606.23444v1](https://arxiv.org/abs/2606.23444v1)
