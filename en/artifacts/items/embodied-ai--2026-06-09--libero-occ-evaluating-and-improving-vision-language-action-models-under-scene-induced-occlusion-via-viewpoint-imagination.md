---
source: arxiv
url: https://arxiv.org/abs/2606.10862v1
published_at: '2026-06-09T13:39:49'
authors:
- Taishan Li
- Jiwen Zhang
- Siyuan Wang
- Xuanjing Huang
- Zhongyu Wei
topics:
- vision-language-action
- robot-manipulation
- occlusion-robustness
- viewpoint-imagination
- robot-benchmarks
- world-models
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# LIBERO-Occ: Evaluating and Improving Vision-Language-Action Models under Scene-Induced Occlusion via Viewpoint Imagination

## Summary
LIBERO-Occ tests VLA robot policies when task objects or goal regions are hidden by real scene geometry. VIM improves occluded manipulation by generating a likely wrist/gripper view from the visible camera image and using that generated view for action prediction.

## Problem
- Standard LIBERO-style VLA evaluation often assumes that task-relevant objects are visible, while real manipulation scenes can hide the object, receptacle, or both.
- Occlusion turns action prediction into a partial-observation problem: the policy may need object location, shape, or goal-region evidence that the camera cannot see.
- The paper matters for deployable robot policies because adding cameras or active camera hardware can add calibration, placement, and maintenance cost.

## Approach
- The authors build LIBERO-Occ by adding physical occluder objects to LIBERO tasks while preserving task semantics and checking executability with demonstration replay.
- LIBERO-Occ contains 2,000 occluded tasks across manipulated-object occlusion, receptacle occlusion, and dual occlusion, split into light, medium, and heavy severity by segmentation-based visibility loss.
- VIM first predicts visual tokens for a complementary view, such as a wrist/gripper view, from the occluded primary view and language instruction.
- The policy then predicts action tokens conditioned on the primary view, instruction, and imagined complementary view.
- Training has two stages: view generation first, then joint action prediction plus view-generation loss with weight λ = 0.5.

## Results
- On LIBERO-Occ without a real complementary view, VIM reaches 65.05% average success, beating the strongest baseline, UniVLA at 57.10%, by 7.95 percentage points.
- OpenVLA-OFT has the best original LIBERO average at 95.75%, but drops to 47.95% on LIBERO-Occ; VIM scores 90.75% on original LIBERO and 65.05% on LIBERO-Occ.
- VIM has the smallest original-to-occluded average drop among the listed no-complementary-view methods: 25.70 points, compared with UniVLA 31.15, OpenVLA 52.00, OpenVLA-OFT 47.80, π-0 39.95, and π-0.5 49.45.
- Providing a ground-truth complementary view to the VIM model raises LIBERO-Occ average success from 65.05% to 74.00%, giving an upper-bound reference for missing visual evidence.
- The complementary-view performance gap is 2.2 to 8.3 points on original LIBERO and 22.1 to 45.5 points on LIBERO-Occ, showing that occlusion increases dependence on hidden visual evidence.
- By occlusion target type, VIM scores 54.67% on manipulated-object occlusion, 91.33% on receptacle occlusion, and 35.43% on dual occlusion, leading all listed baselines in each group.

## Link
- [https://arxiv.org/abs/2606.10862v1](https://arxiv.org/abs/2606.10862v1)
