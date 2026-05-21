---
source: arxiv
url: https://arxiv.org/abs/2605.00078v1
published_at: '2026-04-30T14:16:15'
authors:
- Hao Luo
- Wanpeng Zhang
- Yicheng Feng
- Sipeng Zheng
- Haiweng Xu
- Chaoyi Xu
- Ziheng Xi
- Yuhui Fu
- Zongqing Lu
topics:
- latent-world-model
- vision-language-action
- robot-foundation-model
- egocentric-video
- robot-data-scaling
- generalist-robot-policy
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Being-H0.7: A Latent World-Action Model from Egocentric Videos

## Summary
Being-H0.7 trains a robot policy to use future video information during training while acting from current observations at test time. It targets the gap between direct VLA policies and video-rollout world-action models by moving future reasoning into latent tokens.

## Problem
- Direct VLA policies can learn shortcut mappings from observations to actions because action labels are sparse compared with visual input.
- Video-based world-action models add future prediction, but pixel rollout costs training and inference compute and may model visual detail that does not affect control.
- The problem matters for long-horizon and dynamic manipulation where contact, object motion, and task progress affect the next action.

## Approach
- The model inserts K=16 learnable latent queries between the multimodal context and the action chunk, so the Transformer builds a compact action-oriented state before predicting actions.
- Training uses two matched branches: a prior branch sees current instruction, H=4 observation frames, state, and latent queries; a posterior branch replaces those queries with embeddings from future observations.
- Future frames are encoded with a frozen ViT and Perceiver resampler into K embeddings, then aligned with the prior latent states over the last L=9 Transformer layers.
- Both branches train with a flow-matching action objective over T=20 action chunks, plus latent alignment and norm/rank regularizers to reduce latent collapse.
- At inference, the posterior branch is removed, so the policy predicts actions without generating future images.

## Results
- The excerpt claims state-of-the-art or comparable performance across 6 simulation benchmarks, but the provided text does not include the table values, metrics, or success rates.
- Real-world evaluation is reported on 3 robot platforms and 12 tasks covering dynamic scenes, physical reasoning, motion reasoning, long-horizon execution, and generalization.
- The paper claims Being-H0.7 leads all 5 ability-oriented real-world suites, with examples including catching a fast rolling ball, pouring into a moving container, folding garments, conveyor package sorting, and hammering a nail.
- Deployment with latency-aware universal asynchronous chunking is reported at 3-4 ms/step for Being-H variants, with no test-time future-frame generation.

## Link
- [https://arxiv.org/abs/2605.00078v1](https://arxiv.org/abs/2605.00078v1)
