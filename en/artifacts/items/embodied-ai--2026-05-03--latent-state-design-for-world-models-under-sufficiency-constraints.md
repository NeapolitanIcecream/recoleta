---
source: arxiv
url: https://arxiv.org/abs/2605.01694v1
published_at: '2026-05-03T03:19:42'
authors:
- Keon Woo Kim
topics:
- world-models
- latent-state
- sufficiency-constraints
- model-based-rl
- robot-planning
- counterfactual-reasoning
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Latent State Design for World Models under Sufficiency Constraints

## Summary
The paper argues that world-model research should be judged by what the latent state must preserve for a task. It proposes a function-based taxonomy and an evaluation scheme for checking whether a latent state supports prediction, control, planning, memory, grounding, or counterfactual reasoning.

## Problem
- World model is used for different systems: model-based RL, video prediction, generative simulation, object-centric modeling, robotics, and VLA planning. The shared issue is latent state design, since each system needs the state to keep different information.
- The paper says common comparisons are misleading when they group methods by architecture. A good video predictor can fail at control, and a compact control state can discard details needed for image reconstruction.
- This matters for embodied agents because planning and action need states that track reachability, value, interventions, memory, and hidden world state under partial observability.

## Approach
- The paper defines a latent world model as a learned state-update system: it maps history to a latent state, written as z_t = phi(h_t), and learns action-conditioned dynamics, written as p_theta(z_{t+1} | z_t, a_t).
- It groups methods by 6 latent-state roles: predictive embedding, recurrent belief state, object/causal structure, latent action interface, grounded planning interface, and memory substrate.
- It formalizes 3 sufficiency relationships: exact belief states subsume prediction and control under POMDP assumptions; predictive sufficiency does not guarantee control sufficiency; passive prediction does not identify counterfactual dynamics without interventions, action data, causal assumptions, or grounding.
- It proposes evaluation along 7 axes: representation, prediction, planning, controllability, causal/counterfactual support, memory, and uncertainty.
- It maps methods onto a compression spectrum, including reconstruction-heavy models, token compression, representation prediction, reward/value-shaped models, value-equivalent models, and causal/counterfactual models.

## Results
- The excerpt reports no new benchmark accuracy, return, success-rate, or dataset-scale numbers.
- The main concrete claim is a 6-role taxonomy for latent world models, covering predictive, belief-state, structured, action-interface, planning-interface, and memory roles.
- The paper gives 3 propositions that separate belief-state sufficiency, predictive sufficiency, control sufficiency, and counterfactual sufficiency.
- It gives a 7-axis evaluation matrix intended to diagnose what a latent state preserves, discards, and enables.
- It lists benchmark tests for 3 common failure modes: occlusion/revisitation/delayed-cue tests for belief state; frozen/adapted control and sparse-reward planning tests for control sufficiency; held-out action substitutions and object interventions for counterfactual support.
- Its literature map spans 2018-2026 examples, including World Models, SimPLe, IRIS, GAIA-1, I-JEPA, V-JEPA 2, LeWorldModel, MuZero, EfficientZero, TD-MPC2, Causal-JEPA, and CausalVAE-WM.

## Link
- [https://arxiv.org/abs/2605.01694v1](https://arxiv.org/abs/2605.01694v1)
