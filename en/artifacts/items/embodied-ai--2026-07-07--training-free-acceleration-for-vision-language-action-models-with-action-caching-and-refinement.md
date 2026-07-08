---
source: arxiv
url: https://arxiv.org/abs/2607.06370v1
published_at: '2026-07-07T15:10:15'
authors:
- Ryuji Oi
- Hikari Otsuka
- Kosuke Matsushima
- Yuki Ichikawa
- Masato Motomura
- Tatsuya Kaneko
- Daichi Fujiki
topics:
- vision-language-action
- robot-policy-acceleration
- action-caching
- flow-matching
- robot-manipulation
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Training-Free Acceleration for Vision-Language-Action Models with Action Caching and Refinement

## Summary
ActionCache speeds up flow-based vision-language-action models by retrieving past action chunks and refining them with few or no action-head steps. It targets real-time robot control, where iterative flow matching adds large inference latency.

## Problem
- Flow-based VLA models generate continuous action chunks through repeated action-head evaluations, which slows closed-loop robot control.
- The paper reports that the action head accounts for 37-66% of end-to-end latency on representative VLA models.
- Simple NFE reduction hurts task success because the model starts from noise and has too few refinement steps.

## Approach
- ActionCache stores intermediate action chunks from successful past generations, paired with compact keys built from VLM output embeddings and, for GR00T-N1.6, encoded robot-state features.
- At inference time, it projects the current multimodal context into a 500-dimensional sparse random key and retrieves the nearest cache entry by cosine similarity.
- If similarity passes a threshold, the retrieved action chunk is executed directly or refined for 1-2 flow steps under the current context.
- If similarity is too low, the system falls back to the original full-step generation from Gaussian noise.
- The method needs no retraining and does not change the VLA backbone or action head.

## Results
- On VLABench with π0.5, the full base model gets 38.8% success at 18.8 ms action-head latency. ActionCache with NFE=0 gets 32.9% success at 1.6 ms, a 11.75x speedup.
- On VLABench with GR00T-N1.6, the full base model gets 34.0% success at 24.1 ms. ActionCache with NFE=0 gets 22.3% success at 0.7 ms, a 34.43x speedup.
- With π0.5 at NFE=1, direct NFE reduction gets 6.8% success at 2.5 ms, while ActionCache gets 32.4% success at 3.6 ms, a 5.22x speedup over full generation.
- With GR00T-N1.6 at NFE=2, ActionCache gets 35.7% success at 13.4 ms, slightly above the 34.0% full-base success rate, with a 1.79x speedup.
- Compared with EfficientVLA on π0.5, ActionCache performs better in the low-latency setting: at NFE=1, EfficientVLA gets 2.3% success at 5.1 ms, while ActionCache gets 32.4% at 3.6 ms.
- In a cross-task VLABench test, a cache built on select_fruit gives progress scores of 20.0% on select_painting and 51.7% on select_toy, close to base-model scores of 21.0% and 50.5%; cache hit rates are 2.7% and 8.1%, with more than 80% hit rate at early episode timesteps.

## Link
- [https://arxiv.org/abs/2607.06370v1](https://arxiv.org/abs/2607.06370v1)
