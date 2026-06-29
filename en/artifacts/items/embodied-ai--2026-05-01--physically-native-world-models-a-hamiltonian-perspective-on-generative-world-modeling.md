---
source: arxiv
url: https://arxiv.org/abs/2605.00412v1
published_at: '2026-05-01T05:09:32'
authors:
- Sen Cui
- Jingheng Ma
topics:
- hamiltonian-dynamics
- world-models
- embodied-ai
- model-based-planning
- robotics
- physical-priors
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Physically Native World Models: A Hamiltonian Perspective on Generative World Modeling

## Summary
The paper argues that embodied world models need physically structured latent dynamics for action-conditioned prediction. It proposes Hamiltonian World Models, which encode observations into phase-space variables, evolve them with Hamiltonian-inspired dynamics, decode future observations, and use rollouts for planning.

## Problem
- Robots and autonomous agents need predictions that stay physically feasible under actions, because planning from bad rollouts can choose unsafe or failing actions.
- Current 2D video models, 3D scene models, and JEPA-like latent models optimize different targets and can miss contact, momentum, object permanence, action effects, or long-horizon stability.
- Generic latent transitions such as z_{t+1}=fθ(z_t,a_t) often entangle appearance, semantics, and motion, which raises data needs and makes errors compound over planning horizons.

## Approach
- The core mechanism is simple: encode past observations into a latent phase state z_t=[q_t,p_t], where q holds generalized coordinates and p holds generalized momenta.
- Learn an energy-like scalar H(q,p), then derive latent motion from its gradients: qdot=∂H/∂p and pdot=-∂H/∂q.
- Add action control, dissipation, and residual terms so the model can handle robots, friction, contact, impacts, and other non-conservative effects.
- Decode the predicted latent trajectory into future observations, then score candidate action sequences with a utility function for planning.
- The proposed architecture has 4 named parts: encoder Eθ, Hamiltonian rollout T_H, decoder Dθ, and planner or utility U.

## Results
- The excerpt reports 0 benchmark numbers, 0 dataset results, and 0 direct comparisons against baselines.
- The main claimed contribution is conceptual: it groups current world models into 3 routes, 2D video-generative, 3D scene-centric, and JEPA-like latent prediction, and identifies their physical modeling gaps.
- It claims Hamiltonian structure can improve long-horizon stability by preserving phase-space structure, especially when paired with symplectic integration; no rollout-length metric is provided.
- It claims better data efficiency because one learned energy function can constrain dynamics across initial conditions; no sample-efficiency number is provided.
- It claims better interpretability because latent variables map to phase coordinates, momenta, energy variation, and interaction terms; no user study or diagnostic benchmark is reported.

## Link
- [https://arxiv.org/abs/2605.00412v1](https://arxiv.org/abs/2605.00412v1)
