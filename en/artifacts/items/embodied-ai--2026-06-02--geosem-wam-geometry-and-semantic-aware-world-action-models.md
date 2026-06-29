---
source: arxiv
url: https://arxiv.org/abs/2606.03188v1
published_at: '2026-06-02T05:48:02'
authors:
- Fulong Ma
- Daojie Peng
- Wenjun Yue
- Jiahang Cao
- Bintao Wang
- Qiang Zhang
- Jun Ma
topics:
- world-action-model
- vision-language-action
- robot-manipulation
- structured-world-modeling
- semantic-supervision
- geometry-supervision
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# GeoSem-WAM: Geometry- and Semantic-Aware World Action Models

## Summary
GeoSem-WAM improves World Action Models by training them to predict future RGB, geometry, and semantic maps, then uses the learned latent state to predict robot actions at test time. It targets better action success under clutter, geometry shifts, and semantic changes without generating future video during deployment.

## Problem
- RGB-only WAM training can miss spatial structure and object meaning needed for manipulation.
- Future video rollout at inference adds latency; the paper argues WAM gains mainly come from predictive training shaping latent features.
- This matters for real robots because failures often come from occlusion, distractors, height changes, and long-horizon object interactions.

## Approach
- Builds on Wan2.2-5B video DiT with a T5 instruction encoder, VAE video tokens, and an action DiT in a Mixture-of-Transformer architecture.
- Trains with four losses: future RGB latent flow matching, action chunk denoising, geometry L1 prediction, and semantic pixel-wise cross-entropy.
- Uses DPT-style dense heads over intermediate transformer tokens, extended with 3D reassemble and fusion modules for video.
- Removes geometry and semantic heads at deployment; action prediction uses the current observation and language, then denoises an action chunk without future video generation.

## Results
- LIBERO average success rate is 98.55%, above Fast-WAM at 97.60%, LingBot-VA at 98.50%, and Motus at 97.70%; suite success rates are Spatial 99.0%, Object 100.0%, Goal 98.2%, and Long 97.0%.
- RoboTwin 2.0 average success rate is 92.52%, above Fast-WAM at 91.80% and LingBot-VA at 92.20%; clean setting is 92.94% and random setting is 92.14%, with no embodied pre-training.
- LIBERO ablation reports RGB-only at 97.6% average success rate; adding geometry gives 98.2% (+0.61), adding semantics gives 98.1% (+0.51), and adding both gives 98.6% (+1.02).
- Real Franka robot average success rate rises from 88.9% for Fast-WAM to 95.4% for GeoSem-WAM (+6.6) across 7 settings with 50 trials each.
- Real generalization gains include Easy-Pick-B1 +10, Easy-Pick-B2 +8, and Easy-Pick-D with a 4 cm height change +12; multi-step task gains are Multi-Pick +6, Multi-Goal +6, and Pick-Pour +4.

## Link
- [https://arxiv.org/abs/2606.03188v1](https://arxiv.org/abs/2606.03188v1)
