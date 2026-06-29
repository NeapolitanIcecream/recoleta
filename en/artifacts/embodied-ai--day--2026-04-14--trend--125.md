---
kind: trend
trend_doc_id: 125
granularity: day
period_start: '2026-04-14T00:00:00'
period_end: '2026-04-15T00:00:00'
topics:
- robotics
- vla-safety
- humanoid-manipulation
- tactile-sensing
- 3d-geometry
run_id: materialize-outputs
aliases:
- recoleta-trend-125
tags:
- recoleta/trend
- topic/robotics
- topic/vla-safety
- topic/humanoid-manipulation
- topic/tactile-sensing
- topic/3d-geometry
language_code: en
pass_output_id: 70
pass_kind: trend_synthesis
---

# Robotics work tightens evaluation around safety, touch, and 3D control

## Overview
This day’s robotics set is easy to read: evaluation gets stricter, and model design follows the same pressure. HazardArena measures whether a VLA can tell a feasible action from a dangerous one. HTD shows that tactile prediction improves real humanoid manipulation. VGA posts the strongest benchmark result of the set with a 3D geometry backbone. Together, the papers favor control signals that match the real decision: semantic risk, contact state, and scene geometry.

## Clusters

### Semantic safety becomes a measurable control problem
HazardArena puts semantic safety at the center of VLA evaluation. Its safe and unsafe twin tasks keep motion demands fixed and change only the meaning that makes an action allowed or dangerous. That design exposes a practical failure mode: models can improve task skill and unsafe completion together. The clearest example is pi_0 on `insert outlet`, where safe success rises from 0.08 to 0.47 while unsafe success also rises from 0.02 to 0.44 across checkpoints. The paper also shows why endpoint success is too narrow. On unsafe `insert outlet`, pi_0 reaches attempt 0.93 and commit 0.80 before final success 0.44, so risky progress is visible well before completion. The proposed Safety Option Layer is a useful guard idea, but the main contribution here is the benchmark and the stage-wise view of risk.

#### Evidence
- [HazardArena: Evaluating Semantic Safety in Vision-Language-Action Models](../Inbox/2026-04-14--hazardarena-evaluating-semantic-safety-in-vision-language-action-models.md): Summary of benchmark design, twin-task setup, stage-wise metrics, and observed coupling between safe-task gains and unsafe behavior.

### Tactile prediction pays off on real humanoid tasks
Touch becomes a first-class input for humanoid manipulation when the task depends on contact. HTD combines multi-view vision, proprioception, hand-joint force, and tactile sensing in one policy, then adds future-touch prediction during behavior cloning. The reported gains are large for a small daily set: a 90.9% relative improvement in average success over ACT across five real-world tasks, plus a 30% relative gain for latent tactile prediction over raw tactile prediction. The task list matters here. Insert-T, towel folding, litter scooping, and tea serving all require contact state that camera views do not fully reveal. The paper also grounds the claim in deployment details, with 3.5 mm insertion clearance and policy execution at 30 Hz on a full humanoid stack.

#### Evidence
- [Learning Versatile Humanoid Manipulation with Touch Dreaming](../Inbox/2026-04-14--learning-versatile-humanoid-manipulation-with-touch-dreaming.md): Summary covers multimodal policy design, touch-dreaming loss, five-task evaluation, and quantitative gains.

### 3D geometry backbones keep the edge on manipulation benchmarks
Geometry-heavy visual backbones keep gaining ground for manipulation. VGA argues that the backbone should model 3D structure directly, then uses a pretrained 3D world model with multi-view RGB, language, and proprioception to drive control. The benchmark result is strong: 98.1% average on LIBERO, with gains over pi_0.5, OpenVLA-oft, VLA-Thinker, GeoVLA, and SpatialVLA. The margins are modest against the strongest baselines, but they are consistent across the suite, and the paper also reports better zero-shot transfer to unseen camera viewpoints on real robots. In a period that already emphasized cleaner evaluation, this paper gives a concrete model-side answer: stronger geometry priors still translate into better placement and viewpoint robustness.

#### Evidence
- [Robotic Manipulation is Vision-to-Geometry Mapping ($f(v) \rightarrow G$): Vision-Geometry Backbones over Language and Video Models](../Inbox/2026-04-14--robotic-manipulation-is-vision-to-geometry-mapping-f-v-rightarrow-g-vision-geometry-backbones-over-language-and-video-models.md): Summary gives the model claim, LIBERO scores, baseline comparisons, and real-world cross-view generalization claim.
