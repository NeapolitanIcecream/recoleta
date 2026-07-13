---
source: arxiv
url: https://arxiv.org/abs/2607.08283v1
published_at: '2026-07-09T09:24:30'
authors:
- Yushen Liang
- Yue Peng
- Baosheng Jin
- Tianluo Zhang
- Xinyu Zhang
- Shuyi Zhou
- Zhuoran Chen
- Xinqi Liu
- Shenji Wan
topics:
- robot-foundation-model
- vision-language-action
- generalist-robot-policy
- robot-data-scaling
- dexterous-manipulation
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# TFP: Temporally Conditioned Memory-Fusion Policies for Visuomotor Learning

## Summary
TFP adds an episode-local, continuous-time memory state to a 3.3B-parameter VLA policy so actions depend on task progress and elapsed time, not only the current observation. It improves simulation benchmarks and real-robot stage-dependent manipulation, with the largest gains on long-horizon, occluded, and visually perturbed tasks.

## Problem
- Reactive VLA policies can choose the wrong action when visually similar scenes require different actions at different task stages.
- Occlusion, contact, release, and irregular policy-query intervals make fixed-step memory updates unreliable.
- The problem matters because manipulation requires retaining task progress through ambiguous observations while updating the belief when new interaction evidence arrives.

## Approach
- TFP maintains a 256-dimensional episode-local latent belief that summarizes task progress and interaction history.
- A Liquid Time-Constant recurrence uses the measured elapsed time and input-dependent time constants to decide how much belief to retain or revise.
- The updated belief is projected into the flow-matching action decoder and injected through AdaLN modulation, so memory directly changes the generated action chunk.
- Episode-Aware Temporal Batching trains on contiguous chunks while preserving separate hidden states for active episodes.
- An adaptive receding-horizon executor shortens action chunks near gripper transitions or high-risk regions and passes the actual elapsed interval to the memory update.

## Results
- On LIBERO, TFP reaches 98.75% average success versus 96.85% for the reactive pi0.5 baseline; on the Long-10 split it reaches 97.0% versus 92.4%.
- On LIBERO-plus, TFP reaches 93.77% average success versus 91.4% for pi0.5, including gains from 85.2% to 88.5% under noise and from 93.9% to 96.1% under lighting perturbations.
- On MIKASA-Robo ShellGameTouch, TFP reaches 75.0%, above the reported OpenVLA-OFT result of 47.0%, but below MemoryVLA's reported 88.0%.
- On a Galaxea A1 robot, object-swap success rises from 3/20 with pi0.5 to 15/20 with TFP, and counting pick-and-place success rises from 8/20 to 18/20.
- Mechanistic tests report write-gain changes near manipulation events about 6 times larger than during distant non-event phases, while hidden-state interventions show that the belief causally changes generated action chunks.

## Link
- [https://arxiv.org/abs/2607.08283v1](https://arxiv.org/abs/2607.08283v1)
