---
source: arxiv
url: https://arxiv.org/abs/2607.19719v1
published_at: '2026-07-22T03:38:15'
authors:
- Jiaqi Li
- Xinglong Zhang
- Haibin Xie
- Yixing Lan
- Wei Pan
- Xin Xu
topics:
- world-model
- model-based-reinforcement-learning
- koopman-dynamics
- latent-imagination
- continuous-control
- autonomous-navigation
relevance_score: 0.62
run_id: materialize-outputs
language_code: en
---

# Koopman Dreamer: Spectrally Constrained Latent Dynamics for Stable World-Model Imagination

## Summary
Koopman Dreamer adds a spectrally constrained deterministic latent transition to a DreamerV3-style world model to make long-horizon imagination more stable. It reports improved simulated continuous-control performance, including gains on eight of nine DeepMind Control Suite tasks and a UAV-LiDAR target-success increase from 53.8% to 73.8%.

## Problem
- Generic neural latent transitions do not directly control modal persistence, damping, or oscillation, making long-horizon rollout errors difficult to regulate and diagnose.
- Error accumulation can bias imagined returns, policy updates, and control decisions, especially in continuous-control and autonomous-navigation tasks.
- Excessive contraction can also erase information needed for control, so stability must be balanced against long-term information retention.

## Approach
- Replace the conventional DreamerV3 deterministic recurrent transition with a Koopman-inspired backbone made of two-dimensional rotation–scaling blocks whose modal radii are bounded by a chosen spectral range.
- Add linear action effects, a low-rank bilinear state–action term, and stochastic-state modulation so the structured backbone can represent controlled nonlinear dynamics and local posterior corrections.
- Train the same transition for posterior-conditioned learning and posterior-free imagination using EMA teacher targets, one-step consistency, multi-step rollout, and open-loop observation-prediction objectives.
- Derive a multi-step rollout-error bound that separates autonomous spectral amplification, bilinear interaction effects, stochastic-state mismatch, and modeling residuals.

## Results
- On proprioceptive continuous-control tasks, Koopman Dreamer outperformed DreamerV3 on 8 of 9 tasks in simulation.
- In simulated UAV navigation with vectorized LiDAR observations, target success increased from 53.8% with DreamerV3 to 73.8% with Koopman Dreamer, a 20.0 percentage-point improvement.
- Open-loop evaluations showed the most consistent gains in proprioceptive observation and velocity prediction; reward prediction improved on most tasks.
- Spectral-radius sensitivity and ablation studies supported roles for modal contraction, EMA teacher targets, and state-dependent action effects, while indicating that the most contractive setting is not necessarily best for control.
- The reported validation is simulation-based; the excerpt provides no physical-robot results or complete task-by-task metric tables.

## Link
- [https://arxiv.org/abs/2607.19719v1](https://arxiv.org/abs/2607.19719v1)
