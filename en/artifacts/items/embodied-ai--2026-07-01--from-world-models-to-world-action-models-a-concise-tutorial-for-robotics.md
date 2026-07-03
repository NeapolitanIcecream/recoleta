---
source: arxiv
url: https://arxiv.org/abs/2607.00836v2
published_at: '2026-07-01T11:56:54'
authors:
- Xiaoxiong Zhang
- Xiong Zeng
- Wei Zhang
topics:
- world-models
- world-action-models
- robotics
- vision-language-action
- policy-learning
- embodied-ai
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# From World Models to World Action Models: A Concise Tutorial for Robotics

## Summary
This tutorial argues that robot world models should be defined as action-conditioned predictors of future observations or states. It adds the idea of world action models, where predicted futures are linked to executable robot actions.

## Problem
- Robotics papers use the term "world model" for many different systems, including latent dynamics models, video predictors, physics simulators, and action-conditioned generative models, which makes comparison hard.
- A predictor that shows a likely future does not by itself tell a robot which action to execute, so visual prediction needs a path to control.
- The choice of prediction target, observation type, and action type affects visual fidelity, spatial structure, physical meaning, and control use.

## Approach
- The paper defines a world as the task-relevant robot, objects, and environment, then defines a world model as a model that predicts future observations or states conditioned on observation history and action.
- It splits world models into 2 main classes: observation-space models that predict future observations, and state-space models that predict compact or structured states.
- It organizes observation-space models by 2 axes: observation spatial explicitness, such as RGB, RGB-D, and point clouds, and action abstraction, such as low-level robot commands, latent actions, and language instructions.
- It organizes state-space models by the state type: latent vectors, point tracks, neural-symbolic predicates, and physical variables.
- It defines world action models as policies that model future observations and action sequences together, then groups them into 4 paradigms: imagine-then-execute, video-feature-conditioned action prediction, joint video-action modeling, and auxiliary video prediction for policy learning.

## Results
- The excerpt provides no new quantitative benchmark results, accuracy numbers, success rates, or dataset-scale measurements.
- The main concrete output is a 2-part taxonomy of world models: observation-space prediction and state-space prediction.
- The observation-space taxonomy uses 4 observation levels: RGB, multi-view RGB, RGB-D, and point clouds.
- The action-conditioning taxonomy uses 4 action levels: low-level robot actions, interface actions, latent actions, and language instructions.
- The state-space taxonomy lists 4 state choices: latent states, point tracks, neural-symbolic predicates, and physical states.
- The world action model taxonomy lists 4 ways to connect predicted futures to robot actions: 2-stage visual subgoal execution, feature-conditioned action prediction, joint video-action generation, and auxiliary video prediction during policy training.

## Link
- [https://arxiv.org/abs/2607.00836v2](https://arxiv.org/abs/2607.00836v2)
