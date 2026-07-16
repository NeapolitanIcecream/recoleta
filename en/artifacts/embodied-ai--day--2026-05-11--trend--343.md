---
kind: trend
trend_doc_id: 343
granularity: day
period_start: '2026-05-11T00:00:00'
period_end: '2026-05-12T00:00:00'
topics:
- robotics
- vision-language-action models
- manipulation
- OOD generalization
- world models
- policy adaptation
- spatial grounding
run_id: materialize-outputs
aliases:
- recoleta-trend-343
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action-models
- topic/manipulation
- topic/ood-generalization
- topic/world-models
- topic/policy-adaptation
- topic/spatial-grounding
language_code: en
pass_output_id: 148
pass_kind: trend_synthesis
---

# Robot VLA work is concentrating on OOD adaptation with preserved priors and better action structure

## Overview
Robot Vision-Language-Action (VLA) papers in this period focus on deployment failure points: out-of-distribution scenes, limited demonstrations, and weak action supervision. HarmoWAM, PriorVLA, and UniSteer give the clearest measured signal across real-world manipulation tests.

## Findings

### World models for staged manipulation
HarmoWAM treats manipulation as a phase-dependent control problem. A video world model predicts future frames, while two action experts handle different parts of the task: a reactive expert for transit and a predictive expert for precise interaction. A learned gate chooses the expert during inference.

The paper reports tests on six real-world tasks with background, position, and object variation. In out-of-distribution settings, HarmoWAM claims average gains of 33 percentage points over prior VLA models and 29 points over prior World Action Models. The key detail is the separation between reaching and contact control, which the paper measures directly in its motivation study.

#### Sources
- [HarmoWAM: Harmonizing Generalizable and Precise Manipulation via Adaptive World Action Models](../Inbox/2026-05-11--harmowam-harmonizing-generalizable-and-precise-manipulation-via-adaptive-world-action-models.md): Summary covers HarmoWAM architecture, staged experts, gating, real-world tasks, and OOD gains.

### Adaptation without overwriting pretrained behavior
PriorVLA and UniSteer both keep pretrained policy behavior visible during adaptation. PriorVLA freezes a prior expert and trains a separate adaptation expert, updating about one quarter as many parameters as full fine-tuning. It reports 53% Hard OOD success on RoboTwin 2.0 and 57% OOD success in real-world tests across eight tasks and two embodiments.

UniSteer uses a different route for the same deployment pressure. It freezes the flow-matching decoder and trains a small noise actor. Human corrections are mapped back into noise targets, so corrective actions and reinforcement learning update the same actor. Across four real-world tasks, reported average success reaches 90% after 66 minutes of adaptation, compared with 55% for DSRL and 60% for DAgger.

#### Sources
- [PriorVLA: Prior-Preserving Adaptation for Vision-Language-Action Models](../Inbox/2026-05-11--priorvla-prior-preserving-adaptation-for-vision-language-action-models.md): Summary describes PriorVLA's frozen prior expert, parameter update share, and OOD results.
- [Unified Noise Steering for Efficient Human-Guided VLA Adaptation](../Inbox/2026-05-11--unified-noise-steering-for-efficient-human-guided-vla-adaptation.md): Summary describes UniSteer's noise-target training, frozen decoder, real-world adaptation time, and success rates.

### Action structure learned from unlabeled video
ALAM targets the cost of action-labeled robot data. It learns latent transitions from action-free videos, then regularizes them with composition and reversal constraints. During VLA training, those latent transitions become auxiliary targets while the executed output remains the robot action stream.

The reported gains are large on standard manipulation suites. On MetaWorld MT50, π0 with ALAM reaches 85.0% average success, compared with 47.9% for π0. On LIBERO, it reports 98.1% average success, above the π0 baseline at 94.1%. The result supports a practical reading: unlabeled video is useful when the latent action space carries reusable transition structure.

#### Sources
- [ALAM: Algebraically Consistent Latent Action Model for Vision-Language-Action Models](../Inbox/2026-05-11--alam-algebraically-consistent-latent-action-model-for-vision-language-action-models.md): Summary covers ALAM's action-free video pretraining, algebraic losses, VLA training use, and benchmark results.

### Spatial grounding added at training time
VEGA focuses on a narrower but important failure source: visual encoders trained mainly on 2D images can miss depth, height, and relative position cues. The method aligns OpenVLA-OFT visual features to a frozen 3D-aware DINOv2-FiT3D teacher during training. The teacher and projector are removed at inference, so runtime stays the same as the base model.

On RoboTwin 2.0, VEGA reports 67.5% average success on Easy and 30.7% on Hard across six bimanual tasks. It improves OpenVLA-OFT by 11.5 points on Easy and 8.0 points on Hard, with task-level gains on Move Card Away, Click Bell, and Place Shoe.

#### Sources
- [VEGA: Visual Encoder Grounding Alignment for Spatially-Aware Vision-Language-Action Models](../Inbox/2026-05-11--vega-visual-encoder-grounding-alignment-for-spatially-aware-vision-language-action-models.md): Summary covers VEGA's 3D-aware feature alignment method, no inference overhead, and RoboTwin 2.0 results.
