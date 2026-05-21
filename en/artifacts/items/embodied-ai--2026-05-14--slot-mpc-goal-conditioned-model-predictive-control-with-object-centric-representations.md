---
source: arxiv
url: https://arxiv.org/abs/2605.14937v1
published_at: '2026-05-14T15:12:15'
authors:
- Jonathan Spieler
- Angel Villar-Corrales
- Sven Behnke
topics:
- object-centric-world-model
- model-predictive-control
- robot-manipulation
- visual-planning
- offline-robot-data
- goal-conditioned-control
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Slot-MPC: Goal-Conditioned Model Predictive Control with Object-Centric Representations

## Summary
Slot-MPC uses object-level visual slots and a differentiable action-conditioned dynamics model to plan robot actions toward a goal image. The main claim is that object-centric latent planning improves manipulation success and planning efficiency over holistic world-model baselines in simulated tasks.

## Problem
- It targets visual goal-conditioned robot manipulation, where a robot must choose actions from images and a goal image.
- Reactive policies learned offline can fail when the start state or object layout differs from training data, which matters for long-horizon manipulation.
- Sampling-based MPC can require hundreds or thousands of candidate rollouts per control step, which raises planning cost.

## Approach
- A SAVi-style scene parser maps each image into slots, with each slot intended to encode one object or entity.
- A conditional object-centric video predictor, cOCVP, predicts future slots autoregressively from the current slots and action sequence.
- At test time, the goal image is encoded into goal slots; MPC searches for actions that make the predicted final slots close to the goal slots under an L2 cost.
- The method uses Hungarian matching before the slot-space cost so predicted and goal slots are compared by best object alignment.
- It tests both MPPI sampling-based MPC and gradient-based MPC; the gradient version backpropagates through the differentiable world model and can start from a behavior-cloned policy trained on expert demonstrations.

## Results
- The excerpt reports experiments on 4 simulated manipulation environments: Meta-World Button Press and Lever Pull, plus robosuite Stack and Square.
- Training uses 2 offline dataset types per environment: random exploration trajectories for the scene parser and dynamics model, and a small expert set for the warm-start policy.
- The paper claims slot representations reduce latent dimensionality by 99% compared with patch-based DINO-WM, which improves planning efficiency.
- The paper claims Slot-MPC improves task performance and planning efficiency over non-object-centric world-model baselines, including DINO-WM, and compares against GC-BC and Dreamer-v3.
- The excerpt does not include the success-rate table or exact task success percentages, so the strongest numeric claims available are the 4 environments, 2 dataset types, full-episode evaluation protocol, and 99% latent-size reduction.

## Link
- [https://arxiv.org/abs/2605.14937v1](https://arxiv.org/abs/2605.14937v1)
