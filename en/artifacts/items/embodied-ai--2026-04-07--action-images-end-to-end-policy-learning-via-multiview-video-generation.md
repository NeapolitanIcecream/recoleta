---
source: arxiv
url: http://arxiv.org/abs/2604.06168v2
published_at: '2026-04-07T17:59:30'
authors:
- Haoyu Zhen
- Zixian Gao
- Qiao Sun
- Yilin Zhao
- Yuncong Yang
- Yilun Du
- Pengsheng Guo
- Tsun-Hsuan Wang
- Yi-Ling Qiao
- Chuang Gan
topics:
- robot-policy-learning
- world-action-model
- multiview-video-generation
- pixel-grounded-actions
- zero-shot-robotics
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# Action Images: End-to-End Policy Learning via Multiview Video Generation

## Summary
Action Images learns robot control by turning each 7-DoF action into multiview pixel-space videos and training one video model to generate both future observations and actions. The paper claims this removes the need for a separate policy head and improves zero-shot robot control, especially across new views and real-world shifts.

## Problem
- Video world models can predict future frames, but that does not reliably produce a policy that chooses correct actions in new environments.
- Many prior methods keep action in a separate module or in latent tokens that are not tied to image pixels, so pretrained video knowledge does not transfer cleanly to control.
- A single camera view makes 3D robot motion ambiguous, which hurts action recovery from images.

## Approach
- Convert each robot action \((x,y,z,\text{orientation},\text{gripper})\) into three semantic 3D points: end-effector position, an up point, and a normal point.
- Project those points into each camera view and render them as RGB Gaussian heatmaps. The blue channel also stores gripper openness in low-response regions. This produces a multiview action video aligned with the RGB robot video.
- Train a single pretrained video generator backbone (Wan 2.2) on packed observation-video and action-video tokens, using masking to support joint video-action generation, action-conditioned video generation, video-to-action labeling, and video-only generation.
- Decode generated action images back to continuous 7-DoF control by reading gripper state from the blue channel, lifting heatmap peaks from the main view into 3D with side-view matching, and reconstructing pose from the three recovered 3D points.
- Train on RLBench, DROID, and BridgeV2, with camera conditioning and flow-matching loss on masked latent tokens.

## Results
- On zero-shot RLBench tasks, the method reports success rates of 30% on pick cup, 60% on reach target, 50% on close drawer, and 15% on close laptop.
- On zero-shot real-world tasks with unseen objects, environments, and xArm robot setup, it reports 40% on Place Cup, 20% on Pick Unseen Toy, 15% on Pick Tissue, 45% on Close Drawer, and 10% on Close Box.
- Compared with reproduced baselines in Table 2, it beats MV-Policy, pi_0.5, MolmoAct, TesserAct, and Cosmos-Policy on most listed tasks. Examples: RLBench reach target 60% vs 5% for pi_0.5 and 5% for Cosmos-Policy; real Close Drawer 45% vs 5% for MolmoAct and 0% for the others.
- The abstract also claims stronger zero-shot success rates and better video-action joint generation quality than prior video-space world models, but the excerpt does not provide joint-generation metrics.

## Link
- [http://arxiv.org/abs/2604.06168v2](http://arxiv.org/abs/2604.06168v2)
