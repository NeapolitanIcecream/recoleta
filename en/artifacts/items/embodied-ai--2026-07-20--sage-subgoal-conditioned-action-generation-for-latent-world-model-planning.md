---
source: arxiv
url: https://arxiv.org/abs/2607.17973v1
published_at: '2026-07-20T14:10:56'
authors:
- Letian Cheng
- Qi Zhang
- Yisen Wang
topics:
- latent-world-model
- long-horizon-planning
- subgoal-generation
- action-proposals
- robot-manipulation
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# SAGE: Subgoal-Conditioned Action Generation for Latent World Model Planning

## Summary
SAGE improves long-horizon goal-conditioned planning by using predicted latent subgoals to guide action proposals for a frozen latent world model. On PushT and OGBench Cube, it substantially increases success at distant goals while maintaining strong short-horizon performance.

## Problem
- Latent world-model planners evaluate imagined action sequences, but random or generic proposals cover too little of the action space as the planning horizon grows.
- Distant goals provide weak local guidance, making it difficult for a fixed candidate budget to find reachable, high-quality action sequences.
- This matters for long-horizon robot control, where proposal quality can limit performance even when the predictive world model remains fixed.

## Approach
- A variable-duration Transformer subgoal generator predicts a reachable latent state for the next 15, 20, or 25 steps using the observation history, current state, distant goal, remaining horizon, and requested duration.
- A second Transformer generates trajectory-level Gaussian-mixture action options conditioned on the predicted subgoal and the distant goal, replacing generic random initialization with structured proposals.
- The frozen LeWM latent world model evaluates the proposed futures, and cross-entropy method (CEM) refinement selects and improves the action sequence before execution.
- The planner executes each selected local option, observes the environment, predicts a new subgoal, and replans across multiple temporal stages.

## Results
- At horizon 150, full SAGE increases PushT success from 12.7% with LeWM to 64.7%, and OGBench Cube success from 26.7% to 67.3%; evaluations use the same frozen LeWM, 300 candidates, and 30 CEM rounds.
- On PushT, SAGE reaches 94.0% success at horizon 25 and 81.3% at horizon 50, compared with 56.0% and 12.7% for LeWM at the reported horizons; PRISM reaches 54.7% and 17.3%.
- On OGBench Cube, SAGE reaches 98.7% at horizon 25 and 85.3% at horizon 100, compared with 66.7% and 57.3% for LeWM.
- The generator-only ablation reaches 58.7% on PushT and 51.3% on Cube at horizon 150, while full SAGE reaches 64.7% and 67.3%, showing an additional benefit from subgoal-conditioned action proposals.
- Removing LeWM ranking and CEM refinement reduces PushT success at horizon 150 from 64.7% to 16.0%, indicating that learned proposals still require world-model-guided selection and refinement.
- Results come from PushT and OGBench Cube held-out trajectory queries with three evaluation manifests and 50 start-goal pairs per manifest; the excerpt does not establish performance beyond these benchmarks or against physical-robot and sim-to-real settings.

## Link
- [https://arxiv.org/abs/2607.17973v1](https://arxiv.org/abs/2607.17973v1)
