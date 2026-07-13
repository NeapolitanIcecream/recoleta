---
source: arxiv
url: https://arxiv.org/abs/2607.08182v1
published_at: '2026-07-09T07:28:21'
authors:
- Qi Lyu
- Baicheng Liu
- Xudong Wang
- Jiahua Dong
- Lianqing Liu
- Zhi Han
topics:
- vision-language-action
- robot-foundation-model
- latent-world-model
- robot-data-scaling
- generalist-robot-policy
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# LEEVLA: Seeing What Matters in Latent Environment Evolution for Vision-Language-Action

## Summary
LEEVLA trains a vision-language-action policy to focus on task-relevant visual regions and predict how their latent features will change after actions. It reports state-of-the-art results on LIBERO and CALVIN while adding no inference-time memory or computation.

## Problem
- VLA models often give similar training weight to every visual patch, allowing static backgrounds and irrelevant objects to dilute supervision.
- Methods that depend on human-selected cues such as depth, segmentation, or subgoal images restrict the factors the policy can discover and require extra processing.
- Better task-relevant perception and future-state reasoning matter for long-horizon manipulation, changing object appearances, partial occlusion, and varied scene layouts.

## Approach
- Drift-guided dynamic prioritization combines feature change between time steps with language-image similarity. It assigns higher training weight to regions that change during execution and move toward instruction-relevant semantics.
- Structured feature flow generation predicts future visual features in latent space instead of reconstructing pixels or generating future video.
- Prototype-to-periphery prediction clusters future features and predicts each cluster from its centroid toward its outer members, preserving local spatial and semantic structure.
- A mutual-neighborhood contrastive loss selects reciprocal nearby features as positive pairs, reducing noisy links caused by clustering and weakly labeled demonstrations.
- The action loss, future-feature prediction loss, and contrastive loss train the policy jointly; the prioritization and feature-flow modules are used only during training.

## Results
- On LIBERO, LEEVLA-large reaches 98.2% average success across Spatial, Object, Goal, and Long tasks, compared with 97.1% for OpenVLA-OFT and 97.5% for π0.5. Its category scores are 98.8%, 99.0%, 98.6%, and 96.4%.
- On LIBERO, the 0.5B-parameter LEEVLA-mini reaches 97.5% average success, with category scores of 98.6%, 99.0%, 97.0%, and 95.5%.
- On CALVIN ABC-D, LEEVLA-large reaches an average sequence length of 4.34, exceeding OpenVLA-OFT at 4.10 and π0.5 at 4.02. Its success rates across sequence lengths 1 through 5 are 98.8%, 94.5%, 87.3%, 80.6%, and 72.7%.
- The excerpt states that real-world tests used a UR5 arm, three manipulation tasks, and 20 trials per task, with LEEVLA outperforming OpenVLA; exact real-world success rates are not included in the provided text.
- The reported gains support the claim that task-guided region weighting and structured latent future prediction improve VLA generalization and long-horizon reasoning without extra inference overhead.

## Link
- [https://arxiv.org/abs/2607.08182v1](https://arxiv.org/abs/2607.08182v1)
