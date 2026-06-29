---
source: arxiv
url: https://arxiv.org/abs/2606.26095v1
published_at: '2026-06-24T17:59:56'
authors:
- Dong Jing
- Tianqi Zhang
- Jiaqi Liu
- Jinman Zhao
- Zelong Sun
- Li Erran Li
- Zhiwu Lu
- Mingyu Ding
topics:
- vision-language-action
- cross-embodiment
- action-priors
- robot-manipulation
- flow-matching
- history-compression
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Learning Action Priors for Cross-embodiment Robot Manipulation

## Summary
The paper proposes pretraining the VLA action module on action-only robot trajectories before vision-language-action training. The goal is to give the policy a motion prior so cross-embodiment VLA training starts with an action head that already models temporal robot motion.

## Problem
- Standard VLA models inherit visual and language priors from a VLM, while the action module often starts from random weights or unrelated modality weights.
- Early VLA training must learn action dynamics and visual-language-to-action alignment at the same time, which can slow convergence and produce unstable gradients.
- Cross-embodiment training makes this harder because robots have different action spaces, control conventions, and motion distributions.

## Approach
- Stage 1 trains a Transformer encoder-decoder action module using only state-action trajectories, with no images or language.
- The encoder compresses an interleaved state-action sequence into one normalized latent action embedding.
- The decoder reconstructs the action chunk from that latent using a flow-matching loss, learning a continuous action distribution over robot motion.
- Stage 2 reuses the pretrained decoder as the VLA action head and trains the VLM to predict the action latent from vision, language, dataset prompts, and a query token.
- Early VLA training adds a decaying latent distillation loss from the Stage 1 encoder, and the same encoder can compress past state-action history into one context token.

## Results
- The evaluation covers 13 cross-embodiment manipulation tasks across 2 simulated benchmarks, LIBERO and RoboCasa, plus 1 real-world Franka platform.
- The paper claims higher success rates and faster convergence than VLA training without action priors, but the excerpt gives no exact success-rate or convergence-step numbers.
- The authors report stronger gains on data-scarce real-world tasks, especially long-tail tasks with few demonstrations, but the excerpt gives no per-task numeric results.
- Scaling the amount of action-only data in Stage 1 is reported to improve downstream VLA performance, but the excerpt gives no scaling curve or dataset-size numbers.
- History compression is claimed to help long-horizon tasks by adding a single history token, with negligible added cost, but no quantitative token, latency, or success-rate numbers are included in the excerpt.

## Link
- [https://arxiv.org/abs/2606.26095v1](https://arxiv.org/abs/2606.26095v1)
