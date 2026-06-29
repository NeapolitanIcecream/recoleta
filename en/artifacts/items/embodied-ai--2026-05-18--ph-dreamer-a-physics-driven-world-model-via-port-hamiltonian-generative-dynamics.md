---
source: arxiv
url: https://arxiv.org/abs/2605.18303v1
published_at: '2026-05-18T12:20:54'
authors:
- Xueyu Luan
- Chenwei Shi
topics:
- world-model
- model-based-rl
- port-hamiltonian
- visual-control
- energy-regularization
- physics-informed-rl
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# PH-Dreamer: A Physics-Driven World Model via Port-Hamiltonian Generative Dynamics

## Summary
PH-Dreamer adds Port-Hamiltonian energy structure to an RSSM world model so imagined rollouts follow learned flow, dissipation, and action power signals. On six DeepMind Control visual tasks, it reports higher returns than DreamerV3 and R2Dreamer while reducing phase-space volume, energy use, and jerk.

## Problem
- RSSM world models such as Dreamer and R2Dreamer learn visual dynamics without explicit energy or dissipation structure, so long imagined rollouts can drift away from physical behavior.
- Physics-informed RL methods often need hand-written equations, low-dimensional states, or differentiable simulators, which limits their use in visual control tasks.
- The problem matters because model-based agents train policies inside their learned simulators; wrong imagined dynamics can reduce real-environment return and produce wasteful or jerky control.

## Approach
- The method splits the deterministic RSSM state into a physical part and a residual environment part, then projects the physical part into a low-dimensional phase space.
- A Port-Hamiltonian shadow transition predicts the next projected latent using a learned Hamiltonian, flow matrix, dissipation matrix, and action input matrix; the main RSSM remains the backbone, and the PH loss regularizes the projected dynamics.
- The PH loss is trained with RK4 integration and an annealed weight, so the visual model learns useful features before stronger physical regularization is applied.
- A separate energy model estimates momentum from recent joint-coordinate history, computes kinetic and potential energy, and predicts action-induced energy change through work and dissipation terms.
- The actor-critic stage adds Lagrange-multiplier constraints on predicted energy change and Hamiltonian curvature along the action direction to favor lower-energy, smoother actions.

## Results
- On six DeepMind Control visual tasks at 500k steps, PH-Dreamer reports the best average evaluation return: 789.2, compared with R2Dreamer 762.5, DreamerV3 735.1, Dreamer-INFO 698.3, HRSSM 695.5, and DreamerPro 679.9.
- Per-task evaluation returns for PH-Dreamer are Cheetah Run 798.6, Walker Stand 974.7, Reacher Easy 985.1, Hopper Hop 314.8, Walker Walk 967.2, and Walker Run 694.8; all are higher than the listed baselines in Table 1.
- Imagined reward average is 738.9, compared with R2Dreamer 702.5 and DreamerV3 689.1, which supports the paper's claim that imagined rewards align better with evaluation performance.
- Projected log phase volume drops versus R2Dreamer by 7.35% on Cheetah Run, 4.18% on Walker tasks, 8.00% on Reacher Easy, and 8.41% on Hopper Hop.
- The abstract reports energy consumption reductions of up to 7.80% and mean squared jerk reductions of up to 9.38%.
- The paper claims the learned energy model tracks MuJoCo ground-truth mechanical energy across six DMC tasks, but the provided excerpt does not include numeric energy-prediction error values.

## Link
- [https://arxiv.org/abs/2605.18303v1](https://arxiv.org/abs/2605.18303v1)
