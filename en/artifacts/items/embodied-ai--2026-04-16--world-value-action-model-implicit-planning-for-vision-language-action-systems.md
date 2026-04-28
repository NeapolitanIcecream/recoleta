---
source: arxiv
url: http://arxiv.org/abs/2604.14732v2
published_at: '2026-04-16T07:46:05'
authors:
- Runze Li
- Hongyin Zhang
- Junxi Jin
- Qixin Zeng
- Zifeng Zhuang
- Yiqi Tang
- Shangke Lyu
- Donglin Wang
topics:
- vision-language-action
- world-model
- implicit-planning
- latent-planning
- robot-manipulation
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# World-Value-Action Model: Implicit Planning for Vision-Language-Action Systems

## Summary
WAV adds implicit planning to vision-language-action systems by combining a learned future predictor, a trajectory value estimator, and an action decoder in one model. The paper claims this helps VLA policies handle longer tasks, compositional instructions, and real-world manipulation better than direct action prediction.

## Problem
- Standard VLA models usually predict the next action directly, which makes long-horizon, multi-step decisions brittle because they do not compare candidate futures.
- Direct planning in action space gets harder as the horizon grows; the paper argues the chance of sampling a feasible trajectory drops exponentially with horizon.
- World models alone predict futures, but they do not solve action selection unless the system can also score those futures and steer search toward good ones.

## Approach
- WAV uses three parts: a language-conditioned video/world model to predict future visual trajectories, a value module to score those predicted futures, and an action module that decodes actions from the predicted future plus value features.
- Instead of searching over raw action sequences, WAV searches in latent variables that generate future trajectories. The idea is that latent samples are more likely to decode into feasible behaviors.
- During inference, the model samples latent noise for future prediction and value estimation, scores candidates with a value-based signal-to-noise ratio, keeps elite samples, and updates the latent sampling distributions over several iterations.
- The language encoder is frozen T5-XXL, and the video, value, and action modules use DiT-style transformer blocks trained in stages with flow-matching losses.
- The paper also gives a theory claim: latent planning shifts probability mass toward feasible trajectories, while iterative refinement is needed to find high-value ones within that feasible set.

## Results
- The paper states that WAV consistently outperforms state-of-the-art baselines in simulation and real-world experiments on task success rate, generalization, and robustness.
- The main benchmark named in the excerpt is LIBERO, with four suites: Spatial, Object, Goal, and Long. The excerpt says WAV is tested with a single model across all four suites.
- The excerpt claims the gains are strongest in long-horizon and compositional scenarios.
- The excerpt includes theoretical scaling claims rather than empirical numbers: under the paper's assumptions, feasible-trajectory probability under action-space sampling decays as at most `exp(-cH)`, while the ratio of feasible probability under latent sampling versus uniform action sampling is at least `exp(cH)(1-δ)` as horizon `H` increases.
- The provided text does not include the actual experiment table values, success rates, or exact margins over baselines, so quantitative empirical results cannot be extracted from this excerpt.

## Link
- [http://arxiv.org/abs/2604.14732v2](http://arxiv.org/abs/2604.14732v2)
