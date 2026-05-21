---
source: arxiv
url: https://arxiv.org/abs/2605.10993v1
published_at: '2026-05-09T13:06:33'
authors:
- Yanbin Hu
- Jin Cui
- Jiayi Lu
- Ruixuan Yang
- Jun Ye
- Boran Zhao
- Xingyu Chen
- Xuguang Lan
- Pengju Ren
topics:
- vision-language-action
- robot-foundation-model
- hierarchical-memory
- long-horizon-manipulation
- compositional-generalization
- hyperbolic-embeddings
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# ECHO: Continuous Hierarchical Memory for Vision-Language-Action Models

## Summary
ECHO adds continuous hierarchical memory to a Vision-Language-Action policy so it can reuse past manipulation experience in long-horizon tasks. Integrated with π0, it reports the largest gain on LIBERO-Long.

## Problem
- Long-horizon robot manipulation needs memory of past subgoals and action segments, since current-observation policies can lose task progress across many steps.
- Flat memory banks and linear history buffers store experiences without task-subgoal-action structure, which can make retrieval slower and less reliable as data grows.
- The paper targets compositional generalization: solving new long-horizon task sequences by reusing memories from related source tasks.

## Approach
- ECHO maps π0 hidden states into a Lorentz hyperbolic space with a hyperbolic autoencoder, then stores successful subgoal segments as memory entries.
- Global task embeddings act as parent nodes, and subgoal transition states act as child nodes; entailment-cone losses push child memories inside the parent task region.
- During inference, ECHO runs top-down beam search through the memory tree using hyperbolic distance and cone constraints, then aligns retrieved memories with the current state through cross-attention.
- A VLM-guided downsampler extracts subgoal transitions from continuous control streams and filters failed trajectories before memory insertion.
- Background consolidation splits broad nodes with Lorentzian K-Means and can synthesize temporary virtual memories by geodesic interpolation between related memories.

## Results
- On LIBERO-Long, ECHO reaches 93.5% ± 2.6 success versus 80.7% ± 2.0 for Vanilla π0, a 12.8 percentage-point absolute gain.
- On standard LIBERO suites, ECHO reports 98.3% ± 1.0 on Spatial, 98.8% ± 0.5 on Object, and 98.6% ± 1.0 on Goal, compared with Vanilla π0 at 97.5% ± 1.7, 97.0% ± 1.2, and 92.3% ± 2.5.
- ECHO slightly exceeds MemoryVLA on LIBERO-Long: 93.5% ± 2.6 versus 92.4% ± 1.1 in the paper’s local pipeline.
- On LIBERO-Plus, ECHO improves over Vanilla π0 from 54.2% ± 2.9 to 56.5% ± 2.0.
- In cross-suite generalization, using memories only from LIBERO-Spatial, LIBERO-Object, and LIBERO-Goal, ECHO scores 89.31% on LIBERO-Long versus 80.70% for Vanilla π0, with no LIBERO-Long target memories.
- LIBERO-Long ablations show 80.70% for Vanilla π0, 88.81% with short-term buffer only, 83.25% with flat Euclidean memory, 91.11% with hyperbolic memory, 92.04% with cone tree retrieval, and 93.48% for full ECHO.

## Link
- [https://arxiv.org/abs/2605.10993v1](https://arxiv.org/abs/2605.10993v1)
