---
source: arxiv
url: https://arxiv.org/abs/2607.13597v1
published_at: '2026-07-15T08:45:15'
authors:
- Yuan Xu
- Youheng Shi
- Chengyang Li
- Wentao Zhu
- Yizhou Wang
topics:
- robot-foundation-model
- vision-language-action
- generalist-robot-policy
- robot-data-scaling
- sim2real
- representation-learning
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# Semantic Anchoring for Robotic Action Representations

## Summary
Semantic Anchoring for Robotic Action Representations shows that action-only fine-tuning can erode the semantic structure inherited by VLA models, and that this erosion tracks out-of-distribution performance. Its training-time semantic anchoring method improves simulation and real-robot success while leaving the deployed inference model unchanged.

## Problem
- VLA models inherit semantic representations from pretrained vision-language encoders, but limited and narrow robot demonstrations can push action representations toward task-specific shortcuts.
- This matters because semantic degradation is associated with weaker transfer to new instructions, objects, layouts, visual conditions, and task compositions, even when in-distribution success continues to rise.

## Approach
- Probe mid-layer action features against instruction embeddings across the full fine-tuning trajectory of \(\pi_0\), using bidirectional contrastive retrieval and task-disjoint LIBERO evaluation.
- Add a training-time contrastive alignment loss that anchors action representations to a frozen semantic manifold from the EgoHOD text encoder.
- Decompose action features into shared semantic and private execution-specific channels; align only the shared channel while reconstructing the original features and decorrelating the channels.
- Discard all auxiliary alignment, decomposition, and reconstruction modules at inference, so the deployed policy has the same inference graph as the action-only baseline.

## Results
- On LIBERO, \(\pi_0\) improves from 89.3% to 92.4% average success, a +3.1 percentage-point gain; suite scores improve for Spatial (94.0% to 96.5%), Object (96.5% to 98.5%), Goal (90.0% to 92.5%), and Long (76.5% to 82.0%).
- On SimplerEnv, the method improves \(\pi_0\) from 35.4% to 41.7% (+6.3 points) and SpatialVLA from 43.8% to 51.0% (+7.2 points).
- On the real bimanual robot, average in-distribution success rises from 51.3% to 70.0% (+18.7 points), while out-of-distribution success rises from 49.5% to 71.0% (+21.5 points) over 20 trials per task condition.
- Real-robot gains occur across all five OOD axes: language 75.0% to 85.0%, position 32.5% to 57.5%, object 52.5% to 77.5%, visual 57.5% to 75.0%, and task composition 30.0% to 60.0%.
- During \(\pi_0\) fine-tuning, action-instruction alignment never returns to its pretrained level of 62.74%, while OOD success follows the alignment trend with Spearman \(\rho=0.964\); successful individual rollouts also show higher alignment than failed rollouts.
- The excerpt reports ablations showing incremental gains from contrastive alignment and shared/private decomposition, with the strongest benefit at mid-network layer \(k=10\); it does not provide the exact ablation bar values.

## Link
- [https://arxiv.org/abs/2607.13597v1](https://arxiv.org/abs/2607.13597v1)
