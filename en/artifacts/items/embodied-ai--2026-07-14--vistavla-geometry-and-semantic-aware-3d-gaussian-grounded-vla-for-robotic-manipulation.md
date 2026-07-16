---
source: arxiv
url: https://arxiv.org/abs/2607.12356v1
published_at: '2026-07-14T05:08:50'
authors:
- Mohan Liu
- Zhihao Gu
- Xuanyu Chen
- Haitian Zhang
- Kaimin Mao
- Yan Wu
- Wei-Yun Yau
- Lin Wang
topics:
- robot-foundation-model
- vision-language-action
- 3d-scene-representation
- 3d-gaussian-splatting
- robotic-manipulation
- sim2real
relevance_score: 0.98
run_id: materialize-outputs
language_code: en
---

# VistaVLA: Geometry- and Semantic-Aware 3D Gaussian-Grounded VLA for Robotic Manipulation

## Summary
VistaVLA addresses the limited 3D spatial reasoning of vision-language-action policies by giving them compact, semantically grounded 3D scene tokens. It combines 3D Gaussian features with Merge-then-Query compression and reports stronger manipulation performance in real-world and simulated spatial-shift tests.

## Problem
- 2D-input VLA models lack an explicit scene-level 3D representation, which limits reasoning about spatial layouts and geometric constraints during precise or contact-rich manipulation.
- Existing 3D VLA inputs such as depth and point clouds provide geometry but do not sufficiently bind high-level language-aligned semantics to persistent 3D locations.
- Dense 3D representations are expensive for real-time policy inference, so the problem also requires a compact interface between 3D perception and VLA control.

## Approach
- VistaVLA lifts SigLIP2 and DINOv2-Large features into learnable 3D Gaussian primitives using RGB, depth, and multi-view feature-rendering supervision. A 2,176-dimensional teacher feature is compressed to a 128-dimensional latent code before distillation.
- Each Gaussian stores geometry and a semantic feature, producing multi-view-consistent tokens whose spatial grounding follows the primitive's 3D position, visibility, opacity, and depth ordering.
- Merge-then-Query first applies spatially guided, semantic-similarity-based merging, reducing roughly 100,000 Gaussian primitives to about 1,000 tokens, then uses 64 learned query tokens to summarize them for the VLA backbone.
- The resulting 3D context tokens are inserted alongside image and language tokens in a VLA-Adapter-based policy, which predicts continuous robot actions and replans after executing four actions.

## Results
- In seven real-world manipulation tasks, VistaVLA reports a 22.8-point average success-rate gain over the VLA-Adapter baseline and outperforms the evaluated 2D and 3D baselines, including VLA-Adapter+Depth and the larger pi_0.5 policy.
- Under depth variation on PlaceSponge, VistaVLA achieves 9/10 success versus 6/10 for VLA-Adapter and VLA-Adapter+Depth, and 7/10 for pi_0.5.
- Under position variation on OrganizeSponge, VistaVLA achieves 3/10 success while all listed baselines achieve 0/10, indicating improved but still limited robustness to large position shifts.
- On standard LIBERO, the paper reports a 96.05 average success rate; on the zero-shot LIBERO-Pro-Swap spatial-OOD benchmark, it reaches 12.2 average success versus 1.7 for the baseline.
- MtQ reduces the token count by 99%, from approximately 10^5 Gaussian primitives to 64 policy-facing summary tokens while retaining the reported action-relevant spatial and semantic information.
- The excerpt does not provide full ablation results, confidence intervals, or per-task real-world success rates, so the relative contribution of the Gaussian representation and MtQ cannot be isolated completely from the supplied text.

## Link
- [https://arxiv.org/abs/2607.12356v1](https://arxiv.org/abs/2607.12356v1)
