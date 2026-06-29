---
source: arxiv
url: https://arxiv.org/abs/2606.03240v1
published_at: '2026-06-02T07:01:18'
authors:
- Yizhi Chen
- Zhanxiang Cao
- Xinyi Peng
- Yixiao Zheng
- Xiaxi Si
- Yiheng Li
- Liyun Yan
- Keqi Zhu
- Xueyun Chen
- Shengcheng Fu
- Tianyue Zhan
- Yufei Jia
- Jinming Yao
- Yan Xie
- Kun Wang
- Cewu Lu
- Yue Gao
topics:
- vision-language-action
- robot-foundation-model
- geometry-aware-manipulation
- state-guided-attention
- rgb-d-supervision
- aloha
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# GeoAlign: Beyond Semantics with State-Guided Spatial Alignment in VLA Models

## Summary
GeoAlign adds RGB-derived geometry conditioning to a VLA policy so fine manipulation can use local shape cues during action generation. It reports higher success on LIBERO, SimplerEnv-Fractal, and real ALOHA tasks than matched RGB-only baselines.

## Problem
- VLA policies can identify the right object and instruction but fail on tight clearances, transparent objects, ring-like parts, insertion, release, and other geometry-sensitive actions.
- Measured depth can be missing or fragmented on transparent and thin objects, so using raw depth at rollout can hurt the tasks that need geometry.
- The problem matters because a general robot policy must choose executable actions, not just semantically correct targets.

## Approach
- GeoAlign post-trains a Depth Anything V2-Small branch on robot RGB-D data with metric depth supervision, then discards the depth head.
- At rollout, the policy feeds only RGB, language, and proprioceptive state to the model; the retained encoder produces Geometry-Enhanced Post-Trained (GEP) feature grids from RGB.
- The robot state generates 8 query slots that cross-attend to the GEP grid, selecting local geometry for the current pose and action phase.
- The 8 geometry tokens are concatenated with RGB-language tokens and condition an Isaac-GR00T N1.6-3B flow-matching DiT action decoder.

## Results
- LIBERO: GeoAlign reports 99.0% average success across 8,000 rollouts, compared with 97.0% for the controlled RGB-only GR00T baseline; Spatial improves from 97.65% to 100.0%, and Long improves from 94.35% to 96.6%.
- SimplerEnv-Fractal: GeoAlign reports 85.3% unweighted average success across Pick Coke Can, Move Near, and Open/Close Drawer, a +5.7 percentage-point gain over RGB-only; per-task success is 100.0%, 85.5%, and 70.3%.
- Real-world ALOHA: across 8 tasks with 20 trials each, GeoAlign reports 78.8% average success versus 65.0% for RGB-only and 67.5% for pi-0.5.
- Real-world geometry-critical gains include transparent bottle at 75.0% versus 35.0% RGB-only and tape-roll insertion at 65.0% versus 40.0% RGB-only.
- Ablations on LIBERO report 95.9% without robot-domain geometry post-training, 91.6% without spatial querying, 96.2% without state-generated queries, and 95.93% with an unfrozen geometry encoder, versus 99.0% for the full model.

## Link
- [https://arxiv.org/abs/2606.03240v1](https://arxiv.org/abs/2606.03240v1)
