---
source: hn
url: https://arxiv.org/abs/2606.17030
published_at: '2026-06-18T23:28:34'
authors:
- gmays
topics:
- embodied-world-model
- language-conditioned-video
- robot-data-scaling
- generalist-robot-policy
- vision-language-action
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Unifying Embodied World Modeling Through Language-Conditioned Video Gen

## Summary
Qwen-RobotWorld is a language-conditioned video world model that predicts future visual trajectories for embodied agents across manipulation, driving, navigation, and human-to-robot settings. It matters because the same model can generate synthetic robot data, support policy evaluation, and provide planning signals for control.

## Problem
- Embodied agents need world models that predict how scenes change after actions, but robot data is split across embodiments, tasks, and action formats.
- Many robot policies cannot easily use data from driving, navigation, manipulation, and human demonstrations because the action spaces differ.
- Better predictive video models could reduce data collection cost and improve testing before running policies on real robots.

## Approach
- The paper uses natural language as the shared action interface: the model receives a current observation and a language-described action, then generates the future video trajectory.
- The core model is a 60-layer double-stream diffusion transformer that connects frozen Qwen2.5-VL semantic features with video-VAE latents through layer-wise joint attention.
- Training uses Embodied World Knowledge, an 8.6M video-text corpus with 200M+ frames, 20+ embodiments, and 500+ action categories.
- The training curriculum has two stages: learn general visual priors first, then specialize on embodied data under the same language-action format.

## Results
- The excerpt gives no raw benchmark scores, but it reports rank and comparison outcomes.
- Qwen-RobotWorld ranks 1st overall on EWMBench and DreamGen Bench.
- It outperforms all open-source models on WorldModelBench and PBench, according to the abstract.
- Zero-shot tests on RoboTwin-IF are reported to support generalization and multi-view consistency, but no numeric scores are included in the excerpt.
- The claimed training scale is 8.6M video-text samples and 200M+ frames across 20+ embodiments and 500+ action categories.

## Link
- [https://arxiv.org/abs/2606.17030](https://arxiv.org/abs/2606.17030)
