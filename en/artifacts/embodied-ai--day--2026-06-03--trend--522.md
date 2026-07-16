---
kind: trend
trend_doc_id: 522
granularity: day
period_start: '2026-06-03T00:00:00'
period_end: '2026-06-04T00:00:00'
topics:
- robotics
- vision-language-action
- world models
- 3D geometry
- tactile sensing
- quadrotor navigation
run_id: materialize-outputs
aliases:
- recoleta-trend-522
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/world-models
- topic/3d-geometry
- topic/tactile-sensing
- topic/quadrotor-navigation
language_code: en
pass_output_id: 252
pass_kind: trend_synthesis
---

# Robot policy work is being tested against geometry, contact, and real execution

## Overview
Robotics dominates the day, with policy quality treated as an execution problem. The strongest papers add geometry, physical validation, success scoring, or spatial memory before deployment. OSCAR, 3DThinkVLA, and MAD give the clearest evidence.

## Findings

### Geometry-guided VLA policies
Vision-language-action (VLA) papers center on signals that make actions physically meaningful. 3DThinkVLA aligns Qwen3-VL visual features with VGGT 3D features and distills a spatial reasoning anchor into normal action prompts. It reports 98.7% average success on LIBERO and 81.0% on LIBERO-PLUS while using only 2D images at inference.

VISTA attacks the data side of the same problem. It adapts Universal Manipulation Interface (UMI) demonstrations by training on an 8M-sample fisheye VQA set and filtering trajectories for completeness, continuity, self-collision risk, and execution fidelity. ForesightFlow adds a lighter policy-improvement path: each action chunk carries generated success-potential scores, giving best-of-K selection without a separate critic. Its real-world bimanual success rate is 35.4%, above IDQL at 32.6%, with reported training compute falling from 287 to 178 GPU hours.

#### Sources
- [3DThinkVLA: Endowing Vision-Language-Action Models with Latent 3D Priors via 3D-Thinking-Guided Co-training](../Inbox/2026-06-03--3dthinkvla-endowing-vision-language-action-models-with-latent-3d-priors-via-3d-thinking-guided-co-training.md): 3DThinkVLA method and LIBERO/LIBERO-PLUS results.
- [VISTA: Vision-Grounded and Physics-Validated Adaptation of UMI data for VLA Training](../Inbox/2026-06-03--vista-vision-grounded-and-physics-validated-adaptation-of-umi-data-for-vla-training.md): VISTA fisheye VQA data, physical validation, and UMI adaptation.
- [Potential-Guided Flow Matching for Vision-Language-Action Policy Improvement](../Inbox/2026-06-03--potential-guided-flow-matching-for-vision-language-action-policy-improvement.md): ForesightFlow success-potential scoring, real-world results, and compute comparison.

### World models for policy evaluation and spatial memory
World-model work is tied to measurable control outcomes. OSCAR uses 2D kinematic skeleton videos as action conditions for a 2B-parameter video world model that spans robot arms and human hands. On a 200-clip benchmark, it reaches PSNR 24.24 and SSIM 0.846, and it runs at 2.214 FPS on the reported GH200 test.

MAD applies a related predictive idea to quadrotors, training a DreamerV3-style recurrent model to predict local occupancy and visibility maps. The learned policy reaches 9.66 m/s in simulation and 5.05 m/s in real forest flight. A separate quadrotor study adds a caution: the model with the strongest simulation policy score failed on the real platform, while other models reached the target through narrow gaps. The authors find cross-environment reconstruction quality more useful for real transfer than simulated win rate alone.

#### Sources
- [OSCAR: Omni-Embodiment Skeleton-Conditioned World Action Model for Robotics](../Inbox/2026-06-03--oscar-omni-embodiment-skeleton-conditioned-world-action-model-for-robotics.md): OSCAR skeleton-conditioned world model, benchmark metrics, speed, and embodiment coverage.
- [MAD: Mapping-Aware World Models for Agile Quadrotor Flight](../Inbox/2026-06-03--mad-mapping-aware-world-models-for-agile-quadrotor-flight.md): MAD mapping-aware world model and quadrotor deployment results.
- [Generalization of World Models under Environmental Variability for Vision-based Quadrotor Navigation](../Inbox/2026-06-03--generalization-of-world-models-under-environmental-variability-for-vision-based-quadrotor-navigation.md): Quadrotor world-model generalization study and simulation-to-real findings.

### Contact-rich data exposes limits of vision-only manipulation
HapTile adds touch and operator feedback to the VLA data mix. The dataset contains 1,726 demonstrations across 38 tasks and 9 skills, with language, third-person RGB, wrist RGB, fingertip tactile images, robot state, 7D actions, timestamps, and haptic feedback at 15 Hz. The strongest gains appear where contact decides success: peg insertion with π0 rises from 0% using vision-only input to 90% with raw tactile images, and whiteboard wiping rises from 50% to 100% with tactile marker features.

The results are not uniformly positive. Pouring degrades when tactile marker features are added in the reported baselines. That makes the dataset useful as a diagnostic tool: touch helps on some contact-heavy tasks, but policy architectures still need better ways to combine tactile signals with visual and language inputs.

#### Sources
- [HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning](../Inbox/2026-06-03--haptile-a-haptic-informed-vision-tactile-language-action-dataset-for-contact-rich-imitation-learning.md): HapTile dataset contents, scale, tactile setup, and benchmark results.
