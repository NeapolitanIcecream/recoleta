---
source: arxiv
url: https://arxiv.org/abs/2605.22283v1
published_at: '2026-05-21T10:32:53'
authors:
- Pengteng Li
- Weiyu Guo
- He Zhang
- Tiefu Cai
- Xiao He
- Yandong Guo
- Hui Xiong
topics:
- vision-language-action
- spatial-memory
- out-of-vision-manipulation
- robot-foundation-model
- partial-observability
- active-perception
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Spatial Memory for Out-of-Vision Manipulation in Vision-Language-Action

## Summary
SOMA adds persistent spatial memory to VLA robot policies so they can act on objects outside the current camera view. It reports higher success and faster target finding on five real-world out-of-vision pick-and-place tasks.

## Problem
- Existing VLAs often depend on the current camera view, so they fail when the instructed object is occluded or outside the field of view.
- This matters for manipulation because the robot may need to remember where an object was seen, move its head or arms, and grasp without repeated visual search.
- Static spatial inference alone can give wrong target locations when the object has no current visual evidence.

## Approach
- If the target cannot be localized, a 2-DoF head camera scans the workspace before manipulation.
- YOLO detects objects, DINOv3 encodes object appearance, and VGGT estimates camera poses plus 3D boxes; the system fuses these detections into object memory tokens with semantic and 3D position data.
- During manipulation, new head-camera observations update the memory through class-wise appearance-geometry matching and a similarity-weighted exponential moving average.
- Vision-language tokens query the memory with cross-attention, and the memory-enhanced tokens feed a DiT action decoder that predicts action chunks.

## Results
- The paper evaluates five real-world out-of-vision pick-and-place tasks; the figure caption states 20 episodes are used for success-rate evaluation.
- In the ablation table, Full SOMA reaches 28.3% average SR, compared with 18.5% for Scan+GR00T, 19.8% for No-Scan SOMA, and 24.1% for Scan-only SOMA.
- Full SOMA per-task SR is 30.0%, 35.0%, 27.5%, 32.5%, and 16.7% on Tasks 1-5; Scan+GR00T scores 19.0%, 22.0%, 16.0%, 25.0%, and 10.5%.
- Compared with GR00T-N1.5, SOMA reduces first-fixation time across Tasks 1-5 from 7.6/21.0/14.8/10.9/11.5 s to 4.2/12.7/8.2/4.9/4.7 s.
- SOMA reduces head search path length from 50.5/51.0/83.8/109.2/164.0 degrees to 27.8/28.1/50.3/54.6/70.4 degrees, and reduces grasp attempts from 1.8/2.0/1.7/2.4/3.7 to 1.0/1.2/1.0/1.2/1.6.
- SOMA reduces time-to-grasp from 58.0/30.0/50.0/65.5/36.5 s to 32.3/16.8/29.7/30.4/14.6 s. The excerpt also says RoboCasa Tabletop GR1 and SimplerEnv support the memory design, but it does not provide their quantitative results.

## Link
- [https://arxiv.org/abs/2605.22283v1](https://arxiv.org/abs/2605.22283v1)
