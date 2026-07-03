---
source: arxiv
url: https://arxiv.org/abs/2607.00678v1
published_at: '2026-07-01T09:21:20'
authors:
- Ronghan Chen
- Yandan Yang
- Zuojin Tang
- Dongjie Huo
- Tong Lin
- Haoning Wu
- Haoyun Liu
- Yuzhi Chen
- Lulu Zheng
- Botai Yuan
- Tianlun Li
- Mingxin Wang
- Dekang Qi
- Bin Hu
- Wei Mei
- Yuze Xuan
- Haolong Yang
- Yanqing Zhu
- Mu Xu
- Zhiheng Ma
- Xinyuan Chang
topics:
- mobile-manipulation
- world-action-model
- vision-language-action
- latent-actions
- generalist-robot-policy
- robot-foundation-model
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# ABot-M0.5: Unified Mobility-and-Manipulation World Action Model

## Summary
ABot-M0.5 is a world-action model for language-conditioned mobile manipulation. It targets long-horizon navigation plus fine object interaction by adding latent motion intents, separated action heads, and training on the model’s own predicted videos.

## Problem
- Mobile manipulation needs both base movement and arm control over long horizons, so reactive VLA policies can lose task context and miss future scene changes.
- Existing World Action Models often predict coarse video chunks, then map them to low-level actions; this can erase contact events, grasp closure, and small alignment corrections.
- Training inverse dynamics on ground-truth future observations creates a mismatch at deployment, where actions depend on the model’s predicted future observations.

## Approach
- The model uses a three-stage cascade: future video latent $z_{t+1}$, frame-level latent action $m_t$, then executable robot action $a_t$.
- A frozen latent-action encoder extracts $m_t$ from consecutive frames, so the intermediate action signal comes from visual state changes rather than robot-specific kinematic labels.
- A dual-level Mixture-of-Transformers separates modality streams for video, latent actions, and executable actions, then splits executable actions into mobility and manipulation subspaces.
- Conditional Flow Matching trains video, latent-action, and action generation under the same autoregressive order used at inference.
- Dream Forcing trains inverse dynamics on self-predicted videos, so action prediction sees the kind of imperfect rollout context it will face during deployment.

## Results
- The excerpt provides no benchmark tables, success rates, control-error values, or numeric ablation results.
- The paper claims state-of-the-art performance on challenging mobile manipulation and fine-grained manipulation benchmarks, covering both long-horizon task success and control accuracy.
- The paper claims real-world mobile manipulation success on tasks named in the figure caption, including Arrange Flower and Find Toaster.
- The paper claims ablations validate the contribution of the three main components: intermediate latent actions, dual-level Mixture-of-Transformers, and Dream Forcing.

## Link
- [https://arxiv.org/abs/2607.00678v1](https://arxiv.org/abs/2607.00678v1)
